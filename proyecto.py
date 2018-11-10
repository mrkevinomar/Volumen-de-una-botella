import numpy as np
import cv2



def escribirTexto(imagen , texto , x ,y):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(imagen, texto,(x,y), font, 0.5,(0,0,255),1,cv2.LINE_AA)

captura = cv2.VideoCapture(0)
while(True):
    ret , frame_original = captura.read()


    # Cambiar imagen original a gris
    img_gray = cv2.cvtColor(frame_original, cv2.COLOR_BGR2GRAY)


    # Suaviza imagen
    img_suavizada = cv2.GaussianBlur(img_gray, (9, 9), 0)

    # Binarizar imagen
    thresh, img_binarizada = cv2.threshold(img_suavizada, 220, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    im_floodfill_inv = cv2.bitwise_not(img_binarizada)

    #Crear un kernel de '1'
    kernel = np.ones((9,9),np.uint8)

    #Se aplica la transformacion: Closing
    transformacion = cv2.morphologyEx(im_floodfill_inv,cv2.MORPH_CLOSE,kernel)

    image, ctrs, hier = cv2.findContours(transformacion.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # obtenemos  los rectangulos
    rects = [cv2.boundingRect(ctr) for ctr in ctrs]


  #  cv2.rectangle(frame_original,(x,y),(x+w,y+h),(255,0,0),2)

    #obtenemos el contorno mas grande
    pixeles_blancos = 0
    volumen_liquido = 0
    distancia_botella =0
    if(len(ctrs) > 0):
        contornoMayor = max(ctrs, key = cv2.contourArea)
        xo,yo,ancho,alto = cv2.boundingRect(contornoMayor)
        cv2.rectangle(frame_original,(xo,yo),(xo+ancho,yo+alto),(255,0,0),2)

        #obtenemos el roi en base a el contorno obtenido
        liquido=transformacion[yo:yo+alto,xo:xo+ancho]
        pixeles_blancos = np.sum(transformacion == 255)
        cv2.imshow("ROI",liquido)

    escribirTexto(frame_original, "Pixeles Liquido :"+str(pixeles_blancos) , 20,20)
    escribirTexto(frame_original, "Volumen Liquido :"+str(volumen_liquido) +" cm3" , 20,40)
    escribirTexto(frame_original, "Distancia Botella :"+str(distancia_botella) +" cm" , 20,60)

    cv2.imshow("Video", frame_original)



    key = cv2.waitKey(33) #Retraso en milisegundos para leer el siguiente frame
    #Termina presionando la tecla Esc
    if (key==27):
        break

cv2.destroyAllWindows()


## Cargar imagen original (hay que hacerlo mediante la camara)
#img_original  = cv2.imread("Imagenes/botella5.jpeg")
#cv2.imshow("img_original", img_original)
#
## Cambiar imagen original a gris
#img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
#
#
## Suaviza imagen
#img_suavizada = cv2.GaussianBlur(img_gray, (9, 9), 0)
#
## Binarizar imagen
#thresh, img_binarizada = cv2.threshold(img_suavizada, 220, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#im_floodfill_inv = cv2.bitwise_not(img_binarizada)
#
##Crear un kernel de '1'
#kernel = np.ones((9,9),np.uint8)
#
##Se aplica la transformacion: Closing
#transformacion = cv2.morphologyEx(im_floodfill_inv,cv2.MORPH_CLOSE,kernel)
#
#image, ctrs, hier = cv2.findContours(transformacion.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
## obtenemos  los rectangulos
#rects = [cv2.boundingRect(ctr) for ctr in ctrs]
#
##obtenemos el contorno mas grande
#contornoMayor = max(ctrs, key = cv2.contourArea)
#xo,yo,ancho,alto = cv2.boundingRect(contornoMayor)
##obtenemos el roi en base a el contorno obtenido
#liquido=transformacion[yo:yo+alto,xo:xo+ancho]
#
#
#
#cv2.imshow("Liquido", liquido)
#
#pixeles_blancos = np.sum(transformacion == 255)
#print('PIXELES BLANCOS:', pixeles_blancos)
#
#pixeles_negros = np.sum(transformacion == 0)
#print('PIXELES NEGROS:', pixeles_negros)
#
#
#
#cv2.imshow("img_binarizada", transformacion)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#
