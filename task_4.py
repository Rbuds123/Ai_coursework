import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class NeuralNetwork:
    def __init__(self, X, HL, Y):
        """
        Initialize the neural network with input size, hidden layers, and output size.

        Args:
            X (int): Number of input features.
            HL (list): List of integers representing the number of neurons in each hidden layer.
            Y (int): Number of output neurons.
        """
        self.X = X
        self.HL = HL
        self.Y = Y

        L = [X] + HL + [Y]

        self.W = [np.random.randn(L[i], L[i + 1]) * np.sqrt(2 / L[i]) for i in range(len(L) - 1)]
        self.B = [np.zeros((1, L[i + 1])) for i in range(len(L) - 1)]

        self.Der_W = [np.zeros_like(w) for w in self.W]
        self.Der_B = [np.zeros_like(b) for b in self.B]

        self.out = [np.zeros(L[i]) for i in range(len(L))]

    def relu(self, x):
        """
        Apply the ReLU activation function.

        Args:
            x (numpy.ndarray): Input array.

        Returns:
            numpy.ndarray: Output array with ReLU applied.
        """
        return np.maximum(0, x)

    def relu_derivative(self, x):
        """
        Compute the derivative of the ReLU activation function.

        Args:
            x (numpy.ndarray): Input array.

        Returns:
            numpy.ndarray: Output array with ReLU derivative applied.
        """
        return np.where(x > 0, 1, 0)

    def FF(self, x):
        """
        Perform forward propagation through the network.

        Args:
            x (numpy.ndarray): Input data.

        Returns:
            numpy.ndarray: Output of the network.
        """
        self.activations = [x]
        self.z_values = []

        for i, (w, b) in enumerate(zip(self.W, self.B)):
            z = np.dot(self.activations[-1], w) + b
            self.z_values.append(z)
            if i == len(self.W) - 1:  # Output layer
                self.activations.append(z)  # Linear activation for regression
            else:
                self.activations.append(self.relu(z))

        return self.activations[-1]

    def BD(self, x, y, learning_rate):
        """
        Perform backpropagation and update weights and biases.

        Args:
            x (numpy.ndarray): Input data.
            y (numpy.ndarray): Target data.
            learning_rate (float): Learning rate for weight updates.
        """
        m = x.shape[0]

        # Calculate error in output layer
        error = self.activations[-1] - y
        deltas = [error]  # Linear activation derivative is 1

        # Backpropagate errors
        for i in range(len(self.W) - 1, 0, -1):
            delta = np.dot(deltas[0], self.W[i].T) * self.relu_derivative(self.z_values[i - 1])
            deltas.insert(0, delta)

        # Update weights and biases
        for i in range(len(self.W)):
            self.W[i] -= learning_rate * np.dot(self.activations[i].T, deltas[i]) / m
            self.B[i] -= learning_rate * np.mean(deltas[i], axis=0, keepdims=True)

    def train(self, x, y, epochs, learning_rate, batch_size):
        """
        Train the neural network using mini-batch gradient descent.

        Args:
            x (numpy.ndarray): Training data.
            y (numpy.ndarray): Target data.
            epochs (int): Number of training epochs.
            learning_rate (float): Learning rate for weight updates.
            batch_size (int): Size of each mini-batch.

        Returns:
            list: History of mean squared error for each epoch.
        """
        history = []
        m = x.shape[0]

        for epoch in range(epochs):
            indices = np.arange(m)
            np.random.shuffle(indices)

            for start_idx in range(0, m, batch_size):
                end_idx = min(start_idx + batch_size, m)
                batch_indices = indices[start_idx:end_idx]
                x_batch = x[batch_indices]
                y_batch = y[batch_indices]

                self.FF(x_batch)
                self.BD(x_batch, y_batch, learning_rate)

            # Calculate mean squared error for tracking
            mse = np.mean((y - self.FF(x)) ** 2)
            history.append(mse)

            if (epoch + 1) % 20 == 0:
                print(f"Epoch {epoch + 1}/{epochs}, MSE: {mse:.6f}")

        return history

    def predict(self, x):
        """
        Predict the output for given input data.

        Args:
            x (numpy.ndarray): Input data.

        Returns:
            numpy.ndarray: Predicted output.
        """
        return self.FF(x)

