import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def create_animation(history):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    def update(frame):
        ax1.clear()
        ax2.clear()
        
        # Data up to the current frame
        h = {k: v[:frame] for k, v in history.items()}
        
        # Plot Layer 1 & 3: Energy Environment
        ax1.plot(h['hr'], h['solar'], label='Solar (kW)', color='gold')
        ax1.plot(h['hr'], h['load'], label='Load (kW)', color='blue')
        ax1.set_title("Layer 1: Real-Time Microgrid Environment")
        ax1.legend(loc='upper left')
        
        # Plot Layer 2 & 4: AI Agent Response
        ax2.fill_between(h['hr'], h['soc'], color='green', alpha=0.3)
        ax2.plot(h['hr'], h['soc'], label='Battery SOC (%)', color='green')
        ax2.set_ylim(0, 100)
        ax2.set_title("Layer 2: AI Agent Adaptive Control")
        ax2.legend(loc='upper left')

    # Create the animation
    ani = FuncAnimation(fig, update, frames=len(history['hr']), repeat=False)
    
    # Save as a GIF (This is the "Website" effect)
    print("Generating live animation...")
    ani.save('live_dashboard.gif', writer='pillow', fps=5)
    plt.close()
