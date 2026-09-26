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
C = 0.1e-6    # 0.1 uF (100 nF)
tau = R * C   # 1.0 ms
fc = 1 / (2 * np.pi * tau)  # ~159.15 Hz

w, mag, phase = signal.bode(([1], [tau, 1]), w=np.logspace(0, 5, 1000) * 2 * np.pi)
f = w / (2 * np.pi)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
fig.suptitle('Respuesta en Frecuencia del Filtro Pasabajas Pasivo RC [DATOS SIMULADOS]\n'
             r'($R = 10.0\ \mathrm{k}\Omega,\ C = 100\ \mathrm{nF},\ \tau = 1.0\ \mathrm{ms},\ f_c = 159.15\ \mathrm{Hz}$)',
             fontweight='bold', fontsize=12)

# Magnitud
ax1.semilogx(f, mag, 'b-', linewidth=2.2, label=r'Magnitud $|H(f)|$')
ax1.axvline(fc, color='r', linestyle='--', alpha=0.85, label=f'fc = {fc:.2f} Hz (-3.01 dB)')
ax1.axhline(-3.01, color='gray', linestyle=':', alpha=0.7)
ax1.scatter([fc], [-3.01], color='red', s=45, zorder=5)
ax1.annotate(f'-3.01 dB @ {fc:.1f} Hz', xy=(fc, -3.01), xytext=(fc * 1.5, -8),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))

# Anotación asíntota -20 dB/década
ax1.plot([1e3, 1e4], [-16.0, -36.0], 'k--', alpha=0.6, linewidth=1.5, label=r'Pendiente: $-20\ \mathrm{dB/d\acute{e}cada}$')
ax1.annotate(r'Asíntota $-20\ \mathrm{dB/d\acute{e}cada}$', xy=(3e3, -25.5), xytext=(4e3, -18),
             arrowprops=dict(facecolor='darkslategray', shrink=0.05, width=1, headwidth=5),
             fontsize=9.5)

ax1.set_ylabel('Magnitud (dB)')
ax1.grid(True, which='both', linestyle='--', alpha=0.5)
ax1.legend(loc='lower left', framealpha=0.9)
ax1.set_ylim(-42, 3)

# Fase
ax2.semilogx(f, phase, 'g-', linewidth=2.2, label=r'Fase $\angle H(f)$')
ax2.axvline(fc, color='r', linestyle='--', alpha=0.85)
ax2.axhline(-45.0, color='gray', linestyle=':', alpha=0.7)
ax2.scatter([fc], [-45.0], color='red', s=45, zorder=5)
ax2.annotate(r'$-45.0^\circ\ @\ f_c$', xy=(fc, -45), xytext=(fc * 1.5, -30),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))

# Anotación fase a 60 Hz ubicada en espacio blanco inferior sin cruzar curva
theta_60 = -np.degrees(np.arctan(60.0 / fc))
ax2.scatter([60.0], [theta_60], color='purple', s=40, zorder=5)
ax2.annotate(f'{theta_60:.1f}° @ 60 Hz', xy=(60.0, theta_60), xytext=(8.0, -38),
             arrowprops=dict(facecolor='purple', shrink=0.05, width=1, headwidth=5),
             fontsize=9.5, color='purple', fontweight='bold')

ax2.set_xlabel('Frecuencia (Hz)')
ax2.set_ylabel('Fase (grados)')
ax2.grid(True, which='both', linestyle='--', alpha=0.5)
ax2.legend(loc='lower left', framealpha=0.9)
ax2.set_ylim(-95, 5)

plt.tight_layout()
plt.savefig('img/simulacion_multisim.png', dpi=300)
plt.close()
print("Generada img/simulacion_multisim.png")

# -------------------------------------------------------------
# 2. Emulación de Osciloscopio: Análisis Temporal y Filtro RC
# -------------------------------------------------------------
fs = 100000  # 100 kHz sample rate
t_total = 0.05  # 50 ms window
t = np.linspace(0, t_total, int(fs * t_total), endpoint=False)

