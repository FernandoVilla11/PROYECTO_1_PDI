import cv2
import numpy as np
import math
from utils import calcular_velocidad, calcular_aceleracion, graficar_resultados, guardar_tablas_excel

# ----------------- CALLBACK MOUSE -----------------
def mouse_callback(event, x, y, flags, param):
    ref_points, paused_frame = param
    if paused_frame[0] is None:
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        ref_points.append((x, y))
        cv2.circle(paused_frame[0], (x, y), 5, (0, 0, 255), -1)
        if len(ref_points) == 2:
            cv2.line(paused_frame[0], ref_points[0], ref_points[1], (0, 0, 255), 2)
        cv2.imshow("Frame", paused_frame[0])


# ----------------- PROCESAR VIDEO -----------------
def procesar_video(VIDEO_PATH):
    cap = cv2.VideoCapture(VIDEO_PATH)

    # Rangos para el color verde
    LOWER_GREEN = np.array([35, 50, 50])
    UPPER_GREEN = np.array([85, 255, 255])

    ref_points = []
    meters_per_pixel = None
    paused_frame = [None]
    fps = cap.get(cv2.CAP_PROP_FPS)
    prev_cx, prev_cy = None, None
    prev_vx, prev_vy = None, None
    tiempo_actual = 0

    posiciones, velocidades, aceleraciones, tiempos = [], [], [], []

    if not cap.isOpened():
        print("❌ No se pudo abrir el video")
        return

    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame", mouse_callback, param=(ref_points, paused_frame))

    while True:
        ret, frame = cap.read()
        if not ret:
            print("✅ Video terminado.")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
        
        # ---- OPERACIONES MORFOLÓGICAS ----
        kernel = np.ones((5,5), np.uint8)  # kernel de 5x5

        mask_erode = cv2.erode(mask, kernel, iterations=1)
        mask_dilate = cv2.dilate(mask, kernel, iterations=1)
        mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask_close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Mostrar todas las máscaras morfológicas
        # cv2.imshow("Mascara Original", mask)
        # cv2.imshow("Erosion", mask_erode)
        # cv2.imshow("Dilatacion", mask_dilate)
        cv2.imshow("Sin operacion morfologica", mask)
        cv2.imshow("Apertura (Open)", mask_open)
        # cv2.imshow("Cierre (Close)", mask_close)

        M = cv2.moments(mask_open)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            posiciones.append((cx, cy))
            tiempos.append(tiempo_actual)

            for i in range(1, len(posiciones)):
                cv2.line(frame, posiciones[i-1], posiciones[i], (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            if prev_cx is not None:
                vx, vy, v = calcular_velocidad(prev_cx, prev_cy, cx, cy, fps)
                velocidades.append((vx, vy, v))
                if prev_vx is not None:
                    ax, ay, a = calcular_aceleracion(prev_vx, prev_vy, vx, vy, fps)
                    aceleraciones.append((ax,ay,a))

                    # Mostrar posicion en px
                    texto_px = f"Pos_x={cx:.1f}px"
                    cv2.putText(frame, texto_px, (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    texto_px = f"Pos_y={cy:.1f}px"
                    cv2.putText(frame, texto_px, (230, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
                    # Mostrar velocidad en px/s
                    texto_px = f"Vel={v:.1f}px/s"
                    cv2.putText(frame, texto_px, (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    texto_px = f"Vel_x={vx:.1f}px/s"
                    cv2.putText(frame, texto_px, (230, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    texto_px = f"Vel_y={vy:.1f}px/s"
                    cv2.putText(frame, texto_px, (460, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
                    # Mostrar aceleracion en px/s^2
                    texto_px = f"Ace={a:.1f}px/s2"
                    cv2.putText(frame, texto_px, (10, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    texto_px = f"Ace_x={ax:.1f}px/s2"
                    cv2.putText(frame, texto_px, (230, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    texto_px = f"Ace_y={ay:.1f}px/s2"
                    cv2.putText(frame, texto_px, (460, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                prev_vx, prev_vy = vx, vy

            prev_cx, prev_cy = cx, cy

        cv2.imshow("Frame", frame)

        k = cv2.waitKey(30) & 0xFF
        if k == ord('q'):
            break
        if k == ord('p'):
            print("⏸ Pausa. Selecciona 2 puntos para calibrar.")
            paused_frame[0] = frame.copy()
            ref_points.clear()
            cv2.imshow("Frame", paused_frame[0])
            while True:
                key2 = cv2.waitKey(0) & 0xFF
                if key2 == ord('c'):
                    if len(ref_points) == 2:
                        dx = ref_points[1][0] - ref_points[0][0]
                        dy = ref_points[1][1] - ref_points[0][1]
                        pixel_dist = math.sqrt(dx**2 + dy**2)
                        real_len = float(input("Introduce la longitud real (m): "))
                        meters_per_pixel = real_len / pixel_dist
                        print(f"✅ Escala definida: {meters_per_pixel:.6f} m/px")
                    paused_frame[0] = None
                    break
                elif key2 == ord('r'):
                    print("▶️ Reanudar sin calibrar.")
                    paused_frame[0] = None
                    break

        tiempo_actual += 1 / fps

    cap.release()
    cv2.destroyAllWindows()

    # Graficar resultados en m/s y m/s²
    if posiciones and velocidades and meters_per_pixel is not None:
        graficar_resultados(tiempos, posiciones, velocidades, aceleraciones, meters_per_pixel)
        guardar_tablas_excel(tiempos, posiciones, velocidades, aceleraciones)

