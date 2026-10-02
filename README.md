# Sistema Híbrido de Detección de Somnolencia y Distracción 🚘👁️

Este proyecto es un sistema de visión computacional diseñado para prevenir accidentes de tránsito. Utiliza una arquitectura híbrida que combina geometría facial (EAR) y Eye Tracking (análisis de la esclerótica) para evaluar el estado del conductor en tiempo real.

## 🚀 Características Principales
1. **Detección de Somnolencia (Plan A):** Calcula la Distancia Euclidiana (Pitágoras) de los párpados usando `dlib`. Inmune a los cambios de luz.
2. **Detección de Distracción (Plan B):** Binariza el área de los ojos para rastrear la esclerótica y la pupila mediante un umbral dinámico adaptativo.
3. **Sistema Anti-Trampas:** Evalúa la desviación estándar del movimiento ocular para detectar si la cámara está siendo engañada con fotografías estáticas.
4. **Auditoría ("Caja Negra"):** Registra automáticamente la fecha, hora y el tipo de infracción en un archivo `.csv` y toma una captura fotográfica como evidencia.

## 🛠️ Tecnologías Utilizadas
* Python 3.x
* OpenCV (`cv2`)
* Dlib (Detector facial y 68 landmarks)
* NumPy (Cálculos matemáticos y desviación estándar)

## ⚙️ Instalación y Uso
1. Clona este repositorio: `git clone https://github.com/tu-usuario/detector-somnolencia.git`
2. Instala las dependencias: `pip install opencv-python dlib numpy`
3. **Importante:** Descarga el modelo preentrenado [shape_predictor_68_face_landmarks.dat][(http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2](https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2), descomprímelo y colócalo en la raíz del proyecto.
4. Añade dos archivos de audio cortos en la raíz con los nombres `somnolencia.wav` y `distraccion.wav`.
5. Ejecuta el sistema: `python main.py`

## 📁 Estructura del Proyecto
* `main.py`: Controlador principal de la cámara y de estados.
* `procesamiento.py`: Motores matemáticos para somnolencia y distracción.
* `auditoria.py`: Generación automática de logs y capturas de evidencia.
