import sys
sys.path.append("/Users/Ryan/Documents/Research/mitsuba2/build/dist/python")
from xml.etree import ElementTree as et

import numpy as np
import cv2
import mitsuba
mitsuba.set_variant('scalar_rgb')
from mitsuba.core import Thread, xml, Struct, Bitmap
from mitsuba.core.xml import load_file
import mitsuba.python.autodiff as autodiff
from shutil import copyfile
from flow_gen.flow_gen import run as f_run
import os

dataset_output_dir = 'dataset/'
graycode_dir = 'flow_gen/graycode_1024_1024/'
output_dir = 'flow_gen/test_1024/'

Thread.thread().file_resolver().append(".")

def run(prefix):
	img= cv2.imread(dataset_output_dir + prefix + 'mask_2x.png')
	img_i = cv2.bitwise_not(img)
	cv2.imwrite(output_dir + 'graycode_01.png', img_i)
	
	copyfile(dataset_output_dir + prefix + 'rho_2x.png', output_dir + 'graycode_02.png')
	
	tree = et.parse('img_gen.xml')
	root = tree.getroot()
	for i in range(1, 21):
			
		r = root.find('shape/emitter/texture/string')
		r.set('value', graycode_dir + 'graycode_'+ str(i) +'.png')
		r = root.findall('sensor/film/integer')
		[rr.set('value', '1024') for rr in r]
		tree.write('img_gen.xml')
		
		
		scene = load_file("img_gen.xml")
		sensor = scene.sensors()[0]
		scene.integrator().render(scene, sensor)
		film = sensor.film()
		
		result = film.bitmap(raw=False)
		result = np.array(result, copy=False).astype(np.float)
		image = np.stack([result[:, :, 2], result[:, :, 1], result[:, :, 0]], axis=-1)
		image = np.array(Bitmap(image, Bitmap.PixelFormat.RGB).convert(Bitmap.PixelFormat.RGB, Struct.Type.UInt8, srgb_gamma=True))
		
		#cv2.imshow("image", image)
		cv2.imwrite(output_dir + 'graycode_'+ str(f'{i+2:02d}') +'.png',image)
		cv2.waitKey()
	
	f_run()
	
	copyfile('flow_gen/flow/flow.flo', dataset_output_dir + prefix + 'flow_2x.flo')
	copyfile('flow_gen/flow/flow.png', dataset_output_dir + prefix + 'flow_2x.png')