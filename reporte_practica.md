---
title: "Lab Session 1: Signal Conditioning, Characterization, and Visualization"
subtitle: "Diseño de Interfaces Digitales"
author:
  - "Nombre del Alumno 1 - ID"
  - "Nombre del Alumno 2 - ID"
  - "Nombre del Alumno 3 - ID"
instructor: "Israel Cayetano Jiménez, ing. microtechn. dipl. EPF, M.Sc."
institution: "Universidad Anáhuac México"
date: "Septiembre 25, 2026"
keywords: ["Signal Conditioning", "Operational Amplifier", "LM741", "ESP32", "LabVIEW", "Low-Pass Filter", "Voltage Comparator", "Data Acquisition"]
lang: "es"
---

# Abstract

En este laboratorio se diseñó, simuló e implementó una cadena completa de acondicionamiento, adquisición y monitoreo de señales para transductores analógicos. El sistema físico se estructuró a partir de amplificadores operacionales LM741 organizados en cuatro etapas: un amplificador diferencial con ganancia $A_d = 10$, un amplificador no inversor con ganancia $A_v = 2$, un filtro pasabajas pasivo $RC$ ($f_c \approx 159.15\text{ Hz}$) y un comparador de voltaje configurado a un umbral de $1.0\text{ V}$ para activación de alarma visual mediante LED. La señal de salida acondicionada ($1.2\text{ V}$) garantiza el aprovechamiento óptimo del rango lineal de entrada del convertidor analógico-digital (ADC) del microcontrolador ESP32 sin riesgo de saturación. La adquisición y visualización en tiempo real se validó empleando el microcontrolador ESP32 y un sensor de medición, comunicados mediante protocolo UART hacia un Instrumento Virtual (VI) desarrollado en LabVIEW. Los resultados experimentales confirmaron la atenuación de componentes de ruido de alta frecuencia y la respuesta inmediata del subsistema de protección por hardware.

**Keywords:** Signal Conditioning, Operational Amplifier, LM741, ESP32, LabVIEW, Low-Pass Filter, Voltage Comparator, Data Acquisition.

---

# 1. Introduction

Los transductores de señales mecánicas (como celdas de carga basadas en galgas extensométricas en puente de Wheatstone) proporcionan señales eléctricas diferenciales de baja magnitud, comúnmente en el orden de los milivoltios. Dichas señales son altamente susceptibles a interferencias electromagnéticas, variaciones de modo común y ruido de conmutación. Por lo tanto, el acondicionamiento analógico de la señal es indispensable antes de cualquier proceso de digitalización para asegurar una adecuada relación señal a ruido (SNR), evitar aliasing y adaptar el rango dinámico del sensor al rango admisible del convertidor analógico a digital (ADC) del microcontrolador.

En este trabajo se aborda el acondicionamiento mediante etapas modulares con amplificadores operacionales LM741, integrando amplificación diferencial balanceada, ganancia en cascada no inversora, filtrado pasivo y protección por comparación en hardware, complementado con la transmisión serial de datos a una interfaz gráfica de supervisión en LabVIEW.

## 1.1. Objective

Diseñar, simular, implementar y validar experimentalmente una cadena analógica de acondicionamiento de señal con amplificadores operacionales LM741, integrando adquisición mediante microcontrolador ESP32 y supervisión en tiempo real en LabVIEW, evaluando las características estáticas y dinámicas de cada etapa.

---

# 2. Methodology

## 2.1. Materials

En la Tabla 1 se detallan los equipos, instrumentos y componentes electrónicos utilizados en la implementación del laboratorio.

