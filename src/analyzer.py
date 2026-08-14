"""
Lima Automa - Calificador de Restaurantes
==========================================
Determina qué restaurantes contactar primero y por qué.
"""


def analizar_restaurante(restaurant):
    """
    Analiza un restaurante y retorna insights accionables.
    """
    nombre = restaurant.get("nombre", "Restaurante")
    rating = restaurant.get("rating", 0)
    reviews = restaurant.get("reviews", 0)
    tipo = restaurant.get("tipo", "restaurante")
    instagram = restaurant.get("instagram", "")
    website = restaurant.get("website", "")

    insights = {
        "nombre": nombre,
        "fortalezas": [],
        "debilidades": [],
        "oportunidades": [],
        "accion_sugerida": "",
        "prioridad": "MEDIA",
        "score": 0,
    }

    # Analizar fortalezas
    if reviews > 1000:
        insights["fortalezas"].append("Alta base de clientes (1000+ reseñas)")
    if rating >= 4.5:
        insights["fortalezas"].append("Excelente reputación (4.5+)")
    if instagram:
        insights["fortalezas"].append(f"Presencia en Instagram ({instagram})")
    if website:
        insights["fortalezas"].append("Tiene página web")

    # Analizar debilidades
    if reviews < 100:
        insights["debilidades"].append(f"Solo {reviews} reseñas - muy pocas")
        insights["score"] += 30
    elif reviews < 500:
        insights["debilidades"].append(f"{reviews} reseñas - puede mejorar")
        insights["score"] += 15

    if rating < 4.0:
        insights["debilidades"].append(f"Calificación {rating} - bajo")
        insights["score"] += 25
    elif rating < 4.3:
        insights["debilidades"].append(f"Calificación {rating} - mejorable")
        insights["score"] += 10

    if not website:
        insights["debilidades"].append("Sin página web")
        insights["score"] += 15

    if not instagram:
        insights["debilidades"].append("Sin Instagram")
        insights["score"] += 10

    # Detectar oportunidades
    if reviews < 500 and rating >= 4.0:
        insights["oportunidades"].append(
            "Buen servicio pero poca visibilidad → campañas de reseñas"
        )
    if not website:
        insights["oportunidades"].append(
            "Oportunidad de crear web que aparezca en Google"
        )
    if rating < 4.3 and reviews > 200:
        insights["oportunidades"].append(
            "Basta con mejorar servicio para subir calificación"
        )

    # Determinar prioridad
    if insights["score"] >= 40:
        insights["prioridad"] = "ALTA"
    elif insights["score"] >= 20:
        insights["prioridad"] = "MEDIA"
    else:
        insights["prioridad"] = "BAJA"

    # Acción sugerida
    if insights["debilidades"]:
        debilidad_principal = insights["debilidades"][0]
        if "reseñas" in debilidad_principal:
            insights["accion_sugerida"] = (
                "Ofrecer campaña de reseñas: traer clientes que dejen Google review"
            )
        elif "calificación" in debilidad_principal:
            insights["accion_sugerida"] = (
                "Ofrecer sistema de feedback + seguimiento post-visita"
            )
        elif "web" in debilidad_principal:
            insights["accion_sugerida"] = (
                "Ofrecer landing page optimizada para Google"
            )
        else:
            insights["accion_sugerida"] = (
                "Ofrecer paquete de presencia digital completa"
            )
    else:
        insights["accion_sugerida"] = (
            "Restaurante sólido → ofrecer servicio de crecimiento (más clientes)"
        )

    return insights


def generar_informe(restaurants):
    """
    Genera un informe resumen de todos los restaurantes analizados.
    """
    informe = {
        "total": len(restaurants),
        "alta_prioridad": [],
        "media_prioridad": [],
        "baja_prioridad": [],
        "stats": {
            "promedio_rating": 0,
            "promedio_reviews": 0,
            "sin_web": 0,
            "sin_instagram": 0,
        },
    }

    total_rating = 0
    total_reviews = 0

    for r in restaurants:
        insights = analizar_restaurante(r)
        total_rating += r.get("rating", 0)
        total_reviews += r.get("reviews", 0)

        if not r.get("website"):
            informe["stats"]["sin_web"] += 1
        if not r.get("instagram"):
            informe["stats"]["sin_instagram"] += 1

        entrada = {
            "nombre": insights["nombre"],
            "score": insights["score"],
            "prioridad": insights["prioridad"],
            "debilidades": insights["debilidades"],
            "accion": insights["accion_sugerida"],
        }

        if insights["prioridad"] == "ALTA":
            informe["alta_prioridad"].append(entrada)
        elif insights["prioridad"] == "MEDIA":
            informe["media_prioridad"].append(entrada)
        else:
            informe["baja_prioridad"].append(entrada)

    # Calcular promedios
    if restaurants:
        informe["stats"]["promedio_rating"] = round(
            total_rating / len(restaurants), 2
        )
        informe["stats"]["promedio_reviews"] = round(
            total_reviews / len(restaurants), 0
        )

    # Ordenar por score dentro de cada categoría
    for key in ["alta_prioridad", "media_prioridad", "baja_prioridad"]:
        informe[key].sort(key=lambda x: x["score"], reverse=True)

    return informe


# === TESTING ===
if __name__ == "__main__":
    from scraper_restaurantes import buscar_restaurantes

    restaurants = buscar_restaurantes("Miraflores")
    informe = generar_informe(restaurants)

    print(f"\n{'='*60}")
    print(f"  INFORME DE PRIORIDADES - MIRAFLORES")
    print(f"{'='*60}")
    print(f"\n  Total: {informe['total']} restaurantes")
    print(f"  Rating promedio: {informe['stats']['promedio_rating']}")
    print(f"  Reviews promedio: {informe['stats']['promedio_reviews']}")
    print(f"  Sin web: {informe['stats']['sin_web']}")
    print(f"  Sin Instagram: {informe['stats']['sin_instagram']}")

    print(f"\n  ALTA PRIORIDAD ({len(informe['alta_prioridad'])}):")
    for r in informe["alta_prioridad"]:
        print(f"    {r['nombre']} (Score: {r['score']})")
        print(f"      Acción: {r['accion']}")

    print(f"\n  MEDIA PRIORIDAD ({len(informe['media_prioridad'])}):")
    for r in informe["media_prioridad"]:
        print(f"    {r['nombre']} (Score: {r['score']})")
