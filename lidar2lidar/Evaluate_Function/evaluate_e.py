import numpy as np
import math 
from e1 import Calculate_theta
from e2 import Calculate_serface_center
from e2 import Calculate_distance


'''e1 为角度，先转换为弧度'''
def e_theta(e1):
    return math.sin(min(e1/180*math.pi, math.pi/2))


def e_length(e2, Lmax):
    return min(1/math.tanh(Lmax)*math.tanh(e2), 1)


def main():
    e1 = Calculate_theta()
    e2 = Calculate_distance()
    print("//////////////////////////////////////")
    print("//////////////////////////////////////")
    Lmax = 0.2
    print("θ:", e1, "°")
    print("distance:", e2, "meters")
    e_t = e_theta(e1)
    # print(e_t)
    e_l = e_length(e2, Lmax)
    # print(e_l)
    '''调和平均数'''
    e = 2 * e_t * e_l / (e_t + e_l) #+ math.exp(-e_t)*e_l + math.exp(-e_l)*e_t

    return e

score = main()
print("socre:", score)