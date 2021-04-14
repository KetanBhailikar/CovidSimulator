# Author      : Ketan Bhailikar
# Requrements : 1) Python3.x
#               2) pygame [https://pypi.org/project/pygame/]

import pygame
import matplotlib.pyplot as plt
import random
import math
import time
pygame.init()
startT = time.time()
# Colour Code :-
# Alive and Uninfected : White
# Alive and Infected   : Red
# Alive and Immune     : Blue   ( People who have been infected before )
# Dead                 : Grey


# Variable that you can alter:
screenSize = 800                # Screen Size
cellSize = 5                    # Size of individual Person

populationSize = 400            # Number of People
speed = 0.09			 # Increase/Decrease in Speed of individual person (Recomended speed = 0.001 - 0.009)
infectedTime = 5                # Amount of time for which a person can remain infected
probImmunity = 50		 # Probability if a person getting immune to the virus after being infected ( If the person does not die )
probabilityOfDying = 50         # Probability that an infected person will die
radiusOfSpread = 20		 # The maximum distance that a person has to remain from a infected person to not get infecte
probabilityOfInfecting = 30     # Probability of a person gettinTrueg infected if he comes in contact with a infected person
lockDown = False		 # Is there lockdown?
selfIsolation = False		 # Are the infected people isolated?s
infectionRecognitionTime = 3	 # Time required to isolate infected people  ( Works only if self-isolation is True )
showGraph = True		 # Should the graph be shown at the end?


people = []                     # this array holds the list of people


class person():
    def __init__(self):
        self.infected = False
        self.removed = False
        if selfIsolation:
            while True:
                self.x = random.randint(0, screenSize)
                self.y = random.randint(0, screenSize)
                if (self.x < (screenSize//4) and self.y > (screenSize - (screenSize//4))) == False:
                    break
        else:
            self.x = random.randint(0, screenSize)
            self.y = random.randint(0, screenSize)
        self.xvel = 0
        self.yvel = 0
        self.carryingTime = 0
        self.dead = False
        self.infectionStartTime = 0
        self.isolated = False

        # If there is Lockdown then only 4% of the people will move around
        if lockDown:
            if random.randint(0, 100) < 4:
                self.moveable = True
            else:
                self.moveable = False
        else:
            self.moveable = True

    def move(self):
        # removing the person
        if time.time() - self.carryingTime > infectedTime and self.carryingTime != 0 and self.removed == False:
            self.remove()

        # infect people around the infected person
        if self.infected:
            if selfIsolation and self.isolated == False:
                if self.infectionStartTime != 0:
                    if time.time() - self.infectionStartTime > infectionRecognitionTime:
                        self.isolate()
                else:
                    self.infectionStartTime = time.time()
            for i in range(len(people)):
                d = math.sqrt(
                    (math.pow(self.x - people[i].x, 2)) + (math.pow(self.y - people[i].y, 2)))
                if (d < radiusOfSpread) and random.randint(0, 100) < probabilityOfInfecting and people[i].removed == False and people[i].infected == False:
                    people[i].infect()

        if self.moveable:
            # Randomly changing the speed
            self.yvel += random.randint(-1, 1)*speed
            self.xvel += random.randint(-1, 1)*speed
        else:
            self.xvel = 0
            self.yvel = 0

        # Changing the positon according to the change in time ( Euler Integration (I guess) )
        self.x += self.xvel
        self.y += self.yvel

    # this method removes a person
    def remove(self):
        self.removed = True
        self.infected = False

        # Determining the person will die or not  ( probability )
        k = random.randint(0, 100)
        if k < probabilityOfDying:
            self.dead = True
        else:
            self.dead = False
            if random.randint(0, 100) > probImmunity:
                self.removed = False

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

        # Check collisions with the isolation chamber ( If it is enabled )
        if selfIsolation:
            if self.isolated == False and self.x < (screenSize//4) and self.y > (screenSize - (screenSize//4)):
                self.xvel *= -1
                self.yvel *= -1

    # this method draws the person onto the screen
    def drawCell(self, win):
        colour = (255, 255, 255)
        if self.removed:
            if self.dead:
                colour = (50, 50, 50)
            else:
                colour = (0, 0, 200)
        elif self.infected:
            colour = (200, 0, 0)
        pygame.draw.circle(win, colour, (self.x, self.y), cellSize)

        if selfIsolation:
            pygame.draw.rect(win, (255, 255, 255), pygame.Rect(
                0, screenSize-(screenSize//4), (screenSize//4), (screenSize//4)), 3)

    def isolate(self):
        self.isolated = True
        self.moveable = False
        self.x = random.randint(0, (screenSize//4)-radiusOfSpread)
        self.y = random.randint(
            screenSize-(screenSize//4)+radiusOfSpread, screenSize)

# driver code


def main():
    global people
    finfected = open("infected.txt", "w")
    fimmune = open("immune.txt", "w")
    fdead = open("dead.txt", "w")

    # add multiple "person" objects in the "people" array
    for i in range(populationSize):
        people.append(person())

    # infect a single person randomly
    people[random.randint(0, 49)].infect()

    # create a window to display the simulation
    win = pygame.display.set_mode((screenSize, screenSize))

    # set the name of the window to "Covid Simulation"
    pygame.display.set_caption("Covid Simulation")

    # the main loop:
    loop = True
    while loop:
        infectedc = 0
        immunec = 0
        deadc = 0
        # draw the black background
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(
            0, 0, screenSize, screenSize))

        # change the position, draw the people
        for pers in people:
            if pers.infected:
                infectedc += 1
            if pers.removed and pers.dead == False:
                immunec += 1
            if pers.dead:
                deadc += 1
            pers.move()
            pers.drawCell(win)
            pers.checkBounds()
        if showGraph:
            finfected.write(str(time.time()-startT)+","+str(infectedc)+"\n")
            fimmune.write(str(time.time()-startT)+","+str(immunec)+"\n")
            fdead.write(str(time.time()-startT)+","+str(deadc)+"\n")
            if infectedc == 0:
                loop = False
        # check if "X" is pressed if yes then Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                quit()

        # update the display
        pygame.display.flip()

    # Display the Graph after the virus is extinct
    if showGraph:
        xs1 = []
        ys1 = []
        xs2 = []
        ys2 = []
        xs3 = []
        ys3 = []

        graph_data1 = open('infected.txt', 'r').read()
        lines1 = graph_data1.split('\n')

        graph_data2 = open('immune.txt', 'r').read()
        lines2 = graph_data2.split('\n')

        graph_data3 = open('dead.txt', 'r').read()
        lines3 = graph_data3.split('\n')

        for line1 in lines1:
            if len(line1) > 1:
                x, y = line1.split(',')
                xs1.append(float(x))
                ys1.append(float(y))

        for line2 in lines2:
            if len(line2) > 1:
                x, y = line2.split(',')
                xs2.append(float(x))
                ys2.append(float(y))

        for line3 in lines3:
            if len(line3) > 1:
                x, y = line3.split(',')
                xs3.append(float(x))
                ys3.append(float(y))

        plt.plot(xs1, ys1)
        plt.plot(xs2, ys2)
        plt.plot(xs3, ys3)
        plt.xlabel("Time")
        plt.ylabel("Number of People")
        plt.legend(["Infected", "Immune", "Dead"])

        plt.ylim(0, 400)
        plt.xlim(0, 35)
        plt.show()


# run the simulation
main()
