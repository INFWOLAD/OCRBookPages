"""
This is a function that can help you organize your book pages.
"""

import os
import sys

import pytesseract
from PIL import Image, ImageEnhance
from tqdm import tqdm

import mark


def del_not_img():
    print("We'll let you input two paths, and we'll delete all files which isn't images.")
    img_path = input("Please input your image file path:")
    out_img_path = input("Please input where to save new images:")

    if os.path.exists(img_path) is False:
        sys.exit(1)
    if os.path.exists(out_img_path) is False:
        os.makedirs(out_img_path)
    print("Path verified finished!")

    file_name = os.listdir(img_path)
    for i in range(len(file_name)):
        if not file_name[i].endswith(".jpg"):
            print("there is some files not images, removing")
            if file_name[i] != "pages_number":
                os.remove(os.path.join(img_path, file_name[i]))

    file_name = os.listdir(out_img_path)
    for i in range(len(file_name)):
        if not file_name[i].endswith(".jpg"):
            print("there is some files not images, removing")
            os.remove(os.path.join(out_img_path, file_name[i]))

    print("Content verified finished!")
    return img_path, out_img_path


def cut_pic(img_path, out_img_path, coordinates):
    # If you want to set coordinates, please set here
    coordinates_split1 = (0, 0, 2480, 3508)
    coordinates_split2 = (2480, 0, 4960, 3508)
    coordinates_page1 = (coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1])
    coordinates_page2 = (coordinates[2][0], coordinates[2][1], coordinates[3][0], coordinates[3][1])

    print("Being process of cutting...")
    pic_name = os.listdir(img_path)
    for i in tqdm(range(len(pic_name))):
        image = Image.open(os.path.join(img_path, pic_name[i]))
        image_cut = image.crop(coordinates_split1)
        image_cut.save(os.path.join(out_img_path, "left_" + pic_name[i]))
        image_cut = image.crop(coordinates_split2)
        image_cut.save(os.path.join(out_img_path, "right_" + pic_name[i]))

    new_pic_name = os.listdir(out_img_path)
    for i in tqdm(range(len(new_pic_name))):
        if os.path.exists(os.path.join(img_path, "pages_number")) is False:
            os.makedirs(os.path.join(img_path, "pages_number"))
        pages_path = os.path.join(img_path, "pages_number")
        image = Image.open(os.path.join(out_img_path, new_pic_name[i]))
        image_cut = image.crop(coordinates_page1)
        image_cut = ImageEnhance.Contrast(image_cut).enhance(3)
        image_cut.save(os.path.join(pages_path, "L-number_" + new_pic_name[i]))
        image_cut = image.crop(coordinates_page2)
        image_cut = ImageEnhance.Contrast(image_cut).enhance(3)
        image_cut.save(os.path.join(pages_path, "R-number_" + new_pic_name[i]))

    return new_pic_name, pages_path


def main():
    coordinates = mark.mark()
    img_path, out_img_path = del_not_img()
    pic_name, pages_path = cut_pic(img_path, out_img_path, coordinates)
    # pic_name = os.listdir(out_img_path)
    # pages_path = os.path.join(img_path, "pages_number")
    print("Recognizing images' page number...")
    for i in tqdm(range(len(pic_name))):
        image = Image.open(os.path.join(pages_path, "L-number_" + pic_name[i]))
        # image = Image.open("/Users/cosz/Downloads/cc/500_bg_4009-BAA-1901A.jpg")
        number = pytesseract.image_to_string(image, lang='eng', config="--psm 6")
        if number != "":
            try:
                number = str(int(number))
            except ValueError:
                number = "error" + number
            os.rename(os.path.join(out_img_path, pic_name[i]), os.path.join(out_img_path, number + ".jpg"))
        else:
            image = Image.open(os.path.join(pages_path, "R-number_" + pic_name[i]))
            number = pytesseract.image_to_string(image, lang='eng', config="--psm 6")
            number.replace("\n", "")
            if number != "":
                try:
                    number = str(int(number))
                except ValueError:
                    number = "error" + number
                os.rename(os.path.join(out_img_path, pic_name[i]), os.path.join(out_img_path, number + ".jpg"))
            else:
                # print("R-number_" + pic_name[i] + "--This page is not available")
                os.remove(os.path.join(out_img_path, pic_name[i]))
    print("All stuff has been finished")


if __name__ == '__main__':
    main()
