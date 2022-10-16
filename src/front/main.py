
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3

def main():
    s = pd.Series([1, 2, 3])
    fig, ax = plt.subplots()
    s.plot.bar()
    fig.savefig('my_plot.png')




if (__name__ == "__main__"):
    main()