| Componente / Dispositivo | Cantidad | Especificaciones / Modelo |
| :--- | :---: | :--- |
| Amplificador Operacional | 4 | LM741 / UA741 (DIP-8) |
| Microcontrolador | 1 | ESP32 NodeMCU (30 pines) |
| Sensor Ultrasónico | 1 | HC-SR04 |
| Resistencia $1\text{ k}\Omega$ | 2 | $1/4\text{ W}$, tolerancia $5\%$ |
| Resistencia $10\text{ k}\Omega$ | 5 | $1/4\text{ W}$, tolerancia $5\%$ |
| Resistencia $330\ \Omega$ | 1 | Limitadora de corriente para LED |
| Potenciómetro | 1 | $10\text{ k}\Omega$ multigiro / lineal |
| Capacitor cerámico | 1 | $0.1\ \mu\text{F}$ ($100\text{ nF}$) |
| Diodo LED | 1 | Difuso rojo ($V_f \approx 2.0\text{ V}$) |
| Fuente de alimentación DC | 1 | Voltaje dual regulado ($\pm 12\text{ V}$ o $\pm 5\text{ V}$) y $5\text{ V}$ unipolar |
| Osciloscopio Digital | 1 | 2 canales, ancho de banda $\ge 50\text{ MHz}$ |
| Multímetro Digital | 1 | Medición de tensión DC y resistencia |
| Protoboard y cableado | 1 | Alambre calibre 22 AWG |

: Table 1. Materiales y equipos de laboratorio.

---

## 2.2. Procedure

El desarrollo experimental se organizó en las siguientes fases metodológicas:

### 2.2.1. Diseño y Ensamble de la Etapa de Acondicionamiento Analógico

1. **Amplificador Diferencial ($A_d = 10$):**
   Para rechazar el modo común y amplificar el diferencial de tensión en milivoltios, se conectaron resistencias balanceadas $R_1 = 1\text{ k}\Omega$ a las entradas inversora y no inversora, con resistencias de realimentación y referencia a tierra $R_2 = 10\text{ k}\Omega$.
   $$\Delta V_{in} = V_2 - V_1 = 80\text{ mV} - 20\text{ mV} = 60\text{ mV}$$
   $$V_{o1} = \frac{R_2}{R_1}(V_2 - V_1) = \frac{10\text{ k}\Omega}{1\text{ k}\Omega}(60\text{ mV}) = 10 \cdot 60\text{ mV} = 0.6\text{ V}$$

2. **Amplificador No Inversor ($A_v = 2$):**
   La salida de la primera etapa se acopló directamente a la entrada no inversora del segundo LM741, configurado con resistencias $R_f = 10\text{ k}\Omega$ y $R_{in} = 10\text{ k}\Omega$:
   $$A_v = 1 + \frac{R_f}{R_{in}} = 1 + \frac{10\text{ k}\Omega}{10\text{ k}\Omega} = 2$$
   $$V_{o2} = A_v \cdot V_{o1} = 2 \cdot 0.6\text{ V} = 1.2\text{ V}$$
   Esta ganancia en cascada ($A_{total} = A_d \cdot A_v = 20$) ajusta el nivel de la señal por debajo del límite de $3.0\text{ V}$ para proteger y no saturar el conversor analógico del microcontrolador.

3. **Filtro Pasabajas Pasivo $RC$:**
   Se acopló a la salida un filtro pasivo de primer orden constituido por una resistencia en serie $R = 10\text{ k}\Omega$ y un capacitor a tierra $C = 0.1\ \mu\text{F}$:
   $$f_c = \frac{1}{2\pi R C} = \frac{1}{2\pi (10\,000\,\Omega)(0.1\times 10^{-6}\,\text{F})} \approx 159.15\text{ Hz}$$
   $$\tau = R \cdot C = 1\text{ ms}$$

4. **Comparador de Voltaje y Alarma Visual:**
   Se implementó un comparador de tensión utilizando un tercer LM741 en lazo abierto. La señal acondicionada ($V_{filt} = 1.2\text{ V}$) se conectó a la terminal no inversora ($V_+$), mientras que a la terminal inversora ($V_-$) se aplicó una tensión de referencia fija de $V_{ref} = 1.0\text{ V}$ mediante un divisor resistivo con potenciómetro. Al cumplirse $V_+ > V_{ref}$, la salida satura positivamente ($V_{sat}^+$) y polariza en directa un LED rojo en serie con $330\ \Omega$.

