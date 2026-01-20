class GlobalCoordinator:
    def compute_reward(self, price, solar):
        if solar > 60: return 1.0   # High renewable availability
        if price > 0.45: return -1.0 # High grid stress/price
        return 0.1
