import time
import datetime as dt
import pytz
import os
import random
from PIL import Image, ImageFont, ImageDraw


def format_timestamp(timestamp):
    local_time = time.localtime(timestamp)
    fmt_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
    return fmt_time

def gen_date(timezone = 'Asia/Shanghai'):
    tz = pytz.timezone(timezone)
    date_ = dt.datetime.now(tz).isoformat().split('T')[0]
    return date_

def gen_img_with_text(content, font_file_path, img_save_path, file_extension = 'png', 
        font_size = 28, bg_folder = None
    ):
    '''Generate images from text.
    Arguments:
        content -- text to convert
        font_file_path -- the path to a font
        img_save_path -- path to save images
        file_extension -- the image type you want to save.
        font_size -- font size of text.
        bg_folder -- a folder that contains backgroud images, if not given the backgroud is white.
    Returns:
        saved_imgs_list --  a list contains saved images paths.
    '''
    saved_imgs_list = []
    if bg_folder:
        bg_filenames = os.listdir(bg_folder)
        bg_num = len(bg_filenames)
    font = ImageFont.truetype(font_file_path, font_size)    
    opacity = 0.6
    id_ = 0
    content: list = content.split('\n')
    
    while True:
        page_full = False
        if bg_folder:
            bg = Image.open(f'{bg_folder}/{bg_filenames[random.randint(0,bg_num-1)]}')
        else:
            bg = Image.new('RAG', (720, 1280), 'white')
        width, height = bg.width, bg.height
        rect_width, rect_height = (width-100, height-200)
        tbox_w, tbox_h = (rect_width-40, rect_height-60)

        draw = ImageDraw.Draw(bg, 'RGBA')
        draw.rounded_rectangle(
            [((width-rect_width)/2, (height-rect_height)/2), ((width+rect_width)/2, (height+rect_height)/2)], 
            radius = 10, 
            fill = (255, 255, 255, int(255*opacity))
        )

        y_text = (height-tbox_h)/2
        x_text = (width-tbox_w)/2
        line_space = 10
        paragraph_space = 20
        for i_paragraph in range(len(content)):
            paragraph = content[i_paragraph]
            for i_char in range(len(paragraph)):
                char = paragraph[i_char]
                char_w, char_h = font.getsize(char)
                if char_w + x_text > (width+rect_width)/2:
                    y_text = y_text + char_h + line_space
                    x_text = (width-tbox_w)/2
                if char_h + y_text > (height+rect_height)/2:
                    page_full = True
                    content = content[i_paragraph+1::]
                    content.insert(0, paragraph[i_char::])
                    break
                draw.text(
                    (x_text, y_text),
                    char,
                    fill = 'blue',
                    font = font
                )
                x_text = x_text + char_w
            if page_full: break
            x_text = (width-tbox_w)/2
            y_text = y_text + char_h + paragraph_space

        id_ += 1
        img_filename = f'{img_save_path}_{id_}.{file_extension}'
        bg.save(img_filename)
        saved_imgs_list.append(img_filename)
        bg.close()
        if not page_full: break
    
    return saved_imgs_list