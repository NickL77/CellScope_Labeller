import argparse
import cv2
import os
 
# initialize the list of reference points and boolean indicating
selecting = False
b_boxes, past_images = [], []
x_coor, y_coor = 0, 0
dirname = os.path.realpath('.') 

def click_and_crop(event, x, y, flags, param):

	# grab references to the global variables
	global selecting, b_boxes, x_coor, y_coor
	x_coor, y_coor = x, y
	
	# if the left mouse button was clicked, record (x, y),
	# set slecting to True, and record the current image state
	if event == cv2.EVENT_LBUTTONDOWN:
		past_images.append(image.copy())
		selecting = True
		b_boxes.append((x, y))
 
	# if the left mouse button was released, record (x, y),
	# add the rectangle to the main image, and set selecting
	# to False
	elif event == cv2.EVENT_LBUTTONUP:
		selecting = False
		b_boxes.append((x, y))
		
		index = len(b_boxes)
		cv2.rectangle(image, b_boxes[index - 2], b_boxes[index - 1], (0, 255, 0), 2)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
 
# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args['image'])
cv2.namedWindow('image')
cv2.setMouseCallback('image', click_and_crop)

while True:

	# display the image and wait for a keypress
	key = cv2.waitKey(1) & 0xFF
	clone = image.copy()

	#display bounding box being selected
	if selecting:
		cv2.rectangle(clone, b_boxes[len(b_boxes) - 1], (x_coor, y_coor), (0, 255, 0), 2)
	cv2.imshow('image', clone)
	
	# 'q' to quit, 'u' to undo, 'e' to export 
	# TODO: 'n' to go to next image
	if key == ord('q'):
		break
	elif key == ord('u'):
		if len(b_boxes) > 1:
			b_boxes.pop()
			b_boxes.pop()
			image = past_images.pop()
	elif key == ord('e'):
		filename = args['image'][:len(args['image']) - 3] + 'txt'
		filename = os.path.join(dirname, 'labels/' + filename)
		f = open(filename, 'w')
		f.write(args['image'] + '\n')
		f.write(str(b_boxes) + '\n')
		f.close()
 
cv2.destroyAllWindows()
