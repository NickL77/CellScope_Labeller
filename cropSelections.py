import os
import cv2
import ast

dirname = os.path.realpath('.')
label_dir = os.path.join(dirname, 'labels/')
cropped_dir = os.path.join(dirname, 'cropped/')

for filename in os.listdir(label_dir):

	if filename.endswith('.txt'):

		f = open(os.path.join(label_dir, filename), 'r')
		img_name = f.readline().rstrip()
		b_boxes = ast.literal_eval(f.readline().rstrip())

		for i in range(len(b_boxes) // 2):
			bl_x, bl_y = b_boxes[i * 2][0], b_boxes[i * 2][1]
			tr_x, tr_y = b_boxes[i * 2 + 1][0], b_boxes[i * 2 + 1][1]
			
			img = cv2.imread(img_name)
			crop_img = img[bl_y: tr_y, bl_x: tr_x]
			crop_img_name = img_name + '_' + str(i) + '.png'
			cv2.imwrite(os.path.join(cropped_dir, crop_img_name), crop_img)

		f.close()