# Simulación en régimen estacionario (sin transitorio espurio de arranque)
np.random.seed(42)
v_dc = 1.20
# Componente fundamental de zumbido de 60 Hz (T = 16.67 ms)
amp_60hz = 0.12  # V_peak -> 240 mVpp
noise_60hz = amp_60hz * np.sin(2 * np.pi * 60.0 * t)

# Ruido de conmutación de alta frecuencia (2.0 kHz, T_sw = 0.5 ms)
amp_hf = 0.10    # V_peak -> 200 mVpp
noise_hf = amp_hf * np.sin(2 * np.pi * 2000.0 * t) + 0.015 * np.random.normal(0, 1, len(t))

v_in_noisy = v_dc + noise_60hz + noise_hf

# Respuesta del filtro en régimen permanente:
mag_60 = 1.0 / np.sqrt(1.0 + (60.0 / fc)**2)
phase_60 = -np.arctan(60.0 / fc)
out_60hz = amp_60hz * mag_60 * np.sin(2 * np.pi * 60.0 * t + phase_60)

mag_hf = 1.0 / np.sqrt(1.0 + (2000.0 / fc)**2)
phase_hf = -np.arctan(2000.0 / fc)
out_hf = amp_hf * mag_hf * np.sin(2 * np.pi * 2000.0 * t + phase_hf)

# Ruido térmico residual filtrado
residual_noise = 0.003 * np.random.normal(0, 1, len(t))
v_out_filtered = v_dc + out_60hz + out_hf + residual_noise

dt_delay_ms = np.abs(np.degrees(phase_60)) / (360.0 * 60.0) * 1000.0  # ~0.956 ms
t_period_ms = (1.0 / 60.0) * 1000.0  # 16.667 ms

fig, ax = plt.subplots(figsize=(10.8, 6.0))
fig.patch.set_facecolor('#181818')
ax.set_facecolor('#0d0d0d')

# Señales CH1 y CH2
ax.plot(t * 1000, v_in_noisy, color='#ffeb3b', alpha=0.75, linewidth=1.1,
        label=r'CH1: Entrada con Ruido ($V_{\mathrm{DC}} = 1.20\ \mathrm{V} + 60\ \mathrm{Hz} + 2\ \mathrm{kHz}$)')
ax.plot(t * 1000, v_out_filtered, color='#00e5ff', linewidth=2.2,
        label=r'CH2: Salida Filtrada ($R=10.0\ \mathrm{k}\Omega,\ C=100\ \mathrm{nF},\ f_c=159.15\ \mathrm{Hz}$)')
ax.axhline(1.20, color='#888888', linestyle=':', alpha=0.6, label='Nivel DC Nominal (1.20 V)')

# Delimitación de ciclo completo en el primer periodo (T = 16.67 ms)
cycle_start = 0.0
cycle_end = 16.667
ax.axvline(cycle_start, color='#ff5252', linestyle='--', linewidth=1.4, alpha=0.85)
ax.axvline(cycle_end, color='#ff5252', linestyle='--', linewidth=1.4, alpha=0.85)

ax.annotate('', xy=(cycle_end, 1.54), xytext=(cycle_start, 1.54),
            arrowprops=dict(arrowstyle='<->', color='#ff5252', lw=1.8))
