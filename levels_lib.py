import random, math
import pygame, os


class Level:
    def __init__(self, game_canvas, level_size=(16, 12), tile_size=16, chunk_size=8) -> None:
        """Create starting variables, specifying level_size and size of tiles
        used in the level; file which the level will be written to;
        list to store the level file and initialized objects built from the
        level file."""
        self.rows = level_size[0]
        self.columns = level_size[1]
        self.CHUNK_SIZE = chunk_size
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
                if y < self.columns // 3:
                    f.write("1{}1\n".format("0" * (self.rows - 2)))
                elif y == self.columns // 3:
                    f.write("1{}1\n".format("3" * (self.rows - 2)))
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
                if tile != "0" and tile != "3":
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
                    pass
                    # canvas.blit(
                    #     tile_images["sky"], (tile_pos_x, tile_pos_y)
                    # )
                elif tile == "1":
                    canvas.blit(
                        tile_images["grass"], (tile_pos_x, tile_pos_y)
                    )
                elif tile == "2":
                    canvas.blit(
                        tile_images["dirt"], (tile_pos_x, tile_pos_y)
                    )
                elif tile == "3":
                    canvas.blit(
                        tile_images["plant"], (tile_pos_x, tile_pos_y)
                    )
                x += 1
            y += 1
    
    def generate_chunk(self, x, y):
        chunk_data = []
        for y_pos in range(self.CHUNK_SIZE):
            for x_pos in range(self.CHUNK_SIZE):
                target_x = x * self.CHUNK_SIZE + x_pos
                target_y = y * self.CHUNK_SIZE + y_pos
                tile_type = 0
                if target_y > 10:
                    tile_type = 2
                elif target_y == 10:
                    tile_type = 1
                elif target_y == 9:
                    if random.random() < 0.3:
                        tile_type = 3
                if tile_type != 0:
                    chunk_data.append([[target_x, target_y], tile_type])
        return chunk_data

    def draw_chunks(self, x, y):
        game_map = {}


class LevelInf():
    def __init__(self, game_canvas, tile_size=16, chunk_size=8) -> None:
        """Create starting variables, specifying level_size and size of tiles
        used in the level; file which the level will be written to;
        list to store the level file and initialized objects built from the
        level file."""
        self.CHUNK_SIZE = chunk_size
        self.tile_size = tile_size
        self.game_map = {}
        self.collision_map = []
        # self.file = ""
        # self.map_file = []
        # self.tile_rect_map = []
        # self.tile_map_surf = pygame.Surface(
        #     (game_canvas.get_size()[0], game_canvas.get_size()[1])
        # )

    def generate_chunk(self, x, y):
        chunk_data = []
        for y_pos in range(self.CHUNK_SIZE):
            for x_pos in range(self.CHUNK_SIZE):
                target_x = x * self.CHUNK_SIZE + x_pos
                target_y = y * self.CHUNK_SIZE + y_pos
                tile_type = "sky"
                if target_y > 10:
                    tile_type = "dirt"
                elif target_y == 10:
                    tile_type = "grass"
                elif target_y == 9:
                    if random.random() < 0.3:
                        tile_type = "plant"
                if tile_type != "sky":
                    chunk_data.append([[target_x, target_y], tile_type])
        return chunk_data

    def load_chunks(self, canvas, camera, tile_images):
        self.collision_map = []
        chunks_to_draw_x = math.ceil(canvas.get_width() / (self.CHUNK_SIZE*self.tile_size)) + 1
        chunks_to_draw_y = math.ceil(canvas.get_height() / (self.CHUNK_SIZE*self.tile_size)) + 1
        for y in range(chunks_to_draw_y):
            for x in range(chunks_to_draw_x):
                target_x = int(x + math.floor(camera.x / (self.CHUNK_SIZE*self.tile_size)))
                target_y = int(y + math.floor(camera.y / (self.CHUNK_SIZE*self.tile_size)))
                target_chunk = str(target_x) + "_" + str(target_y)
     
                if target_chunk not in self.game_map:
                    self.game_map[target_chunk] = self.generate_chunk(target_x, target_y)
                for tile in self.game_map[target_chunk]:
                    tile_type = tile_images[tile[1]] #tile[1] stores what type of tile it should be
                    canvas.blit(tile_type, (tile[0][0]*self.tile_size-camera.x, tile[0][1]*self.tile_size-camera.y))

                    if tile[1] != "plant":
                        #print(tile[0][0]*self.tile_size, tile[0][1]*self.tile_size, camera.x, camera.y, camera.player_pos[0], camera.player_pos[1])
                        self.collision_map.append(pygame.Rect(tile[0][0]*self.tile_size, tile[0][1]*self.tile_size, self.tile_size, self.tile_size))
                        #self.collision_map.pop(0)
