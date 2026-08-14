"""
Lima Automa - Generador de Cupones QR
======================================
Script principal para generar cupones unicos.
"""
import sys
import json
sys.path.append("src")

from coupon_generator import crear_cupon, generar_qr_texto, crear_landing_page_html, generar_reporte_cupones


def main():
    print("=" * 60)
    print("  LIMA AUTOMA - Generador de Cupones QR")
    print("=" * 60)

    # Cargar restaurantes
    with open("data/restaurantes_lima_completo.json", encoding="utf-8") as f:
        restaurantes = json.load(f)

    print(f"\n  Restaurantes encontrados: {len(restaurantes)}")

    # Generar cupones
    cupones = []

    for restaurante in restaurantes:
        cupon = crear_cupon(restaurante, descuento_pct=15)
        cupones.append(cupon)

        print(f"\n  Restaurante: {cupon['restaurante']}")
        print(f"  Codigo rastreo: {cupon['codigo_rastreo']}")
        print(f"  Codigo descuento: {cupon['codigo_descuento']}")
        print(f"  Landing URL: {cupon['landing_url']}")

        # Generar landing page HTML
        html = crear_landing_page_html(cupon)
        filename = f"data/landing_{cupon['codigo_rastreo']}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Landing page: {filename}")

    # Guardar cupones
    with open("data/cupones.json", "w", encoding="utf-8") as f:
        json.dump(cupones, f, ensure_ascii=False, indent=2)

    # Reporte
    print("\n" + "=" * 60)
    print("  REPORTE")
    print("=" * 60)
    reporte = generar_reporte_cupones(cupones)
    print(f"  Total cupones: {reporte['total_cupones']}")
    print(f"  Cupones activos: {reporte['cupones_activos']}")
    print(f"  Total usos: {reporte['total_usos']}")
    print(f"  Clientes atribuidos: {reporte['clientes_atribuidos']}")

    print("\n  Archivos generados:")
    print("  - data/cupones.json")
    print("  - data/landing_*.html")


if __name__ == "__main__":
    main()
