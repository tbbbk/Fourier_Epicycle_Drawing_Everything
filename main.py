from dataclasses import dataclass, field
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import math


@dataclass
class Operator:
    # x + y * i, which is the initial status of the circle
    coefficient: complex = field(default=complex(0, 0))
    # e ^ (n * pi * i * t), index is the n
    index: int = field(default=0)
    
    def position(self, t: float) -> complex:
        """Returns a vector representation of the operator."""
        assert t >= 0 and t <= 1, "t must be in the range [0, 1]"
        angle = np.cos(self.index * 2.0 * math.pi * t) + np.sin(self.index * 2.0 * math.pi * t) * 1j
        return self.coefficient * angle


# [REPLACE HERE] shape function (heart example)
shape = lambda t: complex(
    16 * np.sin(2 * math.pi * t)**3,
    13 * np.cos(2 * math.pi * t) - 5 * np.cos(4 * math.pi * t) - 2 * np.cos(6 * math.pi * t) - np.cos(8 * math.pi * t)
)


# Initialize operators
OPERATOR_NUM = 50 // 2
MONTE_CARLO_NUM = 1000
DRAW_SAMPLES = 100

frequencies = np.arange(-OPERATOR_NUM, OPERATOR_NUM + 1)
operators = [Operator(complex(0, 0), f) for f in frequencies]

# Calculate init position of each operator
t_grid = np.linspace(0, 1, MONTE_CARLO_NUM)
shape_vals = [shape(t) for t in t_grid]
for operator in operators:
    exponents = np.exp(-1j * operator.index * 2 * np.pi * t_grid)
    operator.coefficient = np.sum(shape_vals * exponents) / MONTE_CARLO_NUM
        
# Begin drawing
points = []
for i in tqdm(range(DRAW_SAMPLES + 1), desc="Drawing points"):
    t = i / DRAW_SAMPLES
    point = sum(operator.position(t) for operator in operators)
    points.append([point.real, point.imag])
    # Draw the point (this is a placeholder, replace with actual drawing code)
    
x_vals, y_vals = zip(*points) if points else ([], [])

plt.figure(figsize=(6, 6))
plt.plot(x_vals, y_vals, 'o-', color='red')  # 'o-' means dots connected with lines
plt.axis('equal')  # Keep aspect ratio square
plt.grid(True)
plt.title("Points Plot")
plt.xlabel("x")
plt.ylabel("y")

# Show the plot
plt.show()
