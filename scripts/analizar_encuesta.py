"""
Lima Automa - Analizador de Encuesta
=====================================
Analiza los resultados de la encuesta de validación.
"""
import json
from pathlib import Path


def crear_encuesta_ejemplo():
    """Crea datos de ejemplo para probar el análisis."""
    datos = {
        "respuestas": [
            {
                "timestamp": "2026-08-15 10:30",
                "tipo_restaurante": "Cevichería",
                "distrito": "Miraflores",
                "clientes_diarios": "21-50 clientes",
                "clientes_nuevos_necesita": "31-50 clientes nuevos",
                "mayor_problema": "No tengo suficientes clientes",
                "gasto_marketing": "S/ 0 - 500 al mes",
                "interes_comision": "Sí, me interesa mucho",
                "disposicion_pagar": "S/ 15 por cliente",
                "servicio_interes": "Traer clientes nuevos a mi restaurante",
                "mes_gratis": "Sí, obvio que sí",
                "nombre": "Juan Pérez",
                "whatsapp": "+51999123456",
                "email": "juan@email.com"
            },
            {
                "timestamp": "2026-08-15 11:15",
                "tipo_restaurante": "Pollería",
                "distrito": "San Isidro",
                "clientes_diarios": "51-100 clientes",
                "clientes_nuevos_necesita": "11-30 clientes nuevos",
                "mayor_problema": "La competencia es muy fuerte",
                "gasto_marketing": "S/ 500 - 1,000 al mes",
                "interes_comision": "Sí, pero tengo dudas",
                "disposicion_pagar": "S/ 10 por cliente",
                "servicio_interes": "Ambos servicios juntos",
                "mes_gratis": "Tal vez, necesito más información",
                "nombre": "María García",
                "whatsapp": "+51999789012",
                "email": "maria@email.com"
            },
            {
                "timestamp": "2026-08-15 12:45",
                "tipo_restaurante": "Café/Cafetería",
                "distrito": "Barranco",
                "clientes_diarios": "0-20 clientes",
                "clientes_nuevos_necesita": "0-10 clientes nuevos",
                "mayor_problema": "No tengo tiempo para marketing",
                "gasto_marketing": "Nada, no invierto en marketing",
                "interes_comision": "Sí, me interesa mucho",
                "disposicion_pagar": "S/ 20 por cliente",
                "servicio_interes": "Traer clientes nuevos a mi restaurante",
                "mes_gratis": "Sí, obvio que sí",
                "nombre": "Carlos López",
                "whatsapp": "+51999345678",
                "email": ""
            }
        ]
    }
    
    output_file = Path("data/encuesta_resultados.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    print(f"Datos de ejemplo creados: {output_file}")
    return datos


def analizar_resultados(datos):
    """Analiza los resultados de la encuesta."""
    respuestas = datos.get("respuestas", [])
    total = len(respuestas)
    
    if total == 0:
        print("No hay respuestas para analizar.")
        return
    
    print("=" * 60)
    print("  ANÁLISIS DE ENCUESTA - LIMA AUTOMA")
    print("=" * 60)
    print(f"\n  Total de respuestas: {total}")
    
    # Análisis por pregunta
    preguntas = {
        "tipo_restaurante": "Tipo de Restaurante",
        "distrito": "Distrito",
        "clientes_diarios": "Clientes Diarios",
        "clientes_nuevos_necesita": "Clientes Nuevos Necesita",
        "mayor_problema": "Mayor Problema",
        "gasto_marketing": "Gasto en Marketing",
        "interes_comision": "Interés en Modelo de Comisión",
        "disposicion_pagar": "Disposición a Pagar",
        "servicio_interes": "Servicio Más Interesante",
        "mes_gratis": "Interés en Mes Gratis"
    }
    
    resultados = {}
    
    for key, titulo in preguntas.items():
        print(f"\n  {titulo}:")
        print("  " + "-" * 40)
        
        conteo = {}
        for respuesta in respuestas:
            valor = respuesta.get(key, "No especificado")
            conteo[valor] = conteo.get(valor, 0) + 1
        
        # Ordenar por cantidad
        ordenado = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
        
        for valor, cantidad in ordenado:
            porcentaje = (cantidad / total) * 100
            barra = "█" * int(porcentaje / 5)
            print(f"    {valor}: {cantidad} ({porcentaje:.0f}%) {barra}")
        
        resultados[key] = ordenado
    
    # Métricas clave
    print("\n" + "=" * 60)
    print("  MÉTRICAS CLAVE DE VALIDACIÓN")
    print("=" * 60)
    
    # Interés en servicio
    interes_count = sum(1 for r in respuestas if "interesa" in r.get("interes_comision", "").lower())
    interes_pct = (interes_count / total) * 100
    print(f"\n  ✅ Interés en servicio: {interes_count}/{total} ({interes_pct:.0f}%)")
    
    # Disposición a pagar
    pagar_count = sum(1 for r in respuestas if r.get("disposicion_pagar", "").startswith("S/"))
    pagar_pct = (pagar_count / total) * 100
    print(f"  ✅ Disposición a pagar: {pagar_count}/{total} ({pagar_pct:.0f}%)")
    
    # Interés en mes gratis
    gratis_count = sum(1 for r in respuestas if "sí" in r.get("mes_gratis", "").lower())
    gratis_pct = (gratis_count / total) * 100
    print(f"  ✅ Interés en mes gratis: {gratis_count}/{total} ({gratis_pct:.0f}%)")
    
    # Contactos disponibles
    contactos = [r for r in respuestas if r.get("whatsapp") or r.get("email")]
    print(f"\n  📞 Contactos disponibles: {len(contactos)}/{total}")
    
    # Resumen ejecutivo
    print("\n" + "=" * 60)
    print("  RESUMEN EJECUTIVO")
    print("=" * 60)
    
    if interes_pct >= 60:
        print("  ✅ DEMANDA CONFIRMADA - Los restaurantes necesitan este servicio")
    else:
        print("  ⚠️ DEMANDA BAJA - Revisar propuesta de valor")
    
    if pagar_pct >= 50:
        print("  ✅ MODELO VIABLE - Están dispuestos a pagar por cliente")
    else:
        print("  ⚠️ MODELO EN RIESGO - Revisar precios")
    
    if gratis_pct >= 70:
        print("  ✅ LISTOS PARA PILOTO - Muchos quieren probar gratis")
    else:
        print("  ⚠️ PILOTO DIFÍCIL - Pocos interesados en probar")
    
    return resultados


def main():
    print("=" * 60)
    print("  LIMA AUTOMA - Analizador de Encuesta")
    print("=" * 60)
    
    # Verificar si hay datos reales
    datos_file = Path("data/encuesta_resultados.json")
    
    if datos_file.exists():
        print(f"\n  Cargando datos reales de: {datos_file}")
        with open(datos_file, "r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        print("\n  No se encontraron datos reales.")
        print("  Creando datos de ejemplo para demostración...")
        datos = crear_encuesta_ejemplo()
    
    # Analizar
    analizar_resultados(datos)


if __name__ == "__main__":
    main()
