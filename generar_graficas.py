import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from matplotlib.patches import FancyBboxPatch

# Set overall plot styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['figure.titlesize'] = 13

os.makedirs('img', exist_ok=True)

# -------------------------------------------------------------
# 1. Simulación Bode y Frecuencia del Filtro RC
# -------------------------------------------------------------
R = 10e3      # 10 kOhm
C = 0.1e-6    # 0.1 uF
fc = 1 / (2 * np.pi * R * C)  # ~159.15 Hz

w, mag, phase = signal.bode(([1], [R * C, 1]), w=np.logspace(0, 5, 1000) * 2 * np.pi)
f = w / (2 * np.pi)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
fig.suptitle('Respuesta en Frecuencia del Filtro Pasabajas RC [DATOS SIMULADOS]', fontweight='bold')

# Magnitud
ax1.semilogx(f, mag, 'b-', linewidth=2, label='Magnitud |H(f)|')
ax1.axvline(fc, color='r', linestyle='--', alpha=0.8, label=f'fc = {fc:.2f} Hz (-3 dB)')
ax1.axhline(-3, color='gray', linestyle=':', alpha=0.7)
ax1.scatter([fc], [-3], color='red', zorder=5)
ax1.annotate(f'-3 dB @ {fc:.1f} Hz', xy=(fc, -3), xytext=(fc * 1.5, -8),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))
ax1.set_ylabel('Magnitud (dB)')
ax1.grid(True, which='both', linestyle='--', alpha=0.5)
ax1.legend(loc='lower left')
ax1.set_ylim(-40, 2)

# Fase
ax2.semilogx(f, phase, 'g-', linewidth=2, label='Fase ∠H(f)')
ax2.axvline(fc, color='r', linestyle='--', alpha=0.8)
ax2.axhline(-45, color='gray', linestyle=':', alpha=0.7)
ax2.scatter([fc], [-45], color='red', zorder=5)
ax2.annotate('-45° @ fc', xy=(fc, -45), xytext=(fc * 1.5, -30),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))
ax2.set_xlabel('Frecuencia (Hz)')
ax2.set_ylabel('Fase (grados)')
ax2.grid(True, which='both', linestyle='--', alpha=0.5)
ax2.legend(loc='lower left')
ax2.set_ylim(-95, 5)

plt.tight_layout()
plt.savefig('img/simulacion_multisim.png', dpi=300)
plt.close()
print("Generada img/simulacion_multisim.png")

# -------------------------------------------------------------
# 2. Emulación de Osciloscopio: Antes y Después del Filtro RC
# -------------------------------------------------------------
fs = 50000  # 50 kHz sample rate
t = np.linspace(0, 0.05, int(fs * 0.05))  # 50 ms window

# Señal antes del filtro: DC (1.2V) + 60 Hz hum (0.12V) + ruido HF (conmutación)
np.random.seed(42)
v_dc = 1.2
noise_60hz = 0.12 * np.sin(2 * np.pi * 60 * t)
noise_hf = 0.08 * np.sin(2 * np.pi * 1200 * t) + 0.04 * np.random.normal(0, 1, len(t))
v_in_noisy = v_dc + noise_60hz + noise_hf

# Filtrado con el filtro RC continuo simulado
sys_rc = signal.TransferFunction([1], [R * C, 1])
tout, v_out_filtered, _ = signal.lsim(sys_rc, U=v_in_noisy, T=t, X0=[0.0])

# Gráfica estilo osciloscopio
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#1a1a1a')
ax.set_facecolor('#0d0d0d')

ax.plot(t * 1000, v_in_noisy, color='#ffeb3b', alpha=0.75, linewidth=1.2, label='CH1: Entrada al Filtro (Salida No Inversor)')
ax.plot(t * 1000, v_out_filtered, color='#00e5ff', linewidth=2.2, label='CH2: Salida Filtrada (Bornes de C)')
ax.axhline(1.2, color='#ffffff', linestyle='--', alpha=0.5, label='Nivel DC Teórico (1.20 V)')

ax.set_title('Emulación de Osciloscopio: Efecto del Filtro RC [DATOS SIMULADOS]', color='white', fontweight='bold', pad=12)
ax.set_xlabel('Tiempo (ms)', color='white')
ax.set_ylabel('Voltaje (V)', color='white')
ax.tick_params(colors='white')
ax.grid(True, color='#333333', linestyle='--', alpha=0.7)
ax.set_ylim(0.8, 1.6)

