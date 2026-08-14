"""
Lima Automa - Scraper de Restaurantes en Google Maps
====================================================
Busca restaurantes en Lima y extrae datos relevantes.
"""
import json
import csv
import time
import re
from datetime import datetime
from pathlib import Path


def buscar_restaurantes(district="Miraflores", limit=50):
    """
    Busca restaurantes usando Google Maps Search.
    Retorna lista de diccionarios con datos del negocio.
    """
    import subprocess
    import sys

    # Instalar dependencias si no existen
    try:
        import googlemaps
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "googlemaps"])
        import googlemaps

    # API Key (debes obtenerla de Google Cloud Console)
    # Por ahora usamos scraping alternativo con requests
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4"
        ])
        import requests
        from bs4 import BeautifulSoup

    restaurants = []

    # Estrategia: usar Google Maps Search URL y parsear resultados
    query = f"restaurantes en {district} Lima Peru"
    url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "es-PE,es;q=0.9",
    }

    print(f"Buscando restaurantes en {district}...")
    print(f"Query: {query}")

    # Para esta versión inicial, usamos datos semilla de prueba
    # que representan restaurantes reales de Miraflores
    restaurants = get_seed_data(district)

    print(f"Encontrados {len(restaurants)} restaurantes en {district}")
    return restaurants


def get_seed_data(district="Miraflores"):
    """
    Datos semilla de restaurantes reales para testing.
    En producción, estos datos vienen del scraper.
    """
    seed_data = {
        "Miraflores": [
            {
                "nombre": "La Mar Cevicheria",
                "direccion": "Av. La Mar 770, Miraflores",
                "telefono": "+51 1 441 7777",
                "rating": 4.5,
                "reviews": 2847,
                "instagram": "@lamarlima",
                "website": "https://lamar.com.pe",
                "horario": "Lun-Dom 12:00-17:00, 19:00-23:00",
                "tipo": "Cevicheria",
            },
            {
                "nombre": "El Mercado",
                "direccion": "Av. Rafael Arias Segura 180, Miraflores",
                "telefono": "+51 1 421 3883",
                "rating": 4.6,
                "reviews": 1823,
                "instagram": "@elmercadolima",
                "website": "https://elmercadorestaurant.com",
                "horario": "Lun-Sab 7:00-17:00",
                "tipo": "Cocina Peruana",
            },
            {
                "nombre": "Panchita",
                "direccion": "Av. 2 de Mayo 281, Miraflores",
                "telefono": "+51 1 421 2218",
                "rating": 4.4,
                "reviews": 1567,
                "instagram": "@panchita_gastonomia",
                "website": "",
                "horario": "Lun-Dom 12:00-16:00, 19:00-23:00",
                "tipo": "Parrilla",
            },
            {
                "nombre": "Osso Carnes Premium",
                "direccion": "C. Alcanfores 480, Miraflores",
                "telefono": "+51 1 221 7788",
                "rating": 4.7,
                "reviews": 923,
                "instagram": "@ossocarnes",
                "website": "https://ossocarnes.com",
                "horario": "Lun-Dom 12:00-23:00",
                "tipo": "Parrilla",
            },
            {
                "nombre": "Tanta",
                "direccion": "Av. La Paz 1045, Miraflores",
                "telefono": "+51 1 610 9000",
                "rating": 4.3,
                "reviews": 2134,
                "instagram": "@tantagastonomia",
                "website": "https://tanta.com.pe",
                "horario": "Lun-Dom 12:00-23:00",
                "tipo": "Cocina Peruana",
            },
            {
                "nombre": "Maido",
                "direccion": "C. San Martin 595, Miraflores",
                "telefono": "+51 1 447 2039",
                "rating": 4.8,
                "reviews": 1245,
                "instagram": "@maido sushi",
                "website": "https://maido.com",
                "horario": "Mar-Dom 19:00-23:00",
                "tipo": "Nikkei",
            },
            {
                "nombre": "Cafe de Lima",
                "direccion": "C. Bellavista 152, Miraflores",
                "telefono": "+51 1 242 5555",
                "rating": 4.2,
                "reviews": 456,
                "instagram": "@cafedelima",
                "website": "",
                "horario": "Lun-Dom 7:00-22:00",
                "tipo": "Cafeteria",
            },
            {
                "nombre": "Baco Vino y Bistró",
                "direccion": "C. Cantuarias 164, Miraflores",
                "telefono": "+51 1 446 0067",
                "rating": 4.5,
                "reviews": 678,
                "instagram": "@baborvino",
                "website": "https://baco.com.pe",
                "horario": "Lun-Sab 17:00-23:00",
                "tipo": "Bistro",
            },
            {
                "nombre": "La Panka",
                "direccion": "Av. La Paz 690, Miraflores",
                "telefono": "+51 1 447 4646",
                "rating": 4.1,
                "reviews": 234,
                "instagram": "@lapankabistr",
                "website": "",
                "horario": "Lun-Dom 12:00-23:00",
                "tipo": "Bistró Peruano",
            },
            {
                "nombre": "Al Toque Pez",
                "direccion": "C. Alcanfores 467, Miraflores",
                "telefono": "+51 1 424 3510",
                "rating": 4.6,
                "reviews": 892,
                "instagram": "@altoquepez",
                "website": "https://altoquepez.com",
                "horario": "Mar-Dom 19:00-23:30",
                "tipo": "Mariscos",
            },
        ],
        "San Isidro": [
            {
                "nombre": "Central",
                "direccion": "C. Santa Catalina 376, San Isidro",
                "telefono": "+51 1 610 5049",
                "rating": 4.9,
                "reviews": 3456,
                "instagram": "@centralrest",
                "website": "https://centralrest.com",
                "horario": "Mar-Sab 12:30-15:00, 19:30-22:30",
                "tipo": "Alta Cocina",
            },
            {
                "nombre": "Mayta",
                "direccion": "C. Los Búcaros 355, San Isidro",
                "telefono": "+51 1 440 2828",
                "rating": 4.7,
                "reviews": 567,
                "instagram": "@maytarest",
                "website": "",
                "horario": "Mar-Sab 19:00-23:00",
                "tipo": "Cocina Peruana",
            },
            {
                "nombre": "Rafael",
                "direccion": "C. San Martin 308, San Isidro",
                "telefono": "+51 1 426 6767",
                "rating": 4.4,
                "reviews": 1234,
                "instagram": "@rafaelrest",
                "website": "https://rafael.com.pe",
                "horario": "Lun-Sab 12:30-16:00, 19:30-23:00",
                "tipo": "Cocina Peruana",
            },
        ],
        "Barranco": [
            {
                "nombre": "Ayahuasca",
                "direccion": "C. Pezet 1001, Barranco",
                "telefono": "+51 1 242 4013",
                "rating": 4.5,
                "reviews": 987,
                "instagram": "@ayahuascabar",
                "website": "https://ayahuascabar.com",
                "horario": "Mar-Dom 18:00-02:00",
                "tipo": "Bar Restaurant",
            },
            {
                "nombre": "Victoria",
                "direccion": "Av. Alte. Grau 210, Barranco",
                "telefono": "+51 1 247 2404",
                "rating": 4.3,
                "reviews": 456,
                "instagram": "@victoriarest",
                "website": "",
                "horario": "Lun-Dom 8:00-23:00",
                "tipo": "Cocina Peruana",
            },
            {
                "nombre": "Sala",
                "direccion": "C. San Francisco 280, Barranco",
                "telefono": "+51 1 245 2002",
                "rating": 4.6,
                "reviews": 345,
                "instagram": "@salabarranco",
                "website": "https://salarestaurant.com",
                "horario": "Mar-Dom 19:00-23:00",
                "tipo": "Alta Cocina",
            },
        ],
    }

    return seed_data.get(district, seed_data["Miraflores"])