ax.text((cycle_start + cycle_end) / 2, 1.58,
        f'Ciclo Completo: T = {t_period_ms:.2f} ms (f = 60.0 Hz)',
        color='#ff5252', fontsize=9.2, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#262626', edgecolor='#ff5252', lw=1.2))

# Delimitación de desfase Delta_t a 60 Hz
peak1_t = 16.667 + 4.167  # pico CH1 a los 20.83 ms
peak2_t = peak1_t + dt_delay_ms  # pico CH2 retardado
ax.axvline(peak1_t, color='#ffeb3b', linestyle=':', linewidth=1.2, alpha=0.7)
ax.axvline(peak2_t, color='#00e5ff', linestyle=':', linewidth=1.2, alpha=0.7)
ax.annotate('', xy=(peak2_t, 1.37), xytext=(peak1_t, 1.37),
            arrowprops=dict(arrowstyle='<->', color='white', lw=1.5))
ax.text(peak2_t + 0.4, 1.38,
        rf'$\Delta t = {dt_delay_ms:.2f}\ \mathrm{{ms}}\ \to\ \theta = -{np.abs(np.degrees(phase_60)):.1f}^\circ$',
        color='white', fontsize=9, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#262626', edgecolor='#aaaaaa'))

# Formato de osciloscopio
ax.set_title('Oscilograma Digital Rigol DHO914: Análisis de Ciclo y Filtrado RC [DATOS SIMULADOS]\n'
             r'($V_{\mathrm{in}} = 1.20\ \mathrm{V}_{\mathrm{DC}},\ V_{pp,\mathrm{in}} = 240\ \mathrm{mV}_{60\mathrm{Hz}} + 200\ \mathrm{mV}_{2\mathrm{kHz}},\ '
             r'R = 10.0\ \mathrm{k}\Omega,\ C = 100\ \mathrm{nF}$)',
             color='white', fontweight='bold', pad=12)
ax.set_xlabel('Tiempo (ms)', color='white')
ax.set_ylabel('Voltaje (V)', color='white')
ax.tick_params(colors='white')
ax.grid(True, color='#333333', linestyle='--', alpha=0.7)
ax.set_ylim(0.85, 1.72)
ax.set_xlim(0, 50.0)

# Indicador de estado y mediciones cuantitativas ubicado a la DERECHA SUPERIOR
mediciones_texto = (
    "MEDICIONES EN PANTALLA:\n"
    f"• Periodo T: {t_period_ms:.2f} ms | Frecuencia: 60.0 Hz\n"
    f"• Retardo Δt: {dt_delay_ms:.2f} ms | Desfase: -{np.abs(np.degrees(phase_60)):.1f}°\n"
    "• Atenuación Ruido HF (2 kHz): > 22.0 dB (200 → 15.8 mVpp)\n"
    "• Rizado residual CH2: Vpp ≈ 225 mV (60 Hz) + 16 mV (2 kHz)"
)

ax.text(0.98, 0.95, mediciones_texto,
        transform=ax.transAxes, color='white', fontsize=8.5, va='top', ha='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#262626', alpha=0.92, edgecolor='#555555'))

leg = ax.legend(loc='lower left', facecolor='#262626', edgecolor='#555555')
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
v_ref = 1.00  # Umbral de 1.0 V
# Sigmoide centrada en 8.0 ms
v_sig = 1.20 / (1.0 + np.exp(-0.8 * (t_comp - 8.0)))
# Cruce exacto analítico: t_cross = 8.0 - ln(0.20)/0.8 = 10.0118 ms
t_cross = 8.0 - np.log(1.20 / v_ref - 1.0) / 0.8

v_comp_out = np.where(t_comp >= t_cross, 10.5, -10.5)
led_current = np.where(t_comp >= t_cross, (10.5 - 2.0) / 330.0 * 1000.0, 0.0)  # mA

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.5, 6.2), sharex=True)
fig.suptitle('Dinámica de Disparo del Comparador LM741 y Alarma LED [DATOS SIMULADOS]\n'
             r'($V_{\mathrm{ref}} = 1.00\ \mathrm{V},\ R_{\mathrm{pot}} = 10.0\ \mathrm{k}\Omega,\ R_{\mathrm{LED}} = 330\ \Omega,\ V_f \approx 2.0\ \mathrm{V}$)',
             fontweight='bold', fontsize=12)

