import pygame, spritesheet


class Player():
    def __init__(self, pos, images, speed=2) -> None:
        """Create an instance of Player object, consisting of
        pygame.Surface, pygame.Rects and all the variables
        used by physics engine"""
        # Pygame surf and rect object setup
        self.sprite = pygame.image.load("src/images/player.png")
        self.sprite.set_colorkey((0, 0, 0))
        self.rect = self.sprite.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        #Animation; first word in name of every file in images/player should be here
        self.animation_keys = images
        self.animations = {}
        self.active_animation = None
        self.previous_animation = None
        self.frame_index = 0
        self.frame_timer = 0
        self.flip = [False, False]
        #Sounds
        self.sounds = {}
        # Inputs
        self.inputs = {"jump": 0, "squat": 0, "left": 0, "right": 0}
        # Physics and render engine variables
        self.speed = speed
        self.x_movement = 0
        self.y_movement = 0
        self.jump_ability = 0
        self.momentum = 0
        self.g_force = 0.14

    def setup_animations(self):
        for key, value in self.animation_keys.items():
            frames = spritesheet.Spritesheet(value, (32,32), (16,16)).get_frames()
            for frame in frames:
                frame.set_colorkey((0,0,0))
            self.animations[key] = frames

    def eval_inputs(self, event):
        """For every pressed or released key, check if player has an action
        variable assigned to the key and change it accordingly"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.inputs["jump"] = 1
            if event.key == pygame.K_s:
                self.inputs["squat"] = 1
            if event.key == pygame.K_d:
                self.inputs["right"] = 1
            if event.key == pygame.K_a:
                self.inputs["left"] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.inputs["jump"] = 0
            if event.key == pygame.K_s:
                self.inputs["squat"] = 0
            if event.key == pygame.K_d:
                self.inputs["right"] = 0
            if event.key == pygame.K_a:
                self.inputs["left"] = 0

    def collision_test(self, tiles):
        """For every tile in the list of rects passed as an argument,
        run a pygame func checking if it collides with player rect
        and if it does, add it to the list and return the list"""
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions

    def eval_movement(self):
        """Check the inputs related to the player's movement
        calculate the  horizontal movement using them, calculate vertical movement
        using physics engine (momentum, g_force); check if player can jump and tries to jump"""
        x_input = self.inputs["right"] - self.inputs["left"]
        y_input = self.inputs["squat"] - self.inputs["jump"]
        self.x_movement = x_input * self.speed
        self.momentum = min(3, self.momentum + self.g_force)
        self.y_movement = self.momentum

        if self.jump_ability > 0 and y_input == -1:
            self.momentum = -3
            self.y_movement = self.momentum
            self.jump_ability -= 1
            pygame.mixer.Sound.play(self.sounds["jump"])

    def clamp_to_level_edge(self, level_size):
        """In case player gets to the edge of the world/level, clamp his position
        to said edge"""
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, level_size[0])
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, level_size[1])

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

    def update(self, tile_rects, level_size=0) -> None:
        """Updates state of the player. Calls eval_movement to update how the
        player should move according to inputs and physics. Adds the values calculated
        in eval_movement one at a time and applies collisions. First checks movement and
        collisions in one axis, then in the other."""
        self.eval_movement()  # calculate movement

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

        # Calculates player's y coordinate and overwrites it in case the new value would
        # push a player into a physical tile
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

        # Screen edge collisions
        if level_size != 0:
            self.clamp_to_level_edge(level_size)


# class Entity():
#     def __init__(self, pos, images, speed=2) -> None:
#         """Create an Entity object, consisting of
#         pygame.Surface, pygame.Rects, images and all the variables
#         used by physics engine"""
#         # Pygame surf and rect object setup
#         self.sprite = pygame.image.load(images["idle"][0])
#         self.sprite.set_colorkey((0, 0, 0))
#         self.rect = self.sprite.get_rect()
#         #Where is object in the game world
#         self.rect.x, self.rect.y = pos[0], pos[1]
#         #Sounds
#         self.sounds = {}
#         # Physics and render engine variables
#         self.speed = speed
#         self.x_movement = 0
#         self.y_movement = 0
#         self.jump_ability = 0
#         self.momentum = 0
#         self.g_force = 0.14


# class AnimatedEntity(Entity):
#     def __init__(self, pos, images, speed=2) -> None:
#         super().__init__(pos, images, speed)
#         #Animation; 
#         self.animation_keys = images
#         self.animations = {}
#         self.active_animation = None
#         self.previous_animation = None
#         self.frame_index = 0
#         self.frame_timer = 0
#         self.flip = [False, False]