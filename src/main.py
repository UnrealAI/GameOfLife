import pygame, sys, numpy as np
import traits
from time import sleep
from sklearn.neighbors import NearestNeighbors
import networkx as nx
import scipy
import copy
from collections import Counter
import scipy
from sklearn.decomposition import KernelPCA
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline


from pygame.locals import *

white = [255, 255, 255]

class Environment:
    def __init__(self, WINDOWSIZE=None):
        self.WINDOWSIZE = WINDOWSIZE

pygame.init()

env = Environment(WINDOWSIZE=(800,800))
SCREEN = pygame.display.set_mode(env.WINDOWSIZE)

pygame.display.set_caption('Game of Life')
SCREEN.fill(white)

agents = {}
n_born = 0
mutation_rate = 0.9
crossover_rate = 0.2

clan_view = 1

agents = pygame.sprite.Group()
terrain = pygame.sprite.Group()

def generate_agents():
    global agents
    for i in range(50):
        agents.add(traits.Organism(size=np.random.randint(20,50),attack=np.random.randint(400),speed=np.random.randint(50),defense=np.random.randint(200),pos=(np.random.randint(800),np.random.randint(800)),max_health=np.random.randint(2000,5000),lifespan=np.random.randint(30,50),env=env))

def visualizeAgent(agent):
    pygame.draw.circle(SCREEN, agent.color, agent.pos, agent.size)

def visualizeAgents():
    for agent in agents:
        visualizeAgent(agent)

def assign_species_names():
    global agents, n_born, color_changer

    X = [agent.dna for agent in agents]
    """for agent in agents:
        print(agent)
    print(X)"""
    nn = NearestNeighbors(metric='cosine',algorithm='brute')
    nn.fit(X)
    nbrs_graph = nn.radius_neighbors_graph(X,radius=0.001)
    _, connected_components = scipy.sparse.csgraph.connected_components(nbrs_graph)
    #print('HI')
    #print(connected_components)
    for agent,cluster in zip(agents,connected_components):
        agent.update_species_name('species%d'%cluster)
    if n_born == 0:
        color_changer = Pipeline([('pca',KernelPCA(n_components=3,kernel="cosine")),('minmax',MinMaxScaler())])
        color_changer.fit(X)

    colors = (MinMaxScaler().fit_transform(color_changer.transform(X)*255.)*255.).astype(int)#(MinMaxScaler().fit_transform(KernelPCA(n_components=3,kernel="cosine").fit_transform(X))*255).astype(int).tolist()
    #print(colors)
    for agent,color in zip(agents,colors):
        print(color)
        agent.color = color



def movement(agent):
    key = pygame.key.get_pressed()
    theta = np.random.rand()*2.*np.pi
    if 0:
        theta = None
        if key[pygame.K_LEFT]:
            theta = -np.pi
        if key[pygame.K_RIGHT]:
            theta = 0
        if key[pygame.K_UP]:
            theta = -np.pi/2.
        if key[pygame.K_DOWN]:
            theta = np.pi/2
    agent.move(theta)
    return agent

def create_background():
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
            block = traits.Block("land", column * (block_width), row * block_height)
            terrain.add(block)
        for column in range(int(cols/2),cols):
            # Create a block (color,x,y)
            block = traits.Block("water", column * (block_width), row * block_height)
            terrain.add(block)
        # Move the top of the next row down
        top += block_height

def collision(organism1,organism2):
    if organism1.species_name != organism2.species_name:
        pass

def traverse_collisions():
    global n_born
    agent_dead_list = []
    new_agent_list = []
    for agent in agents:
        agents_hit = pygame.sprite.spritecollide(agent,agents, False, pygame.sprite.collide_circle)
        for agent2 in agents_hit:
            agent.interaction(agent2)
            if agent.mated:
                new_agent_dna = agent.produce_child_dna(agent2,crossover_rate,mutation_rate)
                new_agent = traits.Organism(size=new_agent_dna[0], attack=new_agent_dna[1], speed=new_agent_dna[2], defense=new_agent_dna[3],total_calories=new_agent_dna[4],pos=agent.pos,max_health=new_agent_dna[5],lifespan=new_agent_dna[6],env=env)
                new_agent.species_name = agent.species_name
                new_agent.color = agent.color
                new_agent.pos += (np.random.rand(2)*new_agent.speed/4.).astype(np.int)
                new_agent_list.append(new_agent) # this is a clone for now, but should update the DNA
                agent.mated = False
        agent.is_dead()
        if agent.dead:
            agent_dead_list.append(agent)
        #if agent.mated: # mate with multiple members too, no clone
        #new_agent = traits.Organism(size=agent.size, attack=agent.attack, speed=agent.speed, defense=agent.defense,total_calories=agent.total_calories,pos=agent.pos,health=np.random.randint(2000,5000),env=env)
        #    new_agent.pos += (np.random.rand(2)*new_agent.speed/4.).astype(np.int)
        #    new_agent_list.append(new_agent) # this is a clone for now, but should update the DNA
    #print(new_agent_list)
    for agent in agent_dead_list:
        agent.kill()
        del agent

    if len(agents) <= 150:
        for agent in new_agent_list:
            n_born += 1
            agents.add(agent)


# create_background()
traits.Terrain(terrain,env)
generate_agents()

counter = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if n_born % 30 == 0 or n_born == 0:# change to 0 when ready to implement
        assign_species_names()

    sleep(0.01)
    for agent in agents:
        agent = movement(agent)

    # for agent in agents:
    #     print(agents[agent].pos)

    SCREEN.fill(white)
    terrain.draw(SCREEN)
    visualizeAgents()
    pygame.display.update()
    traverse_collisions()

    for agent in agents:
        agent.gain_calories()
        agent.hungry()
        agent.cap_calories()
        agent.is_dead()
        if agent.dead:
            agent.kill()
            del agent


    #print("counter {} pop {} born {}".format(counter,len(agents),n_born))
    if counter % 10 == 0 or counter == 0:
        species_count = Counter([agent.species_name for agent in agents])
        p_dist = np.array(list(species_count.values()))/sum(species_count.values())
        entropy = scipy.stats.entropy(p_dist)
        for agent in agents:
            agent.add_year()
            if agent.dead:
                agent.kill()
                del agent
        print("Diversity Index:%f"%(entropy))
        print("Number Born: %d"%n_born)
    counter += 1




    # calories, mutation, birth calorie loss, calories at 0 lose health