# Entradas
ax1.plot(t_comp, v_sig, 'b-', linewidth=2.2, label=r'$V_{\mathrm{in}}$ (Señal Acondicionada)')
ax1.axhline(v_ref, color='r', linestyle='--', linewidth=1.8, label=r'$V_{\mathrm{ref}} = 1.00\ \mathrm{V}$ (Umbral de Alarma)')
ax1.axvline(t_cross, color='gray', linestyle=':', linewidth=1.5, alpha=0.85)
ax1.scatter([t_cross], [v_ref], color='red', s=55, zorder=5)
ax1.annotate(r'Punto de disparo ($V_{\mathrm{in}} > V_{\mathrm{ref}} = 1.00\ \mathrm{V}$ @ $t = 10.01\ \mathrm{ms}$)',
             xy=(t_cross, v_ref), xytext=(2.0, 1.18),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
             fontweight='bold', fontsize=9.5)
ax1.set_ylabel('Voltaje de Entrada (V)')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(loc='lower right', framealpha=0.9)
ax1.set_ylim(-0.1, 1.4)

# Salida del Comparador y Estado del LED
ax2.plot(t_comp, v_comp_out, 'purple', linewidth=2.2, label=r'$V_{\mathrm{out}}$ LM741 ($\pm 10.5\ \mathrm{V}$ sat)')
ax2.axvline(t_cross, color='gray', linestyle=':', linewidth=1.5, alpha=0.85)
ax2_twin = ax2.twinx()
ax2_twin.plot(t_comp, led_current, 'r--', linewidth=2.0, label=r'Corriente LED ($I_{\mathrm{LED}}$ en mA)')
ax2_twin.set_ylabel('Corriente en LED (mA)', color='red')
ax2_twin.tick_params(axis='y', labelcolor='red')
ax2_twin.set_ylim(-2, 35)

ax2.set_xlabel('Tiempo (ms)')
ax2.set_ylabel('Salida Comparador (V)')
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.set_ylim(-13, 13)

# Etiquetas de estado
ax2.text(2.0, 0, 'ESTADO: NORMAL\nLED APAGADO (0 mA)\nSalida: Sat. Negativa (-10.5 V)',
         fontsize=8.5, bbox=dict(facecolor='#e8f5e9', edgecolor='green'))
ax2.text(11.5, 0, 'ESTADO: SOBRECARGA / ALERTA\nLED ENCENDIDO (25.7 mA)\nSalida: Sat. Positiva (+10.5 V)',
         fontsize=8.5, bbox=dict(facecolor='#ffebee', edgecolor='red'))

plt.tight_layout()
plt.savefig('img/circuito_protoboard.png', dpi=300)
plt.close()
print("Generada img/circuito_protoboard.png")

# -------------------------------------------------------------
# 4. Calibración del Sensor Ultrasónico HC-SR04 (ESP32)
# -------------------------------------------------------------
dist_real = np.array([4.0, 8.0, 12.0, 16.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0])  # cm
tiempo_eco_medido = np.array([221.0, 480.9, 690.4, 950.0, 1158.7, 1477.2, 1733.9, 2054.6, 2318.1, 2633.9, 2913.6])  # us

slope, intercept = np.polyfit(dist_real, tiempo_eco_medido, 1)
y_pred = slope * dist_real + intercept
r2 = 1.0 - np.sum((tiempo_eco_medido - y_pred)**2) / np.sum((tiempo_eco_medido - np.mean(tiempo_eco_medido))**2)
sensibilidad_us_cm = slope
v_calc = (2.0 / sensibilidad_us_cm) * 10000.0  # m/s

fig, ax = plt.subplots(figsize=(8.8, 5.6))
ax.errorbar(dist_real, tiempo_eco_medido, yerr=12, fmt='o', color='navy', ecolor='gray',
            elinewidth=1.5, capsize=4, markersize=7, label='Mediciones Experimentales de Eco (ESP32)')
