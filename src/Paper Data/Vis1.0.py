import matplotlib.pyplot as plt

# Your data
results = {10: {'precision': 60.0, 'recall': 37.5, 'f1_score': 0.4615384615384615},
           20: {'precision': 30.0, 'recall': 37.5, 'f1_score': 0.33333333333333326},
           30: {'precision': 26.666666666666668, 'recall': 50.0, 'f1_score': 0.3478260869565218},
           50: {'precision': 16.0, 'recall': 50.0, 'f1_score': 0.24242424242424243},
           100: {'precision': 12.0, 'recall': 75.0, 'f1_score': 0.20689655172413793},
           150: {'precision': 8.666666666666668, 'recall': 81.25, 'f1_score': 0.1566265060240964}}

res = {10: {'precision': 60.0, 'recall': 37.5, 'f1_score': 0.4615384615384615},
       20: {'precision': 30.0, 'recall': 37.5, 'f1_score': 0.33333333333333326},
       30: {'precision': 26.666666666666668, 'recall': 50.0, 'f1_score': 0.3478260869565218},
       50: {'precision': 16.0, 'recall': 50.0, 'f1_score': 0.24242424242424243},
       100: {'precision': 12.0, 'recall': 75.0, 'f1_score': 0.20689655172413793},
       150: {'precision': 8.666666666666668, 'recall': 81.25, 'f1_score': 0.1566265060240964}}

# Split the dictionary into lists
thresholds = list(res.keys())
precision = [val['precision'] for val in res.values()]
recall = [val['recall'] for val in res.values()]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot precision and recall
ax.plot(thresholds, precision, marker='o', label='Precision')
ax.plot(thresholds, recall, marker='o', label='Recall')

ax.set_xlabel('Threshold (Top-N)')
ax.set_ylabel('Percentage')
ax.legend(loc='upper right')

plt.grid(True)
plt.title('Precision and Recall at Different Thresholds')
plt.show()
