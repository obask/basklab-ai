import pyximport

pyximport.install()

import numpy as np

import board


def main():
    a = np.array([2, 3, 4])
    print("a.sum =", a.sum())
    x = board.fib(11)
    print(x)


if __name__ == "__main__":
    main()
