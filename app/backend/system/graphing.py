import pandas as pd
import matplotlib.pyplot as plt

# Data
df = pd.read_csv('PID_TESTING.csv')
time = df['time']
percent = df['percent']
adjustment = df['adjustment']


# Plotting
fig, ax1 = plt.subplots()

# Plotting percent on the right y-axis
ax1.plot(time, percent, marker='o', linestyle='-', color='b', label='Percent')
ax1.set_xlabel('Time')
ax1.set_ylim(0,8)
ax1.set_ylabel('Percent', color='b')
ax1.tick_params('y', colors='b')

# Creating a twin axis for the left y-axis
ax2 = ax1.twinx()
ax2.plot(time, adjustment, marker='s', linestyle='-', color='g', label='Adjustment')
ax2.set_ylim(-0.05, 0.75)
ax2.set_ylabel('Adjustment', color='g')
ax2.tick_params('y', colors='g')

# Adding a horizontal dashed red line at y=0.5 for the percent plot
ax1.axhline(y=0.5, color='r', linestyle='--', label='Y=0.5')

# Adding a legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

# Adding title
plt.title('Percent and Adjustment vs Time')

# Display the plot
plt.show()
