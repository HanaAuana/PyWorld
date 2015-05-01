#Michael Lim CS431 Fall 2013


import random

# A class to hold a binary string representing the DNA of an organism
class DNA():
    #Takes an int representing the number of genes, and possibly an existing genotype to use
    def __init__(self, numGenes, existingGenes):

        self.numGenes = numGenes
        #If a genotype is given, use this
        if existingGenes is not None:
            self.dna = existingGenes
        #Else, create a random genotype
        else:
            self.dna = ""
            #Randomly pick 1 or 0 for the required number of genes
            for i in range(0, numGenes):
                value = random.randint(0, 1)

                if value == 0:
                    self.dna += "0"
                else:
                    self.dna += "1"
    #Given a number, return the corresponding bit
    def getGene(self, num):
        return self.dna[num]

    #Return a string containing the genotype of this instance. Bits are grouped as they are expressed in an Organism
    def getGeneotype(self):
        #Get a string for each gene that an Organism will express
        gene0to4   = self.getGene(0)  + self.getGene(1)  + self.getGene(2)  + self.getGene(3) + self.getGene(4)
        gene5to8   = self.getGene(5)  + self.getGene(6)  + self.getGene(7)  + self.getGene(8)
        gene9to12  = self.getGene(9)  + self.getGene(10) + self.getGene(11) + self.getGene(12)
        gene13to17 = self.getGene(13) + self.getGene(14) + self.getGene(15) + self.getGene(16) + self.getGene(17)
        gene18to23 = self.getGene(17) + self.getGene(18) + self.getGene(19) + self.getGene(20) + self.getGene(21) + self.getGene(22)
        gene24to30 = self.getGene(24) + self.getGene(25) + self.getGene(26) + self.getGene(27) + self.getGene(28) + self.getGene(29) + self.getGene(30)
        gene31to33 = self.getGene(31) + self.getGene(32) + self.getGene(33)
        gene34to36 = self.getGene(34) + self.getGene(35) + self.getGene(36)
        gene37to39 = self.getGene(37) + self.getGene(38) + self.getGene(39)

        #Prints out each chunk
        genes = ""
        genes += str(gene0to4)+"   "
        genes += str(gene5to8)+"   "
        genes += str(gene9to12)+"   "
        genes += str(gene13to17)+"   "
        genes += str(gene18to23)+"   "
        genes += str(gene24to30)+"   "
        genes += str(gene31to33)+"  "
        genes += str(gene34to36)+"  "
        genes += str(gene37to39)+"  "
        genes += "   "
        #Genes past 40 are also unused, group these together too
        for i in range(40, self.numGenes):
            genes += self.dna[i]

        return genes
    #Returns the genotype as a single contiguous string
    def getGeneotypeString(self):
        genes = ""
        for i in range(0, len(self.dna)):
            genes += self.dna[i]
        return genes