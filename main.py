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
    images = setup_lib.load_images(src_dir)
    tile_size = images["dirt"].get_width()
    # Creating a level
    level = levels_lib.Level(level_size=(32, 32))
    level.generate_level_file(src_dir)
    level.load()
    level.create_tile_map_surface(images)
    # Setting up the player object
    player = player_lib.Player((100, 100), speed=3)
    # Setting up camera following the player
    camera = camera_lib.Camera()

    pygame.init()
    running = True
    while running:
        clock.tick(60)
        # Event loop
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

        # Calculating physics
        player.update(
            level.tile_rect_map, (level.rows * tile_size, level.columns * tile_size)
        )
        camera.update(
            player, game_canvas.get_size(), (level.rows, level.columns), tile_size
        )

        # Drawing things onto screen
        game_canvas.fill((100, 100, 255))
        # level.draw_tile_map(game_canvas, images, camera)
        game_canvas.blit(level.tile_map_surf, (-camera.x, -camera.y))
        game_canvas.blit(player.sprite, camera.player_pos)
        # translating game canvas onto entire game window
        window.blit(pygame.transform.scale(game_canvas, window.get_size()), (0, 0))
        # updating the image
        pygame.display.update()


if __name__ == "__main__":
    main()
