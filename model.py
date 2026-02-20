import mesa
import random

class PharmaAgent(mesa.Agent):
    def __init__(self, model, agent_type, capacity, yield_rate):
        super().__init__(model)
        self.agent_type = agent_type
        self.inventory = 0
        self.capacity = capacity
        self.yield_rate = yield_rate

    def step(self):
        # 1. Production Logic
        if self.inventory > 0:
            amount_to_process = min(self.inventory, self.capacity)
            produced = amount_to_process * self.yield_rate
            self.inventory -= amount_to_process
            
            # 2. Logistics Logic (Push to next stage)
            # Get agents in the order they were added
            all_agents = list(self.model.agents)
            current_idx = all_agents.index(self)
            
            if current_idx + 1 < len(all_agents):
                next_agent = all_agents[current_idx + 1]
                next_agent.inventory += produced

class PharmaModel(mesa.Model):
    def __init__(self, init_stock, capacity):
        super().__init__()
        
        stages = [
            "Starting Material CMO", 
            "API CMO", 
            "Spray Drying CMO", 
            "Tabletting CMO", 
            "Packaging CMO", 
            "Hospital/Pharmacy"
        ]
        
        for i, stage_name in enumerate(stages):
            # Create agent
            a = PharmaAgent(self, stage_name, capacity, random.uniform(0.95, 0.99))
            # Seed the first stage
            if i == 0:
                a.inventory = init_stock

    def step(self):
        """
        FIX: Instead of calling self.agents.step(), 
        we manually tell each agent to step.
        """
        for agent in self.agents:
            agent.step()
