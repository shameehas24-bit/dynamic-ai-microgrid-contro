class StorageAgent:
    def decide_action(self, reward_signal):
        if reward_signal > 0.6: return 1  # Buy power when cheap/abundant
        if reward_signal < -0.6: return -1 # Sell power when expensive/scarce
        return 0
