# Análisis Acústico y Caracterización de Bioseñales de Voz: Estudio de Caso en una Hablante en Adultez Temprana


Este estudio presenta la caracterización acústica de una voz femenina de 22 años a través de la extracción sistemática de descriptores bioseñales utilizando una integración de Praat y la librería `parselmouth` en Python. Se procesaron 50 muestras segmentadas de un vocabulario de emergencia capturadas a una tasa de muestreo de 8000 Hz, con el objetivo de contrastar la precisión de la extracción de parámetros bajo configuraciones estándar frente a ajustes técnicos fundamentados.

La metodología incluyó la comparación de la frecuencia fundamental ($F_0$), formantes ($F_1, F_2$), coeficientes MFCC y LPC, aplicando el límite de Nyquist (4000 Hz) para optimizar la detección de resonancias. Los resultados demuestran que, mientras el seguimiento de $F_0$ se mantiene robusto y alineado con los rangos reportados por la literatura para mujeres jóvenes (Zraick et al., 2021), la precisión de los formantes superiores depende críticamente del ajuste de los rangos de búsqueda y el orden de predicción lineal. Este trabajo valida un flujo de trabajo automatizado que garantiza la fidelidad técnica y la coherencia anatómica en el análisis de señales de voz con ancho de banda limitado.



## Modo de Uso

Este proyecto utiliza **uv**, un administrador de paquetes de Python que gestiona automáticamente el entorno virtual y las dependencias.

### Instalación de uv
Si no tienes instalado `uv` en tu sistema, puedes obtenerlo con un solo comando:

*   **macOS / Linux:**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
*   **Windows (PowerShell):**
    ```powershell
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
### Flujo de Ejecución

El flujo general se diseñó aislando el análisis del código fuente, derivando su ejecución bajo archivos de configuración con extensión `.ini`. Para ejecutar el procesamiento en tu terminal:

```bash
uv run main.py <archivo_de_configuracion.ini>
```

Por ejemplo, puedes ejecutar tu script con la configuración principal y la configuración de defecto para observar las variaciones en los resultados de la siguiente manera:
```bash
uv run main.py configuraciones.ini
uv run main.py configuraciones_default.ini
```

### Personalización de Parámetros

El sistema está diseñado para que todos los parámetros de análisis (como los umbrales de Pitch, máximos de Formantes, orden LPC y coeficientes MFCC) puedan ser alterables editando directamente en `configuraciones.ini` o `configuraciones_default.ini`. 

Alternativamente, puedes crear archivos `.ini` nuevos usando estos archivos existentes base como "esqueleto". Solo necesitas copiar la estructura y adaptar los datos a tu conveniencia sin modificar las pruebas originales, bastará con indicarle a `main.py` tu nuevo archivo al ejecutarlo.




## Análisis de Resultados y Conclusiones

Se realizaron dos ejecuciones sistemáticas produciendo dos conjuntos de datos almacenados en el directorio `resultados/`: `resultados_analisis_default.csv` y `resultados_analisis_ajustado.csv`. Estos representan el análisis crudo en Praat por defecto versus un ajuste paramétrico en los mínimos de búsqueda y rangos espectrales. Al revisar los datos CSV tabulados y sus respectivas gráficas emitidas, identificamos los siguientes hallazgos:

Al ajustar la cota máxima del tracto vocal (`maximum_formant`) de `5500.0` Hz a `4000.0` Hz (considerando el Teorema de Nyquist para grabaciones muestreadas a 8000 Hz), ocurrió una diferencia muy notable en la estimación de formantes. El algoritmo de *Burg* redirigió sus estimaciones, cambiando la localización espectral de las resonancias. Esto demuestra que las estimaciones de formantes se dispersan erróneamente al no adaptar de antemano las proporciones anatómicas y limitaciones de frecuencia de corte de la grabación original.

![Mapa del Espacio Vocálico (F1 vs F2)](resultados/img/espacio_formantes.png)  
*Mapa relacional F1 vs F2 mostrando la radical reubicación gráfica de los formantes entre la configuración por defecto y la ajustada.*

Al aumentar el límite de piso (`pitch_floor` de 75 a 100 Hz) previno que el estimador F0 incluyera frecuencias indeseadas que usualmente corresponden a ruido ambiental grave o falsos sub-armónicos de la voz en lugar del auténtico tono fundamental de la locutora.

![Estabilidad del Pitch (F0)](resultados/img/pitch_por_palabra.png)  
*Comparativa lineal por vocabulario que evidencia una variación sutil en la estimación de la frecuencia del Pitch al depurar el rango de análisis mínimo.*

Finalmente, al contrastar ambas salidas, las métricas observadas para variables volumétricas y compuestas (como *Intensidad* y *MFCC*) resultaron completamente idénticas numéricamente pese a las alteraciones inyectadas en las capas de análisis espectral de su alrededor (Pitch/Margen de Formantes). Esto verifica la fuerte independencia técnica y granular de las transformaciones individuales cuando utilizamos Parselmouth.

El resumen absoluto de los promedios es el siguiente:

![Comparación de Métricas Promedio](resultados/img/comparacion_promedios.png)  
*Gráfica de promedios consolidada comparando lado a lado las 3 frecuencias principales tratadas. Se ilustra drásticamente la divergencia paramétrica en formantes altos (F1/F2).*
