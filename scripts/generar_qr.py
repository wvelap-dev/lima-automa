"""
Lima Automa - Generador de QR Codes para Imprimir
==================================================
Genera imagenes QR que el restaurante puede imprimir en mesas.
"""
import json
import os
import urllib.request
from pathlib import Path


def generar_qr_imagen(url, codigo, output_dir="data/qr"):
    """
    Genera una imagen QR usando una API publica.
    """
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Generar nombre del archivo
    filename = os.path.join(output_dir, f"QR_{codigo}.png")

    # URL de la API de QR
    qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={url}&format=png"

    try:
        # Descargar imagen
        urllib.request.urlretrieve(qr_api_url, filename)
        return filename
    except Exception as e:
        print(f"  Error generando QR para {codigo}: {e}")
        return None


def generar_todos_los_qr():
    """
    Genera QR codes para todos los cupones.
    """
    print("=" * 60)
    print("  LIMA AUTOMA - Generador de QR Codes")
    print("=" * 60)

    # Cargar cupones
    with open("data/cupones.json", encoding="utf-8") as f:
        cupones = json.load(f)

    print(f"\n  Cupones encontrados: {len(cupones)}")

    # Generar QR para cada cupon
    qr_generados = []

    for cupon in cupones:
        print(f"\n  Restaurante: {cupon['restaurante']}")
        print(f"  Codigo: {cupon['codigo_rastreo']}")
        print(f"  URL: {cupon['landing_url']}")

        qr_file = generar_qr_imagen(cupon["landing_url"], cupon["codigo_rastreo"])

        if qr_file:
            qr_generados.append({
                "restaurante": cupon["restaurante"],
                "codigo": cupon["codigo_rastreo"],
                "archivo_qr": qr_file,
                "url": cupon["landing_url"],
            })
            print(f"  QR generado: {qr_file}")

    # Guardar lista de QR generados
    with open("data/qr_generados.json", "w", encoding="utf-8") as f:
        json.dump(qr_generados, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("  RESUMEN")
    print("=" * 60)
    print(f"  QR generados: {len(qr_generados)}")
    print(f"  Carpeta: data/qr/")
    print(f"  Lista: data/qr_generados.json")

    print("\n  SIGUIENTE PASO:")
    print("  1. Abrir carpeta data/qr/")
    print("  2. Imprimir cada QR en papel")
    print("  3. Pegar en mesas del restaurante")

    return qr_generados


if __name__ == "__main__":
    generar_todos_los_qr()
