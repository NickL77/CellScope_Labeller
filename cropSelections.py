import os
import cv2
import ast

dirname = os.path.realpath('.')
label_dir = os.path.join(dirname, 'labels/')
cropped_dir = os.path.join(dirname, 'cropped/')
crop_size_x = 120
crop_size_y = 120
pos_dirs = [os.path.join(cropped_dir, 'positives_' + str(i)) for i in range(1, 4)]
neg_dirs = [os.path.join(cropped_dir, 'negatives_' + str(i)) for i in range(1, 4)]

for pos_dir in pos_dirs:
	if not os.path.isdir(pos_dir):
		os.mkdir(pos_dir)
for neg_dir in neg_dirs:
	if not os.path.isdir(neg_dir):
		os.mkdir(neg_dir)



#loop through each file in the labels directory
for filename in os.listdir(label_dir):

	#verify file is text file
	if filename.endswith('.txt'):

		#read 3 image names and the bounding box arrays
		f = open(os.path.join(label_dir, filename), 'r')
		img_name_0 = f.readline().rstrip()
		img_name_1 = f.readline().rstrip()
		img_name_2 = f.readline().rstrip()
		imgs = [img_name_0, img_name_1, img_name_2]
		b_boxes = ast.literal_eval(f.readline().rstrip())
		neg_boxes = ast.literal_eval(f.readline().rstrip())

		#create directory names for cropped images and negatives per image
		'''
		pos_dir = os.path.join(cropped_dir, filename[:len(filename) - 4])
		neg_dir = pos_dir + '_negatives'
		
		if not os.path.isdir(pos_dir):
			os.mkdir(pos_dir)
		if not os.path.isdir(neg_dir):
			os.mkdir(neg_dir)
		'''

		#loop through bounding boxes to get the coordinates for cropping
		for i in range(len(b_boxes) // 2):
			bl_x, bl_y = b_boxes[i * 2][0], b_boxes[i * 2][1]
			tr_x, tr_y = b_boxes[i * 2 + 1][0], b_boxes[i * 2 + 1][1]
			center_x, center_y = (bl_x + tr_x) // 2, (bl_y + tr_y) // 2

			s_box_x1, s_box_x2 = center_x - (crop_size_x // 2), center_x + (crop_size_x // 2)
			s_box_y1, s_box_y2 = center_y - (crop_size_y // 2), center_y + (crop_size_y // 2)

			#loop through each of the three filtered images and crop the selections
			for j in range(len(imgs)):
				img = cv2.imread(dirname + '/' + imgs[j])
				h, w, _ = img.shape
				if s_box_x1 < 0 or s_box_x2 > w:
					print "Staticly sized bounding box extends outside of image"
					print "Skipping {}".format(imgs[j])
					continue
				
				#Use this to crop the drawn box
				#crop_img = img[bl_y: tr_y, bl_x: tr_x]

				#Use this to get staticly sized boxes based on the crop_size variables
				#and the center of the drawn boxes
				crop_img = img[s_box_y1: s_box_y2, s_box_x1: s_box_x2]

				crop_img_name = imgs[j][15:len(imgs[j]) - 4] + '_crop' + str(i) + '.png'
				cv2.imwrite(os.path.join(pos_dirs[j], crop_img_name), crop_img)

		#loop through negative boxes to get coordinates for cropping
		for i in range(len(neg_boxes) // 2):
			bl_x, bl_y = neg_boxes[i * 2][0], neg_boxes[i * 2][1]
			tr_x, tr_y = neg_boxes[i * 2 + 1][0], neg_boxes[i * 2 + 1][1]
			center_x, center_y = (bl_x + tr_x) // 2, (bl_y + tr_y) // 2
			s_box_x1, s_box_x2 = center_x - (crop_size_x // 2), center_x + (crop_size_x // 2)
			s_box_y1, s_box_y2 = center_y - (crop_size_y // 2), center_y + (crop_size_y // 2)

			#loop through each of the three filtered images and crop the selections
			for j in range(len(imgs)):
				img = cv2.imread(dirname + '/' + imgs[j])
				if s_box_x1 < 0 or s_box_y1 < 0 or s_box_x2 > w or s_box_y2 > h:
					print "Staticly sized negative box extends outside of image"
					print "Skipping {}".format(imgs[j])
					continue

				#Use this to crop the drawn box
				#crop_img = img[bl_y: tr_y, bl_x: tr_x]

				#Use this to get staticly sized boxes based on the crop_size variables
				#and the center of the drawn boxes
				crop_img = img[s_box_y1: s_box_y2, s_box_x1: s_box_x2]
				
				crop_img_name = imgs[j][15:len(imgs[j]) - 4] + '_neg' + str(i) + '.png'
				cv2.imwrite(os.path.join(neg_dirs[j], crop_img_name), crop_img)


		f.close()

