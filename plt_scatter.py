import matplotlib.pyplot as plt
import numpy as np

def main():
    NVALUES=1000
    x = np.random.randn(NVALUES)
    y = np.random.randn(NVALUES)

    plt.figure(figsize=(10,10))
    plt.axis([-5, 5, -5, 5])
    plt.scatter(x, y, alpha=0.5, color=(1,1,0), s=100, edgecolors='red')
    plt.show()

if __name__ == "__main__":
    main()