import urllib.request
import os

URL = 'https://static-content.springer.com/esm/art%3A10.3758%2FBRM.40.4.1030/MediaObjects/DeDeyne-BRM-2008b.zip'


def download_url(url, save_path):
    with urllib.request.urlopen(url) as dl_file:
        with open(save_path, 'wb') as out_file:
            out_file.write(dl_file.read())


if not os.path.exists('download'):
    os.makedirs('download')

download_url(URL, os.path.join('download', 'DeDeyne-BRM-2008b.zip'))
