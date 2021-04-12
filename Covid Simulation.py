# Author      : Ketan Bhailikar
# Requrements : 1) Python3.x 
#               2) pygame [https://pypi.org/project/pygame/]

import pygame
import random
import math
import time
pygame.init()

# Colour Code :-
# Alive and Uninfected : White 
# Alive and Infected   : Red
# Alive and Immune     : Blue   ( People who have been infected before )
# Dead                 : Grey


# Variable that you can alter:
screenSize = 400                # Screen Size
cellSize = 5                    # Size of individual Person
populationSize = 200            # Number of People
speed = 0.009                   # Increase/Decrease in Speed of individual person (Recomended speed = 0.001 - 0.009)
infectedTime = 5                # Amount of time for which a person can remain infected
probabilityOfDying = 10         # Probability that an infected person will die
radiusOfSpread = 20             # The maximum distance that a person has to remain from a infected person to not get infected
probabilityOfInfecting = 30     # Probability of a person getting infected if he comes in contact with a infected person



people = []                     # this array holds the list of people 

class person():
    def __init__(self):
        self.infected = False
        self.removed = False
        self.x = random.randint(0,screenSize)
        self.y = random.randint(0,screenSize)
        self.xvel = 0
        self.yvel = 0
        self.carryingTime = 0
        self.dead = False

    def move(self):

        # removing the person
        if time.time() - self.carryingTime > infectedTime and self.carryingTime != 0 and self.removed == False:
            self.remove()

        # infect people around the infected person
        if self.infected:
            for i in range(len(people)):
                d = math.sqrt((math.pow(self.x - people[i].x,2)) + (math.pow(self.y - people[i].y,2)))
                if (d < radiusOfSpread) and random.randint(0,100) < probabilityOfInfecting and people[i].removed == False and people[i].infected == False:
                    people[i].infect()
        
        # limiting the max speed
        if self.xvel > 0.5:
            self.xvel = 0.1
        if self.yvel > 0.5:
            self.yvel = 0.1

        # Randomly changing the speed
        self.yvel += random.randint(-1,1)*speed
        self.xvel += random.randint(-1,1)*speed

        # Changing the positon according to the change in time ( Euler Integration (I guess) )
        self.x += self.xvel
        self.y += self.yvel

    # this method removes a person
    def remove(self):
        self.removed = True
        self.infected = False

        # Determining the person will die or not  ( probability )
        k = random.randint(0,100)
        if  k < probabilityOfDying:
            self.dead = True
        else:
            self.dead = False
    
    # this method infects a person
    def infect(self):
        self.infected = True
        self.carryingTime = time.time()

    # this method checks if the person hits a wall,
    # if the person hits a wall then reverse their direction
    def checkBounds(self):
        if self.x <= 0 or self.x >= screenSize-cellSize:
            if self.x < screenSize//2:
                self.x = 1
            else:
                self.x = screenSize - cellSize - 1
            self.xvel *= -0.5
        if self.y <= 0 or self.y >= screenSize-cellSize:
            if self.y < screenSize//2:
                self.y = 1
            else:
                self.y = screenSize - cellSize - 1
            self.yvel *= -0.5
    
    # this method draws the person onto the screen
    def drawCell(self,win):
        colour = (255,255,255)
        if self.removed:
            if self.dead:
                colour = (50,50,50)
            else:
                colour = (0,0,200)
        elif self.infected:
            colour = (200,0,0)
        pygame.draw.circle(win, colour, (self.x, self.y), cellSize)

# driver code
def main():
    global people

    # add multiple "person" objects in the "people" array
    for i in range(populationSize): 
        people.append(person())

    # infect a single person randomly
    people[random.randint(0,49)].infect()

    # create a window to display the simulation
    win = pygame.display.set_mode((screenSize,screenSize))

    # set the name of the window to "Covid Simulation"
    pygame.display.set_caption("Covid Simulation")
    
    # the main loop:
    loop = True
    while loop:
        #draw the black background 
        pygame.draw.rect(win,(0,0,0),pygame.Rect(0,0,screenSize,screenSize))

        #change the position, draw the people
        for pers in people:
            pers.move()
            pers.drawCell(win)
            pers.checkBounds()
        
        # check if "X" is pressed if yes then Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                quit()
        
        # update the display
        pygame.display.flip()

# run the simulation
main()
