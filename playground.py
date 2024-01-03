import matplotlib.pyplot as plt
import numpy as np

def gradient_descent(starting_w, learning_rate, num_iterations):
    
    w = starting_w
    w_history = [w]
    cost_history = [(50*w - 20)**2]

    for _ in range(num_iterations):
        gradient = 2 * (50 * w - 20) * 50
        w -= learning_rate * gradient
        w_history.append(w)
        cost_history.append((50*w - 20)**2)

        if np.isnan(cost_history[-1]):
            break

    return w_history, cost_history

starting_w = 0.5  # 초기 W값
learning_rate = 0.00001  # 학습률
num_iterations = 10000 # 반복 횟수


w_history, cost_history = gradient_descent(starting_w, learning_rate, num_iterations)

plt.figure(figsize=(12, 6))

# W에 따른 Cost 표시
plt.subplot(1, 2, 1)
plt.plot(w_history, cost_history)
plt.xlabel('W value')
plt.ylabel('Cost')
plt.title('Cost Function')

plt.subplot(1, 2, 2)
plt.plot(range(len(cost_history)), cost_history)
plt.yscale('log')  
plt.xlabel('Iteration')
plt.ylabel('Cost (log scale)')
plt.title('Cost over Iterations (Log Scale)')
plt.xlim(0, len(cost_history) - 1) 

plt.tight_layout()
plt.show()
