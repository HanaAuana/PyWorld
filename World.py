#Michael Lim CS431 Fall 2013

#Basic structure adapted from below project template:
#http://programarcadegames.com/python_examples/f.php?file=pygame_base_template.py


#Runs a simulation of an ecosystem

#Press the up or down arrow to increase/decrease simulation by steps of 10
#Press the left arrow to set simulation speed to 10, press the right arrow to set speed to 10,000



import pygame
import random
import Organism
import Food
import DNA
import math

#The following values can be changed to affect the overall simulation

#Define the size of the population for each genereation
POPSIZE = 20
#Define the "frames per second" (Not exactly, but this determines how fast the simulation runs)
fps = 100
#Define how many Generations we want to run for
NUMGENERATIONS = 50


#Changing the below values is not advised

#Define the size of the ecosystem
ECOWIDTH = 1000
ECOHEIGHT = 1000
#Define a constant for white
WHITE = (255, 255, 255)
#Define the number of genes the Organisms will have
NUMGENES = 40



#Determines a new population, given an array of candidates and the size of the population
#Each candidate is evaluated based on its "fitness," and chosen proportionally depending on how it did
#compared to the rest of the candidates
def getNextPop(candidates, sizeOfNextPop):

    sumFitness = 0
    #Initialize an array that will hold the probabilities of each candidate being chosen
    candidateProbs = ['' for i in range(len(candidates))]
    #Loop through all the candidates and compute the sum of all of their fitness scores
    for c in range(len(candidates)):
        sumFitness += float(candidates[c][1])
        #Store the fitness of each candidate in the probability array for now
        candidateProbs[c] = (c, candidates[c][1])

    for i in range(len(candidateProbs)):
        #Divide each candidates fitness by the sum of all the fitnesses to determine its proportion
        candidateProbs[i] = (i, (candidateProbs[i][1]/sumFitness)*100)

    prevBoundry = 0.0
    #Set up an array to hold the "boundrys" for each candidate,
    # which are proportionate based on the individuals fitness
    candidateBoundrys = [(0, 0, 0) for i in range(len(candidateProbs))]
    b = 0
    for p in candidateProbs:
        #Give each candidate a range, based on its proportion, and the end of the last boundry
        candidateBoundrys[b] = (p[0], prevBoundry, float(prevBoundry+p[1]))
        prevBoundry = candidateBoundrys[b][2]
        b += 1

    #Create an empty array to hold the next population
    nextPop = []
    #We will need n/2 sets of parents, where n is the size of the population we want
    for counter in range((int(math.ceil(sizeOfNextPop/2)))):
        parentA = None
        parentB = None
        #While we still need to select a parent A

        #Will be used to store parent A to be reintroduced after parentB is chosen
        parentATemp = None
        while parentA is None:

            #Pick a random number (1-100, scaled up by 100)
            nextMate = random.randrange(100.0, 10000.0)/100.0
            #Look through all of the boundries
            for a in candidateBoundrys:
                #Select the candidate whose boundry contains the selected random value
                if a[1] < nextMate < a[2]:
                    #Set that candidate to be Parent A
                    parentA = candidates[a[0]][0]
                    #Remove that candidate from the list
                    parentATemp = a
                    candidateBoundrys.remove(a)
        #While we still need to select a parent B
        while parentB is None:
            #If there's only one candidate left, just use that one, no need to randomly select
            if len(candidateBoundrys) == 1:
                b = candidateBoundrys.pop()
                #Set that candidate to be Parent B
                parentB = candidates[b[0]][0]
            else:
                #Pick a random number (1-100, scaled up by 100)
                nextMate = random.randrange(100.0, 10000.0)/100.0
                #Look through all of the boundries
                for b in candidateBoundrys:
                    #Select the candidate whose boundry contains the selected random value
                    if b[1] < nextMate < b[2]:
                        #Set that candidateto be Parent B, and remove the candidate from the list
                        parentB = candidates[b[0]][0]
                        #candidateBoundrys.remove(b)
        candidateBoundrys.append(parentATemp)
        #Using the two parents , create two children DNA using crossover
        childADNA, childBDNA = crossover(parentA, parentB, len(parentA.genes.dna))
        #Mutate the DNA of each child
        childADNA = mutate(childADNA)
        childBDNA = mutate(childBDNA)
        #Add the children DNA to the next population
        nextPop.append(childADNA)
        nextPop.append(childBDNA)
    #Return the population
    return nextPop

#Given two parent Organisms and the length of those parents DNA, generate two children
def crossover(parentA, parentB, numGenes):
    #Initialize two empty strings for the children
    childADNA = ""
    childBDNA = ""
    #For the length of the genotype
    for thisGene in range(numGenes):
        #Randomly pick to use either Parent A or Parent B
        if random.randint(0, 1) == 0:
            #If child A gets gene from Parent A, child B gets gene from Parent B
            childADNA += parentA.genes.getGene(thisGene)
            childBDNA += parentB.genes.getGene(thisGene)
        else:
            #If child A gets gene from Parent B, child B gets gene from Parent A
            childADNA += parentB.genes.getGene(thisGene)
            childBDNA += parentA.genes.getGene(thisGene)
    #Return the created DNA strings
    return childADNA, childBDNA

#Given a sring containing a genotype, perform some mutations
def mutate(genes):

    newGenes = ""
    #For each gene in the genotype
    for g in range(len(genes)):
        gene = genes[g]
        #Use a 5% chance of mutating. If we decide to mutate this gene, reverse it's value
        if random.randrange(0, 100) < 5:
            if gene == "0":
                newGenes += "1"
            else:
                newGenes += "0"
        #Otherwise, leave it unchanged
        else:
            newGenes += gene
    #Return the new genotype
    return newGenes
	
