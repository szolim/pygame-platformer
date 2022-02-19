from genericpath import exists
from numpy import size, tile
import pygame, math, os


class Level:
    def __init__(self, game_canvas, level_size=(16, 12), tile_size=16) -> None:
        """Create starting variables, specifying level_size and size of tiles
        used in the level; file which the level will be written to;
        list to store the level file and initialized objects built from the
        level file."""
        self.rows = level_size[0]
        self.columns = level_size[1]
        self.tile_size = tile_size
        self.file = ""
        self.map_file = []
        self.tile_rect_map = []
        self.tile_map_surf = pygame.Surface(
            (game_canvas.get_size()[0], game_canvas.get_size()[1])
        )

    def generate_level_file(self, src_dir):
        """WIP. Generates text file filled with digits which determine what
        image will be drawn onto the game canvas. """
        path_to_file = os.path.join(src_dir, "levels{}test_level.txt".format(os.sep))
        with open(path_to_file, "w+") as f:
            for y in range(self.columns):
                if y <= self.columns // 3:
                    f.write("1{}1\n".format("0" * (self.rows - 2)))
                elif y <= self.columns // 2:
                    f.write("{}\n".format("1" * self.rows))
                else:
                    f.write("{}\n".format("2" * self.rows))
        self.file = path_to_file

    def load(self):
        """Loads the level file, e.g. created by generate_level_file func
        and creates fixed rect map"""
        with open(self.file) as f:
            data = f.read()
            data = data.split("\n")
            #Omits the last line of a file as it's just an empty line
            for row in data[:len(data)-1:]:
                self.map_file.append(list(row))
        self.tile_rect_map = []
        y = 0
        for row in self.map_file:
            x = 0
            for tile in row:
                if tile != "0":
                    rect = pygame.Rect(
                        x * self.tile_size,
                        y * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    )
                    self.tile_rect_map.append(rect)
                x += 1
            y += 1

    def update_surface(self, tile_images, camera, canvas):
        y = 0
        for row in self.map_file:
            x = 0
            for tile in row:
                tile_pos_x = x * self.tile_size - camera.x
                tile_pos_y = y * self.tile_size - camera.y
                if tile == "0":
                    canvas.blit(
                        tile_images["sky"], (tile_pos_x, tile_pos_y)
                    )
                if tile == "1":
                    canvas.blit(
                        tile_images["grass"], (tile_pos_x, tile_pos_y)
                    )
                if tile == "2":
                    canvas.blit(
                        tile_images["dirt"], (tile_pos_x, tile_pos_y)
                    )
                x += 1
            y += 1
    
    # def draw_tile_map(self, surface, tile_images, camera):
    #     y = 0
    #     for row in self.map_file:
    #         x = 0
    #         for tile in row:
    #             tile_pos_x = x * self.tile_size - camera.x
    #             tile_pos_y = y * self.tile_size - camera.y
    #             if tile == "0":
    #                 surface.blit(tile_images["sky"], (tile_pos_x, tile_pos_y))
    #             if tile == "1":
    #                 surface.blit(tile_images["grass"], (tile_pos_x, tile_pos_y))
    #             if tile == "2":
    #                 surface.blit(tile_images["dirt"], (tile_pos_x, tile_pos_y))
    #             x += 1
    #         y += 1