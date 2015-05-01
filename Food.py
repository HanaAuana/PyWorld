#Michael Lim CS431 Fall 2013

import pygame
import random
#Define some color constants
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
#Define size constant
SIZE = 10

#A class to define the food objects. Inherits from the pygame.Sprite class to facilitate drawing
class Food(pygame.sprite.Sprite):

    # Constructor. Takes a tuple in the form (x,y) that denotes the starting location
    def __init__(self, loc):
        #Call the super class constructor
        pygame.sprite.Sprite.__init__(self)

        #Set up some variables used by the Sprite for drawing purposes
        #Determines the size of the Sprite
        self.image = pygame.Surface([SIZE, SIZE])
        #Determines the background color of the Sprite
        self.image.fill(WHITE)
        #Sets up the boundry of the Sprite
        self.rect = self.image.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]
        self.radius = SIZE*0.1
        #Draws what the Sprite will look like when it is displayed
        pygame.draw.ellipse(self.image, GREEN, [0, 0, SIZE, SIZE])

        #Food has a 50% chance of being poisonous. Will impact Organisms that eat it
        isEdible = random.randint(0, 1)
        if isEdible == 0:
            self.isEdible = False
        else:
            self.isEdible = True