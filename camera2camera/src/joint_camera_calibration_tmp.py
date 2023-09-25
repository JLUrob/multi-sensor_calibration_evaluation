import numpy as np
import cv2
import glob
import math

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# size of borad
# board_size = (7, 6)
board_size = (12, 8)
# board_size = (8, 6)
h, w = board_size
numer_of_conners = h*w

# camera1_calibration_images_path = 'calib_images/checkerboard/*.jpg'
# camera1_calibration_images_path = 'calib_images/test_images/*.jpg'
# camera1_calibration_images_path = 'datasets_1/camera1/*.jpg'
# camera1_calibration_images_path = 'datasets_2/camera1/*.jpg'
camera1_calibration_images_path = 'datasets_3/camera1/*.jpg'



# camera2_calibration_images_path = 'calib_images/checkerboard/*.jpg'
# camera2_calibration_images_path = 'calib_images/test_images/*.jpg'
# camera2_calibration_images_path = 'datasets_1/camera2/*.jpg'
# camera2_calibration_images_path = 'datasets_2/camera2/*.jpg'
camera2_calibration_images_path = 'datasets_3/camera2/*.jpg'

# the image path of reprojecting to camera1 pixel coordinate axis
# reproject_img_path = 'calib_images/checkerboard/left03.jpg'
# reproject_img_path = 'calib_images/test_images/01.jpg'

# reproject_img_path = 'datasets_1/camera1/10.jpg' #  image of camera1 is the same time captured as camera2
# camera2_img_path = 'datasets_1/camera2/10.jpg' #  image of camera2 is the same time captured as camera1 

# reproject_img_path = 'datasets_2/camera1/09.jpg' #  image of camera1 is the same time captured as camera2
# camera2_img_path = 'datasets_2/camera2/09.jpg' #  image of camera2 is the same time captured as camera1

reproject_img_path = 'datasets_3/camera1/10.jpg' #  image of camera1 is the same time captured as camera2
camera2_img_path = 'datasets_3/camera2/10.jpg' #  image of camera2 is the same time captured as camera1 

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ...,(6,5,0)...
objp = np.zeros((numer_of_conners,3), np.float32)
objp[:,:2] = np.mgrid[0:h,0:w].T.reshape(-1,2)


# Arrays to store object points and image points from all the images.
objpoints1 = [] # Camera1 3d point in real world space
imgpoints1 = [] # Camera1 2d points in image plane.
objpoints2 = [] # Camera2 3d point in real world space
imgpoints2 = [] # Camera2 2d points in image plane.


# Camera1 calibration
images1 = glob.glob(camera1_calibration_images_path)
print(images1)
# print(len(images1))
for fname in images1:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (h,w),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints1.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints1.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (h,w), corners2,ret)
        cv2.imshow("img",img)
        cv2.waitKey(0)


ret1, mtx1, dist1, rvecs1, tvecs1 = cv2.calibrateCamera(objpoints1, imgpoints1, gray.shape[::-1],None,None)


# Camera2 calibration
images2 = glob.glob(camera2_calibration_images_path)
print(images2)
for fname in images2:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (h,w),None)

    # If found, add object points, image points (after refining them)
    if ret == True:

        objpoints2.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints2.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (h,w), corners2,ret)
        cv2.imshow("img",img)
        cv2.waitKey(10)
        
ret2, mtx2, dist2, rvecs2, tvecs2 = cv2.calibrateCamera(objpoints2, imgpoints2, gray.shape[::-1],None,None)
# print(rvecs2)
# print(tvecs2)


# camera2 board world points
camera2_objp = objp
# index1 index2,  the order of images of camera calibration 
# for example :
# 0 = 'calib_images/checkerboard/left02.jpg'
# 1 = 'calib_images/checkerboard/left04.jpg' 
# 2 = 'calib_images/checkerboard/left01.jpg' 
# 3 = 'calib_images/checkerboard/left03.jpg' 
# 4 = 'calib_images/checkerboard/left05.jpg'

index1 = -1 # seek camera1 image's order in images1
index2 = -1 # seek camera2 image's order in images2, and camera2 image is the same time captured as camera1 image

# seek the index of index1 of images1
for i in range(len(images1)):
    if images1[i] == reproject_img_path:
        index1 = i
        break
print("index1:", index1)
# seek the index of index2 of images2
for i in range(len(images2)):
    if images2[i] == camera2_img_path:
        index2 = i
        break
