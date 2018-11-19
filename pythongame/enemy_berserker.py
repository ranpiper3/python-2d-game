from pythongame.core.common import Millis, is_x_and_y_within_distance, EnemyType, Sprite
from pythongame.core.enemy_behavior import register_enemy_behavior, AbstractEnemyMind
from pythongame.core.enemy_pathfinding import EnemyPathfinder
from pythongame.core.game_data import register_entity_sprite_initializer, SpriteInitializer, register_enemy_data, EnemyData
from pythongame.core.game_state import GameState, Enemy, WorldEntity
from pythongame.core.visual_effects import VisualLine, create_visual_damage_text


class BerserkerEnemyMind(AbstractEnemyMind):
    def __init__(self):
        self._attack_interval = 1500
        self._time_since_attack = self._attack_interval
        self._update_path_interval = 900
        self._time_since_updated_path = self._update_path_interval
        self.pathfinder = EnemyPathfinder()
        self.next_waypoint = None
        self._reevaluate_next_waypoint_direction_interval = 1000
        self._time_since_reevaluated = self._reevaluate_next_waypoint_direction_interval

    def control_enemy(self, game_state: GameState, enemy: Enemy, player_entity: WorldEntity, is_player_invisible: bool,
                      time_passed: Millis):
        self._time_since_attack += time_passed
        self._time_since_updated_path += time_passed
        self._time_since_reevaluated += time_passed

        enemy_entity = enemy.world_entity

        if self._time_since_updated_path > self._update_path_interval:
            self._time_since_updated_path = 0
            self.pathfinder.update_path(enemy_entity, game_state)

        new_next_waypoint = self.pathfinder.get_next_waypoint_along_path(enemy_entity)

        should_update_waypoint = self.next_waypoint != new_next_waypoint
        if self._time_since_reevaluated > self._reevaluate_next_waypoint_direction_interval:
            self._time_since_reevaluated = 0
            should_update_waypoint = True

        if should_update_waypoint:
            self.next_waypoint = new_next_waypoint
            if self.next_waypoint:
                direction = self.pathfinder.get_dir_towards_considering_collisions(
                    game_state, enemy_entity, self.next_waypoint)
                _move_in_dir(enemy_entity, direction)
            else:
                enemy_entity.set_not_moving()

        if self._time_since_attack > self._attack_interval:
            self._time_since_attack = 0
            if not is_player_invisible:
                enemy_position = enemy_entity.get_center_position()
                player_center_pos = game_state.player_entity.get_center_position()
                if is_x_and_y_within_distance(enemy_position, player_center_pos, 80):
                    damage_amount = 12
                    game_state.player_state.lose_health(damage_amount)
                    game_state.visual_effects.append(create_visual_damage_text(game_state.player_entity, damage_amount))
                    game_state.visual_effects.append(
                        VisualLine((220, 0, 0), enemy_position, player_center_pos, Millis(100), 3))

def _move_in_dir(enemy_entity, direction):
    if direction:
        enemy_entity.set_moving_in_dir(direction)
    else:
        enemy_entity.set_not_moving()

def register_berserker_enemy():
    size = (50, 50)
    register_enemy_data(EnemyType.BERSERKER, EnemyData(Sprite.ENEMY_BERSERKER, size, 5, 0.1))
    register_enemy_behavior(EnemyType.BERSERKER, BerserkerEnemyMind)
    register_entity_sprite_initializer(
        Sprite.ENEMY_BERSERKER, SpriteInitializer("resources/graphics/orc_berserker.png", size))
