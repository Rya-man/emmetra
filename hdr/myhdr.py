import cv2 as cv
import numpy as np
# Read images
img1 = cv.imread('image0.jpg')
img2 = cv.imread('image1.jpg')
img3 = cv.imread('image2.jpg')
images = [img1, img2, img3]
# Base exposure time (adjust if needed)
base_time = 1  # in seconds

# Calculate times based on EV values
times = np.array([1/2000, 1/160,30], dtype=np.float32)
# Merge to HDR
# merge_debevec = cv.createMergeDebevec()
# hdr_image = merge_debevec.process(images)


# Tone map to 8-bit image
# tonemap_reinhard = cv.createTonemapReinhard(gamma=2.2)
# ldr_image = tonemap_reinhard.process(hdr_image)





# calibrate = cv.createCalibrateDebevec()
# response = calibrate.process(images, times)
 
 
 
merge_debevec = cv.createMergeDebevec()
hdr = merge_debevec.process(images, times)
 
 
 
tonemap = cv.createTonemap(2.2)
ldr = tonemap.process(hdr)
 
 
 
merge_mertens = cv.createMergeMertens()
fusion = merge_mertens.process(images)

ldr_image_8bit = (ldr * 255).clip(0, 255).astype('uint8')

 
 
 
cv.imwrite('fusion.png', fusion * 255)
cv.imwrite('ldr.png', ldr * 255)
cv.imwrite('hdr.hdr', hdr)
cv.imwrite('tone_mapped.jpg', ldr_image_8bit)