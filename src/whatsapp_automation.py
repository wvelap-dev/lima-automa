"""
Lima Automa - Motor de Automatizacion WhatsApp
================================================
Envia mensajes, califica respuestas y programa seguimiento.
"""
import json
import time
import random
from datetime import datetime, timedelta
from pathlib import Path


class WhatsAppAutomation:
    """
    Motor principal de automatizacion para WhatsApp.
    """

    def __init__(self):
        self.leads_file = Path("data/leads_activos.json")
        self.sent_file = Path("data/mensajes_enviados.json")
        self.leads = self._load_leads()
        self.sent = self._load_sent()

    def _load_leads(self):
        if self.leads_file.exists():
            with open(self.leads_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _load_sent(self):
        if self.sent_file.exists():
            with open(self.sent_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save_leads(self):
        with open(self.leads_file, "w", encoding="utf-8") as f:
            json.dump(self.leads, f, ensure_ascii=False, indent=2)

    def _save_sent(self):
        with open(self.sent_file, "w", encoding="utf-8") as f:
            json.dump(self.sent, f, ensure_ascii=False, indent=2)

    def registrar_lead(self, restaurante, mensaje_inicial):
        """
        Registra un nuevo lead para hacer seguimiento.
        """
        lead = {
            "id": len(self.leads) + 1,
            "restaurante": restaurante["nombre"],
            "telefono": restaurante.get("telefono", ""),
            "distrito": restaurante.get("distrito", ""),
            "score": restaurante.get("score", 0),
            "estado": "PENDIENTE_ENVIO",
            "mensaje_inicial": mensaje_inicial,
            "fecha_registro": datetime.now().isoformat(),
            "fecha_ultimo_seguimiento": None,
            "seguimientos_enviados": 0,
            "respuestas": [],
            "calificacion": None,
            "notas": "",
        }
        self.leads.append(lead)
        self._save_leads()
        return lead

    def preparar_envio(self, lead_id):
        """
        Prepara un lead para enviar el mensaje inicial.
        Retorna el mensaje formateado listo para WhatsApp.
        """
        lead = self._find_lead(lead_id)
        if not lead:
            return None

        # Formatear numero de telefono para WhatsApp
        telefono = lead["telefono"]
        telefono_limpio = "".join(c for c in telefono if c.isdigit() or c == "+")
        if not telefono_limpio.startswith("+"):
            telefono_limpio = "+51" + telefono_limpio
        
        # Asegurar que empiece con 51 (código de Perú)
        if telefono_limpio.startswith("+51 ") or telefono_limpio.startswith("+511"):
            telefono_limpio = "+51" + telefono_limpio.replace("+51 ", "").replace("+511", "1")

        # Crear link de WhatsApp (sin espacios ni caracteres especiales)
        mensaje_encoded = lead["mensaje_inicial"].replace(" ", "%20").replace("\n", "%0A")
        whatsapp_link = f"https://wa.me/{telefono_limpio.lstrip('+')}?text={mensaje_encoded}"

        return {
            "lead_id": lead_id,
            "restaurante": lead["restaurante"],
            "telefono": telefono_limpio,
            "whatsapp_link": whatsapp_link,
            "mensaje": lead["mensaje_inicial"],
        }

    def registrar_envio(self, lead_id):
        """
        Marca un lead como enviado.
        """
        lead = self._find_lead(lead_id)
        if lead:
            lead["estado"] = "ENVIADO"
            lead["fecha_envio"] = datetime.now().isoformat()
            lead["fecha_ultimo_seguimiento"] = datetime.now().isoformat()

            self.sent.append({
                "lead_id": lead_id,
                "restaurante": lead["restaurante"],
                "tipo": "INICIAL",
                "fecha": datetime.now().isoformat(),
            })
            self._save_leads()
            self._save_sent()
        return lead

    def registrar_respuesta(self, lead_id, respuesta_texto):
        """
        Registra la respuesta de un restaurante y la califica.
        """
        lead = self._find_lead(lead_id)
        if not lead:
            return None

        calificacion = self._calificar_respuesta(respuesta_texto)

        respuesta = {
            "texto": respuesta_texto,
            "fecha": datetime.now().isoformat(),
            "calificacion": calificacion["tipo"],
        }
        lead["respuestas"].append(respuesta)
        lead["calificacion"] = calificacion["tipo"]
        lead["notas"] = calificacion["razon"]

        # Actualizar estado segun calificacion
        if calificacion["tipo"] == "CALIENTE":
            lead["estado"] = "LISTO_PARA_LLAMADA"
        elif calificacion["tipo"] == "TIBIO":
            lead["estado"] = "SEGUIR_NUTRIENDO"
        elif calificacion["tipo"] == "FRIO":
            lead["estado"] = "SEGUIR_EN_30_DIAS"
        elif calificacion["tipo"] == "NO_INTERESA":
            lead["estado"] = "CERRADO"

        self._save_leads()
        return {"lead": lead, "calificacion": calificacion}

    def _calificar_respuesta(self, texto):
        """
        Clasifica una respuesta del restaurante.
        """
        texto_lower = texto.lower()

        # Palabras clave para cada categoria
        calientes = [
            "si", "claro", "cuando", "como", "quiero", "me interesa",
            "envieme", "mandame", "dame info", "cuanto cuesta",
            "videollamada", "reunion", "hablamos", "dale", "ok",
            "perfecto", "genial", "excelente", "estoy interesado",
        ]

        tibios = [
            "despues", "luego", "piensalo", "no se", "tal vez",
            "quizas", "mandame info", "que mas", "cuéntame",
            "interesante", "voy a ver", "no ahora",
        ]

        frios = [
            "no gracias", "no me interesa", "ya tengo", "no necesito",
            "no puedo", "estoy ocupado", "no es momento",
            "no tengo tiempo", "no",
        ]

        # Verificar calientes primero
        for palabra in calientes:
            if palabra in texto_lower:
                return {
                    "tipo": "CALIENTE",
                    "score": 90,
                    "razon": f"Respuesta positiva detectada: '{palabra}'",
                    "accion": "Agendar videollamada inmediatamente",
                }

        # Verificar tibios
        for palabra in tibios:
            if palabra in texto_lower:
                return {
                    "tipo": "TIBIO",
                    "score": 50,
                    "razon": f"Interes moderado detectado: '{palabra}'",
                    "accion": "Enviar caso de éxito y reintentar en 3 días",
                }

        # Verificar frios
        for palabra in frios:
            if palabra in texto_lower:
                return {
                    "tipo": "FRIO",
                    "score": 20,
                    "razon": f"Rechazo detectado: '{palabra}'",
                    "accion": "Seguimiento suave en 30 días",
                }

        # Sin palabra clave clara → revisar manualmente
        return {
            "tipo": "INDEFINIDO",
            "score": 40,
            "razon": "Respuesta no clara, requiere revisión manual",
            "accion": "Revisar y responder manualmente",
        }

    def preparar_seguimiento(self, lead_id):
        """
        Prepara el siguiente mensaje de seguimiento para un lead.
        """
        lead = self._find_lead(lead_id)
        if not lead:
            return None

        seguimientos = lead.get("seguimientos_enviados", 0)
        nombre = lead["restaurante"]

        mensajes_seguimiento = {
            1: f"Hola, {nombre}. Solo queria saber si vio mi mensaje anterior sobre como conseguir mas clientes. Estoy aqui para ayudarlos.",
            2: f"Hola {nombre}, le envie un ejemplo de como otro restaurante similar aumento sus ventas 30%. Se lo mando?",
            3: f"Ultimo mensaje, {nombre}. No quiero molestar. Si cambian de opinion, aqui estoy. Exitos.",
        }

        if seguimientos >= 3:
            return None

        mensaje = mensajes_seguimiento.get(seguimientos + 1, "")
        telefono = lead["telefono"]
        telefono_limpio = "".join(c for c in telefono if c.isdigit() or c == "+")
        if not telefono_limpio.startswith("+"):
            telefono_limpio = "+51" + telefono_limpio

        mensaje_encoded = mensaje.replace(" ", "%20").replace("\n", "%0A")
        whatsapp_link = f"https://wa.me/{telefono_limpio.lstrip('+')}?text={mensaje_encoded}"

        return {
            "lead_id": lead_id,
            "restaurante": nombre,
            "telefono": telefono_limpio,
            "whatsapp_link": whatsapp_link,
            "mensaje": mensaje,
            "numero_seguimiento": seguimientos + 1,
        }

    def registrar_seguimiento(self, lead_id):
        """
        Marca un seguimiento como enviado.
        """
        lead = self._find_lead(lead_id)
        if lead:
            lead["seguimientos_enviados"] = lead.get("seguimientos_enviados", 0) + 1
            lead["fecha_ultimo_seguimiento"] = datetime.now().isoformat()

            self.sent.append({
                "lead_id": lead_id,
                "restaurante": lead["restaurante"],
                "tipo": f"SEGUIEMIENTO_{lead['seguimientos_enviados']}",
                "fecha": datetime.now().isoformat(),
            })
            self._save_leads()
            self._save_sent()
        return lead

    def obtener_leads_para_seguimiento(self):
        """
        Retorna leads que necesitan seguimiento hoy.
        """
        hoy = datetime.now()
        leads_para_seguimiento = []

        for lead in self.leads:
            if lead["estado"] in ["ENVIADO", "SEGUIR_NUTRIENDO"]:
                if lead["seguimientos_enviados"] >= 3:
                    continue

                fecha_ultimo = lead.get("fecha_ultimo_seguimiento")
                if fecha_ultimo:
                    fecha_ultimo_dt = datetime.fromisoformat(fecha_ultimo)
                    dias_desde = (hoy - fecha_ultimo_dt).days

                    # Seguimiento cada 2-3 dias
                    if dias_desde >= 2:
                        leads_para_seguimiento.append(lead)

        return leads_para_seguimiento

    def obtener_dashboard(self):
        """
        Retorna resumen del estado de todos los leads.
        """
        hoy = datetime.now()
        dashboard = {
            "total": len(self.leads),
            "por_estado": {},
            "por_calificacion": {},
            "enviados_hoy": 0,
            "seguimientos_pendientes": len(self.obtener_leads_para_seguimiento()),
        }

        for lead in self.leads:
            estado = lead.get("estado", "DESCONOCIDO")
            calificacion = lead.get("calificacion", "SIN_CALIFICAR")

            dashboard["por_estado"][estado] = dashboard["por_estado"].get(estado, 0) + 1
            dashboard["por_calificacion"][calificacion] = dashboard["por_calificacion"].get(calificacion, 0) + 1

            # Contar envios de hoy
            fecha_envio = lead.get("fecha_envio")
            if fecha_envio:
                fecha_envio_dt = datetime.fromisoformat(fecha_envio)
                if fecha_envio_dt.date() == hoy.date():
                    dashboard["enviados_hoy"] += 1

        return dashboard

    def _find_lead(self, lead_id):
        for lead in self.leads:
            if lead["id"] == lead_id:
                return lead
        return None


# === TESTING ===
if __name__ == "__main__":
    from scraper_restaurantes import buscar_restaurantes, calcular_score_prioridad
    from message_generator import generar_mensaje_whatsapp

    automation = WhatsAppAutomation()

    # Buscar y preparar primeros 3 restaurantes
    restaurants = buscar_restaurantes("Miraflores")[:3]

    print("=" * 60)
    print("  LIMA AUTOMA - Sistema de Automatizacion WhatsApp")
    print("=" * 60)

    for r in restaurants:
        calcular_score_prioridad(r)
        msg = generar_mensaje_whatsapp(r)

        # Registrar lead
        lead = automation.registrar_lead(r, msg)
        print(f"\nLead #{lead['id']}: {r['nombre']}")

        # Preparar envio
        envio = automation.preparar_envio(lead["id"])
        print(f"  Telefono: {envio['telefono']}")
        print(f"  Link WhatsApp: {envio['whatsapp_link'][:80]}...")

        # Simular envio
        automation.registrar_envio(lead["id"])
        print(f"  Estado: ENVIADO")

    # Simular respuestas
    print("\n" + "=" * 60)
    print("  SIMULANDO RESPUESTAS")
    print("=" * 60)

    respuestas_test = [
        (1, "Si, me interesa. Cuandos podemos hablar?"),
        (2, "Despues le escribo"),
        (3, "No gracias, ya tenemos ayuda"),
    ]

    for lead_id, respuesta in respuestas_test:
        result = automation.registrar_respuesta(lead_id, respuesta)
        if result:
            cal = result["calificacion"]
            print(f"\nLead #{lead_id}: '{respuesta}'")
            print(f"  Calificacion: {cal['tipo']} (Score: {cal['score']})")
            print(f"  Razon: {cal['razon']}")
            print(f"  Accion: {cal['accion']}")

    # Dashboard
    print("\n" + "=" * 60)
    print("  DASHBOARD")
    print("=" * 60)
    dashboard = automation.obtener_dashboard()
    print(f"  Total leads: {dashboard['total']}")
    print(f"  Enviados hoy: {dashboard['enviados_hoy']}")
    print(f"  Seguimientos pendientes: {dashboard['seguimientos_pendientes']}")
    print(f"  Por estado: {dashboard['por_estado']}")
    print(f"  Por calificacion: {dashboard['por_calificacion']}")
