import matplotlib.pyplot as plt
import numpy as np

def plot_metrics(cutoff, precision, recall, f1_score):
    # Data
    metrics = ['Precision', 'Recall', 'F1 Score']
    values = [precision, recall, f1_score]

    # Create figure and axis
    fig, ax = plt.subplots()

    # Create a horizontal bar plot
    y_pos = np.arange(len(metrics))
    ax.barh(y_pos, values, align='center', color=['blue', 'orange', 'green'])

    # Annotate bars with values
    for i, v in enumerate(values):
        ax.text(v, i, f'{v:.2f}', color='black', va='center')

    # Set the labels and title
    ax.set_yticks(y_pos)
    ax.set_yticklabels(metrics)
    ax.set_xlabel('Score')
    ax.set_title(f'Metrics at Match Score Cutoff: {cutoff*100}%')

    # Extend x-axis limit to accommodate text annotation
    ax.set_xlim([0, max(values) + 0.1])

    # Invert y-axis
    ax.invert_yaxis()

    # Show the plot
    plt.show()

# Call the function
plot_metrics(0.75, 0.75, 0.46153846153846156, 0.5714285714285714)
