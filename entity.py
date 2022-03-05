import math, numpy
import pygame, spritesheet

class Entity():
    def __init__(self, pos, sprite_sheet, speed=2, colorkey=(0,0,0)) -> None:
        """Create an Entity object, consisting of
        pygame.Surface, pygame.Rects, sprite_sheet and all the variables
        used by physics engine"""
        # Pygame surf and rect object setup
        self.sprite = sprite_sheet["idle"]
        self.sprite.set_colorkey(colorkey)
        self.rect = self.sprite.get_rect()
        #Where is object in the game world
        self.rect.x, self.rect.y = pos[0], pos[1]
        #Sounds
        self.sounds = {}
        # Physics and render engine variables
        self.physics = True
        self.speed = speed
        self.x_movement = 0
        self.y_movement = 0
        self.jump_ability = 0
        self.momentum = 0
        self.g_force = 0.14

    def collision_test(self, tiles):
        """For every tile in the list of rects passed as an argument,
        run a pygame func checking if it collides with entity rect
        and if it does, add it to the list and return the list"""
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions

    def eval_movement(self):
        self.x_movement = 0
        self.momentum = min(3, self.momentum + self.g_force)
        self.y_movement = self.momentum

    def move_and_collide(self, tile_rects):
        # reset collision that player has with environment
        self.collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        
        # Calculates player's x coordinate and overwrites it in case the new value would
        # push a player into a physical tile
        self.rect.x += self.x_movement
        # Runs a collision test; calls pygame collision func over player and every tile
        for tile in self.collision_test(tile_rects):
            if self.x_movement > 0:
                self.rect.right = tile.left
                self.collision_types["right"] = True
            if self.x_movement < 0:
                self.rect.left = tile.right
                self.collision_types["left"] = True

        # Calculates entity's y coordinate and overwrites it in case the new value would
        # push a entity into a physical tile
        self.rect.y += self.y_movement
        # collision_test ran again to check for collisions after establishing x value, to calculate y value
        for tile in self.collision_test(tile_rects):
            if self.y_movement > 0:
                self.rect.bottom = tile.top
                if self.jump_ability == 0:
                    self.momentum = 0
                    self.jump_ability = 1
                self.collision_types["bottom"] = True
            if self.y_movement < 0:
                self.rect.top = tile.bottom
                self.momentum = 0
                self.collision_types["top"] = True

    def update(self, **kwargs) -> None:
        """Updates state of the entity. Calls eval_movement to update how the
        entity should move according to inputs and physics. Adds the values calculated
        in eval_movement for one axis at a time and applies collisions. First checks
        movement and collisions in one axis, then in the other."""
        # calculate movement
        self.eval_movement() 

        #Update entity's position and check collisions
        self.move_and_collide(kwargs["tile_rects"])

        # Screen edge collisions
        if kwargs["level_size"] != 0:
            self.clamp_to_level_edge(kwargs["tile_rects"])

    
class AnimatedEntity(Entity):
    def __init__(self, pos, sprite_sheet, speed=2, colorkey=(0,0,0), sheet_size=(32,32), frame_size=(16,16)) -> None:
        super().__init__(pos, sprite_sheet, speed, colorkey)
        self.init_pos = pos
        #Animation; 
        self.sheet_size = sheet_size
        self.frame_size = frame_size
        self.animation_keys = sprite_sheet
        self.colorkey = colorkey
        self.animations = {}
        self.active_animation = None
        self.previous_animation = None
        self.frame_index = 0
        self.frame_timer = 0
        self.flip = [False, False]

    def setup_animations(self):
        for key, value in self.animation_keys.items():
            frames = spritesheet.Spritesheet(value, self.sheet_size, self.frame_size).get_frames()
            for frame in frames:
                frame.set_colorkey(self.colorkey)
            self.animations[key] = frames
        self.sprite = self.animations["idle"][0]
        self.sprite.set_colorkey(self.colorkey)
        self.rect = self.sprite.get_rect()
        self.rect.x = self.init_pos[0]
        self.rect.y = self.init_pos[1]
    
    def animate(self):
        """Checks any changes in active animation, updates the state of
        animation and assigns it to player sprite(surface actually)."""
        if self.active_animation == None:
            self.active_animation = "idle"
        if self.x_movement != 0:
            self.active_animation = "run"
        else:
            self.active_animation = "idle"
        
        animation_changed = self.active_animation != self.previous_animation
        if animation_changed:
            self.frame_index = 0
            self.frame_timer = 7

        if self.frame_timer <= 0:
            if self.frame_index + 1 == len(self.animations[self.active_animation]):
                self.frame_index = 0
            else:
                self.frame_index += 1
            self.frame_timer = 7
        self.frame_timer -= 1

        self.sprite = self.animations[self.active_animation][self.frame_index]
        #Handling horizontal and vertical mirroring
        if self.x_movement < 0:
            self.flip[0] = True
        else:
            self.flip[0] = False
        self.sprite = pygame.transform.flip(self.sprite, self.flip[0], self.flip[1])
        self.previous_animation = self.active_animation

    def update(self, **kwargs) -> None:
        return super().update(**kwargs)


