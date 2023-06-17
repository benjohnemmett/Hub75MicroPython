#!/usr/bin/env python3

import sys
import os
import numpy as np
import cv2
import argparse

class Configs:
    def __init__(self):
        self.RED_THRESHOLD   = 127
        self.GREEN_THRESHOLD = 127
        self.BLUE_THRESHOLD  = 127

        self.RED_BIT   = 0b100
        self.GREEN_BIT = 0b010
        self.BLUE_BIT  = 0b001

        self.MAX_ROW_SIZE = 32
        self.MAX_COL_SIZE = 64

        self.variable_name = "img"
        self.output_file = "img_data.py"

def GetReducedImageSize(img, configs):
    orig_rows = img.shape[0]
    orig_cols = img.shape[1]

    reduction = None
    if configs.MAX_ROW_SIZE and configs.MAX_COL_SIZE:
        if (configs.MAX_COL_SIZE / configs.MAX_ROW_SIZE) * orig_rows > orig_cols:
            reduction = configs.MAX_ROW_SIZE / orig_rows
        else:
            reduction = configs.MAX_COL_SIZE / orig_cols
    elif configs.MAX_ROW_SIZE:
        reduction = configs.MAX_ROW_SIZE / orig_rows
    elif configs.MAX_COL_SIZE:
        reduction = configs.MAX_COL_SIZE / orig_cols

    rows = int(orig_rows * reduction)
    cols = int(orig_cols * reduction)

    return (rows, cols)


def ConvertImageTo3BitList(img, configs):
    img_red = np.where(img[:,:,2] < configs.RED_THRESHOLD, 0, configs.RED_BIT)
    img_green = np.where(img[:,:,1] < configs.GREEN_THRESHOLD, 0, configs.GREEN_BIT)
    img_blue = np.where(img[:,:,0] < configs.BLUE_THRESHOLD, 0, configs.BLUE_BIT)

    return img_red + img_green + img_blue


def PrintImageList(img, out=sys.stdout):
    out.write("[")
    for row in range(img.shape[0]-1):
        out.write("[")
        for col in range(img.shape[1]-1):
            out.write("{}, ".format(img[row, col]))
        out.write("{}],\n".format(img[row, col]))
    
    out.write("[")
    for col in range(img.shape[1]-1):
        out.write("{}, ".format(img[-1, col]))
    out.write("{}]]\n\n".format(img[-1, col]))


def ConvertImage(image, configs):
    print("Reading image {}...".format(image))

    img = cv2.imread(image)

    print(" -> size {}".format(img.shape))
    (rows, cols) = GetReducedImageSize(img, configs)

    print("Converting size to {} {}".format(rows, cols))
    img_reduced = cv2.resize(img, (cols, rows)).astype(np.uint8)
    print(" - new size {}".format(img_reduced.shape))

    img_out = ConvertImageTo3BitList(img_reduced, configs)

    return img_out


def run(image_path, configs):

    with open(configs.output_file, "wt") as out_file:
        if os.path.isdir(image_path):
            files_in_dir = [f for f in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, f))]
            files_in_dir.sort()

            out_file.write(f"{configs.variable_name} = [\n")
            for file in files_in_dir:
                if not file.endswith((".png", ".jpg", "jpeg")):
                    continue
                file_path = os.path.join(image_path, file)
                print(f"Reading file {file_path}")
                img_out = ConvertImage(file_path, configs)

                PrintImageList(img_out, out=out_file)
                out_file.write(f",\n")

            out_file.write(f"]\n")
        else:
            out_file.write(f"{configs.variable_name} = ")
            img_out = ConvertImage(image_path, configs)
            PrintImageList(img_out, out=out_file)


def main():
    parser = argparse.ArgumentParser(description="Convert an image to a 2D list of 3-bit mapped values.")
    parser.add_argument("-i", "--image", help="Full path to an image file or directory of image files to be encoded.")
    parser.add_argument("-r", "--rows", type=int, default=32, required=False)
    parser.add_argument("-c", "--cols", type=int, default=64, required=False)
    parser.add_argument("-n", "--var_name", default="img")
    parser.add_argument("-o", "--output_file", default="img_data.py")
    parser.add_argument("--red_thresh", type=int, default=127, required=False)
    args = parser.parse_args()
    print(args)

    configs = Configs()
    configs.MAX_COL_SIZE = args.cols
    configs.MAX_ROW_SIZE = args.rows
    configs.RED_THRESHOLD = args.red_thresh
    configs.variable_name = args.var_name
    configs.output_file = args.output_file

    run(args.image, configs)


if __name__ == "__main__":
    main()
