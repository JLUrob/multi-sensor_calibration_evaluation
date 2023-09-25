import os
import glob
import cv2
from calibrate_helper import Calibrator
import numpy as np
import math

#Camera_1: 方差变大的index:5,21,25  不可检测的图片index：15,16 


def main(rel_index):

    #v1去畸之前的方差，v2去畸之后的方差
    v1 = 0
    v2 = 0

    # 论文中使用的是可视化样例fig7
    index = rel_index

    # shape_inner_corner = (8,11)
    # w, h = shape_inner_corner
    # img_dir = "./pic/IR_camera_calib_img"
    # img_dir = "./pic/IR_dedistortion"
    shape_inner_corner = (6,7)
    w, h = shape_inner_corner
    # img_dir = "./pic/My_img"
    img_dir = "./pic/Cameras/Camera_1/img"
    img_paths = []
    points_pixel = []
    col_len = []
    row_len = []
    for extension in ["jpg", "png", "jpeg"]:
        img_paths += glob.glob(os.path.join(img_dir, "*.{}".format(extension)))
    # assert len(img_paths), "No images for calibration found!"
    img = cv2.imread(img_paths[index])
    cv2.imshow("img",img)
    cv2.waitKey(10)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("img",img)
    # cv2.waitKey(1000)
        # find the corners, cp_img: corner points in pixel space
    # ret, cp_img = cv2.findChessboardCorners(gray_img, (w, h), None)
    ret, cp_img = cv2.findChessboardCorners(gray_img, (w, h), flags=cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_EXHAUSTIVE)
        # if ret is True, save
    if ret:
        # cv2.cornerSubPix(gray_img, cp_img, (11,11), (-1,-1), criteria)
        points_pixel.append(cp_img)
        # view the corners
        cv2.drawChessboardCorners(img, (w, h), cp_img, ret)
        cv2.imshow('FoundCorners', img)
        cv2.waitKey(10)
    f_point = [0, 0]
    s_point = [0, 0]
    count = 0
    for i in range(w):
        for j in range(h):
            idx = j*6 + i
            if j == 0:
                f_point[0] = points_pixel[0][idx][0][0]
                f_point[1] = points_pixel[0][idx][0][1]
                continue
            s_point[0] = points_pixel[0][idx][0][0]
            s_point[1] = points_pixel[0][idx][0][1]
            tmp_len = math.sqrt((f_point[0]-s_point[0])*(f_point[0]-s_point[0])+(f_point[1]-s_point[1])*(f_point[1]-s_point[1]))
            row_len.append(tmp_len)
            f_point[0] = s_point[0]
            f_point[1] = s_point[1]
            count += 1
    
    f_point = [0, 0]
    s_point = [0, 0]
    for i in range(w*h):
        if (i+1)%w == 1:
            f_point[0] = points_pixel[0][i][0][0]
            f_point[1] = points_pixel[0][i][0][1]
            continue
        s_point[0] = points_pixel[0][i][0][0]
        s_point[1] = points_pixel[0][i][0][1]
        tmp_len = math.sqrt((f_point[0]-s_point[0])*(f_point[0]-s_point[0])+(f_point[1]-s_point[1])*(f_point[1]-s_point[1]))
        col_len.append(tmp_len)
        f_point[0] = s_point[0]
        f_point[1] = s_point[1]

    print(len(row_len))
    print(len(col_len))

    e_row = 0
    for i in range(len(row_len)):
        e_row += row_len[i]
    e_row /= len(row_len)

    e_col = 0
    for i in range(len(col_len)):
        e_col += col_len[i]
    e_col /= len(col_len)

    v_row = 0
    for i in range(len(row_len)):
        v_row += (row_len[i]-e_row)*(row_len[i]-e_row)
    v_row /= len(row_len)

    v_col = 0
    for i in range(len(col_len)):
        v_col += (col_len[i]-e_col)*(col_len[i]-e_col)
    v_col /= len(col_len)

    print('e:', e_row)
    print('v:', v_row)
    print('e:', e_col)
    print('v:', v_col)

    v1 = (v_row + v_col) / 2

    # img_dir = "./pic/IR_camera_calib_img"
    # img_dir = "./pic/IR_dedistortion"
    # img_dir = "./pic/My_img_dedistortion"
    img_dir = "./pic/Cameras/Camera_1/img_dist"
    img_paths = []
    points_pixel = []
    row_len = []
    col_len = []
    for extension in ["jpg", "png", "jpeg"]:
        img_paths += glob.glob(os.path.join(img_dir, "*.{}".format(extension)))
    img = cv2.imread(img_paths[index])
    cv2.imshow("img",img)
    cv2.waitKey(10)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("img",img)
    # cv2.waitKey(0)
        # find the corners, cp_img: corner points in pixel space
    # ret, cp_img = cv2.findChessboardCorners(gray_img, (w, h), None)
    ret, cp_img = cv2.findChessboardCorners(gray_img, (w, h), flags=cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_EXHAUSTIVE)
        # if ret is True, save
    if ret:
        # cv2.cornerSubPix(gray_img, cp_img, (11,11), (-1,-1), criteria)
        points_pixel.append(cp_img)
        # view the corners
        cv2.drawChessboardCorners(img, (w, h), cp_img, ret)
        cv2.imshow('FoundCorners', img)
        cv2.waitKey(10)


    f_point = [0, 0]
    s_point = [0, 0]
    count = 0
    for i in range(w):
        for j in range(h):
            idx = j*6 + i
            if j == 0:
                f_point[0] = points_pixel[0][idx][0][0]
                f_point[1] = points_pixel[0][idx][0][1]
                continue
            s_point[0] = points_pixel[0][idx][0][0]
            s_point[1] = points_pixel[0][idx][0][1]
            tmp_len = math.sqrt((f_point[0]-s_point[0])*(f_point[0]-s_point[0])+(f_point[1]-s_point[1])*(f_point[1]-s_point[1]))
            row_len.append(tmp_len)
            f_point[0] = s_point[0]
            f_point[1] = s_point[1]
            count += 1
    
    f_point = [0, 0]
    s_point = [0, 0]
    for i in range(w*h):
        if (i+1)%w == 1:
            f_point[0] = points_pixel[0][i][0][0]
            f_point[1] = points_pixel[0][i][0][1]
            continue
        s_point[0] = points_pixel[0][i][0][0]
        s_point[1] = points_pixel[0][i][0][1]
        tmp_len = math.sqrt((f_point[0]-s_point[0])*(f_point[0]-s_point[0])+(f_point[1]-s_point[1])*(f_point[1]-s_point[1]))
        col_len.append(tmp_len)
        f_point[0] = s_point[0]
        f_point[1] = s_point[1]

    print(len(row_len))
    print(len(col_len))

    e_row = 0
    for i in range(len(row_len)):
        e_row += row_len[i]
    e_row /= len(row_len)

    e_col = 0
    for i in range(len(col_len)):
        e_col += col_len[i]
    e_col /= len(col_len)

    v_row = 0
    for i in range(len(row_len)):
        v_row += (row_len[i]-e_row)*(row_len[i]-e_row)
    v_row /= len(row_len)

    v_col = 0
    for i in range(len(col_len)):
        v_col += (col_len[i]-e_col)*(col_len[i]-e_col)
    v_col /= len(col_len)

    print('e:', e_row)
    print('v:', v_row)
    print('e:', e_col)
    print('v:', v_col)

    v2 = (v_row + v_col) / 2

    return (v1, v2)
    


if __name__ == '__main__':
    v1 = np.zeros((28, 1))
    v2 = np.zeros((28, 1))
    num = 0
    for i in range(30):
        if i == 15 or i == 16:
            continue
        (v11, v22) = main(i)
        v1[num][0] = v11
        v2[num][0] = v22
        num += 1
    print(v1)
    print(v2)

    #路径相对于evaluate_dist.sh
    np.savetxt(f"../results/camera_dist/datasets1/pre_dist_row_col.txt", v1)
    np.savetxt(f"../results/camera_dist/datasets1/removed_dist_row_col.txt", v2)
        
