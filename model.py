import mesa
import random

class PharmaAgent(mesa.Agent):
    def __init__(self, unique_id, model, agent_type, capacity, yield_rate):
        super().__init__(unique_id, model)
        self.agent_type = agent_type
        self.inventory = 0
        self.capacity = capacity
        self.yield_rate = yield_rate
        self.orders_fulfilled = 0

    def step(self):
        # 1. Production Logic: Process inventory into output
        if self.inventory > 0:
            produced = min(self.inventory, self.capacity) * self.yield_rate
            self.inventory -= min(self.inventory, self.capacity)
            
            # 2. Logistics: Find the next agent in the supply chain
            next_agents = [a for a in self.model.schedule.agents if a.unique_id == self.unique_id + 1]
            if next_agents:
                next_agents[0].inventory += produced
                self.orders_fulfilled += produced

class PharmaModel(mesa.Model):
    def __init__(self, n_agents, init_stock, capacity):
        self.schedule = mesa.time.RandomActivation(self)
        types = ["Starting Material", "API", "Spray Drying", "Tabletting", "Packaging", "Hospital"]
        
        for i in range(len(types)):
            a = PharmaAgent(i, self, types[i], capacity, random.uniform(0.9, 0.99))
            if i == 0: a.inventory = init_stock # Start the chain
            self.schedule.add(a)

    def step(self):
        self.schedule.step()
