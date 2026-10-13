import numpy as np

def softmax(values):
    sum = np.sum(np.exp(values))
    values = np.exp(values)
    values /= sum
    return values

def choose_action(probabilities):
    return np.random.choice([0, 1, 2, 3], 1, p=probabilities)

values = np.array([1, 2, 3, 2])
print(np.max(values))