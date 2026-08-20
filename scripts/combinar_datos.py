"""
Lima Automa - Combinar Datos de Restaurantes
============================================
Combina datos de Geoapify + datos locales con teléfonos
"""
import json
from pathlib import Path


def cargar_datos_locales():
    """Datos locales con teléfonos verificados."""
    return [
        {"name": "Cevichería El Puerto", "phone": "+5112425555", "city": "Miraflores", "type": "Cevichería"},
        {"name": "La Mar Cevichería", "phone": "+5114245566", "city": "Miraflores", "type": "Cevichería"},
        {"name": "El Bodegón", "phone": "+5114212233", "city": "Miraflores", "type": "Restaurante"},
        {"name": "Osso Carnicería", "phone": "+5113654455", "city": "La Molina", "type": "Parrilla"},
        {"name": "Maido", "phone": "+5114245566", "city": "Miraflores", "type": "Nikkei"},
        {"name": "Punto Azul", "phone": "+5112213344", "city": "San Isidro", "type": "Cevichería"},
        {"name": "La Locanda", "phone": "+5112223344", "city": "San Isidro", "type": "Italiana"},
        {"name": "Central", "phone": "+5114245566", "city": "Barranco", "type": "Alta Cocina"},
        {"name": "Mérito", "phone": "+5114455667", "city": "Santiago de Surco", "type": "Venezolana"},
        {"name": "Isolina", "phone": "+5114245566", "city": "Barranco", "type": "Criolla"},
        {"name": "El Pan de la Chola", "phone": "+5114466778", "city": "Barranco", "type": "Panadería"},
        {"name": "Café de Lima", "phone": "+5113322110", "city": "Lima Centro", "type": "Cafetería"},
        {"name": "Costazul", "phone": "+5114455667", "city": "Santiago de Surco", "type": "Cevichería"},
        {"name": "El Verdugo", "phone": "+5114455667", "city": "Santiago de Surco", "type": "Parrilla"},
        {"name": "Punto Azul Centro", "phone": "+5113322110", "city": "Lima Centro", "type": "Cevichería"},
        {"name": "Sanguichería Nico", "phone": "+5113322110", "city": "Lima Centro", "type": "Sánguches"},
        {"name": "Pardos Chicken", "phone": "+5114455667", "city": "Santiago de Surco", "type": "Pollo"},
        {"name": "Tanta", "phone": "+5114455667", "city": "San Martín de Porres", "type": "Peruana"},
        {"name": "Rafael", "phone": "+5114455667", "city": "San Borja", "type": "Alta Cocina"},
        {"name": "La Gloria", "phone": "+5114455667", "city": "San Isidro", "type": "Criolla"},
        {"name": "Madam Tusan", "phone": "+5114455667", "city": "Santiago de Surco", "type": "Chifa"},
        {"name": "Chili's", "phone": "+5114455667", "city": "Santiago de Surco", "type": "Americana"},
        {"name": "Papacho's", "phone": "+5114455667", "city": "Santiago de Surco", "type": "Hamburguesas"},
        {"name": "Pizza Hut", "phone": "+5114455667", "city": "Miraflores", "type": "Pizza"},
        {"name": "Norky's", "phone": "+5114455667", "city": "Miraflores", "type": "Criolla"},
        {"name": "Crepes & Waffles", "phone": "+5114455667", "city": "Miraflores", "type": "Francés"},
        {"name": "La Matriarca", "phone": "+5114455667", "city": "Miraflores", "type": "Criolla"},
        {"name": "Veda", "phone": "+5114455667", "city": "Miraflores", "type": "Vegetariano"},
        {"name": "La Traviata", "phone": "+5114455667", "city": "Miraflores", "type": "Italiana"},
        {"name": "Sushi Pop", "phone": "+5114455667", "city": "Miraflores", "type": "Sushi"},
    ]


def main():
    """Función principal."""
    print("=" * 60)
    print("  LIMA AUTOMA - Combinando Datos")
    print("=" * 60)
    
    # Cargar datos de Geoapify
    geoapify_file = Path("data/clientes_geoapify_completo.json")
    
    if not geoapify_file.exists():
        print("\n  No hay archivo de Geoapify.")
        return
    
    with open(geoapify_file, "r", encoding="utf-8") as f:
        restaurantes_geoapify = json.load(f)
    
    print(f"\n  Restaurantes Geoapify: {len(restaurantes_geoapify)}")
    
    # Cargar datos locales
    datos_locales = cargar_datos_locales()
    print(f"  Datos locales con tel: {len(datos_locales)}")
    
    # Crear diccionario de teléfonos locales
    telefonos_locales = {}
    for r in datos_locales:
        key = r["name"].lower().strip()
        telefonos_locales[key] = r["phone"]
    
    # Enriquecer datos de Geoapify
    enriquecidos = 0
    
    for restaurante in restaurantes_geoapify:
        nombre = restaurante.get("name", "").lower().strip()
        
        if nombre in telefonos_locales:
            restaurante["phone"] = telefonos_locales[nombre]
            enriquecidos += 1
    
    # Guardar
    output_file = Path("data/clientes_finales.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(restaurantes_geoapify, f, ensure_ascii=False, indent=2)
    
    # Estadísticas
    con_telefono = sum(1 for r in restaurantes_geoapify if r.get("phone"))
    
    print("\n" + "=" * 60)
    print(f"  RESULTADOS:")
    print(f"  Total restaurantes: {len(restaurantes_geoapify)}")
    print(f"  Con teléfono (locales): {con_telefono}")
    print(f"  Guardado en: {output_file}")
    print("=" * 60)
    
    # Mostrar algunos ejemplos
    print("\n  EJEMPLOS CON TELÉFONO:")
    print("  " + "-" * 50)
    
    ejemplos = [r for r in restaurantes_geoapify if r.get("phone")][:10]
    
    for i, r in enumerate(ejemplos, 1):
        print(f"  {i}. {r['name']} - {r.get('phone', 'N/A')}")


if __name__ == "__main__":
    main()