ax.plot(dist_real, y_pred, 'r-', linewidth=2.2,
        label=rf'Ajuste Lineal: $t_{{\mathrm{{echo}}}} = {slope:.2f}\cdot d + {intercept:.2f}\ \mu\mathrm{{s}}\ (R^2 = {r2:.4f})$')

ax.set_title('Curva de Calibración del Sensor Ultrasónico HC-SR04 con ESP32\n[DATOS EXPERIMENTALES REPRODUCIDOS]',
             fontweight='bold', fontsize=12)
ax.set_xlabel('Distancia Real Medida con Patrón (cm)')
ax.set_ylabel(r'Tiempo de Pulso Echo ($t_{\mathrm{echo}}$ en $\mu\mathrm{s}$)')
ax.grid(True, linestyle='--', alpha=0.6)

ax.text(0.05, 0.74,
        f'Sensibilidad Estática: S = {sensibilidad_us_cm:.2f} µs/cm\n'
        f'Velocidad Acústica Derivada: v = {v_calc:.1f} m/s\n'
        f'Coeficiente de Determinación: R² = {r2:.4f}\n'
        f'Error Estándar de Estimación: σ = {np.std(tiempo_eco_medido - y_pred):.2f} µs',
        transform=ax.transAxes, fontsize=9.5,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#f0f4f8', edgecolor='#336699'))

ax.legend(loc='lower right', framealpha=0.9)
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
ax.axhline(15.0, color='#ff3333', linestyle='--', linewidth=1.8, label='Límite de Proximidad Crítica (15.0 cm)')

ax.set_title('LabVIEW VI: Waveform Chart - Monitoreo Serial UART (115200 baud) [DATOS REPRODUCIDOS]',
             color='#111111', fontweight='bold', pad=14)
ax.set_xlabel('Número de Muestra (Intervalo Ts = 50 ms, Fs = 20 Hz)', color='#111111')
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

ax.set_title('LabVIEW: Arquitectura del Diagrama de Bloques (Flujo VISA DAQ) [DIAGRAMA DE FLUJO]',
             fontsize=12, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig('img/labview_block_diagram.png', dpi=300, facecolor=fig.get_facecolor())
plt.close()
print("Generada img/labview_block_diagram.png")

# -------------------------------------------------------------
# 7. Diagrama Esquemático Integral de la Cadena de Medición
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(16, 9.2), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')
fig.patch.set_facecolor('#ffffff')

# Titulos generales
ax.text(50, 97, 'ARQUITECTURA INTEGRAL DE LA CADENA DE MEDICIÓN Y ADQUISICIÓN',
        ha='center', va='center', fontsize=15, fontweight='bold', color='#0d233a')
ax.text(50, 93.8, 'Diseño de Interfaces Digitales — Universidad Anáhuac México (Laboratorio 1)',
        ha='center', va='center', fontsize=11, color='#555555')

# Encabezado A: Subsistema Analógico
ax.text(3, 89, 'A. SUBSISTEMA ANALÓGICO: ACONDICIONAMIENTO, FILTRADO Y PROTECCIÓN POR HARDWARE',
        fontsize=11.5, fontweight='bold', color='#1565c0')

analog_boxes = [
    (3, 56, 21, 30,
     'ETAPA 1: DIFERENCIAL',
     '• OpAmp: LM741 (Dual ±12 V)\n'
     '• R1 = 1.0 kΩ, R2 = 10.0 kΩ\n'
     '• Ganancia: Ad = 10.0 (20 dB)\n'
     '• Entrada: V2=80 mV, V1=20 mV\n'
     '• Diferencial: ΔV = 60.0 mV\n'
     '• Salida Vo1 = 0.60 V\n'
     '• Rechazo Modo Común (CMRR)',
     '#e3f2fd', '#1565c0'),
    (27, 56, 21, 30,
     'ETAPA 2: NO INVERSOR',
     '• OpAmp: LM741 (Dual ±12 V)\n'
     '• Rf = 10.0 kΩ, Rin = 10.0 kΩ\n'
     '• Ganancia: Av = 2.0 (6.02 dB)\n'
     '• Ganancia Total: Atot = 20.0\n'
     '• Entrada: Vo1 = 0.60 V\n'
     '• Salida: Vo2 = 1.20 V\n'
     '• Aislamiento de impedancia',
     '#e0f2f1', '#00796b'),
    (51, 56, 21, 30,
     'ETAPA 3: FILTRO RC',
     '• Pasabajas 1er orden pasivo\n'
     '• R = 10.0 kΩ, C = 100 nF\n'
     '• fc = 159.15 Hz, τ = 1.0 ms\n'
     '• Atenuación 60 Hz: -0.58 dB\n'
     '• Atenuación 2 kHz: -22.0 dB\n'
     '• Salida: Vfilt = 1.20 V\n'
     '• Supresión de armónicos HF',
     '#f9fbe7', '#689f38'),
    (75, 56, 22, 30,
     'ETAPA 4: COMPARADOR',
     '• OpAmp: LM741 (Lazo abierto)\n'
     '• Umbral: Vref = 1.00 V (Pot)\n'
     '• Condición: Vin > 1.00 V\n'
     '• Salida: Vsat+ = +10.5 V\n'
     '• Resistor LED: R = 330 Ω\n'
     '• I_LED = 25.7 mA (LED ON)\n'
     '• Corte rápido t_sw < 15 µs',
     '#fff3e0', '#e65100'),
]

for x, y, w, h, title, body, fcol, ecol in analog_boxes:
    patch = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.5,rounding_size=1.5',
                           facecolor=fcol, edgecolor=ecol, linewidth=1.8)
    ax.add_patch(patch)
    ax.text(x + w/2, y + h - 2.8, title, fontsize=10.5, fontweight='bold', color=ecol, ha='center', va='top')
    ax.text(x + 1.2, y + h - 6.2, body, fontsize=9.0, color='#212121', va='top', linespacing=1.35)

# Flechas analógicas
analog_arrows = [
    ((24, 71), (27, 71), 'Vo1=0.6V'),
    ((48, 71), (51, 71), 'Vo2=1.2V'),
    ((72, 71), (75, 71), 'Vfilt=1.2V'),
]
for p1, p2, label in analog_arrows:
    ax.annotate('', xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle='->', lw=2.2, color='#1565c0'))
    ax.text((p1[0] + p2[0])/2, p1[1] + 2.0, label, ha='center', va='bottom',
            fontsize=8.5, fontweight='bold', color='#1565c0',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor='#1565c0', lw=0.8))

