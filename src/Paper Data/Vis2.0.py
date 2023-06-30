import matplotlib.pyplot as plt

# Lists of your data
cutoffs = [0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55]
precisions = [0.5, 0.5, 0.7142857142857143, 0.7142857142857143, 0.75, 0.6, 0.4, 0.375, 0.3157894736842105]
recalls = [0.07692307692307693, 0.07692307692307693, 0.38461538461538464, 0.38461538461538464, 0.46153846153846156, 0.46153846153846156, 0.46153846153846156, 0.46153846153846156, 0.46153846153846156]
f1_scores = [0.13333333333333336, 0.13333333333333336, 0.5, 0.5, 0.5714285714285714, 0.5217391304347826, 0.42857142857142855, 0.41379310344827586, 0.37499999999999994]

# Create figure and axis
fig, ax = plt.subplots()

# Plot the data
ax.plot(cutoffs, precisions, marker='o', label='Precision')
ax.plot(cutoffs, recalls, marker='o', label='Recall')
ax.plot(cutoffs, f1_scores, marker='o', label='F1 Score')

# Set the labels and title
ax.set_xlabel('Match Score Cutoff')
ax.set_ylabel('Score')
ax.set_title('Precision, Recall and F1 Score at Different Match Score Cutoffs')

# Show legend
ax.legend()

# Show the plot
plt.show()
