import cv2
import numpy as np

def calcular_distancia_euclidiana(ojo):
    """Calcula las distancias geométricas (Plan A) para detectar somnolencia."""
    A = np.linalg.norm(np.array([ojo[1].x, ojo[1].y]) - np.array([ojo[5].x, ojo[5].y]))
    B = np.linalg.norm(np.array([ojo[2].x, ojo[2].y]) - np.array([ojo[4].x, ojo[4].y]))
    C = np.linalg.norm(np.array([ojo[0].x, ojo[0].y]) - np.array([ojo[3].x, ojo[3].y]))
    return (A + B) / (2.0 * C)

def evaluar_mirada_esclerotica(frame, puntos_ojo):
    """Binariza los tonos con un umbral adaptativo a la luz actual (Plan B)."""
    xs = [p.x for p in puntos_ojo]
    ys = [p.y for p in puntos_ojo]
    roi = frame[min(ys):max(ys), min(xs):max(xs)]
    
    if roi.size == 0: return "Frente"
    
    gris = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    umbral_dinamico = np.mean(gris) * 0.8
    _, binario = cv2.threshold(gris, umbral_dinamico, 255, cv2.THRESH_BINARY)
    
    mitad = binario.shape[1] // 2
    izq_blanco = cv2.countNonZero(binario[:, 0:mitad])
    der_blanco = cv2.countNonZero(binario[:, mitad:])
    
    if izq_blanco > der_blanco * 1.7:
        return "Mirando Derecha"
    elif der_blanco > izq_blanco * 1.7:
        return "Mirando Izquierda"
    return "Frente"