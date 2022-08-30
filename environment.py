import numpy as np
from car import Car

class Environment:
    def __init__(self) -> None:
        self.agent, self.bounaries = None
        self.reset()
    
    def step(self, step):
        self.update(step)
        return (self.next_state, self.reward)
    
    def reset(self):
        self.car = Car(0, 0, 0, [])
        self.bounaries = []
    
    def step_specs(self):
        pass
    
    def render(self):
        return self.win
    
    def update(self, step):
        self.car.update(step)
        