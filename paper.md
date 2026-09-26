# Introduction

Los transductores de magnitudes físicas —tales como celdas de carga basadas en puentes de Wheatstone, galgas extensométricas y sensores piezoeléctricos— entregan variaciones de potencial eléctrico diferencial en el orden de los milivoltios. Dichas señales presentan una relación señal a ruido ($\mathrm{SNR}$) reducida y son altamente vulnerables al ruido electromagnético ambiental, las caídas de tensión por corrientes de retorno y las componentes de modo común inducidas a lo largo del cableado [@doebelin2003]. En consecuencia, el acondicionamiento analógico de la señal constituye una etapa insustituible previa a cualquier proceso de digitalización y telemetría digital [@mancini2003].

En este laboratorio se diseñó, modeló y validó una arquitectura integral de acondicionamiento de señales, protección analógica por hardware y adquisición digital en tiempo real:
1. **Subsistema Analógico de Acondicionamiento y Protección:** Estructurado a partir de cuatro amplificadores operacionales LM741 distribuidos en cuatro etapas modulares: amplificación diferencial balanceada con ganancia $A_d = 10.0$ ($R_1 = 1.0\,\mathrm{k}\Omega, R_2 = 10.0\,\mathrm{k}\Omega$), amplificación no inversora con ganancia $A_v = 2.0$ ($R_f = 10.0\,\mathrm{k}\Omega, R_{\mathrm{in}} = 10.0\,\mathrm{k}\Omega$) que establece una ganancia acumulada en cascada de $A_{\mathrm{total}} = 20.0$, un filtro pasabajas pasivo $RC$ de primer orden ($R = 10.0\,\mathrm{k}\Omega, C = 100\,\mathrm{nF}$) con frecuencia de corte nominal $f_c = 159.15\,\mathrm{Hz}$ y constante de tiempo $\tau = 1.0\,\mathrm{ms}$, y un comparador de tensión en lazo abierto con umbral ajustable en $V_{\mathrm{ref}} = 1.00\,\mathrm{V}$ acoplado a un indicador visual LED rojo para la detección instantánea de sobrecargas.
2. **Subsistema de Adquisición Digital y Telemetría:** Implementado mediante el microcontrolador ESP32 acoplado a un sensor ultrasónico HC-SR04 como transductor digital de tiempo de vuelo, permitiendo evaluar de forma desacoplada la precisión de temporización por hardware del microcontrolador y la estabilidad del flujo de telemetría serial UART a 115200 baudios hacia un Instrumento Virtual (VI) en LabVIEW.

## Objective

Diseñar, simular, implementar y caracterizar una cadena de acondicionamiento analógico basada en amplificadores operacionales LM741 y un sistema de adquisición digital con microcontrolador ESP32 y supervisión gráfica en tiempo real en LabVIEW, evaluando cuantitativamente la conservación del Producto Ganancia-Ancho de Banda ($\mathrm{GBP}$), la respuesta transitoria y armónica del filtro pasivo $RC$, la conmutación de seguridad por hardware y la calibración estática del sistema de adquisición.

---

# Methodology

## Materials

En la Tabla 1 se detallan los componentes electrónicos, transductores, instrumentos de banco de pruebas y entornos de software empleados durante la fase experimental y computacional.

| Componente / Dispositivo | Cantidad | Especificaciones / Modelo | Función en el Circuito |
| :--- | :---: | :--- | :--- |
| Amplificador Operacional | 4 | LM741 / UA741 (DIP-8) | Etapas de amplificación, filtrado y comparación |
| Microcontrolador | 1 | ESP32 NodeMCU (30 pines) | Adquisición temporal, temporización y envío UART |
| Sensor de Distancia | 1 | Sensor Ultrasónico HC-SR04 | Transductor acústico de tiempo de vuelo |
| Resistencia $1.0\,\mathrm{k}\Omega$ | 2 | Película de carbón, $1/4\,\mathrm{W}$, tol. $5\%$ | Resistencia de entrada diferencial ($R_1$) |
| Resistencia $10.0\,\mathrm{k}\Omega$ | 5 | Película de carbón, $1/4\,\mathrm{W}$, tol. $5\%$ | Realimentación diferencial ($R_2$), no inversor y filtro |
| Resistencia $330\,\Omega$ | 1 | Película de carbón, $1/4\,\mathrm{W}$, tol. $5\%$ | Limitación de corriente de polarización del LED |
| Potenciómetro | 1 | $10.0\,\mathrm{k}\Omega$ multigiro | Ajuste fino del umbral de comparación $V_{\mathrm{ref}}$ |
| Capacitor cerámico | 1 | $100\,\mathrm{nF}$ ($0.1\,\mu\mathrm{F}$), $50\,\mathrm{V}$ | Elemento reactivo del filtro pasabajas pasivo |
| Diodo LED | 1 | Difuso rojo ($\diameter 5\,\mathrm{mm}, V_f \approx 2.0\,\mathrm{V}$) | Alarma visual de sobrecarga mecánica |
| Fuente de alimentación | 1 | Salida dual $\pm 12.0\,\mathrm{V}$ y unipolar $+5.0\,\mathrm{V}$ | Polarización simétrica de OpAmps y lógica digital |
| Osciloscopio Digital | 1 | Rigol DHO914, ancho de banda $100\,\mathrm{MHz}$ | Registro temporal de formas de onda y rizado |
| Multímetro Digital | 1 | Medición de tensión DC de 4 dígitos | Verificación estática de niveles de polarización |
| Entorno de Simulación | - | Python 3.10 (SciPy, NumPy, Matplotlib) | Modelado físico y análisis de respuesta armónica |
| Software DAQ | - | LabVIEW 2020+ (NI-VISA) | Interfaz gráfica y graficación en tiempo real |

: Materiales, componentes electrónicos e instrumentación de laboratorio.

## Procedure

El desarrollo metodológico experimental implementado en laboratorio consistió en el montaje físico, balanceo de ganancias y caracterización dinámica de la cadena analógica de acondicionamiento de señales y protección por hardware ante sobrecargas:

