# CellScope_Labeller
Image labeller for CellScope

After cloning, make sure to add `photos`, `cropped`, and respective subdirectories as shown below. The `pre-process.py` script renames image files from the `photots/original` directory and copies the renamed files into the `photos/renamed` directory (currently only `.png` files are supported). The `cropped` directory will be populated by the labelling scripts.

```
CellScope_Labeller
│   README.md
│   labeller.py   
│   ...
|
└───labels
└───photos
    |
    └───original    
    └───renamed
└───cropped
    │   
    └───negatives_1
    └───negatives_2
    └───negatives_3
    └───positives_1
    └───positives_2
    └───positives_3
```

### Descriptions for Scripts
* `preprocessImages.py` - copies and renames files from `photos\original` to `photos\renamed`, the directory all the labelling scipts grab images from.
* `labeller.py` - Runs the labelling program on any image files in `photos/renamed` that do not have a corresponding label file in `labels`.
* `cropSelections.py` - Iterates through `labels` directory, and crops out bounding box images and puts them in their respective folder in `cropped`. Currently statically cropping 120x120 images using the center of the bounding box.
* `autogenNegs.py` - Iterates through the `labels` directory, and generates 250 negative bounding box labels. This overrides exsisting negative bounding box labels
* `relabel.py` - Does the same as `labeller.py`, but iterates (in random order) over images without checking if a label exsists. Currently mainly used for verifying labels are good and has implimentation for manually labelling negatives.

### Labelling Hot keys
* `q` - quit
* `u` - undo, removes the latest bounding box added
* `p` - cylces between 3 filters for each image
* `n` - generates negatives
* `e` - export bounding boxes to corresponding label file, and moves to next image
* `s` - ONLY FOR `relabel.py` switch between labelling positives and negatives

