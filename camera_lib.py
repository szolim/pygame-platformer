import pygame


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.player_pos = [0, 0]
        self.tracked_objects = {}

    def track_surf(self, surface):
        """Adds an object to list of tracked objects with its position.
        This may be later used to update positions of all objects and
        iterate through them to draw them onto screen."""
        surface_x = self.x + surface.get_rect().x
        surface_y = self.y + surface.get_rect().y
        self.objects[surface] = (surface_x, surface_y)

    def eval_player_pos(self, vertical_equator, horizontal_equator, player, max_x, max_y):
        """Evaluates player position - always in the middle of screen, so half
        of the screen size further than camera until they are close to the world's
        edge. The camera.player_pos is then equal to player.rect coordinates,
        while camera coordinates stay tuned with player position, but are capped
        so we don't see beyond the level grid."""
        # self.x is always >= 0 and <= x_max; it is == 0 when player.rect.x < vertical_equator
        #and it is == x_max when player.rect.x > level_size - game_canvas size==camera rect size
        # vertical equator splits the screen in left and right half
        if self.x > 0 and self.x < max_x:
            self.player_pos[0] = vertical_equator
        elif self.x == max_x:
            self.player_pos[0] = player.rect.x - self.x
        else:
            self.player_pos[0] = player.rect.x
        #same as above.
        if self.y > 0 and self.y < max_y:
            self.player_pos[1] = horizontal_equator
        elif self.y == max_y:
            self.player_pos[1] = player.rect.y - self.y
        else:
            self.player_pos[1] = player.rect.y

    def update(self, player, surface_size, level_size):
        """Updates camera position which is used to calculate
        where to blit all the surfaces we want to draw onto our
        game canvas. Player stays in the middle of the screen,
        unless they are close to worlds's edge. All the other surfaces
        are placed with offset equaling to camera's coordinates"""
        #Size of a player and finding central lines on screen for player, 
        # taking player's size into account 
        player_width, player_height = (
            player.sprite.get_width(),
            player.sprite.get_height(),
        )
        vertical_equator = surface_size[0] / 2 - player_width / 2
        horizontal_equator = surface_size[1] / 2 - player_height / 2
        #Max possible camera coord values determined by level size
        #Camera captures surface from its coordinates up to the surface_size coordinates
        #thus we subtract the size of screen captured by camera from max possible coords.
        #camera_x_max = level's x size - game canvas size; the same applies to y coordinate.
        camera_x_max = max(0, level_size[0] - surface_size[0])
        camera_y_max = max(0, level_size[1] - surface_size[1])
        # calculating camera and player positions
        self.x = min(
            max(player.rect.x - vertical_equator, 0), camera_x_max
        )
        self.y = min(
            max(player.rect.y - horizontal_equator, 0), camera_y_max
        )
        self.eval_player_pos(vertical_equator, horizontal_equator, player, camera_x_max, camera_y_max)
