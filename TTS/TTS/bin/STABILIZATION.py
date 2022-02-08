import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_warp(img1, img2, motion = cv2.MOTION_EUCLIDEAN):
    imga = img1.copy().astype(np.float32)
    imgb = img2.copy().astype(np.float32)
    if len(imga.shape) == 3:
        imga = cv2.cvtColor(imga, cv2.COLOR_BGR2GRAY)
    if len(imgb.shape) == 3:
        imgb = cv2.cvtColor(imgb, cv2.COLOR_BGR2GRAY)
    if motion == cv2.MOTION_HOMOGRAPHY:
        warpMatrix=np.eye(3, 3, dtype=np.float32)
    else:
        warpMatrix=np.eye(2, 3, dtype=np.float32)
    warp_matrix = cv2.findTransformECC(templateImage=imga,inputImage=imgb,
                                       warpMatrix=warpMatrix, motionType=motion)[1]
    return warp_matrix 

def create_warp_stack(imgs):
    warp_stack = []
    for i, img in enumerate(imgs[:-1]):
        warp_stack += [get_warp(img, imgs[i+1])]
    return np.array(warp_stack)

def homography_gen(warp_stack):
    H_tot = np.eye(3)
    wsp = np.dstack([warp_stack[:,0,:], warp_stack[:,1,:], np.array([[0,0,1]]*warp_stack.shape[0])])
    for i in range(len(warp_stack)):
        H_tot = np.matmul(wsp[i].T, H_tot)
        yield np.linalg.inv(H_tot)

def apply_warping_fullview(images, warp_stack, PATH=None):
    top, bottom, left, right = get_border_pads(img_shape=images[0].shape, warp_stack=warp_stack)
    H = homography_gen(warp_stack)
    imgs = []
    for i, img in enumerate(images[1:]):
        H_tot = next(H)+np.array([[0,0,left],[0,0,top],[0,0,0]])
        img_warp=cv2.warpPerspective(img,H_tot,(img.shape[1]+left+right,img.shape[0]+top+bottom))
        if not PATH is None:
            filename = PATH + "".join([str(0)]*(3-len(str(i)))) + str(i) +'.png'
            cv2.imwrite(filename, img_warp)
        imgs += [img_warp]
    return imgs

def gauss_convolve(trajectory, window, sigma):
    kernel = signal.gaussian(window, std=sigma)
    kernel = kernel/np.sum(kernel)
    return convolve(trajectory, kernel, mode='reflect')

def moving_average(warp_stack, sigma_mat):
    x,y = warp_stack.shape[1:]
    original_trajectory = np.cumsum(warp_stack, axis=0)
    smoothed_trajectory = np.zeros(original_trajectory.shape)
    for i in range(x):
        for j in range(y):
            kernel = signal.gaussian(10000, sigma_mat[i,j])
            kernel = kernel/np.sum(kernel)
            smoothed_trajectory[:,i,j] = convolve(original_trajectory[:,i,j], kernel, mode='reflect')
    smoothed_warp = np.apply_along_axis(lambda m: 
                     convolve(m, [0,1,-1], mode='reflect'), axis=0, arr=smoothed_trajectory)
    return smoothed_warp, smoothed_trajectory, original_trajectory

def main():
    ws = create_warp_stack(imgs)
    i,j = 0,2
    plt.scatter(np.arange(len(ws)), ws[:,i,j], label='X Velocity')
    plt.plot(np.arange(len(ws)), ws[:,i,j])
    plt.scatter(np.arange(len(ws)), np.cumsum(ws[:,i,j], axis=0), label='X Trajectory')
    plt.plot(np.arange(len(ws)), np.cumsum(ws[:,i,j], axis=0))
    plt.legend()
    plt.xlabel('Frame')

