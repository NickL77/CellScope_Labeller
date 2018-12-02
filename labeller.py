import argparse
import cv2
import os
 
# initialize the list of reference points and boolean indicating
selecting = False
b_boxes, img_list = [], []
x_coor, y_coor, img_index = 0, 0, 1
dirname = os.path.realpath('.') 

def draw_boxes(img, boxes):
	for i in range(1,len(boxes), 2):
		cv2.rectangle(img, boxes[i-1], boxes[i], (0, 225, 0), 8)

def click_and_crop(event, x, y, flags, param):

	# grab references to the global variables
	global selecting, b_boxes, x_coor, y_coor
	x_coor, y_coor = x, y
	
	# if the left mouse button was clicked, record (x, y),
	# set slecting to True, and record the current image state
	if event == cv2.EVENT_LBUTTONDOWN:
		selecting = True
		b_boxes.append((x, y))
 
	# if the left mouse button was released, record (x, y),
	# add the rectangle to the main image, and set selecting
	# to False
	elif event == cv2.EVENT_LBUTTONUP:
		selecting = False
		b_boxes.append((x, y))

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
 
# load the image, clone it, and setup the mouse callback function
img_name = args['image']
print(img_name)
img_index = int(img_name[len(img_name) - 5])

img_list.append(img_name[:len(img_name) - 5] + '0.png')
img_list.append(img_name[:len(img_name) - 5] + '1.png')
img_list.append(img_name[:len(img_name) - 5] + '2.png')

image = cv2.imread(img_name)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', click_and_crop)

while True:

	
	# display the image and wait for a keypress
	key = cv2.waitKey(1) & 0xFF
	clone = image.copy()

	#display bounding box being selected
	if selecting:
		cv2.rectangle(clone, b_boxes[len(b_boxes) - 1], (x_coor, y_coor), (0, 255, 0), 8)

	draw_boxes(clone, b_boxes)
	cv2.imshow('image', clone)
	
	# 'q' to quit, 'u' to undo, 'e' to export 
	# 'n' to go to next image
	if key == ord('q'):
		break

	elif key == ord('u'):
		if len(b_boxes) > 1:
			b_boxes.pop()
			b_boxes.pop()

	elif key == ord('n'):
		img_index = (img_index + 1) % 3
		image = cv2.imread(img_list[img_index])

	elif key == ord('e'):
		filename = args['image'][15:len(args['image']) - 6] + '.txt'
		filename = os.path.join(dirname, 'labels/' + filename)
		f = open(filename, 'w')
		for name in img_list:
			f.write(name + '\n')
		f.write(str(b_boxes) + '\n')
		f.close()
 
cv2.destroyAllWindows()
