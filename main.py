import cv2
import dlib
import numpy as np
import winsound

from auditoria import inicializar_caja_negra, registrar_evento
from procesamiento import calcular_distancia_euclidiana, evaluar_mirada_esclerotica

inicializar_caja_negra()
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

cap = cv2.VideoCapture(0)
historial_ear = []

# VARIABLE DE ESTADO: Recuerda qué está sonando para no repetirlo
estado_audio_actual = "FRENTE" 

while True:
    ret, frame = cap.read()
    if not ret: break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rostros = detector(gray)
    
    # Por defecto, asumimos que todo está normal en cada fotograma
    estado_detectado = "FRENTE"
        
    for rostro in rostros:
        marcas = predictor(gray, rostro)
        ojo_izq = [marcas.part(i) for i in range(36, 42)]
        ojo_der = [marcas.part(i) for i in range(42, 48)]
        
        ear_izq = calcular_distancia_euclidiana(ojo_izq)
        ear_der = calcular_distancia_euclidiana(ojo_der)
        ear_promedio = (ear_izq + ear_der) / 2.0
        
        historial_ear.append(ear_promedio)

        # ---> PEGAR ESTE BLOQUE AQUÍ <---
        # Dibujar los recuadros y los 6 puntos verdes en cada ojo
        for ojo in [ojo_izq, ojo_der]:
            xs = [p.x for p in ojo]
            ys = [p.y for p in ojo]
            
            # Dibuja el rectángulo delimitador
            cv2.rectangle(frame, (min(xs), min(ys)), (max(xs), max(ys)), (0, 255, 0), 1)
            
            # Dibuja los puntos individuales del contorno
            for p in ojo:
                cv2.circle(frame, (p.x, p.y), 2, (0, 255, 0), -1)
        # -----------------------------------
        
        # 1. Anti-Trampas
        if len(historial_ear) > 20:
            historial_ear.pop(0)
            if np.std(historial_ear) < 0.002: 
                cv2.putText(frame, "SERVICIO NO DISPONIBLE", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 3)
                registrar_evento(frame, "SERVICIO_INACTIVO", "Foto estatica detectada")
                historial_ear = [] 
                continue
        
        # 2. EVALUACIÓN DE PRIORIDADES (Somnolencia vs Distracción)
        if ear_promedio < 0.19: 
            estado_detectado = "SOMNOLENCIA"
            cv2.putText(frame, "ALERTA: SOMNOLENCIA", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            # Solo guardamos registro en el Excel 1 de cada 10 veces para no saturar el PC
            if len(historial_ear) % 10 == 0:
                registrar_evento(frame, "ALERTA", "Baja distancia parpados")
                
        else: # Solo evalúa distracción si los ojos están abiertos
            mirada = evaluar_mirada_esclerotica(frame, ojo_izq)
            if mirada != "Frente":
                estado_detectado = "DISTRACCION"
                cv2.putText(frame, f"DISTRACCION: {mirada}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # 3. CONTROLADOR INTELIGENTE DE AUDIO
        # Solo ejecuta órdenes de sonido si tu comportamiento acaba de cambiar
        if estado_detectado != estado_audio_actual:
            if estado_detectado == "SOMNOLENCIA":
                # Reproduce sonido de sueño en bucle ininterrumpido (Loop)
                winsound.PlaySound("somnolencia.wav", winsound.SND_ASYNC | winsound.SND_LOOP)
            elif estado_detectado == "DISTRACCION":
                # Reproduce sonido de distracción en bucle ininterrumpido (Loop)
                winsound.PlaySound("distraccion.wav", winsound.SND_ASYNC | winsound.SND_LOOP)
            elif estado_detectado == "FRENTE":
                # Apaga por completo cualquier sonido que esté sonando
                winsound.PlaySound(None, winsound.SND_PURGE)
            
            # Actualiza la memoria del sistema
            estado_audio_actual = estado_detectado

        # Textos numéricos
        cv2.putText(frame, f"EAR: {ear_promedio:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Sistema Hibrido de Auditoria", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
# Asegurarse de apagar el sonido al cerrar el programa
winsound.PlaySound(None, winsound.SND_PURGE)
cv2.destroyAllWindows()