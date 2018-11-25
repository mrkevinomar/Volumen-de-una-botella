import funciones as funcion
import constantes as const
import numpy as np
import cv2

# Calcular distancia focal
distancia_focal = funcion.obtener_distancia_focal()
print(distancia_focal)
# Empieza captura
captura = cv2.VideoCapture(0)

while True:

    # Leer frame
    ret, frame_original = captura.read()

    img = funcion.transformacion(frame_original)

    contornoMayor = funcion.obtener_contorno(img)

    # Obtener contorno mas grande
    pixeles_blancos = 0
    distancia_botella = 0

    if len(contornoMayor) > 0:

        xo, yo, ancho, alto = cv2.boundingRect(contornoMayor)
        cv2.rectangle(frame_original, (xo, yo), (xo + ancho, yo + alto), (255, 0, 0), 2)
        # Obtenemos el roi en base a el contorno obtenido
        liquido = img[yo:yo+alto, xo:xo+ancho]
        cv2.imshow("ROI Liquido", liquido)
        pixeles_blancos = np.sum(liquido == 255)

        # Calcular la distancia entre la botella y la cámara
        marker = cv2.minAreaRect(contornoMayor)
        distancia_botella = funcion.distance_to_camera(const.ANCHO_BOTELLA, distancia_focal, marker[1][0])  -2

    volumen_liquido = funcion.calcular_volumen(pixeles_blancos)

    # Escribo datos en pantalla
    funcion.escribir_texto(frame_original, "Pixeles Liquido   : "+str(pixeles_blancos)   + " px " , 20,20)
    funcion.escribir_texto(frame_original, "Volumen Liquido   : "+str(volumen_liquido)   + " ml" , 20,40)
    funcion.escribir_texto(frame_original, "Distancia Botella : "+str(distancia_botella) + " cm " , 20,60)

    # Muestra frame nuevo
    cv2.imshow("Video", frame_original)

    # Termina presionando la tecla Esc
    key = cv2.waitKey(33)
    if key == 27:
        break

cv2.destroyAllWindows()

