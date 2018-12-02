import os
import cv2
import ast

dirname = os.path.realpath('.')
label_dir = os.path.join(dirname, 'labels/')
cropped_dir = os.path.join(dirname, 'cropped/')

for filename in os.listdir(label_dir):

	if filename.endswith('.txt'):

		f = open(os.path.join(label_dir, filename), 'r')
		img_name_0 = f.readline().rstrip()
		img_name_1 = f.readline().rstrip()
		img_name_2 = f.readline().rstrip()
		imgs = [img_name_0, img_name_1, img_name_2]
		b_boxes = ast.literal_eval(f.readline().rstrip())

		for i in range(len(b_boxes) // 2):
			bl_x, bl_y = b_boxes[i * 2][0], b_boxes[i * 2][1]
			tr_x, tr_y = b_boxes[i * 2 + 1][0], b_boxes[i * 2 + 1][1]
		
			for j in range(len(imgs)):
				img = cv2.imread(dirname + '/' + imgs[j])
				crop_img = img[bl_y: tr_y, bl_x: tr_x]
				crop_img_name = imgs[j][15:len(imgs[j]) - 4] + '_crop' + str(i) + '.png'
				cv2.imwrite(os.path.join(cropped_dir, crop_img_name), crop_img)

		f.close()

