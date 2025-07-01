import matplotlib.pyplot as plt

# Define data for the papers and their corresponding communication and computation overhead
papers = [
    "Improve Security over the WSNs Case Study: Smart Irrigation in the Agricultural Sector",
    "WSN: Security, Threats, Solutions",
    "AI-Based Intrusion Detection",
    "AI-Based Instinctive Irrigation",
    "Precision Agriculture WSN",
]

# Hypothetical values for communication overhead (in milliseconds) and computation overhead (in bytes)
communication_overhead_bytes = [118, 120, 90, 100, 110]  # in bytes
computation_overhead_ms = [4.2, 256, 320, 280, 240]  # in milliseconds

# Plotting Communication Overhead (bytes)
fig, ax1 = plt.subplots(figsize=(12, 6))  # Increased size for better label visibility
ax1.bar(papers, communication_overhead_bytes, color="blue")
ax1.set_xlabel("Papers", fontsize=12)
ax1.set_ylabel("Communication Overhead (bytes)", fontsize=12)
ax1.set_title("Communication Overhead (bytes)", fontsize=14)

# Rotate x-axis labels 90 degrees for better readability
ax1.tick_params(axis="x", rotation=90)

# Adjust layout and display the first chart
plt.tight_layout()
plt.show()

# Plotting Computation Overhead (ms)
fig, ax2 = plt.subplots(figsize=(12, 6))  # Increased size for better label visibility
ax2.bar(papers, computation_overhead_ms, color="orange")
ax2.set_xlabel("Papers", fontsize=12)
ax2.set_ylabel("Computation Overhead (ms)", fontsize=12)
ax2.set_title("Computation Overhead (ms)", fontsize=14)

# Rotate x-axis labels 90 degrees for better readability
ax2.tick_params(axis="x", rotation=90)

# Adjust layout and display the second chart
plt.tight_layout()
plt.show()
