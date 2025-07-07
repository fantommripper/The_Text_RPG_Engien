from abc import ABC, abstractmethod

class Race(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    def base_stats(self) -> dict:
        return {
            "Dm": 0,
            "Hp": 0,
            "maxHp": 0,
            "speed": 0,
            "maxMana": 0,
            "mana": 0
        }
    
    @property
    def special_abilities(self) -> list:
        """Специальные способности расы"""
        return []

class Human(Race):
    @property
    def name(self) -> str:
        return "Human"
    
    @property
    def base_stats(self) -> dict:
        return {
            "Dm": 10,
            "Hp": 110,
            "maxHp": 110,
            "speed": 2,
            "maxMana": 25,
            "mana": 25
        }
    
    @property
    def special_abilities(self) -> list:
        return ["Versatility", "Extra Skill Point"]  # Универсальность людей

class Kobold(Race):
    @property
    def name(self) -> str:
        return "Kobold"
    
    @property
    def base_stats(self) -> dict:
        return {
            "Dm": 8,
            "Hp": 90,
            "maxHp": 90,
            "speed": 3,
            "maxMana": 20,
            "mana": 20
        }
    
    @property
    def special_abilities(self) -> list:
        return ["Pack Tactics", "Trap Detection"]  # Групповая тактика и обнаружение ловушек

class Owlin(Race):
    @property
    def name(self) -> str:
        return "Owlin"
    
    @property
    def base_stats(self) -> dict:
        return {
            "Dm": 7,
            "Hp": 70,
            "maxHp": 70,
            "speed": 6,
            "maxMana": 40,
            "mana": 40
        }
    
    @property
    def special_abilities(self) -> list:
        return ["Flight", "Night Vision", "Spell Power +20%"]  # Полет и магические бонусы

class Naga(Race):
    @property
    def name(self) -> str:
        return "Naga"

    @property
    def base_stats(self) -> dict:
        return {
            "Dm": 12,
            "Hp": 140,
            "maxHp": 140,
            "speed": 1,
            "maxMana": 30,
            "mana": 30
        }
    
    @property
    def special_abilities(self) -> list:
        return ["Poison Immunity", "Constrict", "Water Breathing"]  # Танковые способности

AVAILABLE_RACES = {
    "human": Human,
    "kobold": Kobold,
    "owlin": Owlin,
    "naga": Naga
}

# Функция для анализа баланса
def analyze_race_balance(races_dict):
    """Анализирует баланс рас"""
    print("=== АНАЛИЗ БАЛАНСА РАС ===")
    
    for race_name, race_class in races_dict.items():
        race = race_class()
        stats = race.base_stats()
        
        # Считаем "силу" расы (условная формула)
        power_score = (
            stats["Dm"] * 2 +          # Урон важен
            stats["Hp"] * 0.1 +        # Здоровье важно, но не так сильно
            stats["speed"] * 5 +       # Скорость очень важна
            stats["maxMana"] * 1.5     # Мана важна для магии
        )
        
        print(f"{race_name:>10}: Урон={stats['Dm']:>2}, HP={stats['Hp']:>3}, "
              f"Скорость={stats['speed']}, Мана={stats['maxMana']:>2}, "
              f"Сила={power_score:.1f}")

if __name__ == "__main__":
    print("Текущий баланс:")
    analyze_race_balance(AVAILABLE_RACES)
    print("\nУлучшенный баланс:")  
    analyze_race_balance(AVAILABLE_RACES)