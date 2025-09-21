import math
import os
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------Calcular velocidad entre dos posiciones---------------------------------------
def calcular_velocidad(prev_cx, prev_cy, cx, cy, fps):
    dt = 1 / fps
    dx = cx - prev_cx
    dy = cy - prev_cy
    vx = dx / dt
    vy = dy / dt
    v = math.sqrt(vx**2 + vy**2)
    return vx, vy, v

# ---------------------------------------Calcular aceleración entre dos velocidades---------------------------------------
def calcular_aceleracion(vx_prev, vy_prev, vx, vy, fps):
    dt = 1 / fps
    ax = (vx - vx_prev) / dt
    ay = (vy - vy_prev) / dt
    a = math.sqrt(ax**2 + ay**2)
    return ax, ay, a


#---------------------------------------Convertir de pixeles a metros---------------------------------------
def convertir_a_metros(v, meters_per_pixel):
    v_m = v * meters_per_pixel
    return v_m

# ---------------------------------------Generar archivo de excel---------------------------------------
def guardar_tablas_excel(tiempos, posiciones, velocidades, aceleraciones, carpeta="resultados", archivo="resultados.xlsx"):
    # 1️⃣ Crear la carpeta si no existe
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
        print(f"Carpeta '{carpeta}' creada.")

    # 2️⃣ Ajustar longitudes de listas
    len_pos = len(posiciones)
    len_vel = len(velocidades)
    len_acel = len(aceleraciones)

    # Recortar tiempos para que coincidan con la longitud de cada variable
    tiempos_pos = tiempos[:len_pos]
    tiempos_vel = tiempos[1:len_vel+1] if len_vel < len(tiempos) else tiempos[:len_vel]
    tiempos_acel = tiempos[2:len_acel+2] if len_acel < len(tiempos) else tiempos[:len_acel]

    # Limpiar velocidades y aceleraciones (solo 2 valores por fila)
    velocidades_limpias = [(vx, vy) for vx, vy, *rest in velocidades]
    aceleraciones_limpias = [(ax, ay) for ax, ay, *rest in aceleraciones]

    # 3️⃣ Crear DataFrames
    df_pos = pd.DataFrame(posiciones, columns=["X", "Y"])
    df_pos["Tiempo"] = tiempos_pos
    df_pos = df_pos[["Tiempo", "X", "Y"]]

    df_vel = pd.DataFrame(velocidades_limpias, columns=["Vx", "Vy"])
    df_vel["Tiempo"] = tiempos_vel
    df_vel = df_vel[["Tiempo", "Vx", "Vy"]]

    df_acel = pd.DataFrame(aceleraciones_limpias, columns=["Ax", "Ay"])
    df_acel["Tiempo"] = tiempos_acel
    df_acel = df_acel[["Tiempo", "Ax", "Ay"]]

    # 4️⃣ Guardar todo en un solo archivo Excel con tres hojas
    ruta_archivo = os.path.join(carpeta, archivo)
    with pd.ExcelWriter(ruta_archivo) as writer:
        df_pos.to_excel(writer, sheet_name="Posiciones", index=False)
        df_vel.to_excel(writer, sheet_name="Velocidades", index=False)
        df_acel.to_excel(writer, sheet_name="Aceleraciones", index=False)

    print(f"Archivo Excel guardado correctamente en '{ruta_archivo}'")
  
# ---------------------------------------Graficar resultados---------------------------------------  
def graficar_resultados(tiempos, posiciones, velocidades, aceleraciones, meters_per_pixel):
    # Convertir posiciones y velocidades a metros y m/s    
    
    x = [convertir_a_metros(p[0], meters_per_pixel) for p in posiciones]
    y = [convertir_a_metros(p[1], meters_per_pixel) for p in posiciones]
    
    vx = [convertir_a_metros(v[0], meters_per_pixel) for v in velocidades]
    vy = [convertir_a_metros(v[1], meters_per_pixel) for v in velocidades]
    v = [convertir_a_metros(v[2], meters_per_pixel) for v in velocidades]
    
    ax = [convertir_a_metros(a[0], meters_per_pixel) for a in aceleraciones]
    ay = [convertir_a_metros(a[1], meters_per_pixel) for a in aceleraciones]
    a = [convertir_a_metros(a[2], meters_per_pixel) for a in aceleraciones]

    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    # --- Trayectoria ---
    axs[0].plot(x, y, 'o-', label="Experimental")
    axs[0].set_title("Trayectoria")
    axs[0].set_xlabel("x (m)")
    axs[0].set_ylabel("y (m)")
    axs[0].invert_yaxis()
    axs[0].legend()
    axs[0].grid(True)

    # --- Velocidad ---
    axs[1].plot(tiempos[:len(vx)], vx, 'r-', label="Vx")
    axs[1].plot(tiempos[:len(vy)], vy, 'g-', label="Vy")
    axs[1].plot(tiempos[:len(v)], v, 'b-', label="V")
    axs[1].set_title("Velocidad")
    axs[1].set_xlabel("Tiempo (s)")
    axs[1].set_ylabel("Velocidad (m/s)")
    axs[1].legend()
    axs[1].grid(True)

    # --- Aceleración ---
    axs[2].plot(tiempos[:len(ax)], ax, 'r-', label="Ax")
    axs[2].plot(tiempos[:len(ay)], ay, 'g-', label="Ay")
    axs[2].plot(tiempos[:len(a)], a, 'b-', label="A")
    axs[2].set_title("Aceleración")
    axs[2].set_xlabel("Tiempo (s)")
    axs[2].set_ylabel("Aceleración (m/s²)")
    axs[2].legend()
    axs[2].grid(True)

    # Ajustar márgenes para que no se superpongan los nombres y leyendas
    fig.subplots_adjust(hspace=0.4, top=0.95, bottom=0.08)

    plt.show()