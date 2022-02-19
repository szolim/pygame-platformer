import pygame

class Player():
    def __init__(self, pos, speed=2) -> None:
        #Pygame surf and rect object setup
        self.sprite = pygame.image.load("src/images/player.png")      
        self.sprite.set_colorkey((0, 0, 0))
        self.rect = self.sprite.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        #Inputs
        self.inputs = {"jump":0,"squat":0,"left":0,"right":0}
        #Physics and render engine variables
        self.speed = speed
        self.x_movement = 0
        self.y_movement = 0
        self.jump_ability = 0
        self.momentum = 0
        self.g_force = 0.14


    def eval_inputs(self, event):
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
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions


    def eval_movement(self):
        x_input = self.inputs["right"] - self.inputs["left"]
        y_input = self.inputs["squat"] - self.inputs["jump"]
        self.x_movement = x_input * self.speed
        self.momentum = min(3, self.momentum+self.g_force)
        self.y_movement = self.momentum
        just_jumped = False
        if self.jump_ability > 0 and y_input == -1:
            just_jumped = True
            self.momentum = -3
            self.jump_ability -= 1
        return just_jumped


    def clamp_to_level_edge(self, level_size):
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, level_size[0])
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, level_size[1])


    def update(self, tile_rects, level_size) -> None:
        just_jumped = self.eval_movement()
        #moving and colliding
        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        
        self.rect.x += self.x_movement       #horizontal
        for tile in self.collision_test(tile_rects):
            if self.x_movement > 0:
                self.rect.right = tile.left
                collision_types["right"] = True
            if self.x_movement < 0:
                self.rect.left = tile.right
                collision_types["left"] = True
       
        self.rect.y += self.y_movement      #vertical
        self.jump_ability = 0
        for tile in self.collision_test(tile_rects):
            if self.y_movement > 0:
                self.rect.bottom = tile.top
                if just_jumped == False:
                    self.momentum = 0
                    self.jump_ability = 1
                collision_types["bottom"] = True
            if self.y_movement < 0:
                self.rect.top = tile.bottom
                self.momentum = 0
                collision_types["top"] = True

        #Screen edge collisions
        self.clamp_to_level_edge(level_size)
