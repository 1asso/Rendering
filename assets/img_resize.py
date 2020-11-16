import numpy as np
import cv2
import os

bg_dir = 'bg/'
files = os.listdir(bg_dir)

for f in files:
	path = os.path.join(bg_dir, f)
	if not os.path.splitext(path)[1] == '.png':
		continue
	img = cv2.imread(path)
	print(f)
	if len(img) > 1024:
		img_resized = img[100:1124, 100:1124]
		cv2.imwrite(path, img_resized)
	
