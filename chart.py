# pie_chart.py

import pandas as pd
import matplotlib.pyplot as plt

def create_dual_pie_charts(a, b):
    # Create two sample DataFrames
    data1 = {'Enemy Type': ['RED', 'BLUE', 'SPIKE'],
            'KNOCK-DOWN': a}
    df1 = pd.DataFrame(data1)

    data2 = {'Outcome': ['ON TARGET', 'MISS'],
             'Quantity': [b[1], b[0] - b[1]]}
    df2 = pd.DataFrame(data2)

    # Create a subplot with 1 row and 2 columns
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # Plot the first pie chart
    df1.set_index('Enemy Type').plot.pie(y='KNOCK-DOWN', autopct='%1.1f%%', startangle=140, legend=False, ax=axes[0])
    axes[0].set_ylabel('') 
    axes[0].set_title('Knock-down rate of each enemy type')

    # Plot the second pie chart
    df2.set_index('Outcome').plot.pie(y='Quantity', autopct='%1.1f%%', startangle=140, legend=False, ax=axes[1])
    axes[1].set_ylabel('')  
    axes[1].set_title('Hit rate of the player')

    plt.axis('equal')  
    plt.tight_layout() 
    plt.show()

