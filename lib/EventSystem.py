from typing import Dict, List, Callable, Any, Optional, Union
from functools import wraps
import weakref
import threading
from dataclasses import dataclass
from enum import Enum
import logging


class EventPriority(Enum):
    """Handler execution priorities"""
    LOWEST = 0
    LOW = 1
    NORMAL = 2
    HIGH = 3
    HIGHEST = 4


@dataclass
class EventData:
    """Base class for event data"""
    event_name: str
    timestamp: float
    source: Optional[Any] = None
    cancelled: bool = False
    
    def cancel(self) -> None:
        """Cancel the event"""
        self.cancelled = True


class EventHandler:
    """Event handler with metadata"""
    
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
        
        # Use weak references for object methods
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
        """Check if handler is still valid"""
        if self._weak_callback:
            return self._weak_callback() is not None
        return True
    
    def call(self, event_data: EventData) -> Any:
        """Invoke the handler"""
        if not self.is_valid():
            return None
            
        callback = self._weak_callback() if self._weak_callback else self._callback
        if callback is None:
            return None
            
        self._call_count += 1
        return callback(event_data)


class EventSystem:
    """Core event system"""
    
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
        Subscribe to an event

        Args:
            event_name: Event name
            callback: Handler function
            priority: Execution priority
            once: Execute only once
            weak_ref: Use weak references
        """
        with self._get_lock():
            if event_name not in self._handlers:
                self._handlers[event_name] = []
            
            handler = EventHandler(callback, priority, once, weak_ref)
            self._handlers[event_name].append(handler)
            
            # Sort by priority (highest first)
            self._handlers[event_name].sort(
                key=lambda h: h.priority.value, 
                reverse=True
            )
            
            self._logger.debug(f"Handler subscribed to event '{event_name}'")
            return handler
    
    def unsubscribe(self, event_name: str, callback: Callable[[EventData], Any]) -> bool:
        """
        Unsubscribe from an event
        
        Args:
            event_name: Event name
            callback: Handler function to remove
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
                self._logger.debug(f"Removed {removed} handler(s) for event '{event_name}'")
            
            return removed > 0
    
    def emit(self, 
             event_name: str, 
             event_data: Optional[EventData] = None,
             **kwargs) -> List[Any]:
        """
        Emit an event
        
        Args:
            event_name: Event name
            event_data: Event data
            **kwargs: Additional parameters for EventData creation
        """
        import time
        
        # Create event data if not provided
        if event_data is None:
            event_data = EventData(
                event_name=event_name,
                timestamp=time.time(),
                **kwargs
            )
        
        # Apply global filters
        for filter_func in self._global_filters:
            if not filter_func(event_data):
                self._logger.debug(f"Event '{event_name}' filtered")
                return []
        
        # Add to history
        self._add_to_history(event_data)
        
        results = []
        handlers_to_remove = []
        
        with self._get_lock():
            if event_name not in self._handlers:
                self._logger.debug(f"No handlers for event '{event_name}'")
                return results
            
            # Create handler copy for safe iteration
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
                
                # Remove one-time handlers
                if handler.once:
                    handlers_to_remove.append(handler)
                    
            except Exception as e:
                self._logger.error(f"Error in handler for event '{event_name}': {e}")
        
        # Remove invalid and one-time handlers
        if handlers_to_remove:
            with self._get_lock():
                for handler in handlers_to_remove:
                    if handler in self._handlers[event_name]:
                        self._handlers[event_name].remove(handler)
        
        self._logger.debug(f"Event '{event_name}' handled by {len(results)} handlers")
        return results
    
    def add_global_filter(self, filter_func: Callable[[EventData], bool]) -> None:
        """Add global event filter"""
        self._global_filters.append(filter_func)
    
    def remove_global_filter(self, filter_func: Callable[[EventData], bool]) -> bool:
        """Remove global event filter"""
        if filter_func in self._global_filters:
            self._global_filters.remove(filter_func)
            return True
        return False
    
    def get_event_handlers(self, event_name: str) -> List[EventHandler]:
        """Get handlers for an event"""
        with self._get_lock():
            return self._handlers.get(event_name, []).copy()
    
    def get_event_names(self) -> List[str]:
        """Get all registered event names"""
        with self._get_lock():
            return list(self._handlers.keys())

    def clear_handlers(self, event_name: Optional[str] = None) -> None:
        """Clear handlers (all or for specific event)"""
        with self._get_lock():
            if event_name:
                self._handlers.pop(event_name, None)
                self._logger.debug(f"Cleared handlers for event '{event_name}'")
            else:
                self._handlers.clear()
                self._logger.debug("Cleared all event handlers")
    
    def get_event_history(self, limit: Optional[int] = None) -> List[EventData]:
        """Get event history"""
        if limit:
            return self._event_history[-limit:]
        return self._event_history.copy()
    
    def clear_history(self) -> None:
        """Clear event history"""
        self._event_history.clear()
    
    def _add_to_history(self, event_data: EventData) -> None:
        """Add event to history"""
        self._event_history.append(event_data)
        if len(self._event_history) > self._max_history_size:
            self._event_history.pop(0)
    
    def _get_lock(self):
        """Get lock or dummy lock"""
        return self._lock if self._lock else _DummyLock()


class _DummyLock:
    """Dummy lock for single-threaded mode"""
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


# Convenience decorators
def event_handler(event_system: EventSystem, 
                  event_name: str,
                  priority: EventPriority = EventPriority.NORMAL,
                  once: bool = False):
    """Decorator to register event handler"""
    def decorator(func):
        event_system.subscribe(event_name, func, priority, once)
        return func
    return decorator


def cancellable_event(func):
    """Decorator to create cancellable event"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, EventData):
            return result
        return result
    return wrapper

event_system = EventSystem()

# Usage example
if __name__ == "__main__":
    class DamageEventData(EventData):
        """Damage event data"""
        def __init__(self, event_name: str, damage_amount: int, damage_type: str):
            self.damage_amount = damage_amount
            self.damage_type = damage_type

    # Create system
    event_system = EventSystem()

    # Subscribe to event
    def handle_damage(event_data):
        print(f"Damage taken: {event_data.damage_amount}")

    event_system.subscribe("gettingDamage", handle_damage)

    # Emit event
    damage_data = DamageEventData(
        event_name="gettingDamage",
        damage_amount=50,
        damage_type="fire"
    )
    event_system.emit("gettingDamage", damage_data)