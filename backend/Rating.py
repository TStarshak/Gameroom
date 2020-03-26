import math

class Rating ():

    def __init__(self, toxic, skill, numEvals):
        #toxic represents how enjoyable it is to play with a certain user
        self.toxic = toxic
        self.skill = skill
        self.numEvals = numEvals

    def updateRating(self, toxic, skill):
        self.toxic = (self.toxic * self.numEvals + toxic) / (self.numEvals + 1)
        self.skill = (self.skill * self.numEvals + skill) / (self.numEvals + 1)
        self.numEvals = self.numEvals + 1

    def getToxRating(self):
        return self.toxic

    def getSkillRating(self):
        return self.skill

    def getRating(self):
        return math.sqrt(self.skill ** 2 + self.toxic ** 2)
