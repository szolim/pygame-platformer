import pygame, os
import levels_lib, entity, setup_lib, camera_lib

class Gui():
    def __init__(self, size) -> None:
        self.surf = pygame.Surface(size)
        self.surf.set_colorkey((0,0,0))
        self.gui_elements = []
        self.color = (255,255,255)

    def draw(self, active_screen):
        self.screen = active_screen
        surf_percent = (self.surf.get_width()/100, self.surf.get_height()/100)
        button_exit = (pygame.Rect(25*surf_percent[0], 35*surf_percent[1], 50*surf_percent[0], 30*surf_percent[1]))
        #button_exit = pygame.Rect(50,50,50,50)
        
        self.gui_elements = [button_exit]
        for element in self.gui_elements:
            pygame.draw.rect(self.surf, (self.color), (element.left, element.top, element.width, element.height))
            #self.surf.blit(element[0], (element[1].x, element[1].y))

    def check_events(self, mousepos, mouse_button_left):
        self.color = (255,0,0)
        for element in self.gui_elements:
            if element.collidepoint(mousepos) and mouse_button_left:
                return "game"
            else:
                return None


class Game():
    def __init__(self):
        self.active_screen = "menu"

    def setup(self):
        # Creating settings.json file
        settings_path = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings.json"))
        with open(str(settings_path), "w") as settings:
            setup_lib.set_settings(settings_path)
        # Reading from json settings file    
        settings = setup_lib.get_settings(settings_path)
        self.src_dir = settings["src_path"]  # source directory path
        # Setting up display and canvas for the game(needed for pixel scaling)
        self.window = pygame.display.set_mode(settings["window_size"])
        self.game_canvas = pygame.Surface((self.window.get_width() // 4, self.window.get_height() // 4))
        # Setting up GUI surface
        self.GUI = Gui((self.window.get_width(), self.window.get_height()))
        # Setting up pygame clock object responsible for handling FPS
        self.clock = pygame.time.Clock()
        # Getting assets
        #images = setup_lib.load_images(src_dir)
        self.tile_images = setup_lib.load_images(self.src_dir, "tiles")
        self.player_images = setup_lib.load_images(self.src_dir, "player")
        self.enemy_images = setup_lib.load_images(self.src_dir, "enemy")

    def menu(self):
        pygame.init()
        pygame.mixer.music.load(os.path.join(self.src_dir, "sounds", "The Seatbelts - Cats on Mars-97xfV6yXcrk.mp3"))
        pygame.mixer.music.play(-1)
        change_screen = False
        while True:
            self.clock.tick(60)
            #* Event loop
            mouse_left_pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    change_screen = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        change_screen = True
                if event.type == pygame.KEYUP:
                    pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_left_pressed = True
            if change_screen:
                self.active_screen = "game"
                return False
            mouse_pos = pygame.mouse.get_pos()
            
            gui_events = self.GUI.check_events(mouse_pos, mouse_left_pressed)
            if gui_events != None:
                print(gui_events)
                self.active_screen = gui_events
                break

            self.GUI.draw("menu")

            self.game_canvas.fill((100,255,100))    
            self.window.blit(pygame.transform.scale(self.game_canvas, self.window.get_size()), (0, 0))
            self.window.blit(self.GUI.surf, (0, 0))
            # updating the image
            pygame.display.update()

    def main_loop(self):
        # Creating a level
        CHUNK_SIZE = 8
        level_dbg = levels_lib.LevelInf(self.game_canvas)
    
        # Setting up the player object
        player = entity.Player((300, 100), self.player_images, speed=3)
        player.setup_animations()
        #Setting up other entities
        enemy1 = entity.Enemy((200, 100), self.enemy_images, frame_size=(32,32))
        enemy1.setup_animations()
        #Animations
        
        # Setting up camera following the player
        camera = camera_lib.Camera()

        pygame.init()
        #sounds
        jump_sound = pygame.mixer.Sound(os.path.join(self.src_dir, "sounds", "jump.wav"))
        jump_sound.set_volume(0.2)
        player.sounds["jump"] = jump_sound
        pygame.mixer.music.load(os.path.join(self.src_dir, "sounds", "beepbox.wav"))
        pygame.mixer.music.play(-1)
        animated_entities = [player, enemy1]
        change_screen = False

        running = True
        while running and self.active_screen == "game":
            self.clock.tick(60)
            #* Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    change_screen = True
                    self.active_screen = "exit_screen"
                if event.type == pygame.KEYDOWN:
                    player.eval_inputs(event)
                    if event.key == pygame.K_ESCAPE:
                        change_screen = True
                        self.active_screen = "exit_screen"
                if event.type == pygame.KEYUP:
                    player.eval_inputs(event)
            
            if change_screen:
                return False

            #* Calculating physics
            camera.update(player, self.game_canvas.get_size())       

            #* Drawing things onto screen
            self.game_canvas.fill((100, 100, 255))
            level_dbg.load_chunks(self.game_canvas, camera, self.tile_images)
            #level.update_surface(tile_images, camera, game_canvas) #Also blits tile map onto game_canvas
            #animations
            for anim_entity in animated_entities:
                anim_entity.update(tile_rects=level_dbg.collision_map, player=player, level_size=0)
                anim_entity.animate()
                if anim_entity is player:
                    self.game_canvas.blit(anim_entity.sprite, camera.player_pos)
                else:
                    self.game_canvas.blit(anim_entity.sprite, (anim_entity.rect.x-camera.x, anim_entity.rect.y-camera.y))
        
            # translating game canvas onto entire game window
            self.window.blit(pygame.transform.scale(self.game_canvas, self.window.get_size()), (0, 0))
            # updating the image
            pygame.display.update()

    def exit_game(self):
        pygame.quit()
        return True

    def swap_screen(self):
        self.screens = {"menu" : self.menu(), "game" : self.main_loop(), "exit_screen" : self.exit_game()}
        if self.active_screen in self.screens:
            print(self.active_screen)
            do_exit_game = self.screens[self.active_screen]
        return do_exit_game