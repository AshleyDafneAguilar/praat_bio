# Análisis de Bioseñales con Praat y Parselmouth

Este proyecto permite extraer diversas características acústicas de grabaciones de voz estructuradas a través de la librería `parselmouth` de Python, la cual provee la implementación directa de los algoritmos de Praat. Con esto extraemos parámetros de procesamiento bioseñal tales como el Pitch (F0), la Intensidad, Formantes (F1, F2), MFCC y LPC.

## Modo de Uso

El flujo general se diseñó aislando el análisis del código fuerte, derivando su ejecución bajo archivos de configuración con extensión `.ini`. Para ejecutar el procesamiento en tu terminal:

```bash
uv run main.py <archivo_de_configuracion.ini>
```

Por ejemplo, puedes ejecutar tu script con la configuración principal y la configuración de defecto para observar las variaciones en los resultados de la siguiente manera:
```bash
uv run main.py configuraciones.ini
uv run main.py configuraciones_default.ini
```

## Análisis de Resultados y Conclusiones

Se realizaron dos ejecuciones sistemáticas produciendo dos conjuntos de datos: `resultados_analisis_default` y `resultados_analisis_ajustado`. Estos representan el análisis crudo en Praat por defecto versus un ajuste paramétrico en los mínimos de búsqueda o rangos espectrales. Al revisar los datos CSV producidos, arrojamos los siguientes hallazgos puntuales:

1. **Alteración Sensible de los Formantes (F1 y F2)**:
   Al ajustar la cota máxima del tracto vocal (`maximum_formant`) de `5500.0` Hz a `4000.0` Hz (considerando el Teorema de Nyquist para grabaciones muestreadas a 8000 Hz), ocurrió una diferencia muy notable en la estimación de formantes. El algoritmo de *Burg* redirigió sus estimaciones, cambiando completamente la localización espectral (p. ej. en variaciones de *terremoto*, F1 pasó de valores cercanos a 300Hz a más de 900Hz). Esto demuestra que las estimaciones de formantes errarán significativamente de no conocer o adaptar de antemano el ratio de sampleo y tracto vocal de la grabaciones de audio provistas.

2. **Precisión depurada de Pitch (F0)**:
   Aumentar el límite de piso (`pitch_floor` de 75 a 100) previno que el estimador F0 incluyera frecuencias indeseadas que usualmente corresponden a ruido ambiental grave o falsos sub-armónicos de la voz en lugar del tono fundamental. Esta restricción provocó de una leve a moderada desviación en los datos finales de la frecuencia fundamental general, produciendo en teoría métricas de Pitch más realistas al usuario.

3. **Independencia del Entorno Modular (MFCC e Intensidad)**:
   Comparando ambas salidas columna a columna, las estadísticas observadas para *Intensidad_dB* y en gran forma para el primer coeficiente *MFCC* se conservaron completamente estáticas y replicables a pesar de todas las alteraciones inyectadas en las capas de análisis sobre los Formantes o frecuencias limitantes (Pitch Floors/Ceilings). Esto prueba la modularidad que provee Parselmouth sobre variables de intensidad (amplitud) e MFCC.
