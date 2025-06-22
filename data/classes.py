from abc import ABC, abstractmethod

class HeroClass(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    def stat_modifiers(self) -> dict:
        return {
            "Dm": 0,
            "Hp": 0,
            "maxHp": 0,
            "speed": 0,
            "maxMana": 0,
            "mana": 0
        }
    
    @property
    def class_abilities(self) -> list:
        """Специальные способности класса"""
        return []
    
    @property
    def weapon_proficiency(self) -> list:
        """Владение оружием"""
        return []

class Swordsman(HeroClass):
    @property
    def name(self) -> str:
        return "Swordsman"
    
    @property
    def stat_modifiers(self) -> dict:
        return {
            "Dm": 4,      # Увеличил урон (основной DD)
            "Hp": 40,     # Увеличил HP (танк/DD гибрид)
            "maxHp": 40,
            "speed": 0,   # Убрал штраф к скорости (избегаем speed=0)
            "maxMana": -8, # Больше штраф к мане
            "mana": -8
        }
    
    @property
    def class_abilities(self) -> list:
        return ["Shield Block", "Power Strike", "Armor Mastery"]
    
    @property
    def weapon_proficiency(self) -> list:
        return ["Sword", "Shield", "Heavy Armor"]

class Magician(HeroClass):
    @property
    def name(self) -> str:
        return "Magician"
    
    @property
    def stat_modifiers(self) -> dict:
        return {
            "Dm": -2,     # Больше штраф к физ. урону
            "Hp": -15,    # Больше штраф к HP (стеклянная пушка)
            "maxHp": -15,
            "speed": 0,   # Нормальная скорость
            "maxMana": 35, # Увеличил ману (главный ресурс)
            "mana": 35
        }
    
    @property
    def class_abilities(self) -> list:
        return ["Spell Power +50%", "Mana Shield", "Elemental Mastery"]
    
    @property
    def weapon_proficiency(self) -> list:
        return ["Staff", "Wand", "Light Armor"]

class Thief(HeroClass):
    @property
    def name(self) -> str:
        return "Thief"
    
    @property
    def stat_modifiers(self) -> dict:
        return {
            "Dm": 2,      # Снизил урон (компенсируется критами)
            "Hp": -10,    # Увеличил штраф к HP
            "maxHp": -10,
            "speed": 3,   # Увеличил скорость (главное преимущество)
            "maxMana": 5, # Небольшой бонус к мане (для способностей)
            "mana": 5
        }
    
    @property
    def class_abilities(self) -> list:
        return ["Stealth", "Critical Strike", "Lockpicking"]
    
    @property
    def weapon_proficiency(self) -> list:
        return ["Dagger", "Bow", "Light Armor"]

class Archer(HeroClass):
    @property
    def name(self) -> str:
        return "Archer"
    
    @property
    def stat_modifiers(self) -> dict:
        return {
            "Dm": 3,      # Увеличил урон (дальний DD)
            "Hp": 10,     # Небольшой бонус к HP
            "maxHp": 10,
            "speed": 2,   # Увеличил скорость (кайтинг)
            "maxMana": 5, # Небольшой бонус к мане
            "mana": 5
        }
    
    @property
    def class_abilities(self) -> list:
        return ["Precise Shot", "Multi-Shot", "Piercing Arrow", "Trap Setting"]
    
    @property
    def weapon_proficiency(self) -> list:
        return ["Bow", "Crossbow", "Medium Armor"]

class Cleric(HeroClass):
    @property
    def name(self) -> str:
        return "Cleric"

    @property
    def stat_modifiers(self) -> dict:
        return {
            "Dm": 0,      # Нейтральный урон
            "Hp": 20,     # Хорошее здоровье
            "maxHp": 20,
            "speed": 0,   # Нейтральная скорость
            "maxMana": 25, # Хорошая мана для лечения
            "mana": 25
        }
    
    @property
    def class_abilities(self) -> list:
        return ["Heal", "Divine Protection", "Blessing"]
    
    @property
    def weapon_proficiency(self) -> list:
        return ["Mace", "Shield", "Medium Armor"]

# —————————————————————————————— Анализ классов и их баланса ——————————————————————————————

def analyze_class_balance(classes_dict, base_stats=None):
    """Анализирует баланс классов"""
    if base_stats is None:
        # Используем средние базовые статы для анализа
        base_stats = {
            "Dm": 9,
            "Hp": 100,
            "maxHp": 100,
            "speed": 2,
            "maxMana": 25,
            "mana": 25
        }
    
    print("=== АНАЛИЗ БАЛАНСА КЛАССОВ ===")
    print(f"Базовые статы: {base_stats}")
    print()
    
    class_power = {}
    
    for class_name, class_obj in classes_dict.items():
        hero_class = class_obj()
        
        # Проверяем, property это или метод
        if hasattr(hero_class.stat_modifiers, '__call__'):
            modifiers = hero_class.stat_modifiers()
        else:
            modifiers = hero_class.stat_modifiers
        
        # Считаем финальные статы
        final_stats = {}
        for stat, base_value in base_stats.items():
            final_stats[stat] = base_value + modifiers.get(stat, 0)
        
        # Считаем "силу" класса
        power_score = (
            final_stats["Dm"] * 2.5 +      # Урон очень важен
            final_stats["Hp"] * 0.08 +     # HP важны для выживания
            final_stats["speed"] * 4 +     # Скорость критична
            final_stats["maxMana"] * 1.2   # Мана важна для способностей
        )
        
        class_power[class_name] = power_score
        
        print(f"{class_name:>10}: Урон={final_stats['Dm']:>2}, HP={final_stats['Hp']:>3}, "
              f"Скорость={final_stats['speed']}, Мана={final_stats['maxMana']:>2}, "
              f"Сила={power_score:.1f}")
    
    print(f"\nСамый сильный: {max(class_power, key=class_power.get)}")
    print(f"Самый слабый: {min(class_power, key=class_power.get)}")
    
    return class_power

def check_critical_combinations():
    """Проверяет комбинации рас и классов на критические проблемы"""
    print("\n=== ПРОВЕРКА КРИТИЧЕСКИХ КОМБИНАЦИЙ ===")
    
    # Базовые статы рас (используем твои сбалансированные)
    races = {
        "Human": {"Dm": 10, "Hp": 110, "speed": 2, "maxMana": 25},
        "Kobold": {"Dm": 8, "Hp": 90, "speed": 3, "maxMana": 20},
        "Owlin": {"Dm": 7, "Hp": 70, "speed": 6, "maxMana": 40},
        "Naga": {"Dm": 12, "Hp": 140, "speed": 1, "maxMana": 30}
    }
    
    classes = {
        "Swordsman": Swordsman(),
        "Magician": Magician(),
        "Thief": Thief(),
        "Archer": Archer(),
        "Cleric": Cleric()
    }
    
    critical_issues = []
    
    for race_name, race_stats in races.items():
        for class_name, hero_class in classes.items():
            modifiers = hero_class.stat_modifiers  # Убрал скобки - это property!
            
            # Считаем финальные статы
            final_stats = {}
            for stat in ["Dm", "Hp", "speed", "maxMana"]:
                final_stats[stat] = race_stats[stat] + modifiers.get(stat, 0)
                final_stats[f"max{stat.capitalize()}"] = final_stats[stat] if stat != "speed" else race_stats.get(f"max{stat.capitalize()}", final_stats[stat])
            
            # Проверяем критические проблемы
            issues = []
            
            if final_stats["speed"] <= 0:
                issues.append(f"НЕ МОЖЕТ ДВИГАТЬСЯ (speed={final_stats['speed']})")
            
            if final_stats["Hp"] <= 0:
                issues.append(f"УМИРАЕТ ПРИ СОЗДАНИИ (HP={final_stats['Hp']})")

            if final_stats["Dm"] <= 0:
                issues.append(f"НЕ МОЖЕТ АТАКОВАТЬ (урон={final_stats['Dm']})")
            
            if final_stats["maxMana"] < 0:
                issues.append(f"ОТРИЦАТЕЛЬНАЯ МАНА ({final_stats['maxMana']})")
            
            # Проверяем слишком низкие статы
            if final_stats["Hp"] < 20:
                issues.append(f"КРИТИЧЕСКИ МАЛО HP ({final_stats['Hp']})")

            if issues:
                critical_issues.append({
                    "combo": f"{race_name} {class_name}",
                    "issues": issues,
                    "stats": final_stats
                })
    
    if critical_issues:
        print("НАЙДЕНЫ КРИТИЧЕСКИЕ ПРОБЛЕМЫ:")
        for issue in critical_issues:
            print(f"\n❌ {issue['combo']}:")
            for problem in issue['issues']:
                print(f"   - {problem}")
            stats = issue['stats']
            print(f"   Финальные статы: Урон={stats['Dm']}, HP={stats['Hp']}, Скорость={stats['speed']}, Мана={stats['maxMana']}")
    else:
        print("✅ Критических проблем не найдено!")
    
    return critical_issues

def analyze_race_class_synergy():
    """Анализирует лучшие комбинации рас и классов"""
    print("\n=== СИНЕРГИЯ РАС И КЛАССОВ ===")
    
    # Примерные базовые статы рас
    races = {
        "Human": {"Dm": 10, "Hp": 110, "speed": 2, "maxMana": 25},
        "Kobold": {"Dm": 8, "Hp": 90, "speed": 3, "maxMana": 20},
        "Owlin": {"Dm": 7, "Hp": 70, "speed": 6, "maxMana": 40},
        "Naga": {"Dm": 12, "Hp": 140, "speed": 1, "maxMana": 30}
    }
    
    classes = {
        "Swordsman": Swordsman(),
        "Magician": Magician(),
        "Thief": Thief(),
        "Archer": Archer()
    }
    
    best_combos = []
    
    for race_name, race_stats in races.items():
        for class_name, hero_class in classes.items():
            modifiers = hero_class.stat_modifiers  # Убрал скобки - это property!
            
            # Считаем финальные статы
            final_stats = {}
            for stat in ["Dm", "Hp", "speed", "maxMana"]:
                final_stats[stat] = race_stats[stat] + modifiers.get(stat, 0)
            
            # Считаем синергию
            power = (
                final_stats["Dm"] * 2.5 +
                final_stats["Hp"] * 0.08 +
                final_stats["speed"] * 4 +
                final_stats["maxMana"] * 1.2
            )
            
            best_combos.append((f"{race_name} {class_name}", power, final_stats))

    # Сортируем по силе
    best_combos.sort(key=lambda x: x[1], reverse=True)
    
    print("Топ-5 комбинаций:")
    for i, (combo, power, stats) in enumerate(best_combos[:5], 1):
        print(f"{i}. {combo:<20}: Сила={power:.1f} "
              f"(Урон={stats['Dm']}, HP={stats['Hp']}, "
              f"Скорость={stats['speed']}, Мана={stats['maxMana']})")



AVAILABLE_CLASSES = {
    "Swordsman": Swordsman,
    "Magician": Magician,
    "Thief": Thief,
    "Archer": Archer,
    "Cleric": Cleric
}

if __name__ == "__main__":
    print("====== АНАЛИЗ КЛАССОВ ======"+"\n")
    analyze_class_balance({name: cls for name, cls in AVAILABLE_CLASSES.items()})

    check_critical_combinations()
    
    analyze_race_class_synergy()