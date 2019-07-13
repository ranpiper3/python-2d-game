from typing import Dict

from pythongame.core.common import ItemType, HeroId, PortraitIconSprite
from pythongame.core.game_data import Sprite, Direction, ConsumableType, AbilityType, SpriteSheet, \
    register_entity_sprite_map, register_portrait_icon_sprite_path, register_hero_data, HeroData, \
    InitialPlayerStateData


def register_hero_mage():
    sprite = Sprite.HERO_MAGE
    portrait_icon_sprite = PortraitIconSprite.HERO_MAGE
    player_sprite_sheet = SpriteSheet("resources/graphics/player.gif")
    original_sprite_size = (32, 48)
    scaled_sprite_size = (60, 60)
    indices_by_dir = {
        Direction.DOWN: [(0, 0), (1, 0), (2, 0), (3, 0)],
        Direction.LEFT: [(0, 1), (1, 1), (2, 1), (3, 1)],
        Direction.RIGHT: [(0, 2), (1, 2), (2, 2), (3, 2)],
        Direction.UP: [(0, 3), (1, 3), (2, 3), (3, 3)]
    }
    sprite_position_relative_to_entity = (-15, -30)
    register_entity_sprite_map(sprite, player_sprite_sheet, original_sprite_size,
                               scaled_sprite_size, indices_by_dir, sprite_position_relative_to_entity)
    register_portrait_icon_sprite_path(portrait_icon_sprite, 'resources/graphics/player_portrait.gif')
    entity_speed = 0.105
    entity_size = (30, 30)
    hero_data = HeroData(sprite, portrait_icon_sprite, _get_initial_player_state_mage(), entity_speed, entity_size)
    register_hero_data(HeroId.MAGE, hero_data)


def _get_initial_player_state_mage() -> InitialPlayerStateData:
    health = 40
    mana = 120
    mana_regen = 4
    consumable_slots = {
        1: ConsumableType.HEALTH_LESSER,
        2: ConsumableType.MANA_LESSER,
        3: None,
        4: None,
        5: None
    }
    abilities = [AbilityType.FIREBALL]
    items: Dict[int, ItemType] = {
        1: None,
        2: None,
        3: None
    }
    new_level_abilities = {
        2: AbilityType.WHIRLWIND,
        3: AbilityType.ENTANGLING_ROOTS,
        4: AbilityType.CHANNEL_ATTACK
    }
    return InitialPlayerStateData(
        health, mana, mana_regen, consumable_slots, abilities, items, new_level_abilities, HeroId.MAGE)
