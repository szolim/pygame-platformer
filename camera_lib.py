import pygame

class Camera():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.player_pos = [0, 0]
        self.tracked_objects = {}


    def track_surf(self, surface):
        surface_x = self.x + surface.get_rect().x
        surface_y = self.y + surface.get_rect().y
        self.objects[surface] = (surface_x, surface_y) 


    def eval_player_pos(self, vertical_equator, horizontal_equator, player):
        #self.x is always >= 0; it is == 0 when player.rect.x < vertical_equator
        #vertical equator splits the screen in left and right half
        if self.x > 0:
            self.player_pos[0] = vertical_equator
        else:
            self.player_pos[0] = player.rect.x

        if self.y > 0:
            self.player_pos[1] = horizontal_equator
        else:
            self.player_pos[1] = player.rect.y


    def update(self, player, surface_size, level_size, tile_size):
        level_x_max = level_size[0]*tile_size 
        level_y_max = level_size[1]*tile_size
        player_width, player_height = player.sprite.get_width(), player.sprite.get_height()
        horizontal_equator = surface_size[1]/2-player_height/2
        vertical_equator = surface_size[0]/2-player_width/2
        #calculating camera and player positions
        self.x = min(max(player.rect.x - vertical_equator, 0), level_x_max - surface_size[0])
        self.y = min(max(player.rect.y - horizontal_equator, 0), level_y_max - surface_size[1])
        self.eval_player_pos(vertical_equator, horizontal_equator, player)
    
    #if selfx > 0 and selfx < val
    #elif selfx < 0
    #elif selx > val ????????????/ 