```
[ +80 mV ] ----(+) \
                     LM741 (Dif, Ad=10) ---> [ 0.6 V ] ----(+) \
[ +20 mV ] ----(-) /                                            LM741 (No Inv, Av=2) ---> [ 1.2 V ]
                                                    GND ----(-) /                               |
                                                                                                |
                                 +--------------------------------------------------------------+
                                 |
                                [R = 10k]
                                 |
                                 +----+----> [ C = 0.1 uF ] ---> GND
                                 |           (Filtro fc = 159.15 Hz)
                                 |
         +-----------------------+-----------------------+
         |                                               |
         v                                               v
    [ Pin ADC ]                                    (+) \
      ESP32                                              LM741 (Comp) ---> [ 330 ohm ] ---> [ LED ]
        |                                  Vref = 1.0V --(-) /
        | (UART: 115200 baud)
        v
    [ LabVIEW VI ]
```
: Figure 1. Diagrama esquemático en bloques de la cadena de acondicionamiento y adquisición.

---

### 2.2.2. Adquisición y Comunicación Serial (ESP32 y LabVIEW)

1. El microcontrolador ESP32 se programó para digitalizar la señal analógica y adquirir los datos temporales del sensor ultrasónico (HC-SR04).
2. Se configuró el puerto serie a una tasa de 115200 baudios para transmitir paquetes de datos continuos hacia la computadora.
3. En LabVIEW se estructuró un Instrumento Virtual (VI) basado en la librería NI-VISA para la apertura, lectura periódica en búfer, decodificación mediante *Scan from String* y graficación continua en un *Waveform Chart*.

---

# 3. Results

En esta sección se presentan las simulaciones por software y las evidencias experimentales recabadas en laboratorio.

## 3.1. Simulación Circuital en Multisim

Se simuló la cadena completa en Multisim Live para verificar la linealidad de la respuesta y la respuesta en frecuencia del filtro pasabajas.

