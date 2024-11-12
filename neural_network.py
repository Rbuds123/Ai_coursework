from random import random
import numpy as np
import matplotlib.pyplot as plt

class Neural_network(object):
    def __init__(self, X=1, HL=[5, 5], Y=1):
        # Initialize the neural network with default values
        self.X = X  # Number of inputs
        self.HL = HL  # Hidden layers
        self.Y = Y  # Number of outputs

        # Create a list representing the network layers
        L = [X] + HL + [Y]

        # Initialize weights with random values
        self.W = [np.random.rand(L[i], L[i + 1]) for i in range(len(L) - 1)]

        # Initialize derivatives with zeros
        self.Der = [np.zeros((L[i], L[i + 1])) for i in range(len(L) - 1)]

        # Initialize outputs with zeros
        self.out = [np.zeros(L[i]) for i in range(len(L))]

    def FF(self, x):
        # Forward propagation
        self.out[0] = x
        out = x
        for i, w in enumerate(self.W):
            Xnext = np.dot(out, w)
            out = self.sigmoid(Xnext)
            self.out[i + 1] = out
        return out

    def BP(self, Er):
        # Backward propagation
        for i in reversed(range(len(self.Der))):
            out = self.out[i + 1]
            D = Er * self.sigmoid_Der(out)
            D_fixed = D.reshape(D.shape[0], 1).T
            this_out = self.out[i].reshape(-self.out[i].shape[0], 1)
            self.Der[i] = np.dot(this_out, D_fixed)
            Er = np.dot(D, self.W[i].T)

    def train_nn(self, x, target, epochs, lr):
    # Train the neural network
        for epoch in range(epochs):
            S_errors = 0
            for j in range(len(x)):
                t = target[j]
                output = self.FF(x[j])
                e = t - output
                self.BP(e)
                self.GD(lr)
                S_errors += self.msqe(t, output)
        
        # Average error for this epoch
            avg_error = S_errors / len(x)
            print(f"Epoch {epoch + 1}/{epochs}, Average Error: {avg_error}")
        
        # Optional: Stop early if error is very low
            if avg_error < 1e-6:
                print("Training stopped early due to low error.")
                break


    def GD(self, lr=0.05):
        # Gradient descent
        for i in range(len(self.W)):
            self.W[i] += self.Der[i] * lr

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1.0 / (1 + np.exp(-x))

    def sigmoid_Der(self, x):
        # Derivative of the sigmoid function
        return x * (1.0 - x)

    def msqe(self, t, output):
        # Mean squared error
        return np.average((t - output) ** 2)

if __name__ == "__main__":
    # Generate training data
    training_inputs = np.array([[random()] for _ in range(500)])
    targets = np.array([[3 * x[0] + 0.7 * x[0] ** 2] for x in training_inputs])
    
    # Initialize and train the neural network
    nn = Neural_network(1, [5, 5], 1)  # Adjust layer sizes if necessary
    nn.train_nn(training_inputs, targets, epochs=500, lr=1)
    
    test_inputs = np.linspace(-15, 10, 100).reshape(-1, 1)
    true_outputs = 3 * test_inputs + 0.7 * (test_inputs ** 2)
    nn_outputs = np.array([nn.FF(x) for x in test_inputs])

# Plot the true function and the neural network approximation
    plt.plot(test_inputs, nn_outputs, label="NN approximation", color="orange")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()