print("index2:", index2)

#get camera2_to_board R
camera2_R ,_ = cv2.Rodrigues(rvecs2[index2])
#world points reject to camera2 corrdinate axis
camera2_camera_coordinate_points = camera2_R.dot(camera2_objp.T) + tvecs2[index2]
camera2_camera_coordinate_points = camera2_camera_coordinate_points.T
# print(camera2_R.shape)
# print(camera2_objp.shape)
# print(camera2_camera_coordinate_points)

# Function to draw the axis
# Draw axis function can also be used.
def drawline(img, corners, imgpts):
    corner = tuple(corners[1].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255, 0, 0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0, 255, 0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0, 0, 255), 5)
    return img
def drawpoints(img, corners, imgpts):
    imgpts = imgpts.astype(np.int)
    corners = corners.astype(np.int)
    for i in range(numer_of_conners):
        img = cv2.circle(img, imgpts[i].ravel(), 2, (255, 255, 0), 2) # camera2
        img = cv2.circle(img, corners[i].ravel(), 1, (0, 0, 255), 2) # camera1
    return img

# axis = np.float32([[3,0,0], [1,3,0], [0,0,-3]]).reshape(-1,3)
# axis = np.float32([[2,0,0], [1,1,0], [1,0,-1]]).reshape(-1,3)
axis = objp
#axis1:camera1 world points
axis1 = axis.T
#axis2:camera2 corrdinate axis points
axis2 = camera2_R.dot(axis.T) + tvecs2[index2]

camera2_to_camera1_R = np.zeros((3,3))
rvecs = np.zeros((3,1))
tvecs = np.zeros((3,1))


# calibrate camera1 and camera2
for fname in glob.glob(reproject_img_path):

    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (h,w),None)

    if ret == True:
        corners_pnp = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
        # global camera2_to_camera1_R
        # global rvecs
        # global tvecs
        # Find the rotation and translation vectors.
        _, rvecs, tvecs, inliers = cv2.solvePnPRansac(camera2_camera_coordinate_points, corners_pnp, mtx1, dist1)
        # get R of camera2 to camera1
        camera2_to_camera1_R ,_ = cv2.Rodrigues(rvecs)
        print("R:")
        print(camera2_to_camera1_R)
        print("T")
        print(tvecs)

        # print(camera2_to_camera1_R)
        # project 3D points to image plane
        # imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx1, dist1)

        # project to camera1 corrdinate axis
        imgpts, jac = cv2.projectPoints(camera2_camera_coordinate_points, rvecs, tvecs, mtx1, dist1)
        # imgpts.astype(int)
        print("board_to_camera1 pixel coordiante axis points :")
        print(corners_pnp)
        print("camera2_to_camera1 pixel coordiante axis points :")
        print(imgpts)
        # int_imgpts = imgpts.astype(np.int)
        # print(int_imgpts)
        # print(int_imgpts.shape)
        # print(corners_pnp)
        # print(corners_pnp.shape)
        # print(corners_pnp[0][0])
        reproject_error = 0
        for i in range(corners_pnp.shape[0]):
            reproject_error = reproject_error + math.sqrt(np.sum((corners_pnp[i][0]-imgpts[i][0])*(corners_pnp[i][0]-imgpts[i][0])))

        # calculate the points of camera1 corrdinate axis
        camera1_R ,_ = cv2.Rodrigues(rvecs1[index1])
        camera1_camera_coordinate_points = camera1_R.dot(axis1) + tvecs1[index1]
        camera2_to_camera1_coordinate_points = camera2_to_camera1_R.dot(axis2) + tvecs

        camera1_camera_coordinate_points_standard = camera1_camera_coordinate_points.T
        camera2_to_camera1_coordinate_points_standard = camera2_to_camera1_coordinate_points.T

        print("No standard camera coordinate :")
        print("board to camera1 coordinate axis points")
        print(camera1_camera_coordinate_points.T)
        print("board to camera2 to camera1 coordinate axis points")
        print(camera2_to_camera1_coordinate_points.T)

        # error of theta and error of sub
        error_theta = np.zeros((numer_of_conners,1),dtype=np.float64)
        error_distance = np.zeros((numer_of_conners,1))
        error_sub = 0
        
        # standardization
        for i in range(numer_of_conners):
            camera1_camera_coordinate_points_standard[i][0] = camera1_camera_coordinate_points_standard[i][0] / camera1_camera_coordinate_points_standard[i][2]
            camera1_camera_coordinate_points_standard[i][1] = camera1_camera_coordinate_points_standard[i][1] / camera1_camera_coordinate_points_standard[i][2]
            camera1_camera_coordinate_points_standard[i][2] = 1
            camera2_to_camera1_coordinate_points_standard[i][0] = camera2_to_camera1_coordinate_points_standard[i][0] / camera2_to_camera1_coordinate_points_standard[i][2]
            camera2_to_camera1_coordinate_points_standard[i][1] = camera2_to_camera1_coordinate_points_standard[i][1] / camera2_to_camera1_coordinate_points_standard[i][2]
            camera2_to_camera1_coordinate_points_standard[i][2] = 1
            error_sub = error_sub + max(camera1_camera_coordinate_points_standard[i][0]/camera2_to_camera1_coordinate_points_standard[i][0], camera2_to_camera1_coordinate_points_standard[i][0]/camera1_camera_coordinate_points_standard[i][0])
            error_sub = error_sub + max(camera1_camera_coordinate_points_standard[i][1]/camera2_to_camera1_coordinate_points_standard[i][1], camera2_to_camera1_coordinate_points_standard[i][1]/camera1_camera_coordinate_points_standard[i][1])

        print("Standard camera corrdinate :")
        print("board to camera1 pixel coordinate axis points")
        print(camera1_camera_coordinate_points_standard)
        print("board to camera2 to camera1 pixel coordinate axis points")
        print(camera2_to_camera1_coordinate_points_standard)

        # calculate the  error of theta
        for i in range(numer_of_conners):
            a = np.array([camera1_camera_coordinate_points_standard[i][0], camera1_camera_coordinate_points_standard[i][1]], dtype=float)
            b = np.array([camera2_to_camera1_coordinate_points_standard[i][0], camera2_to_camera1_coordinate_points_standard[i][1]], dtype=float)
            cos_ = np.dot(a,b)/a.dot(b.T)
            sin_ = np.cross(a,b)/a.dot(b.T)
            arctan2_ = np.arctan2(sin_, cos_)
            error_theta[i][0] = abs(arctan2_*180/np.pi)

        print("reproject_error:")
        print(reproject_error/numer_of_conners)
        print("error_theta:")
        print(error_theta)
        print("error_sub:")
        print(error_sub/numer_of_conners)

        img = drawpoints(img, corners_pnp, imgpts)
        cv2.imshow("img", img)
        cv2.waitKey(10)

