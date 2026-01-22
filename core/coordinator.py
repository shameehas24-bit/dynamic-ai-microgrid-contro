class GlobalCoordinator:
    def compute_reward(self, price, solar, load):
        # Logic: If price is high, reward discharging. If solar is high, reward charging.
        if solar > 50:
            return 1.0  # High Reward for Storage
        if price > 0.40:
            return -1.0 # High Reward for Discharge
        return 0.1