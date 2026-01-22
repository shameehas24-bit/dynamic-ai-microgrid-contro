import numpy as np

class MicrogridEnv:
    def __init__(self):
        self.battery_soc = 50.0  # Percentage
        self.capacity_kwh = 100.0
        
    def step(self, solar, load, action):
        # Action: 1 (Charge), -1 (Discharge)
        power_flow = action * 10.0 # 10kW converter
        
        # Calculate new SOC
        new_soc = self.battery_soc + (power_flow / self.capacity_kwh) * 100
        self.battery_soc = np.clip(new_soc, 10, 90) 
        
        # Calculate Grid Impact (Energy balance)
        # Positive means exporting to grid, negative means importing
        grid_impact = solar - load - power_flow
        
        # KEY FIX: Return BOTH values separated by a comma
        return self.battery_soc, grid_impact