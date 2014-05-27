#!/bin/bash

#######################################AUXILIARTY FUNCTIONS:
#this are useful functions for the script
float_scale=6
function float_eval()
{
    local stat=0
    local result=0.0
    if [[ $# -gt 0 ]]; then
        result=$(echo "scale=$float_scale; $*" | bc -q 2>/dev/null)
        stat=$?
        if [[ $stat -eq 0  &&  -z "$result" ]]; then stat=1; fi
    fi
    echo $result
    return $stat
}

function float_cond()
{
    local cond=0
    if [[ $# -gt 0 ]]; then
        cond=$(echo "$*" | bc -q 2>/dev/null)
        if [[ -z "$cond" ]]; then cond=0; fi
        if [[ "$cond" != 0  &&  "$cond" != 1 ]]; then cond=0; fi
    fi
    local stat=$((cond == 0))
    return $stat
}

# EXAMPLE: ./scriptGetImg.sh barcelona 1 1 1 
#=> uses a folder named barcelona to download inside all files (descargar=1), then unifies all files  (convertir=1) and finally it takes the google logo out (recortar=1)

#######################################INPUT SECTION:
carpeta=""
carpeta=$1
descargar=$2
convertir=$3
recortar=$4
# esquina1Lat=40.522673 #MADRID
# esquina1Long=-3.596476 #MADRID
# esquina3Lat=40.361545 #MADRID
# esquina3Long=-3.771104 #MADRID

#esquina1Lat=41.471362 #BARCELONA
#esquina1Long=2.258741 #BARCELONA
#esquina3Lat=41.312734 #BARCELONA
#esquina3Long=2.084113 #BARCELONA

esquina1Lat=-11.9830 #LIMA
esquina1Long=-76.9077 #LIMA
esquina3Lat=-12.19063 #LIMA
esquina3Long=-77.08233 #LIMA

zoom=15

format="jpg"
pixeles_ancho="452"
pixeles_alto="640"
x="x"

num_imag_ancho=9
num_imag_alto=8

#######################################SOME INTERMEDIATE VALUES:
echo "utilizando carpeta $carpeta"
echo "descargar= "$descargar
echo "convertir= "$convertir
echo $pixeles_ancho_imagenesx

#defino las medidas en función de las dimensiones:
ancho_imagen=$(float_eval "($esquina3Long+-1*$esquina1Long)/$num_imag_ancho")
if $(float_cond "$ancho_imagen<0"); then
    ancho_imagen=$(float_eval "$ancho_imagen*-1")
fi
echo $ancho_imagen
alto_imagen=$(float_eval "($esquina1Lat+-1*$esquina3Lat)/$num_imag_alto")
if $(float_cond "$alto_imagen<0"); then
    alto_imagen=$(float_eval "$alto_imagen*-1")
fi
echo $alto_imagen

centroLat=$(float_eval "$esquina1Lat+-1*$alto_imagen/2")
centroLong=$(float_eval "$esquina1Long+-1*$ancho_imagen/2")
echo "$centroLong,$centroLat"
	
fila=0
columna=0
nombre_final="$carpeta/todo.$format"

#######################################PROCESS:

while $(float_cond "$centroLat>$esquina3Lat"); do
    fila=$(float_eval "$fila+1")
    centroLong=$(float_eval "$esquina1Long+-1*$ancho_imagen/2")
    columna=0
    nomb_fila="$carpeta/$fila.$format"
    while $(float_cond "$centroLong>$esquina3Long"); do
        url="http://maps.googleapis.com/maps/api/staticmap?center=$centroLat,$centroLong&zoom=$zoom&size=$pixeles_ancho$x$pixeles_alto&scale=2&format=$format&sensor=false"
        centroLong=$(float_eval "$centroLong+-1*$ancho_imagen")
        echo "coordenadas= $centroLat, $centroLong"
        columna=$(float_eval "$columna+1")
        nomb_imagen="$carpeta/$fila-$columna.$format"
        echo "nombre de imagen= $nomb_imagen"
        if $(float_cond "$descargar==1"); then
            wget $url -O $nomb_imagen
        fi
        if $(float_cond "$recortar==1"); then
            echo "recortando imagen $nomb_imagen"
            convert $nomb_imagen -gravity South -chop 0x45 $nomb_imagen
        fi
        if $(float_cond "$convertir==1"); then
            if $(float_cond "$columna==1"); then
                echo "borrando imagen $nomb_fila"
                rm -f $nomb_fila
                echo "copiando imagen $nomb_imagen a $nomb_fila"
                cp $nomb_imagen $nomb_fila
            else
                convert $nomb_imagen $nomb_fila +append $nomb_fila 
            fi
        fi
    done
    if $(float_cond "$convertir==1"); then
    if $(float_cond "$fila==1"); then
        rm -f $nombre_final
        cp $nomb_fila $nombre_final
    else
        convert $nombre_final $nomb_fila -append $nombre_final    
    fi
    fi
    centroLat=$(float_eval "$centroLat+-1*$alto_imagen")
done
