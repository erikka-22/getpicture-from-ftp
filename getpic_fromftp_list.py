# encoding: utf-8

import os
import ftplib
import dotenv
# from bs4 import BeautifulSoup
import glob
# import csv
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)


# FTPSの情報
HOST_NAME = "hogehogehoge"
USER_NAME = "hogehogehoge"
PASSWORD = "hogehogehoge"
FTPS_DATA_DIR = "/hoge/hoge"

# 画像保存先ディレクトリ（フルパス）
LOCAL_STORE_DIR = '/path/to/the/dir'
# processingで読み込むための絶対パス付き画像名リスト
path_list = []
# 画像名リストのファイル
LOCAL_STORE_FILE = "picture_name.csv"
# 画像名リスト保存先ディレクトリ
DATA_DIR = '/path/to/the/dir'

img_squareside_pixel = 700


def put_ftp_pictures(pic_name, pic_path):
    with ftplib.FTP_TLS(HOST_NAME) as ftps:
        ftps.set_pasv("true")
        ftps.login(USER_NAME, PASSWORD)
        ftps.prot_p()
        with open(pic_path, 'rb') as fp:
            log = ftps.storbinary('STOR ' + FTPS_DATA_DIR + '/' + pic_name, fp)
            print('[LOG] upload to ftp server ' + pic_name + ' ' + log)


def get_local_pic_list():
    local_pictures = []
    file_paths = glob.glob(LOCAL_STORE_DIR + '*')
    for file_name in file_paths:
        file = os.path.basename(file_name)
        local_pictures.append(file)
    print(local_pictures)
    return local_pictures


def get_ftp_pic_list():
    ftp_pictures = []
    with ftplib.FTP_TLS(HOST_NAME) as ftps:
        ftps.login(USER_NAME, PASSWORD)
        ftps.cwd(FTPS_DATA_DIR)
        all_files = ftps.nlst()
        print(all_files)
        for file_name in all_files:
            extention = os.path.splitext(file_name)
            if extention[1] == '.png':
                ftp_pictures.append(file_name)
        print('[LOG] get ftp picture list. there are ' +
              str(len(ftp_pictures)) + ' files')
        print(ftp_pictures)
        return ftp_pictures


def get_pictures(pic_name):
    with ftplib.FTP_TLS(HOST_NAME) as ftps:
        ftps.login(USER_NAME, PASSWORD)
        ftps.cwd(FTPS_DATA_DIR)
        with open(LOCAL_STORE_DIR + pic_name, 'wb') as fp:
            ftps.retrbinary('RETR %s' % pic_name, fp.write)


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def mask_circle_transparent(pil_img, blur_radius, offset=0):
    print("make image circle")
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse(
        (offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    result = pil_img.copy()
    result.putalpha(mask)

    return result


def change_extention_to_png(pic_path_jpg):
    pic_path_png = os.path.splitext(pic_path_jpg)[0] + ".png"
    return pic_path_png


def get_jpgfile_path(pic_name):
    pic_path_jpg = LOCAL_STORE_DIR + pic_name
    return pic_path_jpg


def pic_to_circle(jpg, png):

    im = Image.open(jpg)

    im_square = crop_center(im, img_squareside_pixel, img_squareside_pixel)
    im_circle = mask_circle_transparent(im_square, 0, 0)
    im_resize = im_circle.resize((200, 200))
    im_resize.save(png)


def path_with_name_file(list_name):
    f = DATA_DIR + LOCAL_STORE_FILE
    if os.path.exists(f):
        with open(f, mode='a') as f:
            for element in list_name:
                f.write(element + '\n')
                print(element)
    else:
        with open(f, 'wt') as f:
            for element in list_name:
                f.write(element + '\n')
                print(element)


def main():
    # FTPサーバにある画像一覧を取得
    ftp_pic_list = get_ftp_pic_list()

    # ローカルにある画像一覧を取得
    local_pic_list = get_local_pic_list()

    # ローカルに画像が存在しなければダウンロードしてリサイズ
    for pic in ftp_pic_list:
        if pic not in local_pic_list:
            print('[LOG] ' + pic)
            get_pictures(pic)
            png_path = change_extention_to_png(get_jpgfile_path(pic))
            pic_to_circle(get_jpgfile_path(pic),
                          png_path)
            png_file_name = os.path.basename(png_path)
            path_list.append(png_file_name[:-4])

    # 新たにダウンロードした画像のフルパス付きファイル名リスト
    path_with_name_file(path_list)


if __name__ == "__main__":
    main()
