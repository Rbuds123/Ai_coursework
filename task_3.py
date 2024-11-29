from random import random
import numpy as np
import matplotlib.pyplot as plt


class Neural_network(object):
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
    
    def relu_Der(self, x):
        return np.where(x > 0, 1, 0)
        
    def FF(self, x):
        self.out[0] = x
        out = x.reshape(1, -1)
        
        for i, (w, b) in enumerate(zip(self.W[:-1], self.B[:-1])):
            Xnext = np.dot(out, w) + b
            out = self.relu(Xnext)
            self.out[i + 1] = out
            
        out = np.dot(out, self.W[-1]) + self.B[-1]
        self.out[-1] = out
        
        return out.flatten()
        
    def BP(self, Er):
        Er = Er.reshape(1, -1)
        
        for i in reversed(range(len(self.Der_W))):
            out = self.out[i + 1]
            
            if i == len(self.Der_W) - 1:
                D = Er
            else:
                D = Er * self.relu_Der(out)
            
            this_out = self.out[i].reshape(-1, 1)
            
            self.Der_W[i] = np.dot(this_out, D)
            self.Der_B[i] = D
            
            if i > 0:
                Er = np.dot(D, self.W[i].T)

    def train_nn(self, x, target, epochs, lr, batch_size=32):
        n_batches = len(x) // batch_size
        history = []
        
        for epoch in range(epochs):
            indices = np.random.permutation(len(x))
            x_shuffled = x[indices]
            target_shuffled = target[indices]
            
            epoch_error = 0
            for batch in range(n_batches):
                start_idx = batch * batch_size
                end_idx = start_idx + batch_size
                
                batch_x = x_shuffled[start_idx:end_idx]
                batch_target = target_shuffled[start_idx:end_idx]
                
                batch_error = 0
                for j in range(len(batch_x)):
                    output = self.FF(batch_x[j])
                    e = batch_target[j] - output
                    self.BP(e)
                    self.GD(lr)
                    batch_error += self.msqe(batch_target[j], output)
                
                epoch_error += batch_error / batch_size
            
            avg_error = epoch_error / n_batches
            history.append(avg_error)
            
            if (epoch + 1) % 100 == 0:
                print(f"Epoch {epoch + 1}/{epochs}, Average Error: {avg_error:.6f}")
            
            if avg_error < 1e-6:
                print("Training stopped early due to low error.")
                break
                
        return history

    def GD(self, lr):
        for i in range(len(self.W)):
            self.W[i] += self.Der_W[i] * lr
            self.B[i] += self.Der_B[i] * lr

    def msqe(self, t, output):
        return np.average((t - output) ** 2)

if __name__ == "__main__":
    np.random.seed(42)
    x_width = 20
    # x_width = int(input("Enter the width of the x-axis: ")) 
    training_inputs = np.array([[random() * x_width * 2 - x_width] for _ in range(100)])
    targets = np.array([[3 * x + 0.7 * x ** 2] for x in training_inputs])
    
    input_mean, input_std = training_inputs.mean(), training_inputs.std()
    target_mean, target_std = targets.mean(), targets.std()
    
    training_inputs = (training_inputs - input_mean) / input_std
    targets = (targets - target_mean) / target_std
    #set HL to  because any lower and the neural network doesnt aproxmite well
    nn = Neural_network(1, [30, 40], 1)
    history = nn.train_nn(training_inputs, targets, epochs=400, lr=0.002, batch_size=32)
    
    test_inputs = np.linspace(x_width * -1, x_width, 200).reshape(-1, 1)
    true_outputs = 3 * test_inputs + 0.7 * (test_inputs ** 2)
    
    test_inputs_std = (test_inputs - input_mean) / input_std
    nn_outputs_std = np.array([nn.FF(x) for x in test_inputs_std])
    
    nn_outputs = nn_outputs_std * target_std + target_mean
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(test_inputs, true_outputs, label="True function", color="blue", linestyle="--")
    plt.plot(test_inputs, nn_outputs, label="NN approximation", color="orange")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.title("Neural Network Approximation vs. True Function")
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(history)
    plt.xlabel("Epoch")
    plt.ylabel("Mean Squared Error")
    plt.title("Training History")
    plt.yscale('log')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()