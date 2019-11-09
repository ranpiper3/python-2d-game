from pythongame.core.common import ItemType, Sprite, UiIconSprite, HeroStat
from pythongame.core.item_inventory import ItemEquipmentCategory
from pythongame.game_data.items.register_items_util import register_stat_modifying_item


def register_hatchet_item():
    register_stat_modifying_item(
        item_type=ItemType.HATCHET,
        ui_icon_sprite=UiIconSprite.ITEM_HATCHET,
        sprite=Sprite.ITEM_HATCHET,
        image_file_path="resources/graphics/item_hatchet.png",
        item_equipment_category=ItemEquipmentCategory.MAIN_HAND,
        name="Hatchet",
        stat_modifiers={HeroStat.DAMAGE: 0.1}
    )