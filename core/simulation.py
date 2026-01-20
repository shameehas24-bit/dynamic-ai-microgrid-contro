import numpy as np

class MicrogridEnv:
    def __init__(self):
        self.battery_soc = 50.0  # Percentage
        self.capacity_kwh = 100.0
        
    def step(self, solar, load, action):
        # Action: 1 (Charge), -1 (Discharge)
        power_flow = action * 10.0
        new_soc = self.battery_soc + (power_flow / self.capacity_kwh) * 100
        self.battery_soc = np.clip(new_soc, 10, 90) # Operational safety limits
        return self.battery_soc
