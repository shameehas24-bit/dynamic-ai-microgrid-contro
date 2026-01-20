import time
import os
from core.simulation import MicrogridEnv
from core.coordinator import GlobalCoordinator
from agents.microgrid_agents import StorageAgent
from utils.visualization import generate_visuals

def run():
    env, coord, agent = MicrogridEnv(), GlobalCoordinator(), StorageAgent()
    history = {'hr': [], 'solar': [], 'load': [], 'soc': []}
    
    for hr in range(24):
        # 1. Clear terminal to create the "Live Dashboard" effect
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # 2. Simulated Inputs
        solar = 80 if 10 <= hr <= 16 else 10
        load = 50 + (25 if 18 <= hr <= 21 else 0)
        price = 0.55 if 17 <= hr <= 22 else 0.15
        
        # 3. AI Decisions
        signal = coord.compute_reward(price, solar)
        action = agent.decide_action(signal)
        soc = env.step(solar, load, action)
        
        # 4. Display the LIVE MONITOR
        print("="*50)
        print(f"🚀 AI MICROGRID REAL-TIME MONITOR | HOUR: {hr:02d}:00")
        print("="*50)
        print(f"{'METRIC':<20} | {'VALUE':<15}")
        print("-" * 40)
        print(f"{'Solar Generation':<20} | {solar:>10} kW")
        print(f"{'System Load':<20} | {load:>10} kW")
        print(f"{'Grid Price':<20} | ${price:>9.2f}")
        print("-" * 40)
        
        status = "🟢 CHARGING" if action > 0 else "🔴 DISCHARGING" if action < 0 else "⚪ IDLE"
        print(f"{'AI CONTROL MODE':<20} | {status}")
        print(f"{'BATTERY SOC':<20} | {soc:>9.1f} %")
        print("-" * 40)
        
        # Show a small "History" table below
        print("\n[RECENT ACTIVITY LOG]")
        for k in range(max(0, hr-4), hr+1):
            print(f"H{k:02d} -> SOC: {history['soc'][k] if k < len(history['soc']) else soc:.1f}%")

        # 5. Record data
        for k, v in zip(history.keys(), [hr, solar, load, soc]): history[k].append(v)
        
        # Refresh speed (0.5s makes it look like a live feed)
        time.sleep(0.5)

    print("\n✅ Simulation Complete. Generating final performance charts...")
    generate_visuals(history)

if __name__ == "__main__":
    run()