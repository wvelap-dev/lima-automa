"""
Lima Automa - Runner Principal
===============================
Ejecuta el ciclo completo de automatizacion.
"""
import sys
sys.path.insert(0, 'src')

from scraper_restaurantes import buscar_restaurantes, calcular_score_prioridad
from message_generator import generar_mensaje_whatsapp
from whatsapp_automation import WhatsAppAutomation
from coupon_generator import crear_cupon, generar_qr_svg, crear_landing_page_html, generar_reporte_cupones
from chatbot_ia import ChatbotRestaurante
import json


def run_ciclo_completo():
    """
    Ejecuta el ciclo completo:
    1. Busca restaurantes
    2. Califica prioridades
    3. Genera mensajes
    4. Registra leads
    5. Prepara envios
    """
    print("=" * 60)
    print("  LIMA AUTOMA - Ciclo Completo de Automatizacion")
    print("=" * 60)

    # 1. Buscar restaurantes
    print("\n[1/5] Buscando restaurantes en Lima...")
    all_restaurants = []
    for district in ["Miraflores", "San Isidro", "Barranco"]:
        restaurants = buscar_restaurantes(district)
        all_restaurants.extend(restaurants)
    print(f"  Encontrados: {len(all_restaurants)} restaurantes")

    # 2. Calificar prioridades
    print("\n[2/5] Calificando prioridades...")
    for r in all_restaurants:
        calcular_score_prioridad(r)
    all_restaurants.sort(key=lambda x: x.get("score", 0), reverse=True)
    print(f"  Top prioridad: {all_restaurants[0]['nombre']} (Score: {all_restaurants[0]['score']})")

    # 3. Generar mensajes y registrar leads
    print("\n[3/5] Generando mensajes y registrando leads...")
    automation = WhatsAppAutomation()

    for r in all_restaurants[:10]:  # Top 10
        # Extraer distrito de la dirección si no existe
        if not r.get("distrito"):
            direccion = r.get("direccion", "")
            if ", " in direccion:
                r["distrito"] = direccion.split(", ")[-1].strip()
            else:
                r["distrito"] = "Lima"

        # Limpiar teléfono para WhatsApp
        telefono = r.get("telefono", "")
        r["telefono_limpio"] = "".join(c for c in telefono if c.isdigit() or c == "+")
        if not r["telefono_limpio"].startswith("+"):
            r["telefono_limpio"] = "+51" + r["telefono_limpio"]

        msg = generar_mensaje_whatsapp(r)
        lead = automation.registrar_lead(r, msg)
        print(f"  Lead #{lead['id']}: {r['nombre']} ({r['distrito']}) Score: {r['score']}")

    # 4. Preparar envios
    print("\n[4/5] Preparando envios WhatsApp...")
    envios_pendientes = []
    for lead in automation.leads[:5]:  # Top 5 para envio inmediato
        envio = automation.preparar_envio(lead["id"])
        envios_pendientes.append(envio)
        automation.registrar_envio(lead["id"])
        print(f"  Listo para enviar: {lead['restaurante']} -> {envio['telefono']}")

    # 5. Guardar envios para ejecutar
    print("\n[5/5] Guardando plan de envios...")
    with open("data/envios_pendientes.json", "w", encoding="utf-8") as f:
        json.dump(envios_pendientes, f, ensure_ascii=False, indent=2)

    # Dashboard final
    print("\n" + "=" * 60)
    print("  RESUMEN DEL CICLO")
    print("=" * 60)
    dashboard = automation.obtener_dashboard()
    print(f"  Leads registrados: {dashboard['total']}")
    print(f"  Enviados hoy: {dashboard['enviados_hoy']}")
    print(f"  Seguimientos pendientes: {dashboard['seguimientos_pendientes']}")

    print("\n  ARCHIVOS GENERADOS:")
    print("  - data/leads_activos.json (todos los leads)")
    print("  - data/mensajes_enviados.json (historial)")
    print("  - data/envios_pendientes.json (listos para enviar)")

    print("\n  SIGUIENTE PASO:")
    print("  Abrir data/envios_pendientes.json")
    print("  Hacer clic en cada link de WhatsApp")
    print("  Enviar mensaje manualmente (o automatizar con API)")

    return automation, envios_pendientes


