#  Proyecto: Análisis de Movimiento Parabólico

**Universidad de Antioquia - Facultad de Ingeniería**  
**Curso:** Procesamiento Digital de Imágenes (PDI)

##  Integrantes
- **Andrés Felipe Giraldo Yusti** - andres.giraldoy@udea.edu.co  
- **Jose Fernando Albornoz** - jose.albornoz@udea.edu.co

##  Descripción
Este proyecto implementa un sistema de **tracking de objetos en tiempo real** para analizar el movimiento parabólico de una pelota utilizando técnicas de procesamiento digital de imágenes con Python y OpenCV.

###  Objetivos
- Detectar automáticamente objetos verdes en movimiento
- Calcular posición, velocidad y aceleración en tiempo real
- Generar análisis cinemático completo
- Exportar resultados a archivos Excel
- Permitir calibración de escala métrica

##  Tecnologías
- **Python 3.13+**
- **OpenCV** - Procesamiento de video e imágenes
- **NumPy** - Cálculos numéricos
- **Matplotlib** - Gráficas de análisis
- **Pandas** - Manipulación de datos
- **Openpyxl** - Exportación a Excel

##  Estructura del Proyecto
```
PROYECTO_1_PDI/
├── main.py              # Archivo principal
├── procesamiento.py     # Lógica de procesamiento
├── utils.py            # Funciones de cálculo y gráficas
├── README.md           # Documentación
├── data/              # Videos de entrada
│   ├── PV_1.mp4
│   ├── PV_2.mp4
│   └── PV_3.mp4
└── resultados/        # Archivos de salida
    └── resultados.xlsx
```

##  Instalación
```bash
pip install opencv-python numpy matplotlib pandas openpyxl
```

##  Uso
```bash
python main.py
```

###  Controles
- **Q / ESC**: Salir del programa
- **P**: Pausar para calibración
- **C**: Confirmar calibración (después de seleccionar 2 puntos)
- **R**: Reanudar sin calibrar

##  Funcionalidades
- **Detección por color HSV** para objetos verdes
- **Operaciones morfológicas** para reducir ruido
- **Cálculo de trayectoria** en tiempo real
- **Análisis cinemático**: posición, velocidad, aceleración
- **Calibración manual** para conversión píxeles → metros
- **Visualización en tiempo real** con datos superpuestos
- **Exportación automática** de resultados

##  Resultados
El sistema genera:
1. **Tracking visual** con trayectoria completa
2. **Gráficas de análisis** (posición, velocidad, aceleración vs tiempo)
3. **Archivo Excel** con todos los datos calculados

##  Configuración
- **Rango de color verde**: Ajustable en `procesamiento.py`
- **Operaciones morfológicas**: Kernel configurable
- **Tamaño de texto**: Modificable en las funciones de visualización

##  Contacto
Para consultas, contactar a los integrantes a través de sus correos institucionales.

---
*Proyecto desarrollado para el curso de Procesamiento Digital de Imágenes - UdeA*
