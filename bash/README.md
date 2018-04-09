gmaps-downloader
================

bash script to download maps using google maps API.

## Pre-requisites - installation

- Linux shell with Internet connection.
- imagemagick
- wget (I think it comes with every Linux distribution...)
- git

One single line:

    sudo apt-get install imagemagick wget git
    git clone git@github.com:pchtsp/gmaps-downloader.git
    cd gmaps-downloader
    chmod 775 scriptGetImg.sh

## EXAMPLE 

    mkdir barcelona
    ./scriptGetImg.sh barcelona 1 1 1 

uses a folder named barcelona to download inside all files (descargar=1), then unifies all files (convertir=1) and finally it takes the google logo out (recortar=1)

