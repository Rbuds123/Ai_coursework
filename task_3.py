from random import random
import numpy as np
import matplotlib.pyplot as plt

class Neural_network(object):
    """
    A simple neural network implementation from scratch with ReLU activation, 
    forward propagation, backpropagation, and gradient descent.

    Attributes:
        X (int): Number of input features.
        HL (list): List specifying the number of neurons in each hidden layer.
        Y (int): Number of output features.
    """
    def __init__(self, X, HL, Y):
        """
        Initialize the neural network with random weights and biases.

        Args:
            X (int): Number of input features.
            HL (list): List specifying the number of neurons in each hidden layer.
            Y (int): Number of output features.
        """
        self.X = X
        self.HL = HL
        self.Y = Y
        
        # Define the structure of the network
        L = [X] + HL + [Y]
        
        # Initialize weights with He initialization and biases to zero
        # Scaled for ReLU
        self.W = [np.random.randn(L[i], L[i + 1]) * np.sqrt(2 / L[i]) for i in range(len(L) - 1)]
        self.B = [np.zeros((1, L[i + 1])) for i in range(len(L) - 1)]
        
        # Initialize gradients for weights and biases
        self.Der_W = [np.zeros_like(w) for w in self.W]
        self.Der_B = [np.zeros_like(b) for b in self.B]
        
        # Initialize output placeholders for each layer
        self.out = [np.zeros(L[i]) for i in range(len(L))]

    def relu(self, x):
        """ReLU activation function."""
        return np.maximum(0, x)

    def relu_Der(self, x):
        """Derivative of the ReLU activation function."""
        return np.where(x > 0, 1, 0)
        
    def FF(self, x):
        """
        Forward pass through the network.

        Args:
            x (array): Input data.

        Returns:
            array: Output of the network.
        """
        self.out[0] = x
        out = x.reshape(1, -1)
        
        # Forward propagate through hidden layers with ReLU activation
        for i, (w, b) in enumerate(zip(self.W[:-1], self.B[:-1])):
            Xnext = np.dot(out, w) + b
            out = self.relu(Xnext)
            self.out[i + 1] = out
            
        # Forward propagate through the output layer
        out = np.dot(out, self.W[-1]) + self.B[-1]
        self.out[-1] = out
        
        return out.flatten()
        
    def BP(self, Er):
        """
        Backpropagation to compute gradients for weights and biases.

        Args:
            Er (array): Error at the output layer.
        """
        Er = Er.reshape(1, -1)
        
        # Loop backward through layers to calculate gradients
        for i in reversed(range(len(self.Der_W))):
            out = self.out[i + 1]
            
            if i == len(self.Der_W) - 1:
                D = Er  # Output layer
            else:
                D = Er * self.relu_Der(out)  # Hidden layers
            
            this_out = self.out[i].reshape(-1, 1)
            
            # Compute gradients
            self.Der_W[i] = np.dot(this_out, D)
            self.Der_B[i] = D
            
            if i > 0:
                Er = np.dot(D, self.W[i].T)

    def train_nn(self, x, target, epochs, lr, batch_size):
        """
        Train the neural network using mini-batch gradient descent.

        Args:
            x (array): Training input data.
            target (array): Target output data.
            epochs (int): Number of training epochs.
            lr (float): Learning rate.
            batch_size (int): Size of each mini-batch.

        Returns:
            list: Training history of mean squared error (MSE) for each epoch.
        """
        n_batches = len(x) // batch_size
        history = []
        
        for epoch in range(epochs):
            # Shuffle the dataset at each epoch
            indices = np.random.permutation(len(x))
            x_shuffled = x[indices]
            target_shuffled = target[indices]
            
            epoch_error = 0
            for batch in range(n_batches):
                # Create mini-batches
                start_idx = batch * batch_size
                end_idx = start_idx + batch_size
                
                batch_x = x_shuffled[start_idx:end_idx]
                batch_target = target_shuffled[start_idx:end_idx]
                
                batch_error = 0
                for j in range(len(batch_x)):
                    output = self.FF(batch_x[j])  # Forward pass
                    e = batch_target[j] - output  # Compute error
                    self.BP(e)  # Backpropagation
                    self.GD(lr)  # Gradient descent
                    batch_error += self.msqe(batch_target[j], output)  # Compute MSE
                
                epoch_error += batch_error / batch_size
            
            avg_error = epoch_error / n_batches
            history.append(avg_error)
            
            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch + 1}/{epochs}, Average Error: {avg_error:.6f}")
            
            if avg_error < 1e-6:
                print("Training stopped early due to low error.")
                break
                
        return history

    def GD(self, lr):
        """
        Update weights and biases using gradient descent.

        Args:
            lr (float): Learning rate.
        """
        for i in range(len(self.W)):
            self.W[i] += self.Der_W[i] * lr
            self.B[i] += self.Der_B[i] * lr

    def msqe(self, t, output):
        """
        Compute the mean squared error (MSE).

        Args:
            t (array): True target values.
            output (array): Predicted values.

        Returns:
            float: Mean squared error.
        """
        return np.average((t - output) ** 2)

if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    x_width = 20  # Define the range of input data

    # Generate training data
    training_inputs = np.array([[random() * x_width * 2 - x_width] for _ in range(100)])
    targets = np.array([[3 * x + 0.7 * x ** 2] for x in training_inputs])
    
    # Normalize input and target data
    input_mean, input_std = training_inputs.mean(), training_inputs.std()
    target_mean, target_std = targets.mean(), targets.std()
    training_inputs = (training_inputs - input_mean) / input_std
    targets = (targets - target_mean) / target_std

    # Initialize and train the neural network
    nn = Neural_network(1, [64, 16, 32], 1)
    history = nn.train_nn(training_inputs, targets, epochs=200, lr=0.002, batch_size=64)
    
    # Generate test data
    test_inputs = np.linspace(x_width * -1, x_width, 200).reshape(-1, 1)
    true_outputs = 3 * test_inputs + 0.7 * (test_inputs ** 2)
    
    # Normalize test inputs
    test_inputs_std = (test_inputs - input_mean) / input_std
    nn_outputs_std = np.array([nn.FF(x) for x in test_inputs_std])
    
    # Denormalize neural network outputs
    nn_outputs = nn_outputs_std * target_std + target_mean
    
    # Plot results
    plt.figure(figsize=(12, 6))
    
    # Plot the true function and the neural network approximation
    plt.subplot(1, 2, 1)
    plt.plot(test_inputs, true_outputs, label="True function", color="blue", linestyle="--")
    plt.plot(test_inputs, nn_outputs, label="NN approximation", color="orange")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.title("True function vs NN approximation")
    
    # Plot training history
    plt.subplot(1, 2, 2)
    plt.plot(history, label="Training Error")
    plt.xlabel("Epoch")
    plt.ylabel("Mean Squared Error")
    plt.legend()
    plt.title("Training History")
    
    plt.tight_layout()
    plt.show()