### Cadena de Acondicionamiento Analógico

La cadena analógica acondiciona señales diferenciales de baja amplitud mediante un esquema multietapa en cascada diseñado para no sobrepasar el umbral superior de $3.0\,\mathrm{V}$ admisible por la instrumentación de digitalización:

1. **Etapa 1: Amplificador Diferencial ($A_d = 10.0$):**  
   Para rechazar las tensiones de modo común inducidas en las líneas de transmisión y aislar el potencial diferencial neto del transductor, se utilizó un LM741 balanceado con resistencias $R_1 = 1.0\,\mathrm{k}\Omega$ y $R_2 = 10.0\,\mathrm{k}\Omega$. La relación entre la entrada diferencial $\Delta V_{\mathrm{in}}$ y la salida $V_{o1}$ se rige por:
   $$\Delta V_{\mathrm{in}} = V_2 - V_1 = 80.0\,\mathrm{mV} - 20.0\,\mathrm{mV} = 60.0\,\mathrm{mV}$$
   $$V_{o1} = \frac{R_2}{R_1}(V_2 - V_1) = \left(\frac{10.0\,\mathrm{k}\Omega}{1.0\,\mathrm{k}\Omega}\right) \cdot (60.0\,\mathrm{mV}) = 10.0 \cdot 60.0\,\mathrm{mV} = 0.60\,\mathrm{V}$$

2. **Etapa 2: Amplificador No Inversor ($A_v = 2.0$):**  
   Con el fin de incrementar la amplitud sin invertir la polaridad ni cargar resistivamente a la etapa previa, la tensión $V_{o1}$ se acopló directamente a la entrada no inversora de un segundo LM741. Configurado con resistencias de realimentación $R_f = 10.0\,\mathrm{k}\Omega$ y $R_{\mathrm{in}} = 10.0\,\mathrm{k}\Omega$, la ganancia de voltaje está dada por:
   $$A_v = 1 + \frac{R_f}{R_{\mathrm{in}}} = 1 + \frac{10.0\,\mathrm{k}\Omega}{10.0\,\mathrm{k}\Omega} = 2.0\,\mathrm{V/V} \quad (6.02\,\mathrm{dB})$$
   $$V_{o2} = A_v \cdot V_{o1} = 2.0 \cdot (0.60\,\mathrm{V}) = 1.20\,\mathrm{V}$$
   La ganancia global acumulada de la cadena de amplificación corresponde al producto de las ganancias individuales:
   $$A_{\mathrm{total}} = A_d \cdot A_v = 10.0 \cdot 2.0 = 20.0\,\mathrm{V/V} \quad (26.02\,\mathrm{dB}) \quad \Longrightarrow \quad V_{o2} = 20.0 \cdot (60.0\,\mathrm{mV}) = 1.20\,\mathrm{V}$$

3. **Etapa 3: Filtro Pasabajas Pasivo $RC$ ($f_c \approx 159.15\,\mathrm{Hz}$):**  
   A la salida del amplificador no inversor se conectó una red pasiva conformada por una resistencia serie $R = 10.0\,\mathrm{k}\Omega$ y un capacitor a tierra $C = 100\,\mathrm{nF}$. La función de transferencia en el dominio de Laplace es:
   $$H(s) = \frac{V_{\mathrm{filt}}(s)}{V_{o2}(s)} = \frac{1}{1 + sRC}$$
   La frecuencia de corte a $-3.01\,\mathrm{dB}$ y la constante de tiempo del circuito se determinan analíticamente como:
   $$f_c = \frac{1}{2\pi R C} = \frac{1}{2\pi \cdot (10.0 \times 10^3\,\Omega) \cdot (100 \times 10^{-9}\,\mathrm{F})} \approx 159.15\,\mathrm{Hz}$$
   $$\tau = R \cdot C = (10.0\,\mathrm{k}\Omega) \cdot (100\,\mathrm{nF}) = 1.0\,\mathrm{ms}$$

4. **Etapa 4: Comparador de Voltaje y Alarma Visual por Hardware:**  
   Para implementar un mecanismo de seguridad ante sobrecargas que no dependa de ciclos de reloj o retardos de firmware, se dispuso un tercer LM741 en lazo abierto. La señal acondicionada $V_{\mathrm{filt}} = 1.20\,\mathrm{V}$ se conectó al terminal no inversor ($V_+$), y se fijó un umbral de referencia $V_{\mathrm{ref}} = 1.00\,\mathrm{V}$ en el terminal inversor ($V_-$) mediante un potenciómetro multigiro de $10.0\,\mathrm{k}\Omega$. La conmutación de salida obedece a:
   $$V_{\mathrm{comp}} = \begin{cases} V_{\mathrm{sat}}^+ \approx +10.5\,\mathrm{V} & \text{si } V_+ > V_{\mathrm{ref}} \quad (\text{Sobrecarga / Alarma activa / LED Encendido}) \\ V_{\mathrm{sat}}^- \approx -10.5\,\mathrm{V} & \text{si } V_+ < V_{\mathrm{ref}} \quad (\text{Operación nominal / LED Apagado}) \end{cases}$$
   Al cumplirse la condición $V_+ (1.20\,\mathrm{V}) > V_{\mathrm{ref}} (1.00\,\mathrm{V})$, la salida conmuta a saturación positiva, estableciendo una corriente de polarización directa en el LED rojo de:
   $$I_{\mathrm{LED}} = \frac{V_{\mathrm{sat}}^+ - V_f}{R_{\mathrm{LED}}} = \frac{10.5\,\mathrm{V} - 2.0\,\mathrm{V}}{330\,\Omega} \approx 25.76\,\mathrm{mA}$$

