import os
import parselmouth
import numpy as np
import matplotlib.pyplot as plt

def generar_analisis_visual(audio_path, output_dir, base_name):
    # Cargar el sonido
    snd = parselmouth.Sound(audio_path)
    
    # 1. Crear el espectrograma
    # maximum_frequency=4000 para respetar el límite de Nyquist (8kHz/2)
    spectrogram = snd.to_spectrogram(window_length=0.05, maximum_frequency=4000)
    
    # 2. Crear el espectro (Power Spectral Density)
    spectrum = snd.to_spectrum()

    # Asegurar que el directorio de salida exista
    os.makedirs(output_dir, exist_ok=True)

    # --- Guardar Espectrograma ---
    plt.figure(figsize=(10, 4))
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    # Sumamos 1e-10 para evitar el error log10(0)
    sg_db = 10 * np.log10(spectrogram.values + 1e-10)
    
    # Normalizamos el contraste para que se vea limpio (rango de 70dB)
    plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - 70, cmap='afmhot')
    plt.title(f"Espectrograma: {base_name}")
    plt.ylabel("Frecuencia [Hz]")
    plt.xlabel("Tiempo [s]")
    plt.ylim(0, 4000) 
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{base_name}_espectrograma.png"))
    plt.close()

    # --- Guardar Espectro ---
    plt.figure(figsize=(10, 4))
    
    # Obtenemos los datos y el grid de frecuencias
    amplitudes = 10 * np.log10(spectrum.values[0, :] + 1e-10)
    frecuencias = spectrum.x_grid()
    
    # Sincronizamos las dimensiones cortando el excedente del eje X
    plt.plot(frecuencias[:len(amplitudes)], amplitudes, color='teal')
    
    plt.title(f"Espectro de Potencia (FFT): {base_name}")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Amplitud [dB]")
    plt.xlim(0, 4000)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{base_name}_espectro.png"))
    plt.close()