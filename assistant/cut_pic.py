import os

from PIL import Image, ImageEnhance
from tqdm import tqdm


def cut_pic(img_path, out_img_path, coordinates):
    # If you want to set coordinates, please set here

    print("Being process of cutting...")
    pic_name = os.listdir(img_path)
    for i in tqdm(range(len(pic_name))):
        image = Image.open(os.path.join(img_path, pic_name[i]))
        size = image.size
        mid_x = int(size[0] / 2)
        total_y = size[1]
        coordinates_split1 = (0, 0, mid_x, total_y)
        coordinates_split2 = (mid_x, 0, size[0], size[1])
        coordinates_page1 = (coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1])
        coordinates_page2 = (coordinates[2][0] - mid_x, coordinates[2][1], coordinates[3][0] - mid_x, coordinates[3][1])

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