picture_reproject = np.zeros((len(images1), 1))
picture_theta = np.zeros((len(images1), 1))
picture_distance = np.zeros((len(images1), 1))
picture_sub = np.zeros((len(images1), 1))


for index in range(len(images1)):
    img = cv2.imread(images1[index])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (h,w),None)
    if ret == True:
        corners_pnp = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
        camera2_R ,_ = cv2.Rodrigues(rvecs2[index])
        print(camera2_R)
        # world points reject to camera2 corrdinate axis
        tmp_camera2_camera_coordinate_points = camera2_R.dot(objp.T) + tvecs2[index]
        tmp_camera2_camera_coordinate_points = tmp_camera2_camera_coordinate_points.T
        tmp_imgpts, jac = cv2.projectPoints(tmp_camera2_camera_coordinate_points, rvecs, tvecs, mtx1, dist1)

        # calculate the points of camera1 corrdinate axis
        camera1_R ,_ = cv2.Rodrigues(rvecs1[index])
        tmp_camera1_camera_coordinate_points = camera1_R.dot(objp.T) + tvecs1[index]
        tmp_camera2_to_camera1_coordinate_points = camera2_to_camera1_R.dot(tmp_camera2_camera_coordinate_points.T) + tvecs
        tmp_camera1_camera_coordinate_points_standard = tmp_camera1_camera_coordinate_points.T
        tmp_camera2_to_camera1_coordinate_points_standard = tmp_camera2_to_camera1_coordinate_points.T
        
        # print(tmp_camera2_camera_coordinate_points.shape)
        # print(tmp_imgpts)

        reproject_error = 0
        error_conner_pixel = np.zeros((numer_of_conners, 1))
        for i in range(corners_pnp.shape[0]):
            reproject_error = reproject_error + math.sqrt(np.sum((corners_pnp[i][0]-tmp_imgpts[i][0])*(corners_pnp[i][0]-tmp_imgpts[i][0])))
            error_conner_pixel[i][0] = math.sqrt(np.sum((corners_pnp[i][0]-tmp_imgpts[i][0])*(corners_pnp[i][0]-tmp_imgpts[i][0])))
            
        
        # print("No standard camera coordinate :")
        # print("board to camera1 coordinate axis points")
        # print(tmp_camera1_camera_coordinate_points.T)
        # print("board to camera2 to camera1 coordinate axis points")
        # print(tmp_camera2_to_camera1_coordinate_points.T)

        # error of theta and error of sub
        error_theta = np.zeros((numer_of_conners,1),dtype=np.float64)
        error_sub = 0
        
        # standardization
        # for i in range(numer_of_conners):
        #     tmp_camera1_camera_coordinate_points_standard[i][0] = tmp_camera1_camera_coordinate_points_standard[i][0] / tmp_camera1_camera_coordinate_points_standard[i][2]
        #     tmp_camera1_camera_coordinate_points_standard[i][1] = tmp_camera1_camera_coordinate_points_standard[i][1] / tmp_camera1_camera_coordinate_points_standard[i][2]
        #     tmp_camera1_camera_coordinate_points_standard[i][2] = 1
        #     tmp_camera2_to_camera1_coordinate_points_standard[i][0] = tmp_camera2_to_camera1_coordinate_points_standard[i][0] / tmp_camera2_to_camera1_coordinate_points_standard[i][2]
        #     tmp_camera2_to_camera1_coordinate_points_standard[i][1] = tmp_camera2_to_camera1_coordinate_points_standard[i][1] / tmp_camera2_to_camera1_coordinate_points_standard[i][2]
        #     tmp_camera2_to_camera1_coordinate_points_standard[i][2] = 1
        #     error_sub = error_sub + max(tmp_camera1_camera_coordinate_points_standard[i][0]/tmp_camera2_to_camera1_coordinate_points_standard[i][0], tmp_camera2_to_camera1_coordinate_points_standard[i][0]/tmp_camera1_camera_coordinate_points_standard[i][0])
        #     error_sub = error_sub + max(tmp_camera1_camera_coordinate_points_standard[i][1]/tmp_camera2_to_camera1_coordinate_points_standard[i][1], tmp_camera2_to_camera1_coordinate_points_standard[i][1]/tmp_camera1_camera_coordinate_points_standard[i][1])

        # print("Standard camera corrdinate :")
        # print("board to camera1 pixel coordinate axis points")
        # print(camera1_camera_coordinate_points_standard)
        # print("board to camera2 to camera1 pixel coordinate axis points")
        # print(camera2_to_camera1_coordinate_points_standard)

        # calculate the  error of theta
        sum_theta = 0.0
        for i in range(numer_of_conners):
            a = np.array([tmp_camera1_camera_coordinate_points_standard[i][0], tmp_camera1_camera_coordinate_points_standard[i][1], tmp_camera1_camera_coordinate_points_standard[i][2]],dtype=np.float64)
            b = np.array([tmp_camera2_to_camera1_coordinate_points_standard[i][0], tmp_camera2_to_camera1_coordinate_points_standard[i][1], tmp_camera2_to_camera1_coordinate_points_standard[i][2]],dtype=np.float64)
            if (index+1) is 6:
                print("a:\n", a)
                print("b:\n", b)
            cos_ = a.dot(b)/(np.sqrt(a.dot(a))*np.sqrt(b.dot(b)))

            #remove float error! for example cos_ = 1.000000000002
            cos_ = min(1, cos_)

            arccos_ = np.arccos(cos_)
            if (index+1) is 6:
                print(cos_)
                print(arccos_)
            # cos_ = np.dot(a,b)/a.dot(b.T)
            # sin_ = np.cross(a,b)/a.dot(b.T)
            # arctan2_ = np.arctan2(sin_, cos_)
            error_theta[i][0] = abs(arccos_*180/np.pi)
            sum_theta = sum_theta + error_theta[i]
        

        sum_distance = 0.0
        for i in range(numer_of_conners):
            a = np.array([tmp_camera1_camera_coordinate_points_standard[i][0], tmp_camera1_camera_coordinate_points_standard[i][1], tmp_camera1_camera_coordinate_points_standard[i][2]], dtype=float)
            b = np.array([tmp_camera2_to_camera1_coordinate_points_standard[i][0], tmp_camera2_to_camera1_coordinate_points_standard[i][1], tmp_camera2_to_camera1_coordinate_points_standard[i][2]], dtype=float)
            error_distance[i][0] = np.sqrt(np.sum((a-b)*(a-b)))
            sum_distance = sum_distance + error_distance[i]
        
        # print(images1[index])
        # print(images2[index])
        # print("reproject_error:")
        # print(reproject_error/numer_of_conners)
        # print("error_theta:")
        # print(error_theta)
        # print("average_theta_error:")
        # print(sum_theta/numer_of_conners)
        # print("error_distance_error:")
        # print(sum_distance/numer_of_conners)

        # print("error_sub_error:")
        # print(error_sub/numer_of_conners)

        # the first line is mean of reproject_error
        # the second line is mean of theta_error
        # the third lind  is mean of sub_error
        results = np.array([[reproject_error/numer_of_conners],[sum_theta/numer_of_conners],[sum_distance/numer_of_conners], [error_sub/numer_of_conners]])

        img = drawpoints(img, corners_pnp, tmp_imgpts)
        picture_reproject[index] = reproject_error/numer_of_conners
        picture_theta[index] = sum_theta/numer_of_conners
        picture_distance[index] = sum_distance/numer_of_conners
        picture_sub[index] = error_sub/numer_of_conners
        # np.savetxt(f"../results/camera2camera/datasets1/jpg_{index+1}/reproject_error.txt", results)
        # np.savetxt(f"../results/camera2camera/datasets1/jpg_{index+1}/error_theta.txt", error_theta)
        # np.savetxt(f"../results/camera2camera/datasets1/jpg_{index+1}/error_distance.txt", error_distance)
        # np.savetxt(f"../results/camera2camera/datasets1/jpg_{index+1}/error_conner_pixel.txt", error_conner_pixel)
        # cv2.imwrite(f"../results/camera2camera/datasets1/jpg_{index+1}/{index+1}.jpg",img)

        # np.savetxt(f"../results/camera2camera/datasets2/jpg_{index+1}/reproject_error.txt", results)
        # np.savetxt(f"../results/camera2camera/datasets2/jpg_{index+1}/error_theta.txt", error_theta)
        # np.savetxt(f"../results/camera2camera/datasets2/jpg_{index+1}/error_distance.txt", error_distance)
        # np.savetxt(f"../results/camera2camera/datasets2/jpg_{index+1}/error_conner_pixel.txt", error_conner_pixel)
        # cv2.imwrite(f"../results/camera2camera/datasets2/jpg_{index+1}/{index+1}.jpg",img)

        np.savetxt(f"../results/camera2camera/datasets3/jpg_{index+1}/reproject_error.txt", results)
        np.savetxt(f"../results/camera2camera/datasets3/jpg_{index+1}/error_theta.txt", error_theta)
        np.savetxt(f"../results/camera2camera/datasets3/jpg_{index+1}/error_distance.txt", error_distance)
        np.savetxt(f"../results/camera2camera/datasets3/jpg_{index+1}/error_conner_pixel.txt", error_conner_pixel)
        cv2.imwrite(f"../results/camera2camera/datasets3/jpg_{index+1}/{index+1}.jpg",img)


        cv2.imshow("img", img)
        cv2.waitKey(10)

# np.savetxt("../results/camera2camera/datasets1/reproject.txt", picture_reproject)
# np.savetxt("../results/camera2camera/datasets1/theta.txt", picture_theta) 
# np.savetxt("../results/camera2camera/datasets1/distance.txt", picture_distance)
# np.savetxt("../results/camera2camera/datasets1/sub.txt", picture_sub)

# np.savetxt("../results/camera2camera/datasets2/reproject.txt", picture_reproject)
# np.savetxt("../results/camera2camera/datasets2/theta.txt", picture_theta)
# np.savetxt("../results/camera2camera/datasets2/distance.txt", picture_distance)
# np.savetxt("../results/camera2camera/datasets2/sub.txt", picture_sub)

np.savetxt("../results/camera2camera/datasets3/reproject.txt", picture_reproject)
np.savetxt("../results/camera2camera/datasets3/theta.txt", picture_theta)
np.savetxt("../results/camera2camera/datasets3/distance.txt", picture_distance)
np.savetxt("../results/camera2camera/datasets3/sub.txt", picture_sub)

        

cv2.destroyAllWindows()
print(images1)
print(images2)
