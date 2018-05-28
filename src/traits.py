import numpy as np
class Organism:

    size = 100
    attack = 100 #{'bite':100,'lunge':55}#{attack_type:damage, ...}
    speed= 100   #{'land':100,'water':}#{speed_type:value}
    defense=100
    color = np.array([128.,128.,128.])
    total_calories=1000
    energy_consumption = 200
    pos = np.array([0,0])

    def __init__(self, size=100, attack=100, speed=100, defense=100, total_calories=1000, energy_consumption=200, pos=np.array([0,0])):
        self.size = size
        self.attack = attack
        self.speed = speed
        self.defense = defense
        self.total_calories = total_calories
        self.energy_consumption = energy_consumption
        self.attribute_array = np.array([self.size,self.attack,self.speed,self.defense,self.total_calories,self.energy_consumption])
        self.color = np.minimum(np.array([np.dot(self.attribute_array,[0,1,0,0,0,0]),np.dot(self.attribute_array,[0,0,1,0,0,0]),np.dot(self.attribute_array,[0,0,0,1,0,0])]),[255,255,255])
        self.pos = pos

    def return_color(self):
        return self.color

    def move(self, theta):
        self.pos += np.array([np.cos(theta),np.sin(theta)])*self.speed


# calories used: 2*size + 100*feet/second
