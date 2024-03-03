import matplotlib.pyplot as plt

# Data
time = [37.801828145980835, 75.90808272361755, 114.0966444015503, 152.19849014282227,
        190.25587391853333, 228.50351691246033, 266.6177513599396, 304.8974072933197,
        343.0685932636261, 381.3316102027893, 419.59605979919434, 457.8683204650879]

percent = [5.70163937528195, 5.507136110102435, 2.5876871054791364, 0.7487364527311957,
           0.19241418314112657, 0.3598832214022325, 0.16112929902242223, 0.11165495460641406,
           0.1708256227789593, 0.16887600501950173, 0.16252810895252567, 0.02663454452841263]

adjustment = [0.05, 0.05, 0.05, 0.04, -0.045, -0.021, -0.05, -0.05, -0.049, -0.05, -0.05, -0.05]


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
