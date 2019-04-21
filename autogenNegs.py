import argparse
import cv2
import os
import random
import ast
 
# initialize the list of reference points and boolean indicating
selecting, quit = False, False
pos_neg = True #True is for positives, False is for negatives
b_boxes, neg_boxes, img_list = [], [], []
x_coor, y_coor, img_index = 0, 0, 1

dirname = os.path.realpath('.') 
label_path = os.path.join(dirname, 'labels')

#check if boxes are intersecting
def intersection(b1, b2):
	x1 = max(b1[0][0], b2[0][0])
	y1 = max(b1[0][1], b2[0][1])
	x2 = min(b1[1][0], b2[1][0])
	y2 = min(b1[1][1], b2[1][1])
	return x2 > x1 and y2 > y1

#generates array of negative boxes
def generateNegatives(bb, height, width, multiples=1):
	negs = []
	for i in range(1, len(bb), 2):
		w, h = bb[i][0] - bb[i-1][0], bb[i][1] - bb[i-1][1]
		for m in range(500 / len(bb)):
			for n in range(10):
				neg_x, neg_y = random.randint(0, width - w), random.randint(0, height - h)
				neg_box = [(neg_x, neg_y), (neg_x + w, neg_y + h)]
				good_box = True
				for j in range(1, len(bb), 2):
					if intersection(neg_box, [bb[j-1],bb[j]]):
						good_box = False
				if good_box:
					negs.append(neg_box[0])
					negs.append(neg_box[1])
					break
	return negs

def draw_boxes(img, boxes, color):
	for i in range(1,len(boxes), 2):
		cv2.rectangle(img, boxes[i-1], boxes[i], color, 8)

def click_and_crop(event, x, y, flags, param):

	# grab references to the global variables
	global selecting, b_boxes, x_coor, y_coor
	x_coor, y_coor = x, y
        box_array = b_boxes
        if not pos_neg:
            box_array = neg_boxes
	
	# if the left mouse button was clicked, record (x, y),
	# set slecting to True, and record the current image state
	if event == cv2.EVENT_LBUTTONDOWN:
		selecting = True
		box_array.append((x, y))
 
	# if the left mouse button was released, record (x, y),
	# add the rectangle to the main image, and set selecting
	# to False
	elif event == cv2.EVENT_LBUTTONUP:
		selecting = False
		box_array.append((x, y))

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-m", "--multiples", help="multiples for generating negatives", default=1)
args = vars(ap.parse_args())
#neg_multiples = int(args['multiples'])
neg_multiples = 100

label_ls = os.listdir(label_path)
for filename in label_ls:
    
    #parse file for images and bounding boxes
    if not filename.endswith('.txt'):
        break

    f = open(os.path.join(label_path, filename), 'r')
    img_name_0 = f.readline().rstrip()
    img_name_1 = f.readline().rstrip()
    img_name_2 = f.readline().rstrip()
    img_list = [img_name_0, img_name_1, img_name_2]
    b_boxes = ast.literal_eval(f.readline().rstrip())
    neg_boxes = ast.literal_eval(f.readline().rstrip())

    img_name = img_list[0]

    image = cv2.imread(img_name)
    height, width, _ = image.shape

    #cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    #cv2.setMouseCallback('image', click_and_crop)

    neg_boxes = generateNegatives(b_boxes, height, width, neg_multiples)

    filename = os.path.join(label_path, filename)
    print(filename)
    f = open(filename, 'w')
    for name in img_list:
            f.write(name + '\n')
    f.write(str(b_boxes) + '\n')
    f.write(str(neg_boxes) + '\n')
    f.close()
    b_boxes, neg_boxes, img_list = [], [], []

cv2.destroyAllWindows()
