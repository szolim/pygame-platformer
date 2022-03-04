import pygame, os
import levels_lib, player_lib, setup_lib, camera_lib

def main():
    # Creating settings.json file
    setup_lib.set_settings(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings.json")
    )
    # Reading from json settings file
    settings = setup_lib.get_settings("src/settings.json")
    src_dir = settings["src_path"]  # source directory path
    # Setting up display and canvas for the game(needed for pixel scaling)
    window = pygame.display.set_mode(settings["window_size"])
    game_canvas = pygame.Surface((window.get_width() // 4, window.get_height() // 4))
    # Setting up pygame clock object responsible for handling FPS
    clock = pygame.time.Clock()
    # Getting assets
    animated_entities = []
    #images = setup_lib.load_images(src_dir)
    tile_images = setup_lib.load_images(src_dir, "tiles")
    tile_size = tile_images["dirt"].get_width()

    player_images = setup_lib.load_images(src_dir, "player")
    # Creating a level
    CHUNK_SIZE = 8
    #Finite level
    # level = levels_lib.Level(game_canvas, level_size=(64, 32), chunk_size=CHUNK_SIZE)
    # level.generate_level_file(src_dir)
    # level.load()
    #Infinite level
    level_dbg = levels_lib.LevelInf(game_canvas)
    # Setting up the player object
    player = player_lib.Player((100, 100), player_images, speed=3)
    player.setup_animations()
    #Animations
    
    # Setting up camera following the player
    camera = camera_lib.Camera()

    pygame.init()
    #sounds
    jump_sound = pygame.mixer.Sound(os.path.join(src_dir, "sounds", "jump.wav"))
    player.sounds["jump"] = jump_sound
    # pygame.mixer.music.load(os.path.join(src_dir, "sounds", "The Seatbelts - Cats on Mars-97xfV6yXcrk.mp3"))
    # pygame.mixer.music.play(-1)
    animated_entities.append(player)

    running = True
    while running:
        clock.tick(60)
        print(clock.get_fps())
        #* Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                player.eval_inputs(event)
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    exit()
            if event.type == pygame.KEYUP:
                player.eval_inputs(event)

        #* Calculating physics
        #finite level
        # player.update(
        #     level.tile_rect_map, (level.rows * tile_size, level.columns * tile_size)
        # )
        # camera.update(
        #     player, game_canvas.get_size(), (level.rows * tile_size, level.columns * tile_size)
        # )
        #infinite level
        player.update(level_dbg.collision_map)
        camera.update(player, game_canvas.get_size())       

        #* Drawing things onto screen
        game_canvas.fill((100, 100, 255))
        level_dbg.load_chunks(game_canvas, camera, tile_images)
        #level.update_surface(tile_images, camera, game_canvas) #Also blits tile map onto game_canvas
        #animations
        for anim_entity in animated_entities:
            anim_entity.animate()

        game_canvas.blit(player.sprite, camera.player_pos)
        # translating game canvas onto entire game window
        window.blit(pygame.transform.scale(game_canvas, window.get_size()), (0, 0))
        # updating the image
        pygame.display.update()


if __name__ == "__main__":
    main()
