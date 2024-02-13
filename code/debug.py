import numpy as np

# Load the data from the .npy file
filename = "grid_data.npy"
loaded_data = np.load(filename, allow_pickle=True)

# Print the loaded data
print(loaded_data)