def run_seguimientos():
    """
    Ejecuta los seguimientos pendientes para el dia.
    """
    print("=" * 60)
    print("  LIMA AUTOMA - Seguimientos del Dia")
    print("=" * 60)

    automation = WhatsAppAutomation()
    leads_seguimiento = automation.obtener_leads_para_seguimiento()

    if not leads_seguimiento:
        print("\n  No hay seguimientos pendientes para hoy.")
        return

    print(f"\n  {len(leads_seguimiento)} leads necesitan seguimiento:")
    print()

    seguimientos_listos = []
    for lead in leads_seguimiento:
        seg = automation.preparar_seguimiento(lead["id"])
        if seg:
            seguimientos_listos.append(seg)
            print(f"  Lead #{seg['lead_id']}: {seg['restaurante']}")
            print(f"    Seguimiento #{seg['numero_seguimiento']}")
            print(f"    Link: {seg['whatsapp_link'][:70]}...")
            print()

    # Guardar seguimientos
    with open("data/seguimientos_pendientes.json", "w", encoding="utf-8") as f:
        json.dump(seguimientos_listos, f, ensure_ascii=False, indent=2)

    print(f"  {len(seguimientos_listos)} seguimientos guardados en data/seguimientos_pendientes.json")


def run_dashboard():
    """
    Muestra el dashboard actual.
    """
    automation = WhatsAppAutomation()
    dashboard = automation.obtener_dashboard()

    print("=" * 60)
    print("  LIMA AUTOMA - Dashboard")
    print("=" * 60)
    print(f"\n  Total leads: {dashboard['total']}")
    print(f"  Enviados hoy: {dashboard['enviados_hoy']}")
    print(f"  Seguimientos pendientes: {dashboard['seguimientos_pendientes']}")

    print("\n  POR ESTADO:")
    for estado, count in dashboard["por_estado"].items():
        print(f"    {estado}: {count}")

    print("\n  POR CALIFICACION:")
    for cal, count in dashboard["por_calificacion"].items():
        print(f"    {cal}: {count}")


def run_cupones():
    """
    Genera cupones QR para todos los restaurantes.
    """
    print("=" * 60)
    print("  LIMA AUTOMA - Generador de Cupones QR")
    print("=" * 60)

    # Cargar leads (contienen todos los datos de restaurantes)
    with open("data/leads_activos.json", encoding="utf-8") as f:
        leads = json.load(f)

    restaurantes = []
    for lead in leads:
        restaurantes.append({
            "nombre": lead["restaurante"],
            "telefono": lead["telefono"],
            "direccion": lead.get("direccion", ""),
            "rating": lead.get("rating", 0),
            "reviews": lead.get("reviews", 0),
            "tipo": lead.get("tipo_cocina", ""),
        })

    print(f"\n  Restaurantes: {len(restaurantes)}")

    # Generar cupones
    cupones = []

    for restaurante in restaurantes:
        cupon = crear_cupon(restaurante, descuento_pct=15)
        cupones.append(cupon)

        print(f"\n  Restaurante: {cupon['restaurante']}")
        print(f"  Codigo rastreo: {cupon['codigo_rastreo']}")
        print(f"  Codigo cliente: {cupon['codigo_cliente']}")
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
    print("  REPORTE DE CUPONES")
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
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "ciclo":
            run_ciclo_completo()
        elif command == "seguimientos":
            run_seguimientos()
        elif command == "dashboard":
            run_dashboard()
        elif command == "cupones":
            run_cupones()
        elif command == "qr":
            from generar_qr import generar_todos_los_qr
            generar_todos_los_qr()
        elif command == "chatbot":
            from chatbot_leads import iniciar_chatbots_leads
            iniciar_chatbots_leads()
        elif command == "chatbot_estado":
            from chatbot_leads import ver_estado_chatbots
            ver_estado_chatbots()
        else:
            print("Comandos: ciclo, seguimientos, dashboard, cupones, qr, chatbot, chatbot_estado")
    else:
        run_ciclo_completo()
