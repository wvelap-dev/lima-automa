"""
Lima Automa - Generador de Mensajes Personalizados
===================================================
Crea mensajes únicos para cada restaurante basado en sus datos.
"""


def generar_mensaje_whatsapp(restaurant):
    """
    Genera un mensaje personalizado de WhatsApp para un restaurante.
    Cada mensaje es único basado en los datos del restaurante.
    """
    nombre = restaurant.get("nombre", "Restaurante")
    rating = restaurant.get("rating", 0)
    reviews = restaurant.get("reviews", 0)
    tipo = restaurant.get("tipo", "restaurante")
    instagram = restaurant.get("instagram", "")
    website = restaurant.get("website", "")
    distrito = restaurant.get("distrito", "Lima")

    # Detectar debilidades
    debilidades = []
    if reviews < 500:
        debilidades.append("pocas reseñas")
    if rating < 4.3:
        debilidades.append("calificación mejorable")
    if not website:
        debilidades.append("sin página web")
    if not instagram:
        debilidades.append("sin Instagram activo")

    # Construir mensaje según debilidades detectadas
    if not debilidades:
        # Restaurante que ya le va bien → enfoque en crecer más
        mensaje = f"""Hola, vi {nombre} en Google Maps. Tienen {reviews} reseñas con {rating} estrellas, eso está muy bien.

Pero sabían que sus competidores en {tipo} están apareciendo PRIMERO en Google cuando alguien busca "{tipo} en {distrito}"?

Les puedo mostrar en 5 minutos cómo aparecer primero sin gastar en publicidad. ¿Cuándo les viene bien?"""
    elif "pocas reseñas" in debilidades:
        # Pocas reseñas → enfoque en visibilidad
        mensaje = f"""Hola, soy fan de {tipo} y encontré {nombre} en {distrito}.

Vi que tienen solo {reviews} reseñas en Google. Sus competidores similares tienen 500+.

¿Saben por qué eso importa? Cuando alguien busca "{tipo} en {distrito}", Google muestra PRIMERO a los que tienen más reseñas.

Tengo una forma de ayudarles a conseguir 30-50 reseñas nuevas en 2 semanas. Sin costo inicial.

¿Les muestro cómo funciona? 15 minutos por videollamada."""
    elif "calificación mejorable" in debilidades:
        # Mala calificación → enfoque en mejorar servicio
        mensaje = f"""Hola, vi {nombre} en Google. Tienen {rating} estrellas con {reviews} reseñas.

Está bien, pero hay espacio para llegar a 4.5+. ¿Saben cuántos clientes pierden por cada décima de estrella?

Un restaurante de {tipo} similar en {distrito} subió de 4.1 a 4.6 en 3 meses y sus ventas subieron 40%.

¿Quieren saber cómo lo hicieron? Les puedo explicar en 10 minutos."""
    elif "sin página web" in debilidades:
        # Sin web → enfoque en presencia digital
        mensaje = f"""Hola, encontré {nombre} en Google Maps. Buen {rating} estrellas.

Pero no tienen página web. ¿Saben cuántos clientes buscan "{tipo} en {distrito}" y eligen al que tiene web?

Puedo crearles una página profesional en 48 horas que aparezca en Google. Sin inversión inicial.

¿Les interesa ver un ejemplo?"""
    else:
        # Mensaje general
        mensaje = f"""Hola, {nombre} apareció en mi búsqueda de {tipo} en {distrito}.

Vi que tienen {rating} estrellas con {reviews} reseñas. Buen comienzo.

Les puedo ayudar a triplicar esos números en 90 días. Sin publicidad pagada, sin complicaciones.

¿Cuándo pueden 15 minutos para que les muestre cómo?"""

    return mensaje


def generar_mensaje_seguimiento(restaurant, dias=1):
    """
    Genera mensaje de seguimiento si no respondieron.
    """
    nombre = restaurant.get("nombre", "Restaurante")

    mensajes = {
        1: f"Hola, {nombre}. Solo queria saber si vio mi mensaje anterior sobre como conseguir mas clientes. Estoy aqui para ayudarlos.",
        3: f"Hola {nombre}, le envie un ejemplo de como otro restaurante similar aumento sus ventas 30%. Se lo mando?",
        7: f"Ultimo mensaje, {nombre}. No quiero molestar. Si cambian de opinion, aqui estoy. Exitos.",
    }

    return mensajes.get(dias, "")


def generar_mensaje_para_calido(restaurant):
    """
    Mensaje cuando el restaurante ya está interesado.
    """
    nombre = restaurant.get("nombre", "Restaurante")
    return f"""¡Perfecto, {nombre}!

¿Cuándo pueden 15 minutos esta semana?

Yo les muestro:
- Cuántos clientes están perdiendo ahora mismo
- Cómo recuperarlos sin gastar en publicidad
- Un caso real de restaurante que lo hizo

¿Martes o miércoles les viene mejor?"""


# === TESTING ===
if __name__ == "__main__":
    test_restaurants = [
        {
            "nombre": "La Panka",
            "rating": 4.1,
            "reviews": 234,
            "tipo": "Bistró Peruano",
            "instagram": "@lapankabistr",
            "website": "",
        },
        {
            "nombre": "Cafe de Lima",
            "rating": 4.2,
            "reviews": 456,
            "tipo": "Cafeteria",
            "instagram": "@cafedelima",
            "website": "",
        },
        {
            "nombre": "Maido",
            "rating": 4.8,
            "reviews": 1245,
            "tipo": "Nikkei",
            "instagram": "@maido sushi",
            "website": "https://maido.com",
        },
    ]

    for r in test_restaurants:
        print(f"\n{'='*50}")
        print(f"RESTAURANTE: {r['nombre']}")
        print(f"{'='*50}")
        print(generar_mensaje_whatsapp(r))
        print(f"\n--- SEGUIMIENTO DÍA 1 ---")
        print(generar_mensaje_seguimiento(r, 1))
