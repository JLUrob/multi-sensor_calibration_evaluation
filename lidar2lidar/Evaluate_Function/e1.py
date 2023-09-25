import numpy as np 
import math 

#相对与Evaluate.sh脚本的路径
path_target_points = 'View_Cloud/Points/target_points.txt'
path_input_points = 'View_Cloud/Points/input_points.txt'

'''向量叉乘，右手定则'''
def Calculate_Normal_vector(v1, v2):
    a = v1[1]*v2[2] - v2[1]*v1[2]
    b = v1[2]*v2[0] - v2[2]*v1[0]
    c = v1[0]*v2[1] - v2[0]*v1[1]
    normal_v = np.array([a, b, c])
    return normal_v


def Calculate_theta():

    # p1 = np.array([2.189,  -0.063,  0.244])
    # p2 = np.array([2.214,  -0.22,   0.266])
    # p3 = np.array([2.15,   -0.1,    0.081])

    p1 = np.array([0, 0, 0], dtype=float)
    p2 = np.array([0, 0, 0], dtype=float)
    p3 = np.array([0, 0, 0], dtype=float)
    with open(path_target_points, encoding='utf-8') as file:
        i = 1
        p = np.zeros((4,3))
        for line in file:
            data_line = line.strip("\n").split()  # 去除首尾换行符，并按空格划分
            if i == 1:
                p1[0] = float(data_line[0])
                p1[1] = float(data_line[1])
                p1[2] = float(data_line[2])
            if i == 2:
                p2[0] = float(data_line[0])
                p2[1] = float(data_line[1])
                p2[2] = float(data_line[2])
            if i == 3:
                p3[0] = float(data_line[0])
                p3[1] = float(data_line[1])
                p3[2] = float(data_line[2])
            if i >= 4:
                break
            i += 1
    normal_v1 = Calculate_Normal_vector(p1-p2, p1-p3)
    print(normal_v1)

    # p1 = np.array([3.47437,  3.80614,  0.0463515])
    # p2 = np.array([3.56908,  3.61657,  0.0403176])
    # p3 = np.array([3.45252,  3.78759, -0.0959274])
    with open(path_input_points, encoding='utf-8') as file:
        i = 1
        p = np.zeros((4,3))
        for line in file:
            data_line = line.strip("\n").split()  # 去除首尾换行符，并按空格划分
            # print(data_line)
            if i == 1:
                p1[0] = float(data_line[0])
                p1[1] = float(data_line[1])
                p1[2] = float(data_line[2])
            if i == 2:
                p2[0] = float(data_line[0])
                p2[1] = float(data_line[1])
                p2[2] = float(data_line[2])
            if i == 3:
                p3[0] = float(data_line[0])
                p3[1] = float(data_line[1])
                p3[2] = float(data_line[2])
            if i >= 4:
                break
            i += 1
    normal_v2 = Calculate_Normal_vector(p1-p2, p1-p3)
    print(normal_v2)

    theta = np.degrees(np.arccos(np.dot(normal_v1, normal_v2)/(np.linalg.norm(normal_v1)*np.linalg.norm(normal_v2))))
    print("θ:",theta,"°")
    return theta

# theta = Calculate_theta()

    

    


