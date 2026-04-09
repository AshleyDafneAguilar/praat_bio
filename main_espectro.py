import os
from espectro import generar_analisis_visual

def main():
    base_dir = "/home/ashley/projects/praat_bio"
    input_dir = os.path.join(base_dir, "grabaciones_segmentadas")
    output_base_dir = os.path.join(base_dir, "resultados", "img")

    # Recorrer cada subcarpeta (palabra)
    if os.path.exists(input_dir):
        for palabra in os.listdir(input_dir):
            palabra_path = os.path.join(input_dir, palabra)
            
            if os.path.isdir(palabra_path):
                # Crear carpeta de salida para la palabra
                output_dir = os.path.join(output_base_dir, palabra)
                os.makedirs(output_dir, exist_ok=True)
                
                # Procesar cada archivo de audio del 1 al 5
                for file_name in os.listdir(palabra_path):
                    if file_name.endswith(".wav"):
                        audio_path = os.path.join(palabra_path, file_name)
                        # el base_name será el nombre sin la extensión, ej: "albergue_1"
                        base_name = os.path.splitext(file_name)[0]
                        
                        print(f"Procesando: {audio_path}")
                        generar_analisis_visual(audio_path, output_dir, base_name)

if __name__ == "__main__":
    main()