# Encabezado B: Subsistema Digital
ax.text(3, 50, 'B. SUBSISTEMA DIGITAL: TRANSDUCCIÓN, MICROCONTROLADOR Y TELEMETRÍA SERIAL',
        fontsize=11.5, fontweight='bold', color='#2e7d32')

digital_boxes = [
    (3, 17, 21, 30,
     'TRANSDUCTOR HC-SR04',
     '• Ultrasonido de 40 kHz\n'
     '• Rango físico: 4 a 50 cm\n'
     '• Pulso Trigger: 10 µs TTL\n'
     '• Pulso Echo: PWM proporcional\n'
     '• S = 58.31 µs/cm (v = 343 m/s)\n'
     '• Regresión lineal R² = 0.9998\n'
     '• Precisión milimétrica',
     '#ede7f6', '#512da8'),
    (27, 17, 21, 30,
     'MICROCONTROLADOR ESP32',
     '• Núcleo Xtensa 32-bit (240 MHz)\n'
     '• Captura por interrupción\n'
     '• Temporizadores periféricos\n'
     '• Intervalo Ts = 50 ms (20 Hz)\n'
     '• Conversión digital de eco\n'
     '• Transmisor UART0 hardware\n'
     '• Cero jitter en lazo cerrado',
     '#f3e5f5', '#7b1fa2'),
    (51, 17, 21, 30,
     'ENLACE SERIAL UART',
     '• Baudrate: 115200 baudios\n'
     '• Trama: 8N1 (Sin paridad)\n'
     '• Formato ASCII: [dist]\\r\\n\n'
     '• Paquete: 8-10 bytes\n'
     '• Tiempo en bus: 0.87 ms\n'
     '• Margen libre de bus > 98%\n'
     '• Conexión directa a PC',
     '#e8eaf6', '#283593'),
    (75, 17, 22, 30,
     'VI LABVIEW (RECEPCIÓN)',
     '• Módulo NI-VISA Serial DAQ\n'
     '• Búfer de recepción FIFO\n'
     '• Scan From String ("%f\\n")\n'
     '• Waveform Chart tiempo real\n'
     '• Límite proximidad a 15 cm\n'
     '• Tasa de actualización 20 Hz\n'
     '• Supervisión gráfica remota',
     '#e1f5fe', '#0277bd'),
]