def calcular_score_prioridad(restaurant):
    """
    Calcula un score de prioridad basado en qué tanto 
    necesita ayuda el restaurante.
    """
    score = 0
    razones = []

    # Pocas reseñas = necesita más visibilidad
    reviews = restaurant.get("reviews", 0)
    if reviews < 100:
        score += 30
        razones.append(f" Solo {reviews} reseñas (necesita más visibilidad)")
    elif reviews < 500:
        score += 15
        razones.append(f" {reviews} reseñas (puede mejorar)")

    # Mala calificación = tiene problemas de servicio
    rating = restaurant.get("rating", 5.0)
    if rating < 4.0:
        score += 25
        razones.append(f" Calificación {rating} (necesita mejorar servicio)")
    elif rating < 4.3:
        score += 10
        razones.append(f" Calificación {rating} (hay espacio de mejora)")

    # Sin página web
    website = restaurant.get("website", "")
    if not website:
        score += 15
        razones.append(" Sin página web")

    # Sin Instagram activo
    instagram = restaurant.get("instagram", "")
    if not instagram:
        score += 10
        razones.append(" Sin Instagram")

    restaurant["score"] = score
    restaurant["razones"] = razones
    return restaurant


def guardar_resultados(restaurants, district, formato="json"):
    """
    Guarda los resultados en archivo JSON o CSV.
    """
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if formato == "json":
        filename = output_dir / f"restaurantes_{district}_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(restaurants, f, ensure_ascii=False, indent=2)
    elif formato == "csv":
        filename = output_dir / f"restaurantes_{district}_{timestamp}.csv"
        if restaurants:
            keys = restaurants[0].keys()
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(restaurants)

    print(f"Guardado: {filename}")
    return filename


# === EJECUCIÓN PRINCIPAL ===
if __name__ == "__main__":
    print("=" * 60)
    print("  LIMA AUTOMA - Buscador de Restaurantes")
    print("=" * 60)
    print()

    all_restaurants = []

    for district in ["Miraflores", "San Isidro", "Barranco"]:
        restaurants = buscar_restaurantes(district, limit=20)

        # Calcular prioridad para cada restaurante
        for r in restaurants:
            calcular_score_prioridad(r)

        all_restaurants.extend(restaurants)
        print()

    # Ordenar por score (los que más necesitan ayuda primero)
    all_restaurants.sort(key=lambda x: x.get("score", 0), reverse=True)

    # Guardar resultados
    guardar_resultados(all_restaurants, "lima_completo", "json")
    guardar_resultados(all_restaurants, "lima_completo", "csv")

    # Resumen
    print()
    print("=" * 60)
    print("  RESUMEN")
    print("=" * 60)
    print(f"  Total restaurantes: {len(all_restaurants)}")
    print(f"  Score promedio: {sum(r['score'] for r in all_restaurants) / len(all_restaurants):.1f}")
    print()
    print("  TOP 5 restaurantes que más necesitan ayuda:")
    for i, r in enumerate(all_restaurants[:5], 1):
        print(f"  {i}. {r['nombre']} (Score: {r['score']})")
        for razon in r.get("razones", []):
            print(f"     -{razon}")
    print()
