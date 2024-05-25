import numpy as np

# Saving
def save_arrays(arrays, filename):
    np.save(filename, arrays)

# Loading
def load_arrays(filename):
    return np.load(filename, allow_pickle=True)

# Appending
def append_array(existing_arrays, new_array):
    return np.append(existing_arrays, new_array)

# Example usage
# Generate some random arrays
x = 10
y = 5
arrays = [np.random.random((x, 7, 7)) for _ in range(y)]

# Save the arrays
save_arrays(arrays, "arrays.npy")

# Load the arrays
loaded_arrays = load_arrays("arrays.npy")

# Generate and append a new array
new_array = np.random.random((x, 7, 7))
appended_arrays = append_array(loaded_arrays, new_array)

# Save the updated arrays
save_arrays(appended_arrays, "arrays.npy")