![Simulación circuital de la cadena completa en Multisim](img/simulacion_multisim.png){#fig:multisim width=85%}

La simulación ratificó las tensiones teóricas de diseño: $0.6\text{ V}$ a la salida del diferencial, $1.2\text{ V}$ a la salida del no inversor, y una frecuencia de corte a $-3\text{ dB}$ en $159\text{ Hz}$.

## 3.2. Medición en Osciloscopio: Efecto del Filtro Pasabajas

Se comparó en el osciloscopio la señal analógica antes de entrar al filtro $RC$ respecto a la señal entregada en bornes del capacitor.

![Oscilograma de la señal antes y después del filtro pasabajas RC](img/osciloscopio_filtro.png){#fig:filtro width=85%}

Se constató una disminución notable del rizado de conmutación y ruido de acoplo inductivo, manteniendo estable la lectura de $1.2\text{ V}$ en DC.

## 3.3. Activación del Comparador y Circuito Físico

Al inyectar los niveles de entrada de $80\text{ mV}$ y $20\text{ mV}$, el voltaje acondicionado de $1.2\text{ V}$ superó la referencia calibrada de $1.0\text{ V}$, provocando la transición a estado alto en la salida del comparador y encendiendo el LED indicador de advertencia.

![Circuito implementado en protoboard con indicador LED activado](img/circuito_protoboard.png){#fig:protoboard width=80%}

## 3.4. Instrumento Virtual en LabVIEW

El flujo continuo de datos transmitido por el ESP32 fue procesado satisfactoriamente por el VI de LabVIEW, desplegando la evolución de la variable en tiempo real.

![Panel Frontal del Instrumento Virtual en LabVIEW](img/labview_front_panel.png){#fig:lv_front width=85%}

![Diagrama de Bloques del Instrumento Virtual en LabVIEW](img/labview_block_diagram.png){#fig:lv_block width=85%}

---

# 4. Discussion

A continuación se analizan los aspectos técnicos y analíticos más relevantes del diseño:

1. **Efectividad del escalamiento de ganancia en etapas:**  
   Dividir la ganancia total de 20 en dos bloques ($A_d = 10$ y $A_v = 2$) en lugar de exigirla en una única etapa diferencial aporta ventajas críticas de diseño:
   - **Producto Ganancia-Ancho de Banda (GBW):** Dado que el LM741 cuenta con un GBW nominal de aproximadamente $1\text{ MHz}$, la implementación en cascada asegura un ancho de banda individual de $100\text{ kHz}$ en la primera etapa y $500\text{ kHz}$ en la segunda, evitando la atenuación de componentes de señal y dispersión de fase.
   - **Relación de Rechazo en Modo Común (CMRR):** Un diferencial con ganancia $10$ utiliza resistencias de $10\text{ k}\Omega$ y $1\text{ k}\Omega$, fáciles de emparejar al $1\%$ comercialmente, manteniendo un elevado CMRR que se degradaría si se intentaran implementar ganancias elevadas con dispersión de tolerancias.
   - **Zona de operación del ADC:** La tensión máxima obtenida ($1.2\text{ V}$) se ubica en el segmento más lineal del convertidor ADC del ESP32, el cual presenta no-linealidades severas (saturación y compresión) por encima de $2.8\text{ V}$ y por debajo de $0.15\text{ V}$.

2. **Impacto del filtro pasabajas en la dinámica del sistema:**  
   Con una frecuencia de corte $f_c \approx 159.15\text{ Hz}$ y una constante de tiempo $\tau = 1\text{ ms}$, el tiempo de asentamiento ($5\tau = 5\text{ ms}$) es insignificante frente a la dinámica física de variación de fuerzas manuales o mecánicas. No obstante, si se aplicaran cambios bruscos tipo escalón de alta frecuencia (impactos), el filtro pasivo de primer orden suavizaría las transiciones abruptas.

3. **Ventajas del comparador analógico por hardware:**  
   Implementar el comparador directamente en el dominio analógico proporciona una respuesta en microsegundos, asegurando una protección de sobrecarga *fail-safe* totalmente inmune a fallos de firmware, cuelgues del microcontrolador o demoras en la comunicación serie.

4. **Propuestas de mejora para alta resolución y velocidad:**  
   En un entorno de grado industrial, se recomienda sustituir la topología discreta de amplificadores LM741 por un amplificador de instrumentación monolítico integrado (ej. **INA128** o **AD620**), el cual cuenta con un CMRR superior a $100\text{ dB}$ gracias a sus resistencias ajustadas internamente por láser. Asimismo, la digitalización ganaría sustancialmente en linealidad y resolución empleando un ADC externo de 16 bits (como el **ADS1115**) con referencia de tensión de precisión.

---

# 5. Conclusions

Se implementó y validó con éxito una cadena completa de acondicionamiento analógico y adquisición digital. El uso en cascada de amplificadores operacionales LM741 permitió elevar una diferencia de potencial débil de $60\text{ mV}$ hasta un nivel robusto de $1.2\text{ V}$, ideal para su digitalización sin saturar el microcontrolador. El filtro $RC$ pasivo demostró atenuar eficazmente el ruido eléctrico sin introducir retardos significativos en la respuesta transitoria. Finalmente, la integración del ESP32 con LabVIEW confirmó la viabilidad de la arquitectura propuesta para adquisición, supervisión gráfica y disparo de alarmas en tiempo real.

---

# References

[1] R. G. Lyons, *Understanding Digital Signal Processing*, 3rd ed. Boston: Prentice Hall, 2010.  
[2] R. Mancini, *Op Amps for Everyone: Design Reference*, 2nd ed. Oxford: Newnes, 2003.  
[3] Texas Instruments, "LM741 Operational Amplifier Datasheet," SNOSC25D, May 2004 (Revised Oct. 2014).  
[4] Espressif Systems, "ESP32 Series Datasheet," v4.2, 2023.  

---

# Personal comments

### Alumno 1
*Reflexión personal del alumno sobre los retos del acondicionamiento analógico, ajuste de ganancias y calibración.*

### Alumno 2
*Reflexión personal del alumno sobre la integración del microcontrolador ESP32 y la comunicación serial con LabVIEW.*

### Alumno 3
*Reflexión personal del alumno sobre la simulación vs. comportamiento físico observado en el osciloscopio.*
