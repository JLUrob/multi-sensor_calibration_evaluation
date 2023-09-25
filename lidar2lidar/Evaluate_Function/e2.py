import numpy as np
import math

path_target_points = 'View_Cloud/Points/target_points.txt'
path_input_points = 'View_Cloud/Points/input_points.txt'

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
    # p1 = np.array([[2.245,  0.028,  0.367]])
    # p2 = np.array([[2.167,  0.063,  0.119]])
    # p3 = np.array([[2.167, -0.483,  0.154]])
    # p4 = np.array([[2.244, -0.414,  0.379]])
    p1 = np.zeros((1,3))
    p2 = np.zeros((1,3))
    p3 = np.zeros((1,3))
    p4 = np.zeros((1,3))
    with open(path_target_points, encoding='utf-8') as file:
        i = 1
        p = np.zeros((4,3))
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
            i += 1
    O1 = Calculate_center(p1, p2 ,p3 ,p4)
    # print(O1)
    # o1 = Calculate_center_serface(p2-p1, p3-p1, p3-p2, O1)
    # print(o1)
    o1 = Calculate_serface_center(p1, p2 ,p3)
    # print(o1)

    # d1 = np.sum((o1-p1)*(o1-p1))
    # d2 = np.sum((o1-p2)*(o1-p2))
    # d3 = np.sum((o1-p3)*(o1-p3))
    # print("d1 = ", d1)
    # print("d2 = ", d2)
    # print("d3 = ", d3)

    # v1 = np.sum((o1-p1)*(o1-O1))
    # v2 = np.sum((o1-p2)*(o1-O1))
    # v3 = np.sum((o1-p3)*(o1-O1))
    # print("v1 = ", v1)
    # print("v2 = ", v2)
    # print("v3 = ", v3)

    # p1 = np.array([[3.4441,  3.85213,  0.110299]])
    # p2 = np.array([[3.41232, 3.81874, -0.246044]])
    # p3 = np.array([[3.67886, 3.44075, -0.244235]])
    # p4 = np.array([[3.69452, 3.47265,  0.115872]])
    with open(path_input_points, encoding='utf-8') as file:
        i = 1
        p = np.zeros((4,3))
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
            i += 1
    O2 = Calculate_center(p1, p2, p3, p4)
    # print(O2)
    # o2 = Calculate_center_serface(p2-p1, p3-p1, p3-p2, O2)
    # print(o2)
    o2 = Calculate_serface_center(p1, p2 ,p3)
    # print(o2) 

    # d1 = np.sum((o2-p1)*(o2-p1))
    # d2 = np.sum((o2-p2)*(o2-p2))
    # d3 = np.sum((o2-p3)*(o2-p3))
    # print("d1 = ", d1)
    # print("d2 = ", d2)
    # print("d3 = ", d3)

    # v1 = np.sum((o2-p1)*(o2-O2))
    # v2 = np.sum((o2-p2)*(o2-O2))
    # v3 = np.sum((o2-p3)*(o2-O2))
    # print("v1 = ", v1)
    # print("v2 = ", v2)
    # print("v3 = ", v3)

    d = math.sqrt(np.sum((o1-o2)*(o1-o2)))
    print("distance:", d)
    return d

# d = Calculate_distance()
