import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# Cargar los datos generados previamente
df_default = pd.read_csv('resultados_analisis_default.csv')
df_ajustado = pd.read_csv('resultados_analisis_ajustado.csv')

# Identificar las fuentes
df_default['Configuracion'] = 'Default'
df_ajustado['Configuracion'] = 'Ajustado'

# Combinar para graficar
df_total = pd.concat([df_default, df_ajustado])

# Comparación de promedios
metrics = ['F0_Promedio', 'F1_Hz', 'F2_Hz']
df_melted = df_total.melt(id_vars=['Configuracion'], value_vars=metrics, var_name='Metrica', value_name='Valor')

plt.figure(figsize=(10, 6))
sns.barplot(data=df_melted, x='Metrica', y='Valor', hue='Configuracion', palette='muted')
plt.title('Comparación de Métricas Promedio: Default vs Ajustado')
plt.ylabel('Frecuencia (Hz)')
plt.savefig('comparacion_promedios.png')

# Espacio de formantes (F1 vs F2)
plt.figure(figsize=(10, 8))
sns.scatterplot(data=df_total, x='F2_Hz', y='F1_Hz', hue='Configuracion', style='Configuracion', s=100, alpha=0.7)
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.title('Mapa del Espacio Vocálico (F1 vs F2)')
plt.xlabel('F2 (Hz) - Resonancia de la Lengua (Anterior/Posterior)')
plt.ylabel('F1 (Hz) - Resonancia de la Mandíbula (Abierta/Cerrada)')
plt.savefig('espacio_formantes.png')

# Pitch por palabra
df_palabras = df_total.groupby(['Palabra', 'Configuracion'])['F0_Promedio'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_palabras, x='Palabra', y='F0_Promedio', hue='Configuracion', marker='o')
plt.xticks(rotation=45)
plt.title('Estabilidad del Pitch (F0) a través del vocabulario')
plt.ylabel('F0 Promedio (Hz)')
plt.tight_layout()
plt.savefig('pitch_por_palabra.png')