class Player(AnimatedEntity):
    def __init__(self, pos, sprite_sheet, speed=2, colorkey=(0,0,0), sheet_size=(32,32), frame_size=(16,16)) -> None:
        super().__init__(pos, sprite_sheet, speed, colorkey, sheet_size, frame_size)
        self.inputs = {"jump": False, "squat": False, "left": False, "right": False, "fly_mode" : False}
        
    def eval_inputs(self, event):
        """For every pressed or released key, check if player has an action
        variable assigned to the key and change it accordingly"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.inputs["jump"] = True
            if event.key == pygame.K_s:
                self.inputs["squat"] = True
            if event.key == pygame.K_d:
                self.inputs["right"] = True
            if event.key == pygame.K_a:
                self.inputs["left"] = True
            if event.key == pygame.K_f:
                self.inputs["fly_mode"] = not self.inputs["fly_mode"]
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.inputs["jump"] = False
            if event.key == pygame.K_s:
                self.inputs["squat"] = False
            if event.key == pygame.K_d:
                self.inputs["right"] = False
            if event.key == pygame.K_a:
                self.inputs["left"] = False

    def clamp_to_level_edge(self, level_size): #! Deprecated
        """In case player gets to the edge of the world/level, clamp his position
        to said edge"""
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, level_size[0])
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, level_size[1])

    def eval_movement(self):
        """Check the inputs related to the player's movement
        calculate the  horizontal movement using them, calculate vertical movement
        using physics engine (momentum, g_force); check if player can jump and tries to jump"""
        x_input = self.inputs["right"] - self.inputs["left"]
        y_input = self.inputs["squat"] - self.inputs["jump"]
        self.x_movement = x_input * self.speed
        self.momentum = min(3, self.momentum + self.g_force)
        if self.inputs["fly_mode"]:
            self.momentum = self.speed * y_input
        self.y_movement = self.momentum

        if self.jump_ability > 0 and y_input == -1:
            self.momentum = -3
            self.y_movement = self.momentum
            self.jump_ability -= 1
            pygame.mixer.Sound.play(self.sounds["jump"])

    
class Enemy(AnimatedEntity):
    def __init__(self, pos, sprite_sheet, speed=2, colorkey=(255,255,255), sheet_size=(32,32), frame_size=(16,16)) -> None:
        super().__init__(pos, sprite_sheet, speed, colorkey, sheet_size, frame_size)

    def eval_movement(self, player):
        player_dist_x = self.rect.x - player.rect.x
        player_dist_y = self.rect.y - player.rect.y
        player_dist = max((player_dist_x**2 + player_dist_y**2)**0.5, 0.1)

        self.x_movement = self.speed * -player_dist_x / player_dist
        
        self.y_movement = self.speed * -player_dist_y / player_dist

    def update(self, **kwargs) -> None:
        """Updates state of the entity. Calls eval_movement to update how the
        entity should move according to inputs and physics. Adds the values calculated
        in eval_movement for one axis at a time and applies collisions. First checks
        movement and collisions in one axis, then in the other."""
        # calculate movement
        self.eval_movement(kwargs["player"]) 

        #Update entity's position and check collisions
        self.move_and_collide(kwargs["tile_rects"])

        # Screen edge collisions
        if kwargs["level_size"] != 0:
            self.clamp_to_level_edge(kwargs["level_size"])
