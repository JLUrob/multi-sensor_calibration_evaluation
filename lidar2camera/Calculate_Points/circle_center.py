import numpy as np
import math
import sys


num = sys.argv[1]
open_path ="./Points/points_" + num + ".txt"
save_path ="./Center_Points/center_points_" + num + ".txt"
'''计算球心'''
def Calculate_center(p1, p2, p3 ,p4):
    w = np.zeros((4,4))
    b = np.zeros((1,4)) 

    x = p1[0][0]
    y = p1[0][1]
    z = p1[0][2]
    b[0][0] = -np.sum(p1*p1)
    w[0][0:3] = p1[0]
    w[0][3] = 1

    x = p2[0][0]
    y = p2[0][1]
    z = p2[0][2]
    b[0][1] = -np.sum(p2*p2)
    w[1][0:3] = p2[0]
    w[1][3] = 1

    x = p3[0][0]
    y = p3[0][1]
    z = p3[0][2]
    b[0][2] = -np.sum(p3*p3)
    w[2][0:3] = p3[0]
    w[2][3] = 1

    x = p4[0][0]
    y = p4[0][1]
    z = p4[0][2]
    b[0][3] = -np.sum(p4*p4)
    w[3][0:3] = p4[0]
    w[3][3] = 1

    # print("w:", w)
    # print("b:", b)

    # result = np.array([[26,1,18]])
    # print(np.linalg.matrix_rank(w))
    w_inv = np.linalg.inv(w)
    c = np.dot(w_inv, b.T)
    O = np.array([[-c[0][0]/2, -c[1][0]/2, -c[2][0]/2]])
    return O

'''计算圆心'''
def Calculate_serface_center(p1, p2, p3):
    w = np.zeros((3,3))
    b = np.zeros((1,3)) 

    x1 = p1[0][0]
    y1 = p1[0][1]
    z1 = p1[0][2]

    x2 = p2[0][0]
    y2 = p2[0][1]
    z2 = p2[0][2]

    x3 = p3[0][0]
    y3 = p3[0][1]
    z3 = p3[0][2]
    
    A1 =  y1*z2 - y1*z3 - z1*y2 + z1*y3 + y2*z3 - y3*z2
    B1 = -x1*z2 + x1*z3 + z1*x2 - z1*x3 - x2*z3 + x3*z2 
    C1 =  x1*y2 - x1*y3 - y1*x2 + y1*x3 + x2*y3 - x3*y2
    D1 =  -x1*y2*z3 + x1*y3*z2 + x2*y1*z3 - x3*y1*z2 - x2*y3*z1 + x3*y2*z1

    A2 = 2*(x2-x1)
    B2 = 2*(y2-y1)
    C2 = 2*(z2-z1)
    D2 = x1*x1 + y1*y1 + z1*z1 - x2*x2 - y2*y2 - z2*z2

    A3 = 2*(x3-x1)
    B3 = 2*(y3-y1)
    C3 = 2*(z3-z1)
    D3 = x1*x1 + y1*y1 + z1*z1 - x3*x3 - y3*y3 - z3*z3

    w[0][0] = A1
    w[0][1] = B1
    w[0][2] = C1
    b[0][0] = D1

    w[1][0] = A2
    w[1][1] = B2
    w[1][2] = C2
    b[0][1] = D2

    w[2][0] = A3
    w[2][1] = B3
    w[2][2] = C3
    b[0][2] = D3
    # result = np.array([[26,1,18]])
    # print(np.linalg.matrix_rank(w))
    w_inv = np.linalg.inv(w)
    c = -np.dot(w_inv, b.T)
    O = np.array([[c[0][0], c[1][0], c[2][0]]])
    return O

def Calculate_distance():
    p1 = np.zeros((1,3))
    p2 = np.zeros((1,3))
    p3 = np.zeros((1,3))
    p4 = np.zeros((1,3))
    with open(open_path,encoding='utf-8') as file:
        i = 1
        p = np.zeros((4,3))
        with open(save_path, 'w',  encoding='utf-8') as f:
            for line in file:
                data_line = line.strip("\n").split()  # 去除首尾换行符，并按空格划分
                if i == 1:
                    p1[0][0] = float(data_line[0])
                    p1[0][1] = float(data_line[1])
                    p1[0][2] = float(data_line[2])
                if i == 2:
                    p2[0][0] = float(data_line[0])
                    p2[0][1] = float(data_line[1])
                    p2[0][2] = float(data_line[2])
                if i == 3:
                    p3[0][0] = float(data_line[0])
                    p3[0][1] = float(data_line[1])
                    p3[0][2] = float(data_line[2])
                if i == 4:
                    p4[0][0] = float(data_line[0])
                    p4[0][1] = float(data_line[1])
                    p4[0][2] = float(data_line[2])
                '''每四个点做一次循环'''
                if i == 4:
                    O = Calculate_serface_center(p1, p2 ,p3)
                    print("center: (", O[0][0], ", ", O[0][1], ", ", O[0][2], ")",)
                    f.write(str(O[0][0]) + " " + str(O[0][1]) + " " + str(O[0][2]) + '\n')
                    # print(str(O[0][0]) + " " + str(O[0][1]) + " " + str(O[0][2]))
                    i = 0
                i += 1
        f.close()
    file.close()

if len(sys.argv) <=1 :
    print("error input !")
    print("example: python circle_center.py 10")
    sys.exit()
Calculate_distance()

