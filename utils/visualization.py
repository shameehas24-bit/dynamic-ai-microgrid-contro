import matplotlib.pyplot as plt

def generate_visuals(history):
    plt.style.use('ggplot')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    ax1.plot(history['hr'], history['solar'], label='Solar', color='gold')
    ax1.plot(history['hr'], history['load'], label='Load', color='blue')
    ax1.set_title('Microgrid Power Balance')
    ax1.legend()
    
    ax2.fill_between(history['hr'], history['soc'], color='green', alpha=0.3)
    ax2.plot(history['hr'], history['soc'], color='green', label='Battery SOC%')
    ax2.set_ylim(0, 100)
    ax2.set_title('AI-Optimized Battery State')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('visual_output.png')
    print("Visual saved as visual_output.png")
