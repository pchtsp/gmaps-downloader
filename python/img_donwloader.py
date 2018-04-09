import requests
import shutil
import os
import wand.image as image
import wand.color as color
import json
import pprint as pp
import io
import re


# os.environ['all_proxy'] = ""
# os.environ['http_proxy'] = ""
# os.environ['https_proxy'] = ""

zoom = 15
pixels = '452', '640'
img_format = 'jpg'
api = 'http://maps.googleapis.com/maps/api/staticmap'


def download_img(api, payload, path):
    r = requests.get(api, params=payload, stream=True)
    if not r.status_code==200:
        print('ERROR with file: {}'.format(payload))
        return
    with open(path, 'wb') as out_file:
        shutil.copyfileobj(r.raw, out_file)
    del r
    return


def download_all(northeast, southwest, img_number, path_download, overwrite=False, max_downloads=None, clean=False):
    if clean:
        clean_directory(path_download)
    lat = 1
    long = 0

    img_size = \
        tuple(abs(northeast[i] - southwest[i]) / img_number[i]
              for i in [long, lat])
    pos = \
        [northeast[i] - img_size[i]/2 for i in [long, lat]]

    row = 0
    count = 0

    while pos[lat] > southwest[lat]:
        row += 1
        pos[long] = northeast[long] - img_size[long] / 2
        col = 0
        while pos[long] > southwest[long]:
            count += 1
            if max_downloads is not None and count > max_downloads:
                break
            col += 1
            img_name = path_download + '{}-{}.{}'.format(row, col, img_format)
            print('row={}, col={}, img_name={}'.format(row, col, img_name))
            payload = {
                'center': "{},{}".format(pos[lat], pos[long])
                , 'zoom': zoom
                , 'size': 'x'.join(pixels)
                , 'scale': 2
                , 'format': img_format
                , 'sensor': 'false'}
            pos[long] -= img_size[long]
            if overwrite or not os.path.exists(img_name):
                download_img(api, payload, img_name)
        pos[lat] -= img_size[lat]


def cut_image(img_path, img_path_dest, bottom=45, right=0):
    with image.Image(filename=img_path) as img:
        with img.clone() as i:
            i.crop(width=img.width - right, height=img.height - bottom)
            i.save(filename=img_path_dest)


def add_images(img1, img2, horizontal=True):
    """
    :param img1: Image object
    :param img2: Image object
    :param horizontal:
    :return: Image object
    """
    if horizontal:
        width_result = img1.width + img2.width
        height_result = img1.height
        width_offset = img1.width
        height_offset = 0
    else:
        width_result = img1.width
        height_result = img1.height + img2.height
        width_offset = 0
        height_offset = img1.height

    dst = \
        image.Image(
            width=width_result,
            height=height_result,
            background=color.Color('WHITE'))
    dst.composite(img1, 0, 0)
    dst.composite(img2, int(width_offset), int(height_offset))
    return dst


def cut_all(source, destination, **kwargs):
    clean_directory(destination)
    files_in = [os.path.join(source, f) for f in os.listdir(source)]
    files_out = [os.path.join(destination, f) for f in os.listdir(source)]
    for pos, f in enumerate(files_in):
        cut_image(f, files_out[pos], **kwargs)
    return


def get_row_col(filename):
    result = re.findall(r'(\d+)-(\d+)', filename)
    if len(result) > 0:
        r, c = result[0]
        return int(r), int(c)
    return ()


def clean_directory(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def paste_all(source, destination, name, max_rows=None):
    files_in = [os.path.join(source, f) for f in os.listdir(source)]
    file_pos = {f: get_row_col(f) for f in files_in if len(get_row_col(f)) > 0}
    max_row = max(r for r, c in file_pos.values())
    max_col = max(c for r, c in file_pos.values())
    all_rows = list(range(1, max_row+1))
    if max_rows is not None:
        all_rows = all_rows[:max_rows]
    all_cols = list(range(1, max_col+1))
    img = {r: {} for r in all_rows}

    for f, (r, c) in file_pos.items():
        if r in img:
            img[r][c] = image.Image(filename=f)

    file_row = {r: img[r][1] for r in all_rows}
    for r in all_rows:
        for c in all_cols[1:]:
            if c in img[r]:
                file_row[r] = add_images(img[r][c], file_row[r])

    file = file_row[1]
    for r in all_rows[1:]:
        file = add_images(file, file_row[r], horizontal=False)

    file.save(filename=destination + name)
    return


if __name__ == "__main__":
    city = "barcelona"
    paths = {'main': '/home/pchtsp/Documents/projects/personal/gmaps-downloader/' + city + '/'}
    for p in ['raw', 'cut', 'paste']:
        paths[p] = paths['main'] + p + '/'

    data = {
        'madrid': {
            'sw_lat_long': (40.361545, -3.771104)
            , 'ne_lat_long': (40.522673, -3.596476)
        }
        , 'toulouse': {
            'sw_lat_long': (43.52000, 1.327389)
            , 'ne_lat_long': (43.67000, 1.502016)
        }
        , 'lima': {
            'sw_lat_long': (-12.19063, -77.12233)
            , 'ne_lat_long': (-11.9830, -76.9477)
        }
        , 'barcelona': {
            'sw_lat_long': (41.312734, 2.084113)
            , 'ne_lat_long': (41.471362, 2.258741)
        }
    }

    cutting = {
        'toulouse': {'bottom': 75, 'right': 0}
    }
    cutting_default = {'bottom': 45, 'right': 0}
    for key in data:
        if key not in cutting:
            cutting[key] = cutting_default

    if city not in data:
        raise IndexError("city {} not found in data: {}".format(city, list(data.keys())))

    if not os.path.exists(paths['main']):
        os.makedirs(paths['main'])

    for p in paths.values():
        if not os.path.exists(p):
            os.makedirs(p)
    # PARAMS:
    # Always (width, height) / (long, lat) format

    northeast = data[city]['ne_lat_long'][1], data[city]['ne_lat_long'][0]
    southwest = data[city]['sw_lat_long'][1], data[city]['sw_lat_long'][0]
    img_number = (9, 8)

    # clean_directory(paths['raw'])
    download_all(northeast=northeast,
                 southwest=southwest,
                 img_number=img_number,
                 path_download=paths['raw'],
                 max_downloads=None,
                 overwrite=False,
                 clean=False)
    cut_all(paths['raw'], paths['cut'], **cutting[city])
    paste_all(paths['cut'], paths['paste'], name=city+'.jpg', max_rows=None)

    # add_images()