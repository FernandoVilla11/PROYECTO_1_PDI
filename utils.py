import math
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

    # ========== GRÁFICAS BÁSICAS ==========
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

    # ========== ANÁLISIS TEÓRICO vs EXPERIMENTAL ==========
    if len(x) > 3 and len(y) > 3:  # Necesitamos suficientes puntos para el ajuste
        print("\n🔄 Generando comparación con trayectoria teórica...")
        
        # Ajustar modelo parabólico a los datos experimentales
        tiempos_ajuste = tiempos[:len(x)]
        parametros = ajustar_modelo_parabolico(tiempos_ajuste, x, y)
        x0, vx0, y0, vy0, g = parametros
        
        # Calcular trayectoria teórica
        x_teorica, y_teorica = calcular_trayectoria_teorica(tiempos_ajuste, x0, vx0, y0, vy0, g)
        
        # Calcular velocidades teóricas
        tiempos_vel = tiempos[1:len(vx)+1] if len(vx) < len(tiempos) else tiempos[:len(vx)]
        vx_teorica, vy_teorica, v_teorica = calcular_velocidad_teorica(tiempos_vel, vx0, vy0, g)
        
        # Graficar comparación
        graficar_comparacion_teorica(tiempos, x, y, vx, vy, v,
                                   x_teorica, y_teorica, vx_teorica, vy_teorica, v_teorica,
                                   parametros)
    else:
        print("\n⚠️  Pocos datos para análisis teórico (necesarios > 3 puntos)")
        print("   Ejecute por más tiempo o reduzca la velocidad del video")

    # Ajustar márgenes para que no se superpongan los nombres y leyendas
    fig.subplots_adjust(hspace=0.4, top=0.95, bottom=0.08)

    plt.show()

# ---------------------------------------Funciones para trayectoria teórica---------------------------------------

def ajustar_modelo_parabolico(tiempos, x_exp, y_exp):
    """
    Ajusta un modelo parabólico a los datos experimentales
    Retorna los parámetros del modelo: x0, vx0, y0, vy0, g
    """
    # Para X: x(t) = x0 + vx0*t (movimiento rectilíneo uniforme)
    # Ajuste lineal para X
    if len(tiempos) > 1:
        coef_x = np.polyfit(tiempos, x_exp, 1)
        vx0 = coef_x[0]  # velocidad inicial en x
        x0 = coef_x[1]   # posición inicial en x
    else:
        x0, vx0 = x_exp[0], 0
    
    # Para Y: y(t) = y0 + vy0*t + 0.5*g*t² (movimiento uniformemente acelerado)
    # Ajuste cuadrático para Y
    if len(tiempos) > 2:
        coef_y = np.polyfit(tiempos, y_exp, 2)
        g = 2 * coef_y[0]    # aceleración (2 * coeficiente de t²)
        vy0 = coef_y[1]      # velocidad inicial en y
        y0 = coef_y[2]       # posición inicial en y
    else:
        y0, vy0, g = y_exp[0], 0, 9.81
    
    return x0, vx0, y0, vy0, g

def calcular_trayectoria_teorica(tiempos, x0, vx0, y0, vy0, g):
    """
    Calcula la trayectoria teórica usando las ecuaciones de movimiento parabólico
    """
    x_teorica = x0 + vx0 * np.array(tiempos)
    y_teorica = y0 + vy0 * np.array(tiempos) + 0.5 * g * np.array(tiempos)**2
    
    return x_teorica, y_teorica

def calcular_velocidad_teorica(tiempos, vx0, vy0, g):
    """
    Calcula las velocidades teóricas
    """
    vx_teorica = np.full_like(tiempos, vx0)  # velocidad constante en x
    vy_teorica = vy0 + g * np.array(tiempos)  # velocidad variable en y
    v_teorica = np.sqrt(vx_teorica**2 + vy_teorica**2)
    
    return vx_teorica, vy_teorica, v_teorica

