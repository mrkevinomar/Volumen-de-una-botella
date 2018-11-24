import numpy as np
import constantes as const
import cv2


def escribir_texto(imagen, texto, x, y):

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(imagen, texto, (x, y), font, 0.6, (0, 0, 255), 1, cv2.LINE_AA)


def calcular_error(volumen_botella):
    error = 0;

    if volumen_botella <= 125:
        error = const.ERROR1

    elif volumen_botella <= 250:
        error = const.ERROR2

    elif volumen_botella <= 375:
        error = const.ERROR3

    elif volumen_botella <= 500:
        error = const.ERROR4

    elif volumen_botella <= 625:
        error = const.ERROR5

    elif volumen_botella <= 800:
        error = const.ERROR6

    return error


def transformacion(imagen):

    # Cambiar imagen original a escala de gris
    img_gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Binarizar imagen
    thresh, img_binarizada = cv2.threshold(img_gray, 220, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Crear un kernel de '1'
    kernel = np.ones((21, 21), np.uint8)

    # Se aplica la transformacion: Closing
    img_open = cv2.morphologyEx(img_binarizada, cv2.MORPH_OPEN, kernel)
    img_close = cv2.morphologyEx(img_open, cv2.MORPH_CLOSE, kernel)
    img_invertida = cv2.bitwise_not(img_close)

    return img_invertida


def obtener_contorno(imagen):

    # Obtener contornos
    imagen, ctrs, hier = cv2.findContours(imagen.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(ctrs) > 0:
        return max(ctrs, key=cv2.contourArea)

    return None


def distance_to_camera(knownWidth, focal_length, perWidth):

    distance = round((knownWidth * focal_length) / perWidth, 2)
    return distance


def obtener_distancia_focal():

    # Se carga imagen de referencia
    image = cv2.imread(const.IMAGEN_REFERENCIA)
    imagen_transformada = transformacion(image)

    (_, cnts, _) = cv2.findContours(imagen_transformada.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        marker = cv2.minAreaRect(c)
    '''
    xo, yo, ancho, alto = cv2.boundingRect(c)
    cv2.rectangle(image, (xo, yo), (xo + ancho, yo + alto), (255, 0, 0), 2)
    cv2.imshow("sdsa", image)
    print(marker)
    print(marker[1][0])
    '''
    
    if marker:
        focal_length = (marker[1][0] * const.DISTANCIA_BOTELLA) / const.ANCHO_BOTELLA

    return focal_length


def calcular_volumen(pixeles_blancos, distancia_botella):

    volumen = round((const.VOLUMEN_LIQUIDO * pixeles_blancos / const.PIXELES_LIQUIDO) + calcular_error(distancia_botella), 2)
    volumen += calcular_error(volumen)

    return volumen



