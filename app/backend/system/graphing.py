import matplotlib.pyplot as plt

# Data
time = [37.74191069602966, 75.86159992218018, 113.95599961280823, 152.04444551467896,
        190.09167456626892, 228.19806551933289, 266.29894828796387, 304.40638399124146,
        342.5032322406769, 380.5662696361542, 418.591037273407, 456.6936719417572]

percent = [7.579045804311968, 6.631672698647018, 4.636129062062077, 2.532293410779839,
           0.9627296081562338, 0.34061899063515, 0.12824577347973065, 0.3126802623760985,
           0.15620942491690615, 0.4181447390289459, 0.45476673008627255, 0.4339094933655798]

adjustment = [0.05, 0.05, 0.05, 0.05, 0.05, -0.024, -0.05, -0.028, -0.05, -0.012, -0.007, -0.01]

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
