import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    df = pd.DataFrame(np.random.randn(20), columns=['Price'])

    df['Category'] = pd.qcut(df['Price'], 3, labels=['Low', 'Middle', 'High'])

    print(df.groupby('Category').count())

    print(df)

if __name__ == "__main__":
    main()