# Indicador de estado
ax.text(0.02, 0.93, 'CANAL 1 (CH1): 1.2V + Ruido\nCANAL 2 (CH2): 1.2V Filtrado',
        transform=ax.transAxes, color='white', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#262626', alpha=0.9, edgecolor='#555555'))

leg = ax.legend(loc='lower right', facecolor='#262626', edgecolor='#555555')
for text in leg.get_texts():
    text.set_color('white')

plt.tight_layout()
plt.savefig('img/osciloscopio_filtro.png', dpi=300, facecolor=fig.get_facecolor())
plt.close()
print("Generada img/osciloscopio_filtro.png")

# -------------------------------------------------------------
# 3. Respuesta Temporal del Comparador y Activación del LED
# -------------------------------------------------------------
t_comp = np.linspace(0, 20, 2000)  # 20 ms
v_sig = 1.2 / (1 + np.exp(-0.8 * (t_comp - 8)))  # sigmoide centrada en 8 ms
v_ref = 1.0  # Umbral de 1.0 V

v_comp_out = np.where(v_sig > v_ref, 10.5, 0.2)
led_current = np.where(v_sig > v_ref, (10.5 - 2.0) / 330 * 1000, 0.0)  # mA

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
fig.suptitle('Dinámica de Disparo del Comparador LM741 y Alarma LED [DATOS SIMULADOS]', fontweight='bold')

# Entradas
ax1.plot(t_comp, v_sig, 'b-', linewidth=2.2, label='Vin (Señal Acondicionada)')
ax1.axhline(v_ref, color='r', linestyle='--', linewidth=1.8, label=f'Vref = {v_ref:.1f} V (Umbral de Alarma)')
ax1.axvline(8.0, color='gray', linestyle=':', alpha=0.7)
ax1.scatter([8.0], [v_ref], color='red', s=50, zorder=5)
ax1.annotate('Punto de disparo (Vin > Vref)', xy=(8.0, v_ref), xytext=(2.0, 1.15),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))
ax1.set_ylabel('Voltaje (V)')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(loc='lower right')
ax1.set_ylim(-0.1, 1.4)

# Salida del Comparador y Estado del LED
ax2.plot(t_comp, v_comp_out, 'purple', linewidth=2.2, label='Vout LM741 (Saturación ~10.5V)')
ax2_twin = ax2.twinx()
ax2_twin.plot(t_comp, led_current, 'r--', linewidth=1.8, label='Corriente LED (mA)')
ax2_twin.set_ylabel('Corriente en LED (mA)', color='red')
ax2_twin.tick_params(axis='y', labelcolor='red')
ax2_twin.set_ylim(-2, 35)

ax2.set_xlabel('Tiempo (ms)')
ax2.set_ylabel('Salida Comparador (V)')
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.set_ylim(-1, 12)

# Etiquetas de estado
ax2.text(3, 3, 'ESTADO: NORMAL\nLED APAGADO', fontsize=9, bbox=dict(facecolor='#e8f5e9', edgecolor='green'))
ax2.text(12, 3, 'ESTADO: ALERTA\nLED ENCENDIDO (~25.7 mA)', fontsize=9, bbox=dict(facecolor='#ffebee', edgecolor='red'))

plt.tight_layout()
plt.savefig('img/circuito_protoboard.png', dpi=300)
plt.close()
print("Generada img/circuito_protoboard.png")

# -------------------------------------------------------------
# 4. Calibración del Sensor Ultrasónico HC-SR04 (ESP32)
# -------------------------------------------------------------
dist_real = np.array([4, 8, 12, 16, 20, 25, 30, 35, 40, 45, 50])  # cm
v_sound_cm_us = 0.0343  # cm/us
tiempo_eco_teorico = (2 * dist_real) / v_sound_cm_us  # us

np.random.seed(101)
tiempo_eco_medido = tiempo_eco_teorico + np.random.normal(0, 12, len(dist_real))

slope, intercept = np.polyfit(dist_real, tiempo_eco_medido, 1)
y_pred = slope * dist_real + intercept
r2 = 1 - np.sum((tiempo_eco_medido - y_pred)**2) / np.sum((tiempo_eco_medido - np.mean(tiempo_eco_medido))**2)

fig, ax = plt.subplots(figsize=(8.5, 5.5))
ax.errorbar(dist_real, tiempo_eco_medido, yerr=15, fmt='o', color='navy', ecolor='gray',
            elinewidth=1.5, capsize=4, markersize=7, label='Mediciones de Tiempo de Eco (ESP32)')
ax.plot(dist_real, y_pred, 'r-', linewidth=2, label=f'Ajuste Lineal: t = {slope:.2f}·d + {intercept:.2f} µs (R² = {r2:.4f})')

ax.set_title('Curva de Calibración del Sensor Ultrasónico HC-SR04 con ESP32 [DATOS SIMULADOS]', fontweight='bold')
ax.set_xlabel('Distancia Real (cm)')
ax.set_ylabel('Tiempo de Pulso Echo (µs)')
ax.grid(True, linestyle='--', alpha=0.6)

