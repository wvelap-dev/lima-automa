"""
Lima Automa - Contactador de Clientes
======================================
Genera mensajes y links de WhatsApp para contactar restaurantes.
"""
import json
from pathlib import Path


def cargar_clientes():
    """Carga la lista de clientes potenciales."""
    clientes_file = Path("data/clientes_potenciales.json")
    if clientes_file.exists():
        with open(clientes_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def limpiar_telefono(telefono):
    """Limpia el teléfono para WhatsApp."""
    if not telefono:
        return ""
    
    # Remover espacios y guiones
    telefono = telefono.replace(" ", "").replace("-", "")
    
    # Asegurar que empiece con +
    if not telefono.startswith("+"):
        if telefono.startswith("51"):
            telefono = "+" + telefono
        else:
            telefono = "+51" + telefono
    
    return telefono


def generar_mensaje(restaurante):
    """Genera un mensaje personalizado para el restaurante."""
    nombre = restaurante.get("name", "Restaurante")
    distrito = restaurante.get("city", "Lima")
    rating = restaurante.get("rating", 0)
    reviews = restaurante.get("reviews", 0)
    
    # Personalizar según calificación
    if rating and rating < 4.0:
        gancho = f"Vi que tienen {rating} estrellas y {reviews} reseñas. Con nuestro servicio pueden mejorar eso y atraer más clientes."
    elif reviews and reviews < 100:
        gancho = f"Vi que tienen solo {reviews} reseñas. Podemos ayudarles a conseguir muchas más."
    else:
        gancho = f"Vi que tienen un restaurante increíble en {distrito}. Tengo una propuesta que les puede ayudar a conseguir más clientes."
    
    mensaje = f"""Hola, soy de Lima Automa. {gancho}

Les ofrecemos:
- Traemos clientes nuevos a su restaurante
- Sin costo inicial
- Solo pagan por cada cliente que les traemos

¿Les gustaría que les explique más?"""
    
    return mensaje


def generar_link_whatsapp(telefono, mensaje):
    """Genera un link de WhatsApp con el mensaje."""
    telefono_limpio = limpiar_telefono(telefono)
    
    if not telefono_limpio:
        return None
    
    # Codificar mensaje para URL
    mensaje_encoded = mensaje.replace(" ", "%20").replace("\n", "%0A")
    
    link = f"https://wa.me/{telefono_limpio[1:]}?text={mensaje_encoded}"
    
    return link


def main():
    """Función principal."""
    print("=" * 60)
    print("  LIMA AUTOMA - Contactador de Clientes")
    print("=" * 60)
    
    # Cargar clientes
    clientes = cargar_clientes()
    
    if not clientes:
        print("\n  No hay clientes para contactar.")
        print("  Ejecuta primero: python scripts/buscador_clientes.py")
        return
    
    print(f"\n  Clientes cargados: {len(clientes)}")
    
    # Filtrar solo los que tienen teléfono
    contactables = [c for c in clientes if c.get("phone")]
    
    print(f"  Contactables (con teléfono): {len(contactables)}")
    
    # Generar mensajes y links
    print("\n  Generando mensajes...")
    
    contactos = []
    
    for cliente in contactables:
        nombre = cliente.get("name", "Sin nombre")
        telefono = cliente.get("phone", "")
        
        mensaje = generar_mensaje(cliente)
        link = generar_link_whatsapp(telefono, mensaje)
        
        if link:
            contactos.append({
                "nombre": nombre,
                "telefono": limpiar_telefono(telefono),
                "mensaje": mensaje,
                "link_whatsapp": link
            })
    
    # Guardar contactos
    output_file = Path("data/contactos_whatsapp.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(contactos, f, ensure_ascii=False, indent=2)
    
    print(f"\n  Contactos generados: {len(contactos)}")
    print(f"  Guardados en: {output_file}")
    
    # Mostrar primeros 5
    print("\n  PRIMEROS 5 CONTACTOS:")
    print("  " + "-" * 50)
    
    for i, contacto in enumerate(contactos[:5], 1):
        print(f"\n  {i}. {contacto['nombre']}")
        print(f"     Tel: {contacto['telefono']}")
        print(f"     Link: {contacto['link_whatsapp'][:80]}...")
    
    print("\n  ¡Listo para contactar!")
    print("  Abre cada link de WhatsApp para enviar el mensaje.")


if __name__ == "__main__":
    main()
