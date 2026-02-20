import mesa
import random

class PharmaAgent(mesa.Agent):
    """An agent representing a single stage in the pharma supply chain."""
    def __init__(self, model, agent_type, capacity, yield_rate):
        # unique_id is now automatically handled by Mesa 3.0+
        super().__init__(model)
        self.agent_type = agent_type
        self.inventory = 0
        self.capacity = capacity
        self.yield_rate = yield_rate

    def step(self):
        # 1. Production Logic: Process raw material into intermediate/final product
        if self.inventory > 0:
            # We process what we have, up to our daily capacity
            amount_to_process = min(self.inventory, self.capacity)
            produced = amount_to_process * self.yield_rate
            self.inventory -= amount_to_process
            
            # 2. Logistics: Find our place in the chain and push to the next agent
            # We convert the model.agents collection to a list to find the next neighbor
            all_agents = list(self.model.agents)
            current_idx = all_agents.index(self)
            
            if current_idx + 1 < len(all_agents):
                next_agent = all_agents[current_idx + 1]
                next_agent.inventory += produced

class PharmaModel(mesa.Model):
    """The model representing the end-to-end supply chain."""
    def __init__(self, init_stock, capacity):
        super().__init__()
        
        # Defining the sequence of the supply chain
        stages = [
            "Starting Material CMO", 
            "API CMO", 
            "Spray Drying CMO", 
            "Tabletting CMO", 
            "Packaging CMO", 
            "Hospital/Pharmacy"
        ]
        
        # Create agents in the order of the supply chain
        for i, stage_name in enumerate(stages):
            # Assign a slight variation in yield for realism
            yield_val = random.uniform(0.94, 0.99)
            a = PharmaAgent(self, stage_name, capacity, yield_val)
            
            # Seed the very first agent with the initial starting material
            if i == 0:
                a.inventory = init_stock

    def step(self):
        # In Mesa 3.0, this replaces self.schedule.step()
        self.agents.step()
