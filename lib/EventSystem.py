from typing import Dict, List, Callable, Any, Optional, Union
from functools import wraps
import weakref
import threading
from dataclasses import dataclass
from enum import Enum
import logging


class EventPriority(Enum):
    """Приоритеты выполнения обработчиков событий"""
    LOWEST = 0
    LOW = 1
    NORMAL = 2
    HIGH = 3
    HIGHEST = 4


@dataclass
class EventData:
    """Базовый класс для данных события"""
    event_name: str
    timestamp: float
    source: Optional[Any] = None
    cancelled: bool = False
    
    def cancel(self) -> None:
        """Отменить событие"""
        self.cancelled = True


class EventHandler:
    """Обработчик события с метаданными"""
    
    def __init__(self, 
                 callback: Callable[[EventData], Any],
                 priority: EventPriority = EventPriority.NORMAL,
                 once: bool = False,
                 weak_ref: bool = False):
        self._callback = callback
        self._priority = priority
        self._once = once
        self._weak_ref = weak_ref
        self._call_count = 0
        self._is_method = hasattr(callback, '__self__')
        
        # Используем слабые ссылки для методов объектов
        if weak_ref and self._is_method:
            self._weak_callback = weakref.WeakMethod(callback)
        else:
            self._weak_callback = None
    
    @property
    def priority(self) -> EventPriority:
        return self._priority

    @property
    def once(self) -> bool:
        return self._once
    
    @property
    def call_count(self) -> int:
        return self._call_count
    
    def is_valid(self) -> bool:
        """Проверить, что обработчик все еще валиден"""
        if self._weak_callback:
            return self._weak_callback() is not None
        return True
    
    def call(self, event_data: EventData) -> Any:
        """Вызвать обработчик"""
        if not self.is_valid():
            return None
            
        callback = self._weak_callback() if self._weak_callback else self._callback
        if callback is None:
            return None
            
        self._call_count += 1
        return callback(event_data)


