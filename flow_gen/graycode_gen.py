import numpy
import cv2

arr = numpy.ones((1024,1024,1),numpy.uint8)

for i in range(1, 11):
	splits = 2 ** i
	length = int(1024 / splits)
	for j in range(splits):
#		arr[j*length: j*length+length, :] = j % 2
		arr[ : , j*length: j*length+length] = j % 2
		
	img = arr*255
	cv2.imwrite('graycode_1024_1024/graycode_'+ str(i+10) +'.png',img)
	cv2.waitKey(0)