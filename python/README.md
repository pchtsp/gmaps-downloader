gmaps-downloader
================

# Python version

Requirements:

* python >= 3.5
* git

## Install dependencies

### Ubuntu:

    sudo apt-get install python3 pip git python3-venv

### Windows

This requires to have `choco` installed.

    choco install python3 git pip -y

Alternatively, one can manually download the latest python version and git. `pip` usually comes with python already.

## Get the software

Steps to set up development environment:

Windows:

    git clone git@github.com:pchtsp/gmaps-downloader.git
    cd gmaps-downloader\python
    python3 -m venv venv
    venv\Scripts\bin\activate
    pip3 install -r requirements

Ubuntu:

    git clone git@github.com:pchtsp/gmaps-downloader.git
    cd gmaps-downloader/python
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements


## How to use it

For now the easier is to edit the code at the last part of the python file.

There's three functions:

    download_all(northeast, southwest, img_number, path_download, overwrite=False, max_downloads=None, clean=False)

This function downloads frames by giving it two corners `northeast` and `southwest` by tuples with format (longitude, latitude).
Also is necessary to give the number of frames per dimension (this should be automatically done from the two squares and the zoom but it's tricky).
I usually fix the number of frames (`imgn_number`) and play with the two corners.

Then the other parameters are options to make configure the file to download, the cleaning of the directory and the directory destionation.

    cut_all(source, destination, **kwargs)

This function cuts images in a `source` directory according to some pattern given in `**kwargs` and moves the resulting images to a `destination` directory.

    paste_all(source, destination, name, max_rows=None)

This last function gets images with a naming convention of (row-col.jpg) in a `source` directory and pastes everything into one image in the `destination` directory with a `name`

To run the script one needs only to do the following:


    cd gmaps-downloader/python
    source venv/bin/activate
    python3 img_downloader.py

or, in windows:

    cd gmaps-downloader\python
    venv\Scripts\bin\activate
    python3 img_downloader.py
