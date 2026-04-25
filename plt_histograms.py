import matplotlib.pyplot as plt
import numpy as np

def main():
    x = np.random.randn(10000)

    n, bins, patches = plt.hist(x, bins=[-5, -1, 1, 5], edgecolor='white')

    print(n, bins, patches)

    plt.show()

if __name__ == "__main__":
    main()