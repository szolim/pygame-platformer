import pygame

class Spritesheet():
    def __init__(self, img, res, frame_size) -> None:
        """Sprite sheet object. Contains an image and grid, evaluated from
        image size and frame size."""
        #self.surf = pygame.image.load(img).convert()
        self.surf = img
        self.surf.set_colorkey((0,0,0))
        self.res = res
        self.frame_size = frame_size

    def get_frames(self, frame_amount=0, starting_point=0):
        """Creates a grid upon an image transformed into a pygame.Surface object. For
        each square/rectangle in grid, takes the square/rectangle and puts its contents
        into a new surface. Returns list of these surfaces. Frame amount lets you specify how many
        consecuting regions in x,y grid you want to be included in frames. Starting
        point is the first region included in list of grid elements you want to get."""
        #How many frames to include
        if frame_amount != 0:
            frame_amount = frame_amount
        else:
            frame_amount = self.res[0] / self.frame_size[0] * self.res[1] / self.frame_size[1]      
        #Returns an error if image size isn't divisible by single frame size
        if (self.res[0] / self.frame_size[0]).is_integer() and (self.res[1] / self.frame_size[1]).is_integer():
            frames_x = self.res[0] // self.frame_size[0]
            frames_y = self.res[1] // self.frame_size[1]
        else:
            print("The image resolution isn't divisible by frame frame_size")
            return
        #Which element in grid will be included as first.
        start_point = starting_point
        starting_x = 0
        starting_y = 0
        while starting_point > 0:
            if starting_point > frames_x:
                starting_y += 1
                starting_point -= frames_x

            starting_x += 1
            starting_point -= 1

        frame_list = [] #list of new surfaces
        #scan the grid and copy each fragment
        for y in range(0, frames_y):
            for x in range(0, frames_x):
                #Ending condition. x = elements in row; y*frames_x = elements in previous rows
                if x + y * frames_x == frame_amount + start_point:
                    return frame_list

                frame_x = (x + starting_x)
                frame_y = (y + starting_y)
                #print(frame_y, frame_x)
                if frame_x == frames_x:
                    starting_x = 0
                    break
                if frame_y == frames_y:
                    break

                new_surf = pygame.Surface((self.frame_size[0], self.frame_size[1])) #creates surface to contain the frame
                new_surf.blit(self.surf, (-frame_x*self.frame_size[0],-frame_y*self.frame_size[1])) #puts current part of image in the frame
                frame_list.append(new_surf)
        return frame_list
