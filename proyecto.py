import numpy as np
import cv2


# Cargar imagen original (hay que hacerlo mediante la camara)
img_original  = cv2.imread("Imagenes/botella5.jpeg")
cv2.imshow("img_original", img_original)

# Cambiar imagen original a gris
img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)


# Suaviza imagen
img_suavizada = cv2.GaussianBlur(img_gray, (9, 9), 0)

# Binarizar imagen
thresh, img_binarizada = cv2.threshold(img_suavizada, 220, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
im_floodfill_inv = cv2.bitwise_not(img_binarizada)

#Crear un kernel de '1' de 3x3
kernel = np.ones((9,9),np.uint8)

#Se aplica la transformacion: Closing
transformacion = cv2.morphologyEx(im_floodfill_inv,cv2.MORPH_CLOSE,kernel)

image, ctrs, hier = cv2.findContours(transformacion.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# obtenemos  los rectangulos
rects = [cv2.boundingRect(ctr) for ctr in ctrs]

#obtenemos el contorno mas grande
contornoMayor = max(ctrs, key = cv2.contourArea)
xo,yo,ancho,alto = cv2.boundingRect(contornoMayor)
#obtenemos el roi en base a el contorno obtenido
liquido=transformacion[yo:yo+alto,xo:xo+ancho]



cv2.imshow("Liquido", liquido)

pixeles_blancos = np.sum(transformacion == 255)
print('PIXELES BLANCOS:', pixeles_blancos)

pixeles_negros = np.sum(transformacion == 0)
print('PIXELES NEGROS:', pixeles_negros)



cv2.imshow("img_binarizada", transformacion)
cv2.waitKey(0)
cv2.destroyAllWindows()