#Initialize a counter for the number of Generations we want to run
runs = 0

#Initialize an array for the next populations DNA
nextPopDNA = []
#While we have another generation to run
while runs < NUMGENERATIONS:

    #Initialize score to 0. This is incremented each loop through the simulation
    #and is used to determine fitness
    score = 0
    #Initialize pygame
    pygame.init()
    #Initialize a list to hold the organisms as they die
    deadList = []
    #Create a Sprite Group to hold the Food objects
    fList = pygame.sprite.Group()
    #Create 100 Food objects to start, all at random locations, and add them to the list
    for i in range(100):
        f = Food.Food([random.randrange(ECOWIDTH), random.randrange(ECOHEIGHT)])

        fList.add(f)
    #Create a Sprite Group to hold the Organisms
    oList = pygame.sprite.Group()

    #The first generation we want to create random organisms

    if runs == 0:
        #Create a list of POPSIZE Organisms, all with random DNA, and at random locations
        for countOrganism in range(POPSIZE):
            d = DNA.DNA(NUMGENES, None)
            o = Organism.Organism(d, [random.randrange(ECOWIDTH), random.randrange(ECOHEIGHT)], fList)
            #Sets the Organisms Sprite location to match its decided location
            o.rect.x = o.location[0]
            o.rect.y = o.location[1]

            oList.add(o)
    #Subsequent generations will be created using crossover and mutation
    else:
        #Create a new list of Organisms, using the generated DNA, all at random locations
        for genes in nextPopDNA:
            d = DNA.DNA(NUMGENES, genes)
            o = Organism.Organism(d, [random.randrange(ECOWIDTH), random.randrange(ECOHEIGHT)], fList)
            #Sets the Organisms Sprite location to match its decided location
            o.rect.x = o.location[0]
            o.rect.y = o.location[1]

            oList.add(o)
        #Clear the list for the next generation
        nextPopDNA = []

    #Set display window size
    displaySize = [ECOWIDTH, ECOHEIGHT]
    display = pygame.display.set_mode(displaySize)

    #Will be used to control the main loop for one generation
    endRun = False

    #Will be used to limit simulation speed
    clock = pygame.time.Clock()
    #While this generation is still running.
    while endRun is False:

        #Handle any PyGame events in the following for loop
        for event in pygame.event.get():
            #If the close button is clicked, then exit
            if event.type == pygame.QUIT:
                endRun = True
            #If a key is pressed
            elif event.type == pygame.KEYDOWN:
                #If the up arrow was pressed, increase simulation speed by 10
                if event.key == pygame.K_UP:
                    fps += 10
                    #Limit simulation speed to 10000 at the fastest
                    fps = min(10000, fps)
                #If the down arrow was pressed, decrease simulation speed by 10
                elif event.key == pygame.K_DOWN:
                    fps -= 10
                    #Limit simulation speed to 10 at the slowest
                    fps = max(10, fps)
                #If the right arrow was pressed, set simulation speed to 10000
                elif event.key == pygame.K_RIGHT:
                    fps = 10000
                #If the left arrow was pressed, set simulation speed to 10
                elif event.key == pygame.K_LEFT:
                    fps = 10

        #Compute game logic
        #There's a 1% chance that a new Food will be generated
        if random.randrange(100) < 1:
            fList.add(Food.Food([random.randrange(ECOWIDTH), random.randrange(ECOHEIGHT)]))
        #If there are no more living Organisms, the generation is over
        #Compute statistics and generate DNA for next generation
        if len(oList) == 0:
            #Sort the list of dead organisms by their score
            deadList.sort(key=lambda item: item[1])
            #Pass the list of dead organisms to be used for deciding the next generation
            nextPopDNA = getNextPop(deadList, (POPSIZE-2))
            #Print some helpful information for watching the DNA change each generation
            print "Top 10 for generation " + str(runs+1)
            print "Size | Speed | Turn | Metab. | P. Res.| PhotoSyn | R | G | B "
            sumScores = 0
            #Print the genotypes of the top 50% of this generation and their scores
            for n in range(int(len(deadList)*0.5)):
                temp = deadList[-(n+1)]
                sumScores += temp[1]

                print temp[0].genes.getGeneotype() + " " + str(temp[1])

            #Print the average score for this generation
            print "Avg score: " + str(sumScores/float(len(deadList)))
            print ""

            #Take the top 2 performing Organisms from this generation and add them to the next population
            nextPopDNA.append(deadList[-1][0].genes.getGeneotypeString())
            nextPopDNA.append(deadList[-2][0].genes.getGeneotypeString())
            #Set flag to end game loop
            endRun = True
        #Increase score by 1
        score += 1
        #For each Organism that's still alive
        for o in oList:
            #Check if it is still alive
            if not o.stillAlive():
                #If not, remove it from the list, and add it to the list of dead Organisms
                oList.remove(o)
                deadList.append((o, score))

        #Clear screen to avoid "ghosting" from last drawing
        display.fill(WHITE)
        #Draw game to the screen
        #Calls the update function for each living Organism
        oList.update()
        #Draws all the food
        fList.draw(display)
        #Draws each organism
        oList.draw(display)

        #Limit "frames per second"
        clock.tick(fps)

        #Update screen with new graphics
        pygame.display.flip()

    #Generation is done, increment counter and close window
    runs += 1
    pygame.quit()
