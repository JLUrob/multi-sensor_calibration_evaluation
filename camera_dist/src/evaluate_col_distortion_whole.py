import os
import glob
import cv2
from calibrate_helper import Calibrator
import numpy as np
import math

#Camera_1: 方差变大的index:5,19,21,25  不可检测的图片index：15,16 

def main(rel_index):
    #v1去畸之前的方差，v2去畸之后的方差
    sub_l = 0

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
    for i in range(w*h):
        if (i+1)%w == 1:
            f_point[0] = points_pixel[0][i][0][0]
            f_point[1] = points_pixel[0][i][0][1]
            continue
        s_point[0] = points_pixel[0][i][0][0]
        s_point[1] = points_pixel[0][i][0][1]
        t_len = math.sqrt((f_point[0]-s_point[0])*(f_point[0]-s_point[0])+(f_point[1]-s_point[1])*(f_point[1]-s_point[1]))
        col_len.append(t_len)
        f_point[0] = s_point[0]
        f_point[1] = s_point[1]
    print(len(col_len))

    all_col_len = []
    ii = 0
    for i in range(h):
        tmp_len = 0
        for j in range(w - 1):
            tmp_len = tmp_len + col_len[ii]
            ii += 1
        all_col_len.append(tmp_len)
    print(len(all_col_len))
    print(all_col_len)


    # img_dir = "./pic/IR_camera_calib_img"
    # img_dir = "./pic/IR_dedistortion"
    # img_dir = "./pic/My_img_dedistortion"
    img_dir = "./pic/Cameras/Camera_1/img_dist"
    img_paths = []
    points_pixel = []
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
    undist_all_col_len = []
    f_point = [0, 0]
    s_point = [0, 0]
    for i in range(h):
        idx1 = i*w
        idx2 = (i+1)*w-1
        print(idx1)
        print(idx2)
        f_point[0] = points_pixel[0][idx1][0][0]
        f_point[1] = points_pixel[0][idx1][0][1]
        s_point[0] = points_pixel[0][idx2][0][0]
        s_point[1] = points_pixel[0][idx2][0][1]
        t_len = math.sqrt((f_point[0]-s_point[0])*(f_point[0]-s_point[0])+(f_point[1]-s_point[1])*(f_point[1]-s_point[1]))
        undist_all_col_len.append(t_len)
    print(len(undist_all_col_len))
    print(undist_all_col_len)
    for i in range(h):
        sub_l = sub_l + abs(all_col_len[i] - undist_all_col_len[i])

    return sub_l
    


if __name__ == '__main__':
    sub_l = np.zeros((28, 1))
    num = 0
    for i in range(30):
        if i == 15 or i == 16:
            continue
        tmp = main(i)
        sub_l[num][0] = tmp
        num += 1
    print(sub_l)

    #路径相对于evaluate_dist.sh
    np.savetxt(f"../results/camera_dist/datasets1/sub_col.txt", sub_l)
