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
- **NumPy** - Cálculos numéricos y análisis matemático
- **Matplotlib** - Gráficas de análisis y comparación
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

###  **Ejecutar el programa**
```bash
python main.py
```

###  **Controles y Funcionalidades**

#### **Controles Básicos**
- **`Q`** o **`ESC`**: Salir del programa y cerrar todas las ventanas
- **`P`**: Pausar el video para realizar calibración manual

#### **Proceso de Calibración (Modo Pausa)**
1. **Pausar**: Presiona `P` durante la reproducción del video
2. **Seleccionar puntos**: 
   - Haz **clic izquierdo** en el primer punto de referencia
   - Haz **clic izquierdo** en el segundo punto de referencia
   - Se dibujará automáticamente una línea roja entre los puntos
3. **Confirmar calibración**: Presiona `C` después de seleccionar los 2 puntos
   - El programa pedirá ingresar la **distancia real** en metros
   - Ejemplo: Si los puntos están separados 1.5 metros, ingresa `1.5`
4. **Opciones adicionales**:
   - **`R`**: Reanudar sin calibrar (mantiene escala en píxeles)
   - **`C`**: Confirmar y aplicar la calibración métrica

#### **Ventanas del Programa**
El programa abre **2 ventanas simultáneamente**:

1. **Ventana Principal "Frame"**:
   - Muestra el video original con tracking en tiempo real
   - Información superpuesta: posición, velocidad, aceleración
   - Trayectoria completa del objeto (línea verde)
   - Centro del objeto detectado (círculo rojo)

2. **Ventana "Apertura (Open)"**:
   - Muestra la máscara de detección procesada
   - Visualización en blanco y negro del objeto detectado
   - Útil para verificar la calidad de la detección

#### **Información Mostrada en Pantalla**
Durante la ejecución se muestra en tiempo real:
- **Posición**: Coordenadas X e Y en píxeles
- **Velocidad**: Componentes Vx, Vy y velocidad total
- **Aceleración**: Componentes Ax, Ay y aceleración total

#### **Flujo de Trabajo Recomendado**
1. **Ejecutar** el programa con `python main.py`
2. **Observar** el tracking automático durante unos segundos
3. **Pausar** con `P` cuando desees calibrar la escala
4. **Seleccionar** dos puntos con distancia conocida
5. **Ingresar** la distancia real en metros
6. **Continuar** el análisis con datos calibrados
7. **Salir** con `Q` cuando termine el video o desees parar

#### **Resultados Automáticos**
Al finalizar la ejecución se generan automáticamente:
- **Gráficas básicas** de análisis cinemático (posición, velocidad, aceleración vs tiempo)
- **Análisis comparativo** entre trayectoria experimental y teórica
- **Métricas de ajuste**: Coeficiente R², RMSE, Error Absoluto Medio
- **Parámetros del modelo**: Velocidades iniciales, posición inicial, aceleración gravitacional
- **Archivo Excel** con todos los datos calculados (`resultados/resultados.xlsx`)

#### **Consejos de Uso**
-  **Iluminación**: Asegúrate de que el objeto verde sea claramente visible
-  **Calibración**: Usa objetos de tamaño conocido para mejor precisión
-  **Pausa oportuna**: Calibra cuando el objeto esté bien visible y estático
-  **Precisión**: Haz clic exactamente en los puntos de referencia deseados

##  Funcionalidades

### 🎯 **Procesamiento de Imagen**
- **Detección por color HSV** para objetos verdes
- **Operaciones morfológicas** para reducir ruido
- **Cálculo de centroide** para posicionamiento preciso

### 📊 **Análisis Cinemático**
- **Cálculo de trayectoria** en tiempo real
- **Análisis cinemático**: posición, velocidad, aceleración
- **Calibración manual** para conversión píxeles → metros
- **Visualización en tiempo real** con datos superpuestos

### 🔬 **Comparación Teórica vs Experimental**
- **Ajuste automático** de modelo parabólico a datos experimentales
- **Cálculo de trayectoria teórica** usando ecuaciones de movimiento
- **Métricas de precisión**: R², RMSE, Error Absoluto Medio
- **Gráficas comparativas** lado a lado
- **Análisis estadístico** automático del ajuste

### 💾 **Exportación de Resultados**
### 💾 **Exportación de Resultados**
- **Exportación automática** de resultados a Excel
- **Gráficas interactivas** con Matplotlib
- **Reportes estadísticos** detallados en consola

##  Resultados

### 📈 **Gráficas Generadas Automáticamente**
El sistema genera dos conjuntos de gráficas:

1. **Gráficas Básicas**:
   - Trayectoria experimental (X vs Y)
   - Velocidad vs tiempo (Vx, Vy, V total)
   - Aceleración vs tiempo (Ax, Ay, A total)

2. **Análisis Comparativo Teórico**:
   - Posición X vs Tiempo (experimental vs teórico)
   - Posición Y vs Tiempo (experimental vs teórico)
   - Trayectoria completa (experimental vs teórico)
   - Velocidades vs Tiempo (experimental vs teórico)

### 📊 **Métricas Estadísticas**
- **Coeficiente de determinación (R²)**: Calidad del ajuste (0-1)
- **Error cuadrático medio (RMSE)**: Precisión en metros
- **Error absoluto medio (MAE)**: Desviación promedio
- **Parámetros del modelo**: x₀, vₓ₀, y₀, vᵧ₀, g

### 📋 **Archivo Excel Exportado**

##  Configuración
- **Rango de color verde**: Ajustable en `procesamiento.py`
- **Operaciones morfológicas**: Kernel configurable
- **Tamaño de texto**: Modificable en las funciones de visualización

##  Contacto
Para consultas, contactar a los integrantes a través de sus correos institucionales.

---
*Proyecto desarrollado para el curso de Procesamiento Digital de Imágenes - UdeA*
