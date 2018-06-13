import numpy as np
import pygame

class Organism(pygame.sprite.Sprite):
    def __init__(self, size=100, attack=100, speed=10, defense=100, total_calories=1000, energy_consumption=200, max_health = 5000, lifespan = 50, pos=np.array([0,0]), attackMoves={}, speedMod={"land":100, "water":100}, env=None):
        pygame.sprite.Sprite.__init__(self)
        self.species_name = 'species0'
        self.size = size
        self.attack = attack
        self.speed = speed
        self.defense = defense
        self.total_calories = total_calories
        self.calories = total_calories
        self.energy_consumption = energy_consumption
        self.pos = pos
        self.max_health = max_health
        self.health = max_health
        self.attackMoves = attackMoves
        self.env = env
        self.lifespan = lifespan
        self.age = 0
        self.dna = np.array([self.size,self.attack,self.speed,self.defense,self.total_calories,self.energy_consumption, self.max_health, self.lifespan])
        self.color = np.minimum(np.array([np.dot(self.dna,[0,1,0,0,0,0,0,0]),np.dot(self.dna,[0,0,1,0,0,0,0,0]),np.dot(self.dna,[0,0,0,1,0,0,0,0])]),[255,255,255])
        self.radius = self.size
        self.dead = False
        self.mated = False
        self.speedMod = speedMod


    @property
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.radius*2, self.radius*2)

    def return_color(self):
        return self.color

    def reduction_factor(self):
        # do something with self.pos self.pos
        return 1.

    def move(self, theta):
        if theta != None:
            self.pos += (np.array([np.cos(theta),np.sin(theta)])*self.speed*self.reduction_factor()).astype(int)
            # clip it right where
            self.pos = (self.pos[0].clip(0,self.env.WINDOWSIZE[0]), self.pos[1].clip(0,self.env.WINDOWSIZE[1]))

    def update_species_name(self, species_name):
        self.species_name = species_name

    def mate(self, organism2):
        # will make twins for now
        if np.random.rand() < 0.005 and self.calories >= self.total_calories*.6:
            self.mated = True
            self.calories /= 2

    def crossover(self, new_dna, organism2, crossover_rate):
        crossed_elements = (np.random.rand(len(self.dna)) <= crossover_rate)
        new_dna[crossed_elements] = organism2.dna[crossed_elements]
        return new_dna

    def mutate(self, new_dna, mutation_rate):
        mutated_elements = (np.random.rand(len(self.dna)) <= mutation_rate)
        #print(new_dna)
        if sum(mutated_elements) > 0:
            new_dna[mutated_elements] = np.maximum(np.vectorize(lambda x: np.random.normal(scale=x/10.) + x)(new_dna[mutated_elements]),np.zeros(sum(mutated_elements)))
        return new_dna

    def produce_child_dna(self, organism2, crossover_rate, mutation_rate):
        new_dna = self.mutate(self.crossover(self.dna.copy(),organism2, crossover_rate),mutation_rate)
        return new_dna

    def interaction(self, organism2):
        self.lose_calories()
        self.mated = False
        if self.species_name != organism2.species_name:
            self.is_attacked(organism2)
        if self.species_name == organism2.species_name:
            if np.random.rand() < 0.3:
                self.is_attacked(organism2)
            self.mate(organism2)

    def is_attacked(self, organism2):
        self.health += np.minimum(0,self.defense-organism2.attack)
        self.health = np.minimum(self.max_health,self.health)

    def lose_calories(self):
        self.calories -= 5

    def gain_calories(self):
        self.calories += 10

    def hungry(self):
        if self.calories <= self.total_calories/4:
            self.health -= self.max_health/15.

    def cap_calories(self):
        self.calories = np.clip(self.calories,0.,self.total_calories)

    def is_dead(self):
        if self.health <= 0.:
            self.dead = True

    def add_year(self):
        self.age += 1
        if self.age > self.lifespan:
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

class Terrain():
    blocks = []
    def __init__(self, terrainGroup, env, pattern=[]):
        self.terrainGroup = terrainGroup

        if(pattern == []):
            self.create_background(self.terrainGroup,env)

        # by default make a half divided block.
    # def player_collide(self, agent):
    #     for x in self.terrainGroup:
    #         x.rect.center.collidepoint(agent.rect.centerx,agent.rect.centery)

    def create_background(self,group,env):
        # Five rows of blocks
        rows = 8
        cols = 8
        block_width = env.WINDOWSIZE[0] / rows
        block_height = env.WINDOWSIZE[1] / cols
        top = 100
        for row in range(rows):
            # 32 columns of blocks
            for column in range(int(cols/2)):
                # Create a block (color,x,y)
                block = Block("land", column * (block_width), row * block_height)
                self.terrainGroup.add(block)
            for column in range(int(cols/2),cols):
                # Create a block (color,x,y)
                block = Block("water", column * (block_width), row * block_height)
                self.terrainGroup.add(block)
            # Move the top of the next row down
            top += block_height


class Block(pygame.sprite.Sprite):
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

    def movementMod(type):
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
        return movementMod

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