def denormalize(data, min_val, max_val):
    """
    Denormalize the data using the exponential function.

    Args:
        data (numpy.ndarray): Data to be denormalized.
        min_val (float): Minimum value of the original data (not used in this function).
        max_val (float): Maximum value of the original data (not used in this function).

    Returns:
        numpy.ndarray: Denormalized data.
    """
    return np.expm1(data)

# Load and preprocess the dataset
data = pd.read_csv('data.csv')

# Select features and target
features = ['carat', 'cut', 'colour', 'clarity', 'depth', 'table', 'x', 'y', 'z']
target = 'price'

# Encode categorical variables
cut_mapping = {'Fair': 1, 'Good': 2, 'Very Good': 3, 'Premium': 4, 'Ideal': 5}
color_mapping = {'J': 1, 'I': 2, 'H': 3, 'G': 4, 'F': 5, 'E': 6, 'D': 7}
clarity_mapping = {'I1': 1, 'SI2': 2, 'SI1': 3, 'VS2': 4, 'VS1': 5, 'VVS2': 6, 'VVS1': 7, 'IF': 8}

data['cut'] = data['cut'].map(cut_mapping)
data['colour'] = data['colour'].map(color_mapping)
data['clarity'] = data['clarity'].map(clarity_mapping)

# Remove rows with missing values
data = data.dropna()

# Convert to numpy arrays to ensure compatibility with the neural network class
X = data[features].values
y = data[target].values.reshape(-1, 1)

# Normalize features
X_min = X.min(axis=0) # Minimum values for normalization
X_max = X.max(axis=0) # Maximum values for normalization
X_max[X_max == X_min] += 1e-8
# we normalize the x to ensure all features are on the same scale
X_norm = (X - X_min) / (X_max - X_min)

# Normalize target using log transformation
y_log = np.log1p(y)

# Split into training and testing sets
indices = np.arange(len(X_norm))
np.random.seed(42)
np.random.shuffle(indices)
split_index = int(0.8 * len(indices))
train_indices = indices[:split_index]
test_indices = indices[split_index:]

X_train = X_norm[train_indices] #training data based on shuffled indices
X_test = X_norm[test_indices]
y_train = y_log[train_indices] #training target values 
y_test = y_log[test_indices]

# Create and train the neural network
nn = NeuralNetwork(X=X_train.shape[1], HL=[32, 16, 8], Y=1)
history = nn.train(X_train, y_train, epochs=100, learning_rate=0.001, batch_size=32)

# Predict on test data
y_pred = nn.predict(X_test)

# Denormalizing is done to bring the predictions and actual values (y_test) back to their original scale
# so they can be interpreted in the context of the original data.
y_test_denorm = denormalize(y_test, 0, 1)
y_pred_denorm = denormalize(y_pred, 0, 1)

# Plot results
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.scatter(y_test_denorm, y_pred_denorm, alpha=0.5, color="blue")
#this line represents a comparasion between the actual and predicted values
plt.plot([min(y_test_denorm), max(y_test_denorm)], [min(y_test_denorm), max(y_test_denorm)], color="red", linestyle="--")
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted Prices")
plt.grid(True)
sample_indices = np.random.choice(y_test_denorm.shape[0], 5, replace=False)
samples = [(y_test_denorm[i][0], y_pred_denorm[i][0], y_test_denorm[i][0] - y_pred_denorm[i][0]) for i in sample_indices]

# Print random samples in a table format with additional columns for number and error percentage
print(f"{'No.':<5}{'Actual':<15}{'Predicted':<15}{'Difference':<15}{'Error (%)':<15}")
print("-" * 65)
for i, (actual, predicted, difference) in enumerate(samples, start=1):
    error_percentage = (abs(difference) / actual) * 100
    print(f"{i:<5}{actual:<15.2f}{predicted:<15.2f}{difference:<15.2f}{error_percentage:<15.2f}")
# display the training loss history    
plt.subplot(1, 2, 2)
plt.plot(history)
plt.xlabel("Epoch")
plt.ylabel("Mean Squared Error")
plt.title("Training Loss History")
plt.grid(True)
plt.tight_layout()
plt.show()