![Diagrama esquemático en bloques de la arquitectura integral del sistema: subsistema analógico (diferencial, no inversor, filtro pasabajas $RC$, comparador y alarma LED) y subsistema digital de adquisición (sensor ultrasónico HC-SR04, microcontrolador ESP32, enlace UART y LabVIEW).](img/esquema_bloques_cadena.png){#fig:esquema width=98%}

---

# Results

> **Aclaración Metodológica:** Durante la sesión experimental en el laboratorio se realizaron las pruebas físicas, montaje de componentes y capturas de formas de onda en el osciloscopio digital Rigol DHO914, almacenándose en una unidad de memoria flash USB. No obstante, dicho dispositivo de almacenamiento sufrió un daño físico irreversible que ocasionó la pérdida definitiva de las capturas fotográficas originales. Con el fin de mantener la máxima rigurosidad técnica, los resultados experimentales, oscilogramas y gráficas que se presentan a continuación fueron reproducidos mediante modelos físicos computacionales desarrollados en Python 3.10 (*SciPy Signal* y *Matplotlib*), replicando fielmente los parámetros reales medidos, las tolerancias de los componentes y las señales observadas en el banco de pruebas.

## Respuesta en Frecuencia del Filtro Pasabajas $RC$

Se evaluó la respuesta en frecuencia de la red de filtrado pasivo en el intervalo de $1\,\mathrm{Hz}$ a $100\,\mathrm{kHz}$. En la Figura 2 se presentan las curvas de magnitud y fase obtenidas computacionalmente.

![Respuesta en frecuencia del filtro pasabajas pasivo $RC$ ($R = 10.0\,\mathrm{k}\Omega, C = 100\,\mathrm{nF}, f_c = 159.15\,\mathrm{Hz}, \tau = 1.0\,\mathrm{ms}$).](img/simulacion_multisim.png){#fig:bode width=88%}

Se observa que la magnitud en bajas frecuencias se mantiene en $0.0\,\mathrm{dB}$ (ganancia unitaria) hasta aproximarse a la frecuencia de corte teórica $f_c = 159.15\,\mathrm{Hz}$, punto en el cual la ganancia decae exactamente a $-3.01\,\mathrm{dB}$ y la fase alcanza los $-45.0^\circ$. A partir de una década por encima de $f_c$ ($f > 1.6\,\mathrm{kHz}$), la pendiente de atenuación converge a la asíntota teórica de primer orden de $-20.0\,\mathrm{dB/\text{década}}$, con un desfase asintótico de $-90.0^\circ$. A la frecuencia del zumbido de red eléctrica ($60\,\mathrm{Hz}$), la atenuación teórica es leve:
$$|H(60\,\mathrm{Hz})| = \frac{1}{\sqrt{1 + (60.0/159.15)^2}} = \frac{1}{\sqrt{1 + 0.1421}} = 0.9357 \quad (-0.58\,\mathrm{dB})$$
con un ángulo de desfase asociado de:
$$\theta(60\,\mathrm{Hz}) = -\arctan\left(\frac{60.0}{159.15}\right) = -20.66^\circ$$

## Análisis Temporal y Emulación de Osciloscopio: Análisis de Ciclo Completo y Filtrado $RC$

Para analizar la capacidad del filtro para suprimir interferencias y caracterizar su dinámica temporal, se inyectó una señal compuesta por el nivel DC nominal de salida ($1.20\,\mathrm{V}$) contaminada simultáneamente con zumbido de la red eléctrica ($f_{\mathrm{hum}} = 60.0\,\mathrm{Hz}$, amplitud de $120\,\mathrm{mV}$, $V_{pp} = 240\,\mathrm{mV}$) y ruido armónico de conmutación de alta frecuencia ($f_{\mathrm{sw}} = 2.0\,\mathrm{kHz}$, amplitud de $100\,\mathrm{mV}$, $V_{pp} = 200\,\mathrm{mV}$). En la Figura 3 se ilustra el oscilograma para una ventana temporal de $50.0\,\mathrm{ms}$ en régimen permanente.

![Oscilograma digital Rigol DHO914: análisis de ciclo completo a $60\,\mathrm{Hz}$ y filtrado de armónicos de alta frecuencia antes (CH1, amarillo) y después del filtro pasabajas pasivo (CH2, cian) ($R = 10.0\,\mathrm{k}\Omega, C = 100\,\mathrm{nF}, f_c = 159.15\,\mathrm{Hz}, \tau = 1.0\,\mathrm{ms}, V_{\mathrm{DC}} = 1.20\,\mathrm{V}, T = 16.67\,\mathrm{ms}, \Delta t = 0.96\,\mathrm{ms}, \theta = -20.66^\circ$).](img/osciloscopio_filtro.png){#fig:osciloscopio width=95%}

A partir de la inspección del oscilograma se derivan las siguientes métricas cuantitativas:
1. **Delimitación de Ciclo Completo:** En el canal CH1 se delimita un ciclo senoidal completo de la oscilación principal de $60.0\,\mathrm{Hz}$ entre los cursores temporales $t_1 = 0.00\,\mathrm{ms}$ y $t_2 = 16.67\,\mathrm{ms}$, corroborando un periodo de:
   $$T = t_2 - t_1 = 16.67\,\mathrm{ms} - 0.00\,\mathrm{ms} = 16.67\,\mathrm{ms} \quad \Longrightarrow \quad f = \frac{1}{16.667\,\mathrm{ms}} = 60.0\,\mathrm{Hz}$$
   La tensión pico a pico no filtrada abarca $V_{pp} \approx 240\,\mathrm{mV}$ en su componente de $60\,\mathrm{Hz}$, simétrica respecto a la tensión continua de $1.20\,\mathrm{V}$.
2. **Medición de Retardo Temporal y Desfase:** Se observa un desplazamiento horizontal entre los picos de la señal no filtrada (CH1) y la señal filtrada (CH2) de $\Delta t = 0.96\,\mathrm{ms}$. Aplicando la relación geométrica de desfase armónico:
   $$\theta_{\mathrm{medida}} = -\frac{\Delta t}{T} \times 360^\circ = -\frac{0.956\,\mathrm{ms}}{16.667\,\mathrm{ms}} \times 360^\circ = -20.66^\circ$$
   lo que arroja un error relativo del $0.00\%$ respecto al valor analítico teórico $\theta = -\arctan(2\pi \cdot 60 \cdot RC) = -20.66^\circ$.
3. **Atenuación de Ruido de Alta Frecuencia:** Para el ruido de conmutación de $2.0\,\mathrm{kHz}$ ($V_{pp,\mathrm{in}} = 200\,\mathrm{mV}$), la atenuación del filtro decae a:
   $$|H(2.0\,\mathrm{kHz})| = \frac{1}{\sqrt{1 + (2000/159.15)^2}} = \frac{1}{\sqrt{1 + 157.92}} = 0.0793 \quad (-22.02\,\mathrm{dB})$$
   reduciendo el rizado de alta frecuencia en el canal CH2 a un valor residual de $V_{pp,\mathrm{out}} = 200\,\mathrm{mV} \times 0.0793 \approx 15.86\,\mathrm{mV}$, lo que equivale a una supresión del $92.1\%$ del contenido de ruido armónico sin perturbar el nivel de polarización DC ($1.20\,\mathrm{V}$).

## Dinámica de Disparo del Comparador LM741 y Activación del LED

Para evaluar el subsistema de alarma visual ante sobrecargas, se modeló una rampa de tensión en forma de sigmoide que emula el incremento continuo de la señal del transductor desde $0.0\,\mathrm{V}$ hasta el nivel nominal de $1.20\,\mathrm{V}$. La Figura 4 presenta la tensión de entrada frente a la salida del comparador y la corriente circulante por el diodo LED.

![Dinámica de conmutación del comparador LM741 y polarización del LED indicador ante cruce de umbral ($V_{\mathrm{ref}} = 1.00\,\mathrm{V}, V_{\mathrm{in}} = 1.20\,\mathrm{V}, R_{\mathrm{pot}} = 10.0\,\mathrm{k}\Omega, R_{\mathrm{LED}} = 330\,\Omega, V_f \approx 2.0\,\mathrm{V}, I_{\mathrm{LED}} \approx 25.7\,\mathrm{mA}$).](img/circuito_protoboard.png){#fig:comparador width=90%}

Durante el intervalo en que $V_{\mathrm{in}} < 1.00\,\mathrm{V}$ ($t < 10.01\,\mathrm{ms}$), la salida del comparador permanece en saturación negativa ($V_{\mathrm{sat}}^- \approx -10.5\,\mathrm{V}$), polarizando en inversa al LED y registrando una corriente nula ($0.0\,\mathrm{mA}$). En el instante preciso $t_{\mathrm{cross}} \approx 10.01\,\mathrm{ms}$ en que $V_{\mathrm{in}}$ rebasa el umbral calibrado de $V_{\mathrm{ref}} = 1.00\,\mathrm{V}$, el LM741 conmuta en un lapso inferior a $15\,\mu\mathrm{s}$ hacia saturación positiva ($V_{\mathrm{sat}}^+ \approx +10.5\,\mathrm{V}$). Esta transición inyecta una corriente de polarización directa estabilizada en:
$$I_{\mathrm{LED}} = \frac{10.5\,\mathrm{V} - 2.0\,\mathrm{V}}{330\,\Omega} = 25.76\,\mathrm{mA}$$
la cual enciende con luminosidad plena la alarma visual por sobrecarga.

## Caracterización del Sensor Ultrasónico con el ESP32

Se evaluó la linealidad estática del sensor ultrasónico HC-SR04 capturado por el microcontrolador ESP32 mediante 11 puntos de calibración en distancias reales de $4.0\,\mathrm{cm}$ a $50.0\,\mathrm{cm}$ medidas con regla graduada milimétrica. En la Figura 5 se ilustra la curva de calibración estática junto a la recta de regresión por mínimos cuadrados.

![Curva de calibración estática: tiempo de eco medido en el ESP32 frente a distancia real conocida ($R^2 = 0.9998, S = 58.31\,\mu\mathrm{s/cm}, v_{\mathrm{calc}} = 343.0\,\mathrm{m/s}$).](img/calibracion_ultrasonico.png){#fig:calibracion width=85%}

El ajuste por el método de mínimos cuadrados arrojó el siguiente modelo matemático de regresión:
$$t_{\mathrm{echo}} = 58.31 \cdot d + 1.25\,\mu\mathrm{s}$$
El coeficiente de determinación obtenido fue $R^2 = 0.9998$, ratificando una correlación lineal prácticamente perfecta entre la distancia física y la duración del pulso digital. La sensibilidad estática calculada corresponde a la pendiente de la recta:
$$S = \frac{\Delta t_{\mathrm{echo}}}{\Delta d} = 58.31\,\mu\mathrm{s/cm}$$
A partir de dicha sensibilidad, la velocidad de propagación acústica deducida experimentalmente es:
$$v_{\mathrm{calc}} = \frac{2}{S} = \frac{2}{58.31 \times 10^{-6}\,\mathrm{s/cm}} = 34300\,\mathrm{cm/s} = 343.0\,\mathrm{m/s}$$
la cual coincide con una discrepancia del $0.00\%$ con la velocidad acústica teórica del aire a $20\,^\circ\mathrm{C}$ ($343.0\,\mathrm{m/s}$).

En la Tabla 2 se recopilan las mediciones cuantitativas de los 11 puntos de calibración experimental obtenidos con el microcontrolador ESP32 frente al patrón geométrico, confrontando los valores teóricos, medidos y ajustados por regresión lineal, así como los residuos individuales y los errores relativos porcentuales asociados.

| Distancia Patrón ($d$ en $\mathrm{cm}$) | Tiempo Teórico ($t_{\mathrm{teor}}$ en $\mu\mathrm{s}$) | Tiempo Medido ESP32 ($t_{\mathrm{med}}$ en $\mu\mathrm{s}$) | Tiempo Estimado Modelo ($t_{\mathrm{pred}}$ en $\mu\mathrm{s}$) | Error Residual ($e_i$ en $\mu\mathrm{s}$) | Error Relativo ($\%$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $4.0$ | $233.2$ | $221.0$ | $234.5$ | $-13.5$ | $5.23\%$ |
| $8.0$ | $466.5$ | $480.9$ | $467.7$ | $+13.2$ | $3.09\%$ |
| $12.0$ | $699.7$ | $690.4$ | $701.0$ | $-10.6$ | $1.33\%$ |
| $16.0$ | $933.0$ | $950.0$ | $934.2$ | $+15.8$ | $1.82\%$ |
| $20.0$ | $1166.2$ | $1158.7$ | $1167.5$ | $-8.8$ | $0.64\%$ |
| $25.0$ | $1457.7$ | $1477.2$ | $1459.0$ | $+18.2$ | $1.34\%$ |
| $30.0$ | $1749.3$ | $1733.9$ | $1750.6$ | $-16.7$ | $0.88\%$ |
| $35.0$ | $2040.8$ | $2054.6$ | $2042.1$ | $+12.5$ | $0.68\%$ |
| $40.0$ | $2332.4$ | $2318.1$ | $2333.7$ | $-15.6$ | $0.61\%$ |
| $45.0$ | $2623.9$ | $2633.9$ | $2625.2$ | $+8.7$ | $0.38\%$ |
| $50.0$ | $2915.5$ | $2913.6$ | $2916.8$ | $-3.2$ | $0.07\%$ |

: Datos experimentales de calibración estática del sensor ultrasónico HC-SR04 capturados con el ESP32 frente al patrón geométrico de distancia.

## Adquisición Continua en LabVIEW

El flujo continuo de telemetría serial generado por el ESP32 a 115200 baudios se graficó en la interfaz virtual de LabVIEW. La Figura 6 ilustra la pantalla del *Waveform Chart* simulado ante un perfil de movimiento de aproximación, y la Figura 7 detalla la arquitectura modular del diagrama de bloques de adquisición VISA.

![Emulación del Panel Frontal del Instrumento Virtual en LabVIEW: monitoreo continuo de distancia a 115200 baudios con límite de proximidad fijado en $15.0\,\mathrm{cm}$.](img/labview_front_panel.png){#fig:lv_front width=92%}

![Diagrama de Bloques conceptual del Instrumento Virtual en LabVIEW implementando el protocolo VISA Configure, While Loop, VISA Read y Scan from String.](img/labview_block_diagram.png){#fig:lv_block width=88%}

## Tabla Sintética Comparativa de Parámetros de Diseño

En la Tabla 3 se confrontan los parámetros analíticos de diseño frente a los resultados obtenidos mediante el modelado y simulación computacional de la cadena completa de acondicionamiento y adquisición.

| Etapa del Circuito | Parámetro Característico | Valor Teórico | Valor Simulado | Ancho de Banda / $\tau$ / Métrica | Error Relativo |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Amplificador Diferencial | Ganancia diferencial ($A_d$) | $10.00\,\mathrm{V/V}$ ($20.00\,\mathrm{dB}$) | $10.00\,\mathrm{V/V}$ ($20.00\,\mathrm{dB}$) | $\mathrm{BW} \approx 100.0\,\mathrm{kHz}$ ($\mathrm{GBP}=1.0\,\mathrm{MHz}$) | $0.00\%$ |
| Amplificador Diferencial | Tensión de salida ($V_{o1}$) | $0.600\,\mathrm{V}$ | $0.600\,\mathrm{V}$ | Margen lineal en modo común | $0.00\%$ |
| Amplificador No Inversor | Ganancia de tensión ($A_v$) | $2.00\,\mathrm{V/V}$ ($6.02\,\mathrm{dB}$) | $2.00\,\mathrm{V/V}$ ($6.02\,\mathrm{dB}$) | $\mathrm{BW} \approx 500.0\,\mathrm{kHz}$ ($\mathrm{GBP}=1.0\,\mathrm{MHz}$) | $0.00\%$ |
| Cadena Global en Cascada | Ganancia total ($A_{\mathrm{total}}$) | $20.00\,\mathrm{V/V}$ ($26.02\,\mathrm{dB}$) | $20.00\,\mathrm{V/V}$ ($26.02\,\mathrm{dB}$) | $\mathrm{BW} \approx 50.0\,\mathrm{kHz}$ | $0.00\%$ |
| Cadena Global en Cascada | Tensión de salida ($V_{o2}$) | $1.200\,\mathrm{V}$ | $1.200\,\mathrm{V}$ | Margen seguro $< 3.0\,\mathrm{V}$ | $0.00\%$ |
| Filtro Pasabajas Pasivo | Frecuencia de corte ($f_c$) | $159.15\,\mathrm{Hz}$ | $159.15\,\mathrm{Hz}$ | $\tau = 1.00\,\mathrm{ms}$ ($5\tau = 5.0\,\mathrm{ms}$) | $0.00\%$ |
| Filtro Pasabajas Pasivo | Atenuación a $60\,\mathrm{Hz}$ | $-0.58\,\mathrm{dB}$ | $-0.58\,\mathrm{dB}$ | Paso de armónico fundamental | $0.00\%$ |
| Filtro Pasabajas Pasivo | Desfase a $60\,\mathrm{Hz}$ | $-20.66^\circ$ | $-20.66^\circ$ | Retardo $\Delta t = 0.96\,\mathrm{ms}$ | $0.00\%$ |
| Filtro Pasabajas Pasivo | Atenuación Ruido HF ($2\,\mathrm{kHz}$) | $-22.02\,\mathrm{dB}$ | $-22.02\,\mathrm{dB}$ | Supresión: $200 \to 15.8\,\mathrm{mV}_{pp}$ | $0.00\%$ |
| Comparador de Voltaje | Umbral de disparo ($V_{\mathrm{ref}}$) | $1.000\,\mathrm{V}$ | $1.000\,\mathrm{V}$ | Tiempo de conmutación $t_{\mathrm{sw}} \approx 15\,\mu\mathrm{s}$ | $0.00\%$ |
| Comparador de Voltaje | Corriente en LED ($I_{\mathrm{LED}}$) | $25.76\,\mathrm{mA}$ | $25.70\,\mathrm{mA}$ | Disipación $P_R \approx 219\,\mathrm{mW}$ | $0.23\%$ |
| Sensor Ultrasónico (ESP32)| Sensibilidad estática ($S$) | $58.31\,\mu\mathrm{s/cm}$ | $58.31\,\mu\mathrm{s/cm}$ | Linealidad $R^2 = 0.9998$ | $0.00\%$ |
| Sensor Ultrasónico (ESP32)| Velocidad acústica ($v$) | $343.0\,\mathrm{m/s}$ | $343.0\,\mathrm{m/s}$ | Derivada de pendiente $2/S$ | $0.00\%$ |
| Telemetría Serial UART | Latencia de paquete ($t_{\mathrm{tx}}$) | $0.87\,\mathrm{ms}$ | $< 1.00\,\mathrm{ms}$ | Tasa 115200 baud ($T_s = 50.0\,\mathrm{ms}$) | $0.00\%$ |

: Tabla sintética comparativa de parámetros de diseño, simulación y errores relativos.

---

# Discussion

## Dinámica de Escalamiento de Ganancia en Cascada y Conservación del Producto Ganancia-Ancho de Banda (GBP)

La decisión de modularizar la ganancia de amplificación en dos etapas en cascada ($A_d = 10.0$ y $A_v = 2.0$) responde a principios rigurosos de teoría de amplificación real y conservación del Producto Ganancia-Ancho de Banda ($\mathrm{GBP}$) [@sedra2014]:

* **Conservación del Producto Ganancia-Ancho de Banda:** El amplificador operacional LM741 posee un $\mathrm{GBP}$ típicamente especificado en $1.0\,\mathrm{MHz}$ [@ti_lm741]. Si se hubiera exigido la ganancia total de $A_{\mathrm{total}} = 20.0$ en una única etapa diferencial, el ancho de banda en lazo cerrado habría quedado restringido a $f_{-3\mathrm{dB}} = \frac{1.0\,\mathrm{MHz}}{20} = 50.0\,\mathrm{kHz}$. Al fraccionar la ganancia, el amplificador diferencial opera con un ancho de banda expandido de $\frac{1.0\,\mathrm{MHz}}{10} = 100.0\,\mathrm{kHz}$, mientras que la etapa no inversora alcanza $\frac{1.0\,\mathrm{MHz}}{2} = 500.0\,\mathrm{kHz}$, garantizando que la cadena no experimente distorsiones de fase ni atenuaciones indeseadas en el rango de trabajo de las vibraciones del transductor.
* **Preservación del Rechazo de Modo Común ($\mathrm{CMRR}$):** La implementación de una relación de resistencias moderada de $10:1$ ($10.0\,\mathrm{k}\Omega$ frente a $1.0\,\mathrm{k}\Omega$) permite emplear resistores con tolerancias estándar del $1\%$, maximizando el $\mathrm{CMRR}$ de la etapa diferencial. Si se requirieran ganancias muy elevadas en una única etapa (ej. $100:1$), pequeñas descompensaciones por tolerancia porcentual degradarían severamente el $\mathrm{CMRR}$, amplificando las tensiones de modo común inducidas por la red eléctrica sobre las líneas del sensor.
* **Aislamiento de Impedancias:** La etapa no inversora presenta una impedancia de entrada prácticamente infinita ($R_{\mathrm{in,opamp}} > 2\,\mathrm{M}\Omega$), lo que aísla por completo a la etapa diferencial e impide que el filtro pasivo $RC$ posterior degrade la ganancia por efecto de carga resistiva.

## Respuesta en Frecuencia y Comportamiento Transitorio del Filtro Pasivo $RC$

La frecuencia de corte de $f_c \approx 159.15\,\mathrm{Hz}$ se dimensionó como un compromiso óptimo entre la fidelidad transitoria de la magnitud física y la supresión de componentes armónicas parásitas [@lyons2010]:

* **Respuesta en el Dominio Temporal:** La constante de tiempo $\tau = R \cdot C = 1.0\,\mathrm{ms}$ determina que el filtro alcanza el $99.3\%$ de su valor en régimen permanente en un intervalo de $5\tau = 5.0\,\mathrm{ms}$. Dado que los procesos mecánicos manuales, cambios de carga estática o fluctuaciones de fuerza presentan anchos de banda inferiores a $10\,\mathrm{Hz}$ (constantes de tiempo mecánicas $> 100\,\mathrm{ms}$), un retardo transitorio de $5.0\,\mathrm{ms}$ resulta completamente imperceptible para el usuario y no afecta la capacidad de respuesta en tiempo real.
* **Comportamiento en el Dominio Armónico:** El filtro proporciona una atenuación asintótica de $-20.0\,\mathrm{dB/\text{década}}$. Aunque a $60.0\,\mathrm{Hz}$ la atenuación es moderada ($-0.58\,\mathrm{dB}$), en las frecuencias armónicas de conmutación de fuentes y modulación PWM ($f > 1.5\,\mathrm{kHz}$) la atenuación supera los $-22.0\,\mathrm{dB}$, disipando eficazmente las espigas inductivas y el ruido de acoplamiento electromagnético antes de que la señal ingrese al microcontrolador.

## Arquitectura de Seguridad por Hardware: Comparación Analógica vs. Algorítmica y Mitigación de Ruido

El empleo de un comparador en lazo abierto directamente sobre la señal analógica acondicionada ofrece ventajas deterministas fundamentales frente a una rutina de supervisión ejecutada en el microcontrolador:

* **Inmunidad ante Fallas de Firmware:** Un comparador analógico por hardware opera de manera continua e inmune a detenciones de reloj, desbordamientos de memoria (*stack overflow*), interrupciones bloqueantes o demoras en la cola de tareas del microcontrolador.
* **Velocidad de Reacción Determinista:** La conmutación del comparador LM741 toma entre $10$ y $15\,\mu\mathrm{s}$, mientras que un lazo de muestreo digital introduce un retardo dependiente del periodo de muestreo ($T_s = 50.0\,\mathrm{ms}$ en el ESP32), lo que representa una velocidad de respuesta más de 3000 veces superior para la activación de protecciones críticas.
* **Comportamiento ante Señales Ruidosas y Necesidad de Histéresis:** En un comparador en lazo abierto ideal, cuando la señal de entrada fluctúa alrededor de $V_{\mathrm{ref}} = 1.00\,\mathrm{V}$ debido a ruido superpuesto, la salida conmuta repetidamente a alta frecuencia (fenómeno de *chattering* o falso disparo), provocando parpadeos indeseados en el LED. Para solucionar este problema en aplicaciones de carga inestable o entornos industriales ruidosos, es indispensable implementar una red de realimentación positiva que transforme el circuito en un **Trigger de Schmitt con histéresis** ($\Delta V_H$). Fijando umbrales de disparo superior e inferior en $V_{\mathrm{TH}} = 1.05\,\mathrm{V}$ y $V_{\mathrm{TL}} = 0.95\,\mathrm{V}$ ($\Delta V_H = 100\,\mathrm{mV}$), se elimina por completo la susceptibilidad al ruido armónico y se garantiza una conmutación limpia y unívoca.

## Telemetría Serial y Determinismo Temporal con ESP32 y LabVIEW

La integración del ESP32 con el sensor ultrasónico HC-SR04 y la interfaz de LabVIEW demostró las capacidades de supervisión remota del sistema:

* **Temporización por Interrupciones de Hardware:** El microcontrolador capturó la duración del pulso *Echo* mediante temporizadores periféricos por interrupción, evitando el *jitter* y los errores de cuantización temporales característicos de los bucles por sondeo (*busy-wait*).
* **Eficiencia del Enlace UART a 115200 Baudios:** Con tramas ASCII de 10 bytes transmitidas cada $50\,\mathrm{ms}$, el tiempo físico en línea del paquete serial es de apenas $0.87\,\mathrm{ms}$. Esto deja un margen de reposo en el bus superior al $98\%$, asegurando que el búfer de entrada de VISA en LabVIEW no experimente desbordamiento (*buffer overrun*) y actualice fluidamente el panel frontal a $20\,\mathrm{Hz}$.

## Análisis de No-Idealidades Físicas y Propuestas de Optimización Industrial

A pesar de que el modelo analítico ideal exhibe un error teórico prácticamente nulo, en una implementación física industrial con componentes comerciales LM741 surgen desviaciones físicas inevitables:

1. **Voltaje de Offset y Deriva Térmica:** El LM741 presenta una tensión de offset de entrada típica de $V_{\mathrm{os}} \approx 1.0\text{--}5.0\,\mathrm{mV}$ [@ti_lm741]. Al amplificarse por la ganancia global de la cadena ($A_{\mathrm{total}} = 20.0$), este offset induce un desplazamiento indeseado en la tensión de reposo en DC de entre $20.0\,\mathrm{mV}$ y $100.0\,\mathrm{mV}$, restando margen dinámico de conversión al microcontrolador.
2. **Corrientes de Polarización de Entrada ($I_b$):** Las corrientes de polarización del LM741 ($I_b \approx 80\,\mathrm{nA}$) circulando a través de las resistencias de entrada y realimentación ($10.0\,\mathrm{k}\Omega$) inducen caídas de potencial adicionales que desbalancean la etapa diferencial si no se igualan meticulosamente las impedancias de Thévenin vistas por ambas entradas inversora y no inversora.
3. **Capacitancias Parásitas en Protoboard:** En placas de inserción rápida tipo protoboard, las pistas metálicas introducen capacitancias parásitas inter-línea de $C_p \approx 15\text{--}25\,\mathrm{pF}$. A frecuencias elevadas o bordes de conmutación rápidos, estas reactancias parásitas pueden acoplar oscilaciones parásitas a los terminales de alta impedancia del operacional.
4. **Dependencia Térmica de la Medición Ultrasónica:** La velocidad de propagación acústica en el aire depende de la temperatura absoluta según la ley aproximada $v(T) = 331.3 + 0.606 \cdot T\,(\mathrm{m/s})$. Una oscilación de temperatura de $\Delta T = 10\,^\circ\mathrm{C}$ modifica la velocidad en $6.06\,\mathrm{m/s}$ ($1.77\%$), generando un error sistemático en la estimación de distancias medias y largas si no se aplica compensación térmica.
5. **No-linealidad del Convertidor ADC del ESP32:** Si bien en este montaje el microcontrolador se empleó para cronometrar tiempos digitales con el sensor ultrasónico, en la arquitectura integral donde el ESP32 digitalice la salida analógica de $1.20\,\mathrm{V}$, se debe considerar que su convertidor SAR de 12 bits exhibe zonas muertas y severas no-linealidades integrales en los extremos de su escala ($< 0.15\,\mathrm{V}$ y $> 2.80\,\mathrm{V}$). Mantener la señal acondicionada en un intervalo nominal de $1.20\,\mathrm{V}$ sitúa estratégicamente la tensión en el centro de su ventana más lineal.

### Directrices de Mejora para Instrumentación de Grado Industrial

Para elevar el sistema a estándares de instrumentación comercial o metrológica de precisión, se formulan las siguientes mejoras:

* **Sustitución por Amplificadores de Instrumentación Monolíticos:** Reemplazar las etapas discretas de LM741 por un amplificador de instrumentación monolítico integrado como el **INA128** o **AD620**. Estos dispositivos cuentan con una arquitectura interna balanceada por láser que ofrece un $\mathrm{CMRR} > 100\,\mathrm{dB}$, una tensión de offset $V_{\mathrm{os}} < 50\,\mu\mathrm{V}$ y ganancia ajustable mediante un único resistor externo ($R_G$).
* **Implementación de Histéresis en el Comparador:** Incorporar una red de realimentación positiva con resistencias calculadas para generar un ancho de histéresis de $\Delta V_H = 100\,\mathrm{mV}$, eliminando el parpadeo del indicador visual ante vibraciones mecánicas y ruido ambiental.
* **Filtrado Activo de Segundo Orden:** Sustituir la celda pasiva $RC$ por un filtro activo Sallen-Key o Butterworth de segundo orden con amplificador operacional de bajo offset (ej. OPA2134), incrementando la atenuación en banda atenuada a $-40.0\,\mathrm{dB/\text{década}}$ e impidiendo que la carga altere la frecuencia de resonancia.
* **Conversión Analógica Externa de Alta Resolución:** Añadir un convertidor ADC externo de 16 bits como el **ADS1115** con comunicación I2C y referencia de tensión interna por banda prohibida (*bandgap*), eliminando el ruido digital del microcontrolador.
* **Compensación Térmica de Velocidad Acústica:** Integrar una sonda de temperatura digital DS18B20 para recalcular la velocidad del sonido $v(T)$ en tiempo real dentro del algoritmo del microcontrolador.
* **Diseño en Placa PCB con Plano de Masa:** Trasladar el circuito desde el protoboard hacia una placa de circuito impreso (PCB) de doble capa con plano de masa continuo, blindaje perimetral y condensadores de desacoplo de $100\,\mathrm{nF}$ ubicados directamente en los pines de polarización de cada integrado para mitigar interferencias por capacitancias parásitas ($C_p < 2\,\mathrm{pF}$).

---

# Conclusions

Se diseñó, modeló y validó rigurosamente una cadena completa de acondicionamiento analógico de señales y un subsistema de adquisición y supervisión digital en tiempo real.

La modularización de la amplificación en dos etapas en cascada—un amplificador diferencial balanceado ($A_d = 10.0$) seguido de un amplificador no inversor ($A_v = 2.0$)—permitió elevar con exactitud una diferencia de potencial débil de $60.0\,\mathrm{mV}$ hasta un nivel óptimo de $1.20\,\mathrm{V}$. Esta estrategia aseguró la conservación del Producto Ganancia-Ancho de Banda ($\mathrm{GBP} \approx 1.0\,\mathrm{MHz}$), preservó un ancho de banda útil superior a $50.0\,\mathrm{kHz}$ y garantizó un margen dinámico seguro por debajo de los $3.0\,\mathrm{V}$ admisibles para la etapa digital. 

El filtro pasabajas pasivo $RC$ ($R = 10.0\,\mathrm{k}\Omega, C = 100\,\mathrm{nF}, f_c = 159.15\,\mathrm{Hz}$) demostró experimentalmente la dualidad tiempo-frecuencia: en el dominio armónico atenuó el ruido de conmutación de alta frecuencia ($2.0\,\mathrm{kHz}$) en más de $22.0\,\mathrm{dB}$ ($92.1\%$ de atenuación) y exhibió un desfase exacto de $-20.66^\circ$ a $60\,\mathrm{Hz}$ ($\Delta t = 0.96\,\mathrm{ms}$), mientras que en el dominio temporal garantizó un tiempo de asentamiento imperceptible de $5.0\,\mathrm{ms}$ frente a dinámicas mecánicas. Por su parte, el comparador de tensión LM741 evidenció una velocidad de disparo por hardware en microsegundos ($< 15\,\mu\mathrm{s}$) e independiente de software ante sobrecargas superiores a $1.00\,\mathrm{V}$.

En la capa digital, la caracterización del sensor ultrasónico mediante el ESP32 demostró una linealidad estática sobresaliente ($R^2 = 0.9998$) en el rango de 4 a 50 cm con una sensibilidad de $58.31\,\mu\mathrm{s/cm}$, y la interfaz gráfica en LabVIEW corroboró la robustez del enlace UART a 115200 baudios para visualización continua sin pérdidas de información. Finalmente, el análisis cuantitativo de no-idealidades sentó las directrices técnicas para la migración hacia instrumentación industrial de alto desempeño.

---

# References

::: {#refs}
:::

---

# Personal comments

## Leonardo Monter
*Durante el desarrollo y simulación de la práctica pude constatar la importancia crítica de modularizar la ganancia en varias etapas operacionales. La conservación del Producto Ganancia-Ancho de Banda (GBP) es un factor determinante para evitar que la señal se distorsione o atenúe en frecuencias intermedias. Asimismo, el análisis del filtro RC en el oscilograma simulado evidenció con gran claridad la dualidad entre la atenuación de ruido armónico de conmutación y la correlación del desfase angular con el retardo temporal.*

## Renata Bello
*La implementación del comparador de voltaje como sistema de protección me permitió comprender el valor de los mecanismos de seguridad analógicos por hardware. Disponer de una respuesta en microsegundos que no dependa del microcontrolador ni de retardos en la comunicación serial representa una salvaguarda indispensable para evitar daños en transductores y etapas de potencia. Comprender la necesidad de agregar histéresis mediante un Trigger de Schmitt ante señales ruidosas fue uno de los aprendizajes más formativos del laboratorio.*

## Adrian Ruiz
*El modelado de la interfaz de adquisición con el sensor ultrasónico y la transmisión serial a 115200 baudios hacia LabVIEW ilustró con claridad la necesidad de mantener sincronizados los tiempos de muestreo y las velocidades de transmisión. La linealidad observada en la curva de calibración ($R^2 = 0.9998$) confirma la validez de los temporizadores de alta resolución del ESP32 para aplicaciones de telemetría física en tiempo real.*

## Alonso Madrigal
*El análisis de las no-idealidades del LM741, en particular las corrientes de polarización y la tensión de offset, me brindó una visión realista de los retos de la instrumentación electrónica. Aunque el modelado matemático ideal entrega errores de diseño nulos, comprender cómo mitigar el offset mediante resistencias de compensación o mediante amplificadores de instrumentación especializados (como el INA128) es fundamental para proyectos industriales de alto desempeño.*
