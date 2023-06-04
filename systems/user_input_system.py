from components import *
from systems.system import *

import pygame

class UserInputSystem(System):
    def on_create(self):
        self.keys_down = []
        self.held_keys = {}
    def on_update(self):
        for entity in self.entity_manager.get_entities():
            components = self.component_manager.get_components(entity, ControlsComponent, RigidbodyComponent)
            try:
                controls = components[ControlsComponent]
                rigidbody = components[RigidbodyComponent]
            except (TypeError, KeyError):
                continue
            try:
                keys_down = self.keys_down.copy()
                while True:
                    button = keys_down.pop(0)
                    if button == controls.custom_keys[Controls.SHOOT]:
                        self.__spawn_projectile(entity)
            except IndexError:
                pass

            direction = pygame.Vector2()
            if self.held_keys[controls.custom_keys[Controls.UP]]:
                direction.y -= 1
            if self.held_keys[controls.custom_keys[Controls.DOWN]]:
                direction.y += 1
            if self.held_keys[controls.custom_keys[Controls.LEFT]]:
                direction.x -= 1
            if self.held_keys[controls.custom_keys[Controls.RIGHT]]:
                direction.x += 1
            try:
                rigidbody.direction = direction.normalize()
            except ValueError:
                rigidbody.direction = pygame.Vector2()
        self.keys_down = []
        
    def __spawn_projectile(self, entity):
        projectile = self.entity_manager.create_entity()
        entity_components = self.component_manager.get_components(entity, TransformComponent, RigidbodyComponent, RectHitboxComponent)
        try:
            entity_transform = entity_components[TransformComponent]
            entity_rigidbody = entity_components[RigidbodyComponent]
        except (TypeError, KeyError):
            return
        #print(entity_transform.position)
        projectile_transform = TransformComponent(
            entity_transform.position.copy(),
            entity_transform.rotation,
            entity_transform.scale.copy(),
        )
        self.component_manager.add_component(projectile, projectile_transform)
        projectile_rigidbody = RigidbodyComponent(
            3,
            CollisionType.KINETIC,
            entity_rigidbody.direction.copy() if entity_rigidbody.direction != pygame.Vector2() else pygame.Vector2(0, 1),
        )
        self.component_manager.add_component(projectile, projectile_rigidbody)
        rect = pygame.Rect(0, 0, 20, 20)
        anchor = pygame.Vector2(rect.center)
        ignore_entity_types = [EntityTypes.PROJECTILE]
        try:
            entity_rect_hitbox = entity_components[RectHitboxComponent]
            ignore_entity_types.append(entity_rect_hitbox.entity_type)
        except KeyError:
            pass
        projectile_rect_hitbox = RectHitboxComponent(
            rect, anchor, EntityTypes.PROJECTILE, ignore_entity_types
        )
        self.component_manager.add_component(projectile, projectile_rect_hitbox)
        projectile_rect_sprite = RectSpriteComponent(rect, anchor, 'green')
        self.component_manager.add_component(projectile, projectile_rect_sprite)
        damage = DamageComponent(1, False)
        self.component_manager.add_component(projectile, damage)