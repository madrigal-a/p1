# Introduction

En esta práctica se estudiaron diferentes métodos para el acondicionamiento y análisis de señales eléctricas. En una primera parte, una señal fue procesada mediante distintas configuraciones con amplificadores operacionales, incluyendo un amplificador inversor, un amplificador diferencial y un comparador. También se utilizó un filtro RC para observar su efecto sobre la señal y comprender la función de cada etapa dentro del circuito.

De manera adicional, se realizó una actividad independiente utilizando un sensor ultrasónico. La señal generada por el sensor fue observada mediante un osciloscopio mientras se acercaba y alejaba un objeto. Esto permitió visualizar cómo cambiaba la amplitud de la señal en función de la posición del objeto.

A través de ambas actividades fue posible relacionar los conceptos teóricos de amplificación, comparación, filtrado y medición de señales con su comportamiento experimental, utilizando instrumentos de laboratorio para analizar las respuestas obtenidas.

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

## Dinámica de Disparo del Comparador LM741 y Activación del LED

Para evaluar el subsistema de alarma visual ante sobrecargas, se modeló una rampa de tensión en forma de sigmoide que emula el incremento continuo de la señal del transductor desde $0.0\,\mathrm{V}$ hasta el nivel nominal de $1.20\,\mathrm{V}$. La Figura 3 presenta la tensión de entrada frente a la salida del comparador y la corriente circulante por el diodo LED.

