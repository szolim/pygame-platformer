import random, math, pygame, noise

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

    def generate_chunk(self, x, y):
        chunk_data = []
        for y_pos in range(self.CHUNK_SIZE):
            for x_pos in range(self.CHUNK_SIZE):
                target_x = x * self.CHUNK_SIZE + x_pos
                target_y = y * self.CHUNK_SIZE + y_pos
                tile_type = "sky"
                height = int(noise.pnoise1(target_x*0.1, repeat=999999) * 5)

                if target_y > 8 - height:
                    tile_type = "dirt"
                elif target_y == 8 - height:
                    tile_type = "grass"
                elif target_y == 8 - height - 1:
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
