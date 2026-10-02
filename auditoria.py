import os
import csv
import cv2
from datetime import datetime

ARCHIVO_LOG = "caja_negra.csv"

def inicializar_caja_negra():
    """Crea la estructura de carpetas y el archivo log si no existen."""
    if not os.path.exists("evidencias"):
        os.makedirs("evidencias")
        
    if not os.path.exists(ARCHIVO_LOG):
        with open(ARCHIVO_LOG, mode='w', newline='') as f:
            csv.writer(f).writerow(["Timestamp", "Evento", "Detalle"])

def registrar_evento(frame, evento, detalle):
    """Guarda el registro de tiempo y toma la fotografía de evidencia."""
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp_img = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with open(ARCHIVO_LOG, mode='a', newline='') as f:
        csv.writer(f).writerow([timestamp_str, evento, detalle])
        
    cv2.imwrite(f"evidencias/{evento}_{timestamp_img}.jpg", frame)