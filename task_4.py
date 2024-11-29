import numpy as np
import csv
import matplotlib.pyplot as plt

class NeuralNetwork:
    def __init__(self, X, HL, Y):
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
        return np.maximum(0, x)

    def relu_derivative(self, x):
        return np.where(x > 0, 1, 0)

    def forward(self, x):
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

    def backward(self, x, y, learning_rate):
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

    def train(self, x, y, epochs, learning_rate):
        history = []

        for epoch in range(epochs):
            self.forward(x)
            self.backward(x, y, learning_rate)

            # Calculate mean squared error for tracking
            mse = np.mean((y - self.activations[-1]) ** 2)
            history.append(mse)

            if (epoch + 1) % 100 == 0:
                print(f"Epoch {epoch + 1}/{epochs}, MSE: {mse:.6f}")

        return history

    def predict(self, x):
        return self.forward(x)

# Load and preprocess the dataset
with open("data.csv", "r") as file:
    reader = csv.reader(file)
    data = list(reader)

header = data[0]  # Column names
rows = data[1:]   # Actual data

# Select features and target
price_index = header.index("price")
features = []
target = []

# Handle features and target
for row in rows:
    features.append([float(row[i]) if row[i].replace('.', '', 1).isdigit() else row[i] for i in range(len(row)) if i != price_index])
    target.append(float(row[price_index]))

features = np.array(features)
target = np.array(target).reshape(-1, 1)

# Handle categorical data (one-hot encoding manually)
categorical_columns = [header.index("cut"), header.index("colour"), header.index("clarity")]
encoded_features = []

def encode_categorical(column_values):
    unique_values = sorted(set(column_values))
    encoding_map = {val: idx for idx, val in enumerate(unique_values)}
    return [encoding_map[val] for val in column_values]

# Apply one-hot encoding for categorical columns
for column in categorical_columns:
    column_values = [row[column] for row in rows]
    encoded_column = encode_categorical(column_values)
    encoded_features.append(encoded_column)

encoded_features = np.column_stack(encoded_features)
numerical_indices = [i for i in range(features.shape[1]) if i not in categorical_columns and i != price_index]

# Combine numerical and encoded categorical features
numerical_features = features[:, numerical_indices].astype(float)
features = np.hstack([numerical_features, encoded_features])

# Normalize numerical features and target
numerical_columns = list(range(len(numerical_indices)))
features[:, numerical_columns] = (features[:, numerical_columns] - features[:, numerical_columns].mean(axis=0)) / features[:, numerical_columns].std(axis=0)
target_mean, target_std = target.mean(), target.std()
target = (target - target_mean) / target_std

# Split dataset into training and testing sets
def train_test_split_manual(data, labels, test_size=0.2, seed=42):
    np.random.seed(seed)
    indices = np.arange(data.shape[0])
    np.random.shuffle(indices)

    split_idx = int(data.shape[0] * (1 - test_size))
    train_idx, test_idx = indices[:split_idx], indices[split_idx:]

    return data[train_idx], data[test_idx], labels[train_idx], labels[test_idx]

x_train, x_test, y_train, y_test = train_test_split_manual(features, target, test_size=0.2)

# Create and train the neural network
nn = NeuralNetwork(X=x_train.shape[1], HL=[128, 64, 32], Y=1)
history = nn.train(x_train, y_train, epochs=400, learning_rate=0.001)

# Predict on test data
y_pred = nn.predict(x_test)

# Denormalize predictions and actual values
def denormalize(data, mean, std):
    return data * std + mean

y_test_denorm = denormalize(y_test, target_mean, target_std)
y_pred_denorm = denormalize(y_pred, target_mean, target_std)

# Plot results
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.scatter(y_test_denorm, y_pred_denorm, alpha=0.5, color="blue")
plt.plot([min(y_test_denorm), max(y_test_denorm)], [min(y_test_denorm), max(y_test_denorm)], color="red", linestyle="--")
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted Prices")
plt.grid(True)
sample_indices = np.random.choice(y_test_denorm.shape[0], 5, replace=False)
samples = [(y_test_denorm[i][0], y_pred_denorm[i][0], y_test_denorm[i][0] - y_pred_denorm[i][0]) for i in sample_indices]

print("Random Samples: Actual, Predicted, Difference")
for actual, predicted, difference in samples:
    print(f"Actual: {actual:.2f}, Predicted: {predicted:.2f}, Difference: {difference:.2f}")
plt.subplot(1, 2, 2)
plt.plot(history)
plt.xlabel("Epoch")
plt.ylabel("Mean Squared Error")
plt.title("Training Loss History")
plt.grid(True)
plt.tight_layout()
plt.show()