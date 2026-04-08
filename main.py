import argparse
import configparser
import os
import sys
from procesamiento import procesar_biosenales

def main():
    parser = argparse.ArgumentParser(description="Ejecutar análisis de bioseñales leyendo configuración desde un archivo .ini")
    parser.add_argument("config_file", type=str, help="Ruta al archivo configuraciones.ini")
    args = parser.parse_args()

    config_path = args.config_file

    if not os.path.exists(config_path):
        print(f"Error: El archivo de configuración '{config_path}' no existe.")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(config_path)

    try:
        # Rutas
        input_folder = config.get("Rutas", "carpeta_grabaciones")
        output_csv = config.get("Rutas", "archivo_csv")
        
        # Parámetros numéricos
        pitch_floor = config.getfloat("Parametros", "pitch_floor")
        pitch_ceiling = config.getfloat("Parametros", "pitch_ceiling")
        max_formante = config.getfloat("Parametros", "max_formante")
        lpc_value = config.getint("Parametros", "lpc_valor")
        mfcc_param = config.getint("Parametros", "mfcc_valor")
    except configparser.Error as e:
        print(f"Error al procesar el archivo de configuración: {e}")
        sys.exit(1)

    # Llamar a la función principal
    procesar_biosenales(
        base_path=input_folder,
        output_csv=output_csv,
        pitch_floor=pitch_floor,
        pitch_ceiling=pitch_ceiling,
        max_formante=max_formante,
        lpc_order=lpc_value,
        mfcc_coeffs=mfcc_param
    )

if __name__ == "__main__":
    main()
