import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('flight_trajectory.csv')

# Force everything into raw Numpy arrays immediately to prevent Matplotlib crashes
time_array = ((df['Timestamp'] - df['Timestamp'].iloc[0]) / 1000000.0).to_numpy()
x_array = df['X'].to_numpy()
y_array = df['Y'].to_numpy()
z_array = df['Z'].to_numpy()

# Create the plots
fig = plt.figure(figsize=(12, 8))

# 3D Trajectory Plot
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
ax1.plot(x_array, y_array, z_array, label='Flight Path', color='b', linewidth=2)
ax1.set_xlabel('X (North) [m]')
ax1.set_ylabel('Y (East) [m]')
ax1.set_zlabel('Altitude [m]')
ax1.set_title('3D UAV Trajectory')
ax1.legend()

# X vs Time
ax2 = fig.add_subplot(2, 2, 2)
ax2.plot(time_array, x_array, color='r')
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('X Position [m]')
ax2.set_title('North Movement vs Time')
ax2.grid(True)

# Y vs Time
ax3 = fig.add_subplot(2, 2, 3)
ax3.plot(time_array, y_array, color='g')
ax3.set_xlabel('Time [s]')
ax3.set_ylabel('Y Position [m]')
ax3.set_title('East Movement vs Time')
ax3.grid(True)

# Z vs Time
ax4 = fig.add_subplot(2, 2, 4)
ax4.plot(time_array, z_array, color='purple')
ax4.set_xlabel('Time [s]')
ax4.set_ylabel('Altitude [m]')
ax4.set_title('Altitude vs Time')
ax4.grid(True)

plt.tight_layout()
plt.savefig('square_trajectory_report.png', dpi=300)
print("Success! Saved as square_trajectory_report.png")
plt.show()