class EventSystem:
    """Основная система событий"""
    
    def __init__(self, use_threading: bool = False):
        self._handlers: Dict[str, List[EventHandler]] = {}
        self._event_history: List[EventData] = []
        self._max_history_size: int = 1000
        self._use_threading = use_threading
        self._lock = threading.RLock() if use_threading else None
        self._logger = logging.getLogger(__name__)
        self._global_filters: List[Callable[[EventData], bool]] = []
    
    def subscribe(self, 
                  event_name: str, 
                  callback: Callable[[EventData], Any],
                  priority: EventPriority = EventPriority.NORMAL,
                  once: bool = False,
                  weak_ref: bool = False) -> EventHandler:
        """
        Подписаться на событие

        Args:
            event_name: Название события
            callback: Функция-обработчик
            priority: Приоритет выполнения
            once: Выполнить только один раз
            weak_ref: Использовать слабые ссылки
        """
        with self._get_lock():
            if event_name not in self._handlers:
                self._handlers[event_name] = []
            
            handler = EventHandler(callback, priority, once, weak_ref)
            self._handlers[event_name].append(handler)
            
            # Сортируем по приоритету (от высокого к низкому)
            self._handlers[event_name].sort(
                key=lambda h: h.priority.value, 
                reverse=True
            )
            
            self._logger.debug(f"Подписан обработчик на событие '{event_name}'")
            return handler
    
    def unsubscribe(self, event_name: str, callback: Callable[[EventData], Any]) -> bool:
        """
        Отписаться от события
        
        Args:
            event_name: Название события
            callback: Функция-обработчик для удаления
        """
        with self._get_lock():
            if event_name not in self._handlers:
                return False
            
            original_count = len(self._handlers[event_name])
            self._handlers[event_name] = [
                h for h in self._handlers[event_name] 
                if h._callback != callback
            ]
            
            removed = original_count - len(self._handlers[event_name])
            if removed > 0:
                self._logger.debug(f"Удалено {removed} обработчик(ов) для события '{event_name}'")
            
            return removed > 0
    
    def emit(self, 
             event_name: str, 
             event_data: Optional[EventData] = None,
             **kwargs) -> List[Any]:
        """
        Вызвать событие
        
        Args:
            event_name: Название события
            event_data: Данные события
            **kwargs: Дополнительные параметры для создания EventData
        """
        import time
        
        # Создаем данные события если не переданы
        if event_data is None:
            event_data = EventData(
                event_name=event_name,
                timestamp=time.time(),
                **kwargs
            )
        
        # Применяем глобальные фильтры
        for filter_func in self._global_filters:
            if not filter_func(event_data):
                self._logger.debug(f"Событие '{event_name}' отфильтровано")
                return []
        
        # Добавляем в историю
        self._add_to_history(event_data)
        
        results = []
        handlers_to_remove = []
        
        with self._get_lock():
            if event_name not in self._handlers:
                self._logger.debug(f"Нет обработчиков для события '{event_name}'")
                return results
            
            # Создаем копию списка обработчиков для безопасной итерации
            handlers = self._handlers[event_name].copy()
        
        for handler in handlers:
            if not handler.is_valid():
                handlers_to_remove.append(handler)
                continue
            
            if event_data.cancelled:
                break
            
            try:
                result = handler.call(event_data)
                results.append(result)
                
                # Удаляем одноразовые обработчики
                if handler.once:
                    handlers_to_remove.append(handler)
                    
            except Exception as e:
                self._logger.error(f"Ошибка в обработчике события '{event_name}': {e}")
        
        # Удаляем недействительные и одноразовые обработчики
        if handlers_to_remove:
            with self._get_lock():
                for handler in handlers_to_remove:
                    if handler in self._handlers[event_name]:
                        self._handlers[event_name].remove(handler)
        
        self._logger.debug(f"Событие '{event_name}' обработано {len(results)} обработчиками")
        return results
    
    def add_global_filter(self, filter_func: Callable[[EventData], bool]) -> None:
        """Добавить глобальный фильтр событий"""
        self._global_filters.append(filter_func)
    
    def remove_global_filter(self, filter_func: Callable[[EventData], bool]) -> bool:
        """Удалить глобальный фильтр событий"""
        if filter_func in self._global_filters:
            self._global_filters.remove(filter_func)
            return True
        return False
    
    def get_event_handlers(self, event_name: str) -> List[EventHandler]:
        """Получить список обработчиков для события"""
        with self._get_lock():
            return self._handlers.get(event_name, []).copy()
    
    def get_event_names(self) -> List[str]:
        """Получить список всех зарегистрированных событий"""
        with self._get_lock():
            return list(self._handlers.keys())
    
    def clear_handlers(self, event_name: Optional[str] = None) -> None:
        """Очистить обработчики (все или для конкретного события)"""
        with self._get_lock():
            if event_name:
                self._handlers.pop(event_name, None)
                self._logger.debug(f"Очищены обработчики для события '{event_name}'")
            else:
                self._handlers.clear()
                self._logger.debug("Очищены все обработчики событий")
    
    def get_event_history(self, limit: Optional[int] = None) -> List[EventData]:
        """Получить историю событий"""
        if limit:
            return self._event_history[-limit:]
        return self._event_history.copy()
    
    def clear_history(self) -> None:
        """Очистить историю событий"""
        self._event_history.clear()
    
    def _add_to_history(self, event_data: EventData) -> None:
        """Добавить событие в историю"""
        self._event_history.append(event_data)
        if len(self._event_history) > self._max_history_size:
            self._event_history.pop(0)
    
    def _get_lock(self):
        """Получить блокировку или заглушку"""
        return self._lock if self._lock else _DummyLock()


class _DummyLock:
    """Заглушка для блокировки в однопоточном режиме"""
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


# Декораторы для удобства
def event_handler(event_system: EventSystem, 
                  event_name: str,
                  priority: EventPriority = EventPriority.NORMAL,
                  once: bool = False):
    """Декоратор для регистрации обработчика события"""
    def decorator(func):
        event_system.subscribe(event_name, func, priority, once)
        return func
    return decorator


def cancellable_event(func):
    """Декоратор для создания отменяемого события"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, EventData):
            return result
        return result
    return wrapper


# Пример использования
if __name__ == "__main__":
    class DamageEventData(EventData):
        """Данные события получения урона"""
        def __init__(self, event_name: str, damage_amount: int, damage_type: str):
            self.damage_amount = damage_amount
            self.damage_type = damage_type

    # Создание системы
    event_system = EventSystem()

    # Подписка на событие
    def handle_damage(event_data):
        print(f"Получен урон: {event_data.damage_amount}")

    event_system.subscribe("gettingDamage", handle_damage)

    # Активация события
    damage_data = DamageEventData(
        event_name="gettingDamage",
        damage_amount=50,
        damage_type="fire"
    )
    event_system.emit("gettingDamage", damage_data)