import numpy as np
import constantes as const
import cv2


def escribir_texto(imagen, texto, x, y):

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(imagen, texto, (x, y), font, 0.6, (0, 0, 255), 1, cv2.LINE_AA)


def transformacion(imagen):

    # Cambiar imagen original a escala de gris
    img_gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Suavizar imagen
    img_suavizada = cv2.GaussianBlur(img_gray, (9, 9), 0)

    # Binarizar imagen
    thresh, img_binarizada = cv2.threshold(img_suavizada, 220, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_invertida = cv2.bitwise_not(img_binarizada)

    # Crear un kernel de '1'
    kernel = np.ones((9, 9), np.uint8)

    # Se aplica la transformacion: Closing
    img_transformada = cv2.morphologyEx(img_invertida, cv2.MORPH_CLOSE, kernel)

    return img_transformada


def obtener_contorno(imagen):

    # Obtener contornos
    imagen, ctrs, hier = cv2.findContours(imagen.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(ctrs) > 0:
        return max(ctrs, key=cv2.contourArea)

    return None


def distance_to_camera(knownWidth, focalLength, perWidth):

    distance = round((knownWidth * focalLength) / perWidth, 2)
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
    '''
    print(marker)
    print(marker[1][0])

    if marker:
        focalLength = (marker[1][0] * const.DISTANCIA_BOTELLA) / const.ANCHO_BOTELLA

    print(focalLength)
    return focalLength


def calcular_volumen(pixeles_blancos, distancia_botella):
    return round(const.VOLUMEN_LIQUIDO * pixeles_blancos * const.DISTANCIA_BOTELLA / (const.PIXELES_LIQUIDO * distancia_botella + 2.5), 2)
