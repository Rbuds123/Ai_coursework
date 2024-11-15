import numpy as np
import random

price = range(326, 18823, 1)
carat = range(20, 501, 1) #most important
cut = [1, 2, 3, 4, 5] #cut of the diamond
colour = [7, 6, 5, 4, 3, 2, 1] #colour of the diamond
clarity = [1, 2, 3, 4, 5, 6, 7, 8] #how clear the diamond is
x = range(0, 1074, 1)
y = range(0, 5890, 1)
z = range(0, 3180, 1)
table = range(43, 95, 1) #integers
depth = z/((x+y)*2)

print(depth)
