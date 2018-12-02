from shutil import copy2
import os

dirname = os.path.realpath('.')
origDir = os.path.join(dirname, 'photos/original/')
destDir = os.path.join(dirname, 'photos/renamed/')

for pic in os.listdir(origDir):
	if not pic.endswith('t.png') and len(pic) == 67:
		copy2(origDir + pic, destDir)
		os.rename(destDir + pic, destDir + pic[20:26] + '.png')
