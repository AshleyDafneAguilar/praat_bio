import parselmouth
import pandas as pd
import os
import numpy as np

def procesar_biosenales(base_path, output_csv, pitch_floor, pitch_ceiling, max_formante, lpc_order, mfcc_coeffs):
    palabras = ["terremoto", "erupcion", "albergue", "codigo", "simulacro", 
                "rescate", "evacuacion", "sismico", "replica", "plan"]

    resultados = []

    print("Iniciando el análisis de bioseñales...")

    for palabra in palabras:
        folder_path = os.path.join(base_path, palabra)
        
        for i in range(1, 6):
            file_name = f"{palabra}_{i}.wav"
            file_path = os.path.join(folder_path, file_name)
            
            if os.path.exists(file_path):
                # Cargar el audio
                try:
                    snd = parselmouth.Sound(file_path)
                    
                    # Pitch (F0)
                    pitch = snd.to_pitch(pitch_floor=pitch_floor, pitch_ceiling=pitch_ceiling)
                    f0_mean = parselmouth.praat.call(pitch, "Get mean", 0, 0, "Hertz")
                    
                    # Intensidad
                    intensity = snd.to_intensity()
                    int_mean = parselmouth.praat.call(intensity, "Get mean", 0, 0)
                    
                    # Formantes 
                    punto_medio = snd.get_total_duration() / 2
                    formants = snd.to_formant_burg(
                        max_number_of_formants=5.0, 
                        maximum_formant=max_formante, 
                        window_length=0.025, 
                        pre_emphasis_from=50.0
                    )

                    f1 = formants.get_value_at_time(1, punto_medio)
                    f2 = formants.get_value_at_time(2, punto_medio)
                    
                    # MFCC
                    mfcc_obj = snd.to_mfcc(number_of_coefficients=mfcc_coeffs)
                    mfcc_arr = mfcc_obj.to_array()
                    mfcc_1_mean = np.mean(mfcc_arr[1, :]) # Coeficiente 1
                    
                    # LPC
                    lpc_obj = parselmouth.praat.call(snd, "To LPC (burg)...", lpc_order, 0.025, 0.005, 50.0)
                    
                    # Guardar datos en la lista
                    resultados.append({
                        "Palabra": palabra, 
                        "Repeticion": i, 
                        "F0_Promedio": f0_mean,
                        "Intensidad_dB": int_mean, 
                        "F1_Hz": f1, 
                        "F2_Hz": f2,
                        "MFCC1_Mean": mfcc_1_mean
                    })
                except Exception as e:
                    print(f"Error procesando el archivo '{file_path}': {e}")

    if not resultados:
        print("No se encontraron grabaciones procesables en la carpeta dada.")
        return

    # Convertir a DataFrame y guardar
    df = pd.DataFrame(resultados)
    df.to_csv(output_csv, index=False)
    print(f"\nDatos guardados en '{output_csv}'")