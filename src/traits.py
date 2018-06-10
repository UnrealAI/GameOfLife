import numpy as np
import pygame

class Organism(pygame.sprite.Sprite):
    def __init__(self, size=100, attack=100, speed=10, defense=100, total_calories=1000, energy_consumption=200, health = 5000, pos=np.array([0,0]), attackMoves={}, speedMod={"land":100, "water":100}, env=None):
        pygame.sprite.Sprite.__init__(self)
        self.species_name = 'species0'
        self.size = size
        self.attack = attack
        self.speed = speed
        self.defense = defense
        self.total_calories = total_calories
        self.energy_consumption = energy_consumption
        self.attribute_array = np.array([self.size,self.attack,self.speed,self.defense,self.total_calories,self.energy_consumption])
        self.color = np.minimum(np.array([np.dot(self.attribute_array,[0,1,0,0,0,0]),np.dot(self.attribute_array,[0,0,1,0,0,0]),np.dot(self.attribute_array,[0,0,0,1,0,0])]),[255,255,255])
        self.pos = pos
        self.health = 5000
        self.attackMoves = attackMoves
        self.env = env
        self.radius = self.size
        self.dead = False
        self.mated = False
        self.speedMod = speedMod

    @property
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.radius*2, self.radius*2)

    def return_color(self):
        return self.color

    def move(self, theta):
        if theta != None:
            self.pos += (np.array([np.cos(theta),np.sin(theta)])*self.speed).astype(int)
            # clip it right where
            self.pos = (self.pos[0].clip(0,self.env.WINDOWSIZE[0]), self.pos[1].clip(0,self.env.WINDOWSIZE[1]))

    def update_species_name(self, species_name):
        self.species_name = species_name

    def mate(self, organism2):
        # will make twins for now
        if np.random.rand() < 0.01:
            self.mated = True

    def interaction(self, organism2):
        self.mated = False
        if self.species_name != organism2.species_name:
            self.is_attacked(organism2)
        else:
            self.mate(organism2)

    def is_attacked(self, organism2):
        self.health += np.minimum(0,self.defense-organism2.attack)

    def is_dead(self):
        if self.health <= 0.:
            self.dead = True

    def defend(self):
        pass

    # def render(self):
    #     pygame.draw.circle(SCREEN, agent.color, agent.pos, agent.size)


class Controller:

    def __init__(organism1, organism2):
        self.organism1 = organism1
        self.organism2 = organism2

    def interaction(self):
        if self.organism1:
            pass
        #similarity = np.dot(self.organism1.color,self.organism2.color)/(np.linalg.norm(self.organism1.color)*np.linalg.norm(self.organism2.color))

    # mate, retain same species name, mutate crossover


# calories used: 2*size + 100*feet/second


class Terrain(pygame.sprite.Sprite):
    white = (255, 255, 255)
    block_width = 100
    block_height = 100

    def __init__(self,type,x,y):
        super().__init__()
        self.image = pygame.Surface([self.block_width, self.block_height])
        self.type = type
        self.color = self.getColor(self.type)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def properties(type):
        movementMod = {
            "land": None,
            "water": None
        }
        if(type == "land"):
            movementMod["land"] = 1.0
            movementMod["water"] = 0.0
        elif(type == "water"):
            movementMod["land"] = 0.0
            movementMod["water"] = 1.0
        return {
            "color":self.color,
            "movementMod": movementMod
        }

    def getColor(self,type):
        color = None
        if(type == "land"):
            color = (50,200,50)
        elif(type == "water"):
            color = (50,50,200)
        return color
# planned interaction:
# based off where they are positioned, they will be affected by terrain.
# how to lay terrain?

    # general plan of terrain
    # water
    # land
    # muddy land
    # grassland