sensibilidad_us_cm = slope
ax.text(0.05, 0.78, f'Sensibilidad: S = {sensibilidad_us_cm:.2f} µs/cm\nVelocidad acústica: v = {2/sensibilidad_us_cm * 10000:.1f} m/s\nCoef. Determinación: R² = {r2:.4f}',
        transform=ax.transAxes, fontsize=10,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#f0f4f8', edgecolor='#336699'))

ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig('img/calibracion_ultrasonico.png', dpi=300)
plt.close()
print("Generada img/calibracion_ultrasonico.png")

# -------------------------------------------------------------
# 5. Emulación del Panel Frontal y Chart de LabVIEW
# -------------------------------------------------------------
np.random.seed(55)
n_muestras = 150
t_samples = np.arange(n_muestras)

dist_profile = np.zeros(n_muestras)
dist_profile[0:30] = 45 + np.random.normal(0, 0.4, 30)
dist_profile[30:70] = np.linspace(45, 12, 40) + np.random.normal(0, 0.5, 40)
dist_profile[70:110] = 12 + np.random.normal(0, 0.3, 40)
dist_profile[110:150] = np.linspace(12, 40, 40) + np.random.normal(0, 0.5, 40)

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#dcdcdc')
ax.set_facecolor('#050515')

ax.plot(t_samples, dist_profile, color='#00ff41', linewidth=2.0, label='Distancia Medida (HC-SR04 via ESP32)')
ax.axhline(15.0, color='#ff3333', linestyle='--', linewidth=1.8, label='Límite de Proximidad Crítica (15 cm)')

ax.set_title('LabVIEW VI: Waveform Chart - Monitoreo Serial UART (115200 baud) [DATOS SIMULADOS]',
             color='#111111', fontweight='bold', pad=14)
ax.set_xlabel('Número de Muestra (Intervalo Ts = 50 ms)', color='#111111')
ax.set_ylabel('Distancia (cm)', color='#111111')
ax.grid(True, color='#223344', linestyle=':', alpha=0.8)
ax.set_ylim(0, 55)

ax.text(0.03, 0.90, 'MODO: ADQUISICIÓN CONTINUA\nCOM PORT: /dev/ttyUSB0 (ESP32)\nBAUD: 115200 | Muestras: 150',
        transform=ax.transAxes, color='#00ff41', fontsize=9, fontfamily='monospace',
        bbox=dict(facecolor='#0a1020', edgecolor='#00ff41', pad=4))

ax.text(0.72, 0.90, f'Última Lectura: {dist_profile[-1]:.1f} cm\nEstado: NORMAL',
        transform=ax.transAxes, color='#ffffff', fontsize=9, fontfamily='monospace',
        bbox=dict(facecolor='#0a1020', edgecolor='#aaaaaa', pad=4))

leg = ax.legend(loc='lower left', facecolor='#111a2a', edgecolor='#555555')
for text in leg.get_texts():
    text.set_color('white')

plt.tight_layout()
plt.savefig('img/labview_front_panel.png', dpi=300, facecolor=fig.get_facecolor())
plt.close()
print("Generada img/labview_front_panel.png")

# -------------------------------------------------------------
# 6. Diagrama de Bloques Conceptual de LabVIEW
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9.5, 4.5))
ax.axis('off')
fig.patch.set_facecolor('#f5f5f5')

boxes = [
    (0.04, 0.38, 0.17, 0.34, 'VISA Configure\nSerial Port\n(115200, 8N1)', '#fff3e0'),
    (0.27, 0.28, 0.20, 0.54, 'While Loop\n\nVISA Read\n(Bytes en búfer)', '#e1f5fe'),
    (0.52, 0.28, 0.19, 0.54, 'Scan From\nString\nFormato: "%f\\n"', '#e8f5e9'),
    (0.76, 0.38, 0.18, 0.34, 'Waveform\nChart\n(Tiempo Real)', '#ffebee'),
]

for x, y, w, h, text, color in boxes:
    patch = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.03',
                           facecolor=color, edgecolor='#333333', linewidth=1.5)
    ax.add_patch(patch)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#212121')

arrows = [
    ((0.21, 0.55), (0.27, 0.55)),
    ((0.47, 0.55), (0.52, 0.55)),
    ((0.71, 0.55), (0.76, 0.55)),
]
for p1, p2 in arrows:
    ax.annotate('', xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle='->', lw=2.2, color='#c62828'))

ax.set_title('LabVIEW: Arquitectura del Diagrama de Bloques (Flujo VISA DAQ) [DIAGRAMA CONCEPTUAL]',
             fontsize=12, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig('img/labview_block_diagram.png', dpi=300, facecolor=fig.get_facecolor())
plt.close()
print("Generada img/labview_block_diagram.png")
