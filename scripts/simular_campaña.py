"""
Lima Automa - Simulador de Campaña
===================================
Simula el envío de mensajes y respuestas para demostración.
"""
import json
import random
from pathlib import Path
from datetime import datetime, timedelta


def cargar_clientes():
    """Carga la lista de clientes potenciales."""
    clientes_file = Path("data/clientes_potenciales.json")
    if clientes_file.exists():
        with open(clientes_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def simular_respuesta(restaurante):
    """Simula una respuesta aleatoria del restaurante."""
    probabilidad = random.random()
    
    if probabilidad < 0.3:  # 30% interés alto
        return {
            "tipo": "interes_alto",
            "mensaje": "¡Hola! Me interesa. ¿Cómo funciona?",
            "accion": "agendar_llamada"
        }
    elif probabilidad < 0.5:  # 20% interés medio
        return {
            "tipo": "interes_medio",
            "mensaje": "Dígame más, ¿cuál es el costo?",
            "accion": "enviar_info"
        }
    elif probabilidad < 0.7:  # 20% sin respuesta
        return {
            "tipo": "sin_respuesta",
            "mensaje": None,
            "accion": "seguimiento"
        }
    else:  # 30% no interesado
        return {
            "tipo": "no_interesado",
            "mensaje": "No estamos interesados, gracias.",
            "accion": "agradecer"
        }


def simular_campaña():
    """Simula una campaña completa de contactos."""
    print("=" * 60)
    print("  LIMA AUTOMA - Simulador de Campaña")
    print("=" * 60)
    
    clientes = cargar_clientes()
    
    if not clientes:
        print("\n  No hay clientes para simular.")
        print("  Ejecuta primero: python scripts/buscador_clientes.py")
        return
    
    print(f"\n  Clientes cargados: {len(clientes)}")
    
    # Simular campañas por día
    campañas = []
    
    for i, cliente in enumerate(clientes[:10], 1):  # Primeros 10
        respuesta = simular_respuesta(cliente)
        
        campaña = {
            "id": i,
            "restaurante": cliente.get("name"),
            "distrito": cliente.get("city"),
            "telefono": cliente.get("phone"),
            "mensaje_enviado": f"Hola, somos Lima Automa. ¿Les gustaría recibir más clientes?",
            "respuesta": respuesta,
            "fecha": (datetime.now() - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d %H:%M"),
            "estado": respuesta.get("tipo")
        }
        
        campañas.append(campaña)
    
    # Guardar campañas
    output_file = Path("data/campanas_simuladas.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(campañas, f, ensure_ascii=False, indent=2)
    
    # Generar reporte
    print("\n" + "=" * 60)
    print("  REPORTE DE CAMPAÑA SIMULADA")
    print("=" * 60)
    
    total = len(campañas)
    interes_alto = sum(1 for c in campañas if c["estado"] == "interes_alto")
    interes_medio = sum(1 for c in campañas if c["estado"] == "interes_medio")
    sin_respuesta = sum(1 for c in campañas if c["estado"] == "sin_respuesta")
    no_interesado = sum(1 for c in campañas if c["estado"] == "no_interesado")
    
    print(f"\n  Total contactados: {total}")
    print(f"  Interés alto: {interes_alto} ({interes_alto/total*100:.0f}%)")
    print(f"  Interés medio: {interes_medio} ({interes_medio/total*100:.0f}%)")
    print(f"  Sin respuesta: {sin_respuesta} ({sin_respuesta/total*100:.0f}%)")
    print(f"  No interesados: {no_interesado} ({no_interesado/total*100:.0f}%)")
    
    # Mostrar detalles
    print("\n  DETALLE POR RESTAURANTE:")
    print("  " + "-" * 50)
    
    for campaña in campañas:
        print(f"\n  {campaña['restaurante']} ({campaña['distrito']})")
        print(f"    Estado: {campaña['estado']}")
        if campaña['respuesta']['mensaje']:
            print(f"    Mensaje: {campaña['respuesta']['mensaje']}")
        print(f"    Acción: {campaña['respuesta']['accion']}")
    
    print("\n  ¡Simulación completada!")
    print(f"  Guardado en: {output_file}")
    
    return campañas


if __name__ == "__main__":
    simular_campaña()
