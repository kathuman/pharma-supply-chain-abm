from mesa import Model, Agent
import random

class PharmaAgent(mesa.Agent):
    def __init__(self, model, agent_type, capacity, yield_rate):
        # In newer Mesa, unique_id is often handled automatically, 
        # but we'll pass it to be safe.
        super().__init__(model)
        self.agent_type = agent_type
        self.inventory = 0
        self.capacity = capacity
        self.yield_rate = yield_rate

    def step(self):
        if self.inventory > 0:
            # Production logic
            produced = min(self.inventory, self.capacity) * self.yield_rate
            self.inventory -= min(self.inventory, self.capacity)
            
            # Logistics: Pass to the next agent in the list
            current_index = self.model.agents_list.index(self)
            if current_index + 1 < len(self.model.agents_list):
                next_agent = self.model.agents_list[current_index + 1]
                next_agent.inventory += produced

class PharmaModel(mesa.Model):
    def __init__(self, init_stock, capacity):
        super().__init__()
        self.schedule = mesa.time.BaseScheduler(self)
        self.agents_list = []
        
        types = ["Starting Material", "API", "Spray Drying", "Tabletting", "Packaging", "Hospital"]
        
        for i, t in enumerate(types):
            a = PharmaAgent(self, t, capacity, random.uniform(0.9, 0.99))
            if i == 0: 
                a.inventory = init_stock
            self.schedule.add(a)
            self.agents_list.append(a)

    def step(self):
        self.schedule.step()
