#Michael Lim CS431 Fall 2013

#Movement algorithm adapted from http://www.petercollingridge.co.uk/pygame-physics-simulation/movement

import pygame
import random
import math

#Define a constant for the color white
WHITE = (255, 255, 255)

#Define constants for the size of the world the Organism will live in
WORLDWIDTH = 1000
WORLDHEIGHT = 1000

#A class to represent the organisms that we will be evolving.
# Inherits from the pygame.Sprite class to facilitate drawing and collision detection
class Organism(pygame.sprite.Sprite):
    #Constructor takes a DNA instance, an array denoting the starting [x,y] location
    # and an array of x,y coordinates denoting the location of each Food object in the World
    def __init__(self, newDNA, birthplace, foodLocs):
        #Call the super class constructor
        pygame.sprite.Sprite.__init__(self)
        #Set some instance variable from the parameters
        self.genes = newDNA
        self.location = birthplace
        self.foodLocations = foodLocs
        #Pick a random starting direction
        self.direction = random.uniform(0, math.pi*2)
        #Set starting health to 300
        self.health = 300
        #Declare some instance variables that will be set according to the Organisms DNA
        self.size = 0
        self.maxSpeed = 0
        self.color = (0, 0, 0)
        self.turning = 0
        self.metabolism = 0
        self.poisonResistance = 0
        self.photoSyn = 0
        #Call expressGenes() to set above variables based on genotype as determined by the DNA instance
        self.expressGenes()

        #Set size of the sprite
        self.image = pygame.Surface([self.size, self.size])
        #Sets the background of the Sprite
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        #Sets the boundries for the Sprite
        self.rect = self.image.get_rect()
        self.radius = self.size*0.8
        #Draws what the Sprite will look like
        pygame.draw.ellipse(self.image, self.color, [0, 0, self.size, self.size])
    #Overiding the super class update method. Will be called at each frame
    def update(self):
        #If the organism is still alive, process any opportunities to eat nearby food, then move
        #Finally, redraw the Sprite to account for any changes
        if self.stillAlive():
            self.eat()
            self.updateLocation()
            pygame.draw.ellipse(self.image, self.color, [0, 0, self.size, self.size])
    #Handles the organism eating nearby food
    def eat(self):
        #Look at each food object in the World
        for f in self.foodLocations:
            #Use a pygame.sprite method to determine if the Organism has come across some Food
            if pygame.sprite.collide_circle(self, f):
                #Determine if the food is poisonous or not
                #If the food is not poisonous
                if f.isEdible:
                    #The organism gains health according to its size, and the food is removed
                    self.health += max(100 - self.size, 0)
                    self.foodLocations.remove(f)
                #If the food is poisonous
                else:
                    #Calculate a random number 1-100
                    deathThreshold = random.randrange(0, 100)
                    #If the organism's resistance to poison is greater (Organism is immune to the poison)
                    if deathThreshold < self.poisonResistance:
                        #The organism gains health according to its size, and the food is removed
                        self.health += max(100 - self.size, 0)
                        self.foodLocations.remove(f)
                    #If the organism fails the poison check
                    else:
                        #The organism loses health relative to its poison resistance, and the food is removed
                        self.health -= (100-self.poisonResistance)
                        self.foodLocations.remove(f)
        #There is a 1% chance to increase health according to its ability to photosynthesize
        photoSynChance = random.randrange(0, 100)
        if photoSynChance < 1:
            self.health += (self.photoSyn*0.01)
        #Decrease the Organisms health according to its metabolism
        self.health -= (0 + self.metabolism)

        #Update the organisms transparency according to its current health
        self.image.set_alpha(self.health)
    #Computes the Organisms next location
    def updateLocation(self):
        #Compute a random int 0-100
        shouldTurn = random.randrange(0, 100)
        #If the Organisms turning value is greater
        if shouldTurn < self.turning:
            #Pick a new direction
            self.direction = random.uniform(0, math.pi*2)
        #Update the organisms location based on the direction its "facing" and its speed
        self.rect.x -= math.sin(self.direction) * self.maxSpeed
        self.rect.y -= math.cos(self.direction) * self.maxSpeed
        #If the Organism runs into the right hand wall
        if self.rect.right >= WORLDWIDTH:
            #Don't let the organism go past the edge, and make it pick a random direction
            self.rect.x = WORLDWIDTH-self.size
            self.direction = random.uniform(0, math.pi*2)
        #If the Organism runs into the left hand wall
        elif self.rect.left <= 0:
            #Don't let the organism go past the edge, and make it pick a random direction
            self.rect.x = 0
            self.direction = random.uniform(0, math.pi*2)
        #If the Organism runs into the bottom wall
        if self.rect.bottom >= WORLDHEIGHT:
            #Don't let the organism go past the edge, and make it pick a random direction
            self.rect.y = WORLDHEIGHT-self.size
            self.direction = random.uniform(0, math.pi*2)
        #If the Organism runs into the top wall
        elif self.rect.top <= 0:
            #Don't let the organism go past the edge, and make it pick a random direction
            self.rect.y = 0
            self.direction = random.uniform(0, math.pi*2)
    #Calls separate methods to express each gene
    def expressGenes(self):
        self.expressSize()
        self.expressSpeed()
        self.expressTurning()
        self.expressMetabolism()
        self.expressPoisonResistance()
        self.expressPhotoSyn()
        self.expressColor()
    #Uses genes 0-4 to determine the Organism size
    def expressSize(self):
        gene0to4 = self.genes.getGene(0) + self.genes.getGene(1) + self.genes.getGene(2) + self.genes.getGene(3) + self.genes.getGene(4)
        self.size = int(gene0to4, 2)
    #Uses genes 5-8 to determine the Organism speed
    def expressSpeed(self):
        gene5to8 = self.genes.getGene(5) + self.genes.getGene(6) + self.genes.getGene(7) + self.genes.getGene(8)
        self.maxSpeed = int(gene5to8, 2)
    #Uses genes 9-12 to determine the Organism's likelihood of turning
    def expressTurning(self):
        gene9to12 = self.genes.getGene(9) + self.genes.getGene(10) + self.genes.getGene(11) + self.genes.getGene(12)
        self.turning = int(gene9to12, 2)
    #Uses genes 13-17 to determine how quickly the organism loses health
    def expressMetabolism(self):
        gene13to17 = self.genes.getGene(13) + self.genes.getGene(14) + self.genes.getGene(15)+self.genes.getGene(16) + self.genes.getGene(17)
        self.metabolism = 1 + int(gene13to17, 2)
    #Uses genes 18-23 to determine the Organism's likelihood of surviving eating poisonous food
    def expressPoisonResistance(self):
        gene18to23 = self.genes.getGene(18) + self.genes.getGene(19) + self.genes.getGene(20) + self.genes.getGene(21) + self.genes.getGene(22) + self.genes.getGene(23)
        self.poisonResistance = int(gene18to23, 2)
    #Uses genes 24-30 to determine the Organism's ability to generate its own food and raise its health
    def expressPhotoSyn(self):
        gene24to30 = self.genes.getGene(24) + self.genes.getGene(25) + self.genes.getGene(26) + self.genes.getGene(27) + self.genes.getGene(28) + self.genes.getGene(29) + self.genes.getGene(30)
        self.photoSyn = int(gene24to30, 2)
    #Uses genes 31-39 to determine the Organism coloring
    def expressColor(self):
        gene31to33 = self.genes.getGene(31) + self.genes.getGene(32) + self.genes.getGene(33)
        gene34to36 = self.genes.getGene(34) + self.genes.getGene(35) + self.genes.getGene(36)
        gene37to39 = self.genes.getGene(37) + self.genes.getGene(38) + self.genes.getGene(39)
        #31-33 determine the R value, 34-36 determine the G value, and 37-39 determine the B value
        rValue = int(gene31to33, 2)
        gValue = int(gene34to36, 2)
        bValue = int(gene37to39, 2)

        self.color = (31*rValue, 31*gValue, 31*bValue)
    #Determines if the Organism is still alive
    def stillAlive(self):
        #If the Organisms health is 0 or lower, then it is dead
        if self.health <= 0.0:
            return False
        else:
            return True