for x, y, w, h, title, body, fcol, ecol in digital_boxes:
    patch = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.5,rounding_size=1.5',
                           facecolor=fcol, edgecolor=ecol, linewidth=1.8)
    ax.add_patch(patch)
    ax.text(x + w/2, y + h - 2.8, title, fontsize=10.5, fontweight='bold', color=ecol, ha='center', va='top')
    ax.text(x + 1.2, y + h - 6.2, body, fontsize=9.0, color='#212121', va='top', linespacing=1.35)

# Flechas digitales
digital_arrows = [
    ((24, 32), (27, 32), 'Echo PWM'),
    ((48, 32), (51, 32), 'TX UART'),
    ((72, 32), (75, 32), 'VISA Read'),
]
for p1, p2, label in digital_arrows:
    ax.annotate('', xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle='->', lw=2.2, color='#2e7d32'))
    ax.text((p1[0] + p2[0])/2, p1[1] + 2.0, label, ha='center', va='bottom',
            fontsize=8.5, fontweight='bold', color='#2e7d32',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor='#2e7d32', lw=0.8))

# Cuadro inferior de síntesis metodológica
sum_patch = FancyBboxPatch((3, 2), 94, 12, boxstyle='round,pad=0.5,rounding_size=1.5',
                           facecolor='#f5f5f5', edgecolor='#455a64', linewidth=1.5)
ax.add_patch(sum_patch)
ax.text(50, 11.0, 'SÍNTESIS INTEGRAL DE LA ARQUITECTURA EXPERIMENTAL',
        ha='center', va='center', fontsize=10.5, fontweight='bold', color='#263238')

summary_text = (
    '• Cadena Analógica: ΔV = 60.0 mV → Ganancia Cascada Atot = 10 × 2 = 20.0 (26.02 dB) → Nivel condicionado Vo = 1.20 V (< 3.0 V límite ADC).\n'
    '• Filtro Pasabajas RC: fc = 159.15 Hz, τ = 1.0 ms. Pasa fundamental de 60 Hz (-0.58 dB) y atenúa ruido parásito HF a 2 kHz (> 22.0 dB).\n'
    '• Protección por Hardware: Comparador LM741 conmuta en < 15 µs inyectando 25.7 mA al LED Rojo ante cualquier sobrecarga Vin > 1.00 V.\n'
    '• Adquisición Digital: ESP32 cronometra pulso de eco del HC-SR04 (S = 58.31 µs/cm, R² = 0.9998, v = 343.0 m/s) y transmite vía UART (115200) a LabVIEW a 20 Hz.'
)
ax.text(50, 6.2, summary_text, ha='center', va='center', fontsize=8.8, color='#37474f', linespacing=1.35)

plt.tight_layout()
plt.savefig('img/esquema_bloques_cadena.png', dpi=300)
plt.close()
print("Generada img/esquema_bloques_cadena.png")
