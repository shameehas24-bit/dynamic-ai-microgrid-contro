from core.simulation import MicrogridEnv
from core.coordinator import GlobalCoordinator
from agents.microgrid_agents import StorageAgent
from utils.visualization import generate_visuals

def run():
    env, coord, agent = MicrogridEnv(), GlobalCoordinator(), StorageAgent()
    history = {'hr': [], 'solar': [], 'load': [], 'soc': []}

    for hr in range(24):
        solar = 70 if 10 <= hr <= 16 else 10
        load = 40 + (25 if 18 <= hr <= 21 else 0)
        price = 0.50 if 17 <= hr <= 22 else 0.15
        
        signal = coord.compute_reward(price, solar)
        action = agent.decide_action(signal)
        soc = env.step(solar, load, action)
        
        for k, v in zip(history.keys(), [hr, solar, load, soc]): history[k].append(v)
        print(f"Hour {hr:02d} | SOC: {soc:.1f}%")

    generate_visuals(history)

if __name__ == "__main__":
    run()
