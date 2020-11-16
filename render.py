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
import os
from render_flow import run as rf_run
import random

bg_dir = 'assets/bg/'
bg_files = os.listdir(bg_dir)

obj_dir = 'assets/obj/'
obj_files = os.listdir(obj_dir)

rect_obj = 'assets/rectangle.obj'

dataset_output_dir = 'dataset/'

Thread.thread().file_resolver().append(".")

t_img = et.parse('img_gen.xml')
r_img = t_img.getroot()
t_mask = et.parse('mask_gen.xml')
r_mask = t_mask.getroot()
t_rho = et.parse('rho_gen.xml')
r_rho = t_rho.getroot()


obj_node = et.fromstring('''
<shape type="obj">
	<string name="filename" value="assets/obj/glass2.obj" />
		<bsdf type="dielectric">
				<float name="int_ior" value="1.504" />
				<float name="ext_ior" value="1.0" />
		</bsdf>
		<transform name="to_world">
			<translate value="4, -0.4, 0" />
			<scale value="0.02" />
			<rotate angle="30.0" z="1.0" />
	</transform>
</shape>
''')

def run_rendering(xml, save_name):
	scene = load_file(xml)
	sensor = scene.sensors()[0]
	scene.integrator().render(scene, sensor)
	film = sensor.film()
	
	result = film.bitmap(raw=False)
	result = np.array(result, copy=False).astype(np.float)
	image = np.stack([result[:, :, 2], result[:, :, 1], result[:, :, 0]], axis=-1)
	image = np.array(Bitmap(image, Bitmap.PixelFormat.RGB).convert(Bitmap.PixelFormat.RGB, Struct.Type.UInt8, srgb_gamma=True))
	
	cv2.imwrite(dataset_output_dir + save_name, image)
	cv2.waitKey()
	
	
if __name__ == '__main__':
	count = 0
		
	for obj in obj_files:
		obj_path = os.path.join(obj_dir, obj)
		if not os.path.splitext(obj_path)[1] == '.obj':
			continue
		
		while True:
			bg = random.choice(bg_files)
			bg_path = os.path.join(bg_dir, bg)
			if os.path.splitext(bg_path)[1] == '.png':
				break
		
		count += 1
		
		prefix = str(f'{count:09d}') + '_'
		
		scale = random.uniform(0.04, 0.08)
		translate = [random.uniform(-3, 3), random.uniform(-4, 1), random.uniform(1, 4)]
		rotate = random.uniform(-180, 180)
		
		# rho gen
		
		r = r_rho.findall('shape')[1]
		r.find('string').set('value', obj_path)
		r = r.find('transform')
		r.find('translate').set('value', str(translate[0]) + ', ' + str(translate[1]) + ', ' + str(translate[2]))
		r.find('scale').set('value', str(scale))
		r.find('rotate').set('angle', str(rotate))
		t_rho.write('rho_gen.xml')
		
		run_rendering('rho_gen.xml', prefix + 'rho_2x.png')
		
		# mask gen
		
		r = r_mask.find('shape')
		r.find('string').set('value', obj_path)
		r = r.find('transform')
		r.find('translate').set('value', str(translate[0]) + ', ' + str(translate[1]) + ', ' + str(translate[2]))
		r.find('scale').set('value', str(scale))
		r.find('rotate').set('angle', str(rotate))
		
		t_mask.write('mask_gen.xml')
		
		run_rendering('mask_gen.xml', prefix + 'mask_2x.png')
		
		# img_gen
		
		r = r_img.findall('shape')
		if len(r) < 2:
			r_img.append(obj_node)
			
			
		r = r_img.findall('shape')[1]
		r.find('string').set('value', obj_path)
		r = r.find('transform')
		r.find('translate').set('value', str(translate[0]) + ', ' + str(translate[1]) + ', ' + str(translate[2]))
		r.find('scale').set('value', str(scale))
		r.find('rotate').set('angle', str(rotate))
		
		r = r_img.findall('sensor/film/integer')
		[rr.set('value', '1024') for rr in r]
		t_img.write('img_gen.xml')
		
		r = r_img.find('shape/emitter/texture/string')
		r.set('value', bg_path)
		t_img.write('img_gen.xml')
		
		run_rendering('img_gen.xml', prefix + 'img_2x.png')
		
		r = r_img.findall('sensor/film/integer')
		[rr.set('value', '512') for rr in r]
		t_img.write('img_gen.xml')
		
		run_rendering('img_gen.xml', prefix + 'img_1x.png')
		
		r = r_img.findall('sensor/film/integer')
		[rr.set('value', '1024') for rr in r]
		
		rf_run(prefix)
		
		r = r_img.findall('shape')[1]
		r_img.remove(r)
		t_img.write('img_gen.xml')
		
		run_rendering('img_gen.xml', prefix + 'ref_2x.png')
		
		r = r_img.findall('sensor/film/integer')
		[rr.set('value', '512') for rr in r]
		t_img.write('img_gen.xml')
		
		run_rendering('img_gen.xml', prefix + 'ref_1x.png')
		
		