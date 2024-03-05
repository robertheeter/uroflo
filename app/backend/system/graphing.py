import pandas as pd
import matplotlib.pyplot as plt

# Data
file = 'pid_data/PID_TESTING_3.csv'
df = pd.read_csv(file)
time = df['time']
time = [i/60 for i in time]
percent = df['percent']
adjustment = df['adjustment']

flow_rate = 0
flow_rates = []

for a in adjustment[::-1]:
    flow_rate += -1*a

    if flow_rate < 0:
        flow_rate = 0

    flow_rates.insert(0, flow_rate)

print(flow_rates)
print(max(flow_rates))
all_flow_rates = [i*450 for i in flow_rates]

all_flow_rates = [f-100 for f in all_flow_rates]
all_flow_rates = [f if f > 0 else 0 for f in all_flow_rates]

adjustment_new = [p*1000 for p in adjustment]

# Plotting
fig, ax1 = plt.subplots()

# Plotting percent on the right y-axis
ax1.plot(time, percent, marker='o', linestyle='-', color='r', label='Percent')
ax1.set_xlabel('Time After Start (min)')
ax1.set_ylim(0,8)
ax1.set_ylabel('Blood Concentration (%)')
ax1.tick_params('y')

# Creating a twin axis for the left y-axis
ax2 = ax1.twinx()
ax2.plot(time, adjustment_new, marker='s', linestyle='-', color='b', label='Adjustment')
ax2.set_ylim(-50, 750)
ax2.set_ylabel('Linear Actuator Adjustment (ms)')
ax2.tick_params('y')

# Adding a horizontal dashed red line at y=0.5 for the percent plot
ax1.axhline(y=0.5, color='g', linestyle='--', label='Setpoint (0.5%)')

# Adding a legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

# Adding title
#plt.title('PID Testing')

# Display the plot
plt.show()




# Plotting
fig, ax1 = plt.subplots()

# Plotting percent on the right y-axis
ax1.plot(time, percent, marker='o', linestyle='-', color='r', label='Percent')
ax1.set_xlabel('Time After Start (min)')
ax1.set_ylim(0,8)
ax1.set_ylabel('Blood Concentration (%)')
ax1.tick_params('y')

# Creating a twin axis for the left y-axis
ax2 = ax1.twinx()
ax2.plot(time, all_flow_rates, marker='s', linestyle='-', color='#6b1b80', label='Flow Rate')
ax2.set_ylim(-1, 205)
ax2.set_ylabel('Flow Rate (mL/min)')
ax2.tick_params('y')

# Adding a horizontal dashed red line at y=0.5 for the percent plot
ax1.axhline(y=0.5, color='g', linestyle='--', label='Setpoint (0.5%)')

# Adding a legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

# Adding title
#plt.title('PID Testing')

# Display the plot
plt.show()