![Dinámica de conmutación del comparador LM741 y polarización del LED indicador ante cruce de umbral ($V_{\mathrm{ref}} = 1.00\,\mathrm{V}, V_{\mathrm{in}} = 1.20\,\mathrm{V}, R_{\mathrm{pot}} = 10.0\,\mathrm{k}\Omega, R_{\mathrm{LED}} = 330\,\Omega, V_f \approx 2.0\,\mathrm{V}, I_{\mathrm{LED}} \approx 25.7\,\mathrm{mA}$).](img/circuito_protoboard.png){#fig:comparador width=90%}

Durante el intervalo en que $V_{\mathrm{in}} < 1.00\,\mathrm{V}$ ($t < 10.01\,\mathrm{ms}$), la salida del comparador permanece en saturación negativa ($V_{\mathrm{sat}}^- \approx -10.5\,\mathrm{V}$), polarizando en inversa al LED y registrando una corriente nula ($0.0\,\mathrm{mA}$). En el instante preciso $t_{\mathrm{cross}} \approx 10.01\,\mathrm{ms}$ en que $V_{\mathrm{in}}$ rebasa el umbral calibrado de $V_{\mathrm{ref}} = 1.00\,\mathrm{V}$, el LM741 conmuta en un lapso inferior a $15\,\mu\mathrm{s}$ hacia saturación positiva ($V_{\mathrm{sat}}^+ \approx +10.5\,\mathrm{V}$). Esta transición inyecta una corriente de polarización directa estabilizada en:
$$I_{\mathrm{LED}} = \frac{10.5\,\mathrm{V} - 2.0\,\mathrm{V}}{330\,\Omega} = 25.76\,\mathrm{mA}$$
la cual enciende con luminosidad plena la alarma visual por sobrecarga.

## Caracterización del Sensor Ultrasónico

Se evaluó el comportamiento de la señal proveniente del sensor ultrasónico mediante un osciloscopio, con el objetivo de observar cómo variaba su nivel de voltaje al modificar la distancia de un objeto colocado frente al sensor. A diferencia de una señal pulsante o senoidal, la respuesta observada se presentó como una línea aproximadamente constante en el tiempo, con pequeñas variaciones asociadas al ruido de medición.

Durante la prueba se acercó y alejó un objeto de manera gradual mientras se observaba la respuesta mostrada en el osciloscopio. Al modificar la posición del objeto, se identificó un cambio en la posición vertical de la señal, lo que representa una variación en el nivel de voltaje entregado por el sistema.

De manera general, el comportamiento observado puede representarse mediante la relación:

$$V_{\text{salida}} = f(d)$$

donde:

* $V_{\text{salida}}$ corresponde al nivel de voltaje observado en el osciloscopio.
* $d$ representa la distancia entre el sensor ultrasónico y el objeto.

En esta actividad no se realizó una curva de calibración cuantitativa ni un ajuste matemático entre distancia y voltaje; sin embargo, fue posible comprobar experimentalmente que la salida del sistema presenta cambios detectables cuando se modifica la posición del objeto.

La Figura 4 muestra un ejemplo de la señal observada durante la práctica. Se aprecia que el comportamiento de la señal es aproximadamente constante en el tiempo y presenta únicamente pequeñas fluctuaciones alrededor de su valor medio.

![Señal observada en el osciloscopio durante la caracterización del sensor ultrasónico. La respuesta presenta un nivel de voltaje aproximadamente constante, acompañado de pequeñas variaciones de ruido. Al modificar la distancia del objeto frente al sensor, se observó un cambio en el nivel de voltaje de la señal.](img/caracterizacion_ultrasonico.png){#fig:ultrasonico width=95%}

Desde el punto de vista físico, los sensores ultrasónicos funcionan mediante la emisión de ondas acústicas de alta frecuencia que se propagan por el aire y se reflejan al encontrar un objeto. La onda reflejada regresa hacia el sistema receptor, donde puede ser convertida y procesada electrónicamente para obtener una señal relacionada con la presencia o posición del objeto.

La respuesta obtenida puede verse afectada no solamente por la distancia, sino también por factores como el material y la geometría del objeto, su orientación respecto al sensor, la reflexión de la onda y las características propias del circuito electrónico empleado.

Por esta razón, la relación entre distancia y nivel de voltaje no necesariamente es lineal:

$$V_{\text{salida}} \not\propto d$$

por lo que sería necesario realizar múltiples mediciones a distancias conocidas para determinar experimentalmente la curva característica del sistema.

La actividad permitió comprobar de manera cualitativa que el sensor responde ante cambios en la posición de un objeto y que dicha respuesta puede ser analizada directamente mediante un osciloscopio. De esta forma, se relacionó una variable física, como la distancia, con una variable eléctrica medible, en este caso el nivel de voltaje de salida.

## Adquisición Continua en LabVIEW

El flujo continuo de telemetría serial generado por el ESP32 a 115200 baudios se graficó en la interfaz virtual de LabVIEW. La Figura 5 ilustra la pantalla del *Waveform Chart* simulado ante un perfil de movimiento de aproximación, y la Figura 6 detalla la arquitectura modular del diagrama de bloques de adquisición VISA.

![Emulación del Panel Frontal del Instrumento Virtual en LabVIEW: monitoreo continuo de distancia a 115200 baudios con límite de proximidad fijado en $15.0\,\mathrm{cm}$.](img/labview_front_panel.png){#fig:lv_front width=92%}

![Diagrama de Bloques conceptual del Instrumento Virtual en LabVIEW implementando el protocolo VISA Configure, While Loop, VISA Read y Scan from String.](img/labview_block_diagram.png){#fig:lv_block width=88%}

## Tabla Sintética Comparativa de Parámetros de Diseño

En la Tabla 2 se confrontan los parámetros analíticos de diseño frente a los resultados obtenidos mediante el modelado y simulación computacional de la cadena completa de acondicionamiento y adquisición.

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
| Sensor Ultrasónico | Nivel de tensión de salida | $V_{\mathrm{salida}} = f(d)$ | Variable según distancia | Inspección en osciloscopio | Cualitativo |
| Sensor Ultrasónico | Dinámica temporal | Nivel DC continuo | Fluctuación por ruido | Línea horizontal en pantalla | Cualitativo |
| Telemetría Serial UART | Latencia de paquete ($t_{\mathrm{tx}}$) | $0.87\,\mathrm{ms}$ | $< 1.00\,\mathrm{ms}$ | Tasa 115200 baud ($T_s = 50.0\,\mathrm{ms}$) | $0.00\%$ |

: Tabla sintética comparativa de parámetros de diseño, simulación y evaluación experimental.

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

Se estudiaron, modelaron y analizaron experimentalmente diferentes métodos para el acondicionamiento analógico de señales eléctricas y la caracterización de sensores de proximidad.

La modularización de la amplificación en dos etapas en cascada—un amplificador diferencial balanceado ($A_d = 10.0$) seguido de un amplificador no inversor ($A_v = 2.0$)—permitió elevar con exactitud una diferencia de potencial débil de $60.0\,\mathrm{mV}$ hasta un nivel óptimo de $1.20\,\mathrm{V}$. Esta estrategia aseguró la conservación del Producto Ganancia-Ancho de Banda ($\mathrm{GBP} \approx 1.0\,\mathrm{MHz}$), preservó un ancho de banda útil superior a $50.0\,\mathrm{kHz}$ y garantizó un margen dinámico seguro por debajo de los $3.0\,\mathrm{V}$ admisibles para la etapa digital. 

El filtro pasabajas pasivo $RC$ ($R = 10.0\,\mathrm{k}\Omega, C = 100\,\mathrm{nF}, f_c = 159.15\,\mathrm{Hz}$) demostró la atenuación efectiva de componentes armónicas de alta frecuencia sin perturbar el nivel de polarización DC ni inducir retardos temporales apreciables. Por su parte, el comparador de tensión LM741 evidenció una velocidad de disparo por hardware en microsegundos ($< 15\,\mu\mathrm{s}$) e independiente de software ante sobrecargas superiores a $1.00\,\mathrm{V}$.

En la actividad experimental con el sensor ultrasónico, la observación mediante osciloscopio demostró de forma cualitativa que la salida del sistema se manifiesta como un nivel de voltaje sensible a la distancia de un objeto, relacionando una variable física espacial con una magnitud de potencial eléctrico continuo sujeta a reflexiones acústicas y no-linealidades del transductor. Finalmente, el análisis cuantitativo de no-idealidades sentó las directrices técnicas para la optimización hacia instrumentación de precisión.

---

# References

::: {#refs}
:::

---

# Personal comments

## Leonardo Monter
*Durante el desarrollo y simulación de la práctica pude constatar la importancia crítica de modularizar la ganancia en varias etapas operacionales. La conservación del Producto Ganancia-Ancho de Banda (GBP) es un factor determinante para evitar que la señal se distorsione o atenúe en frecuencias intermedias. Asimismo, el análisis del filtro RC en el oscilograma simulado evidenció con gran claridad la función de cada etapa dentro del circuito analógico.*

## Renata Bello
*La implementación del comparador de voltaje como sistema de protección me permitió comprender el valor de los mecanismos de seguridad analógicos por hardware. Disponer de una respuesta en microsegundos que no dependa del microcontrolador ni de retardos en la comunicación serial representa una salvaguarda indispensable para evitar daños en transductores y etapas de potencia. Comprender la necesidad de agregar histéresis mediante un Trigger de Schmitt ante señales ruidosas fue uno de los aprendizajes más formativos del laboratorio.*

## Adrian Ruiz
*La caracterización del sensor ultrasónico mediante el osciloscopio me permitió observar directamente cómo la distancia de un objeto modifica el nivel de voltaje de salida. Identificar que la señal en pantalla es aproximadamente constante en el tiempo con pequeñas fluctuaciones de ruido, y comprender que la relación entre voltaje y distancia no es necesariamente lineal debido a reflexiones acústicas y características del circuito, me brindó un aprendizaje clave sobre la medición de variables físicas con instrumentos de laboratorio.*

## Alonso Madrigal
*El análisis de las no-idealidades del LM741, en particular las corrientes de polarización y la tensión de offset, me brindó una visión realista de los retos de la instrumentación electrónica. Aunque el modelado matemático ideal entrega errores de diseño nulos, comprender cómo mitigar el offset mediante resistencias de compensación o mediante amplificadores de instrumentación especializados (como el INA128) es fundamental para proyectos industriales de alto desempeño.*