def calcular_metricas_error(experimental, teorica):
    """
    Calcula métricas de error entre datos experimentales y teóricos
    """
    experimental = np.array(experimental)
    teorica = np.array(teorica)
    
    # Asegurar que ambos arrays tengan la misma longitud
    min_len = min(len(experimental), len(teorica))
    experimental = experimental[:min_len]
    teorica = teorica[:min_len]
    
    # Error cuadrático medio (RMSE)
    rmse = np.sqrt(np.mean((experimental - teorica)**2))
    
    # Error absoluto medio (MAE)
    mae = np.mean(np.abs(experimental - teorica))
    
    # Coeficiente de determinación (R²)
    ss_res = np.sum((experimental - teorica)**2)
    ss_tot = np.sum((experimental - np.mean(experimental))**2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    return rmse, mae, r2

def graficar_comparacion_teorica(tiempos, x_exp, y_exp, vx_exp, vy_exp, v_exp, 
                                x_teo, y_teo, vx_teo, vy_teo, v_teo,
                                parametros_modelo):
    """
    Grafica la comparación entre datos experimentales y teóricos
    """
    x0, vx0, y0, vy0, g = parametros_modelo
    
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    
    # --- Trayectoria X vs Tiempo ---
    axs[0,0].plot(tiempos[:len(x_exp)], x_exp, 'bo-', label='Experimental', markersize=4)
    axs[0,0].plot(tiempos[:len(x_teo)], x_teo, 'r-', label='Teórico', linewidth=2)
    axs[0,0].set_title('Posición X vs Tiempo')
    axs[0,0].set_xlabel('Tiempo (s)')
    axs[0,0].set_ylabel('Posición X (m)')
    axs[0,0].legend()
    axs[0,0].grid(True, alpha=0.3)
    
    # Calcular y mostrar métricas para X
    rmse_x, mae_x, r2_x = calcular_metricas_error(x_exp, x_teo[:len(x_exp)])
    axs[0,0].text(0.05, 0.95, f'R² = {r2_x:.3f}\nRMSE = {rmse_x:.4f} m', 
                  transform=axs[0,0].transAxes, verticalalignment='top',
                  bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # --- Trayectoria Y vs Tiempo ---
    axs[0,1].plot(tiempos[:len(y_exp)], y_exp, 'bo-', label='Experimental', markersize=4)
    axs[0,1].plot(tiempos[:len(y_teo)], y_teo, 'r-', label='Teórico', linewidth=2)
    axs[0,1].set_title('Posición Y vs Tiempo')
    axs[0,1].set_xlabel('Tiempo (s)')
    axs[0,1].set_ylabel('Posición Y (m)')
    axs[0,1].legend()
    axs[0,1].grid(True, alpha=0.3)
    
    # Calcular y mostrar métricas para Y
    rmse_y, mae_y, r2_y = calcular_metricas_error(y_exp, y_teo[:len(y_exp)])
    axs[0,1].text(0.05, 0.95, f'R² = {r2_y:.3f}\nRMSE = {rmse_y:.4f} m', 
                  transform=axs[0,1].transAxes, verticalalignment='top',
                  bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # --- Trayectoria X vs Y ---
    axs[1,0].plot(x_exp, y_exp, 'bo-', label='Experimental', markersize=4)
    axs[1,0].plot(x_teo, y_teo, 'r-', label='Teórico', linewidth=2)
    axs[1,0].set_title('Trayectoria (X vs Y)')
    axs[1,0].set_xlabel('Posición X (m)')
    axs[1,0].set_ylabel('Posición Y (m)')
    axs[1,0].legend()
    axs[1,0].grid(True, alpha=0.3)
    axs[1,0].invert_yaxis()
    
    # --- Velocidad vs Tiempo ---
    min_len_v = min(len(vx_exp), len(vy_exp), len(v_exp))
    axs[1,1].plot(tiempos[1:min_len_v+1], vx_exp[:min_len_v], 'b-', label='Vx Experimental', alpha=0.7)
    axs[1,1].plot(tiempos[1:min_len_v+1], vy_exp[:min_len_v], 'g-', label='Vy Experimental', alpha=0.7)
    axs[1,1].plot(tiempos[1:len(vx_teo)+1], vx_teo, 'b--', label='Vx Teórico', linewidth=2)
    axs[1,1].plot(tiempos[1:len(vy_teo)+1], vy_teo, 'g--', label='Vy Teórico', linewidth=2)
    axs[1,1].set_title('Velocidades vs Tiempo')
    axs[1,1].set_xlabel('Tiempo (s)')
    axs[1,1].set_ylabel('Velocidad (m/s)')
    axs[1,1].legend()
    axs[1,1].grid(True, alpha=0.3)
    
    # Información del modelo en la gráfica de velocidad
    info_texto = f'Modelo Parabólico:\nx₀ = {x0:.3f} m\nvₓ₀ = {vx0:.3f} m/s\ny₀ = {y0:.3f} m\nvᵧ₀ = {vy0:.3f} m/s\ng = {g:.3f} m/s²'
    axs[1,1].text(0.98, 0.98, info_texto, transform=axs[1,1].transAxes, 
                  verticalalignment='top', horizontalalignment='right',
                  bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.show()
    
    # Imprimir resumen estadístico
    print("\n" + "="*60)
    print("📊 ANÁLISIS DE COMPARACIÓN TEÓRICA vs EXPERIMENTAL")
    print("="*60)
    print(f"📏 Parámetros del modelo parabólico:")
    print(f"   • Posición inicial X: {x0:.4f} m")
    print(f"   • Velocidad inicial X: {vx0:.4f} m/s")
    print(f"   • Posición inicial Y: {y0:.4f} m")
    print(f"   • Velocidad inicial Y: {vy0:.4f} m/s")
    print(f"   • Aceleración gravitacional: {g:.4f} m/s²")
    print(f"\n📈 Métricas de ajuste:")
    print(f"   • Posición X - R²: {r2_x:.4f}, RMSE: {rmse_x:.6f} m")
    print(f"   • Posición Y - R²: {r2_y:.4f}, RMSE: {rmse_y:.6f} m")
    print(f"\n💡 Interpretación:")
    if r2_x > 0.95 and r2_y > 0.95:
        print("   ✅ Excelente ajuste del modelo teórico")
    elif r2_x > 0.90 and r2_y > 0.90:
        print("   ✅ Buen ajuste del modelo teórico")
    elif r2_x > 0.80 and r2_y > 0.80:
        print("   ⚠️  Ajuste moderado - posible ruido o desviaciones")
    else:
        print("   ❌ Ajuste pobre - revisar detección o condiciones experimentales")
    print("="*60)