"""
Lima Automa - Dashboard Web
============================
Panel de control para ver leads, chatbots y citas.
"""
import sys
sys.path.insert(0, 'src')

import json
from pathlib import Path
from datetime import datetime


def cargar_datos():
    """Carga todos los datos del sistema."""
    datos = {
        "leads": [],
        "conversaciones": {},
        "cupones": [],
        "envios": [],
    }

    # Cargar leads
    leads_file = Path("data/leads_activos.json")
    if leads_file.exists():
        with open(leads_file, "r", encoding="utf-8") as f:
            datos["leads"] = json.load(f)

    # Cargar conversaciones
    conv_file = Path("data/conversaciones.json")
    if conv_file.exists():
        with open(conv_file, "r", encoding="utf-8") as f:
            datos["conversaciones"] = json.load(f)

    # Cargar cupones
    cupones_file = Path("data/cupones.json")
    if cupones_file.exists():
        with open(cupones_file, "r", encoding="utf-8") as f:
            datos["cupones"] = json.load(f)

    # Cargar envíos
    envios_file = Path("data/envios_pendientes.json")
    if envios_file.exists():
        with open(envios_file, "r", encoding="utf-8") as f:
            datos["envios"] = json.load(f)

    return datos


def generar_dashboard_html(datos):
    """Genera el HTML del dashboard."""
    
    # Estadísticas
    total_leads = len(datos["leads"])
    leads_enviados = sum(1 for l in datos["leads"] if l.get("estado") == "ENVIADO")
    leads_pendientes = sum(1 for l in datos["leads"] if l.get("estado") == "PENDIENTE_ENVIO")
    total_conversaciones = len(datos["conversaciones"])
    total_cupones = len(datos["cupones"])
    total_envios = len(datos["envios"])

    # Leads por distrito
    distritos = {}
    for lead in datos["leads"]:
        distrito = lead.get("distrito", "Sin distrito")
        distritos[distrito] = distritos.get(distrito, 0) + 1

    # Leads por score
    scores = {"Alta (30+)": 0, "Media (15-29)": 0, "Baja (0-14)": 0}
    for lead in datos["leads"]:
        score = lead.get("score", 0)
        if score >= 30:
            scores["Alta (30+)"] += 1
        elif score >= 15:
            scores["Media (15-29)"] += 1
        else:
            scores["Baja (0-14)"] += 1

    # Citas agendadas
    citas = []
    for conv_id, conv in datos["conversaciones"].items():
        if conv.get("cita_agendada"):
            citas.append({
                "restaurante": conv.get("restaurante"),
                "fecha": conv["cita_agendada"].get("fecha"),
                "hora": conv["cita_agendada"].get("hora"),
                "estado": conv["cita_agendada"].get("estado"),
            })

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lima Automa - Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        .header h1 span {{
            color: #e94560;
        }}
        .header p {{
            opacity: 0.8;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            color: white;
        }}
        .stat-value {{
            font-size: 36px;
            font-weight: 700;
            color: #e94560;
        }}
        .stat-label {{
            font-size: 14px;
            opacity: 0.8;
            margin-top: 5px;
        }}
        .section {{
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .section-title {{
            color: white;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .badge {{
            background: #e94560;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 12px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            color: white;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        th {{
            font-weight: 600;
            opacity: 0.8;
        }}
        .status {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        .status.enviado {{ background: #25d366; }}
        .status.pendiente {{ background: #ffa500; }}
        .status.cita {{ background: #00a884; }}
        .charts {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .chart-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 20px;
            color: white;
        }}
        .chart-title {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 15px;
        }}
        .bar {{
            display: flex;
            align-items: center;
            margin: 10px 0;
        }}
        .bar-label {{
            width: 120px;
            font-size: 14px;
        }}
        .bar-container {{
            flex: 1;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
        }}
        .bar-fill {{
            height: 100%;
            background: #e94560;
            border-radius: 10px;
            transition: width 0.5s ease;
        }}
        .bar-value {{
            width: 50px;
            text-align: right;
            font-size: 14px;
        }}
        .footer {{
            text-align: center;
            color: rgba(255,255,255,0.5);
            margin-top: 30px;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Lima<span>Automa</span> Dashboard</h1>
            <p>Panel de control - {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{total_leads}</div>
                <div class="stat-label">Total Leads</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{leads_enviados}</div>
                <div class="stat-label">Mensajes Enviados</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{leads_pendientes}</div>
                <div class="stat-label">Pendientes</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{total_conversaciones}</div>
                <div class="stat-label">Conversaciones</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(citas)}</div>
                <div class="stat-label">Citas Agendadas</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{total_cupones}</div>
                <div class="stat-label">Cupones QR</div>
            </div>
        </div>

        <div class="charts">
            <div class="chart-card">
                <div class="chart-title">Leads por Distrito</div>"""

    # Agregar barras de distritos
    max_distrito = max(distritos.values()) if distritos else 1
    for distrito, count in sorted(distritos.items(), key=lambda x: x[1], reverse=True):
        width = (count / max_distrito) * 100
        html += f"""
                <div class="bar">
                    <div class="bar-label">{distrito}</div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: {width}%"></div>
                    </div>
                    <div class="bar-value">{count}</div>
                </div>"""

    html += """
            </div>
            <div class="chart-card">
                <div class="chart-title">Leads por Prioridad</div>"""

    # Agregar barras de scores
    max_score = max(scores.values()) if scores else 1
    for score_label, count in scores.items():
        width = (count / max_score) * 100
        html += f"""
                <div class="bar">
                    <div class="bar-label">{score_label}</div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: {width}%"></div>
                    </div>
                    <div class="bar-value">{count}</div>
                </div>"""

    html += """
            </div>
        </div>

        <div class="section">
            <div class="section-title">
                Últimos Leads
                <span class="badge">""" + str(total_leads) + """</span>
            </div>
            <table>
                <tr>
                    <th>Restaurante</th>
                    <th>Distrito</th>
                    <th>Score</th>
                    <th>Estado</th>
                </tr>"""

    # Agregar últimos 10 leads
    for lead in datos["leads"][-10:]:
        estado = lead.get("estado", "PENDIENTE")
        estado_class = "enviado" if estado == "ENVIADO" else "pendiente"
        html += f"""
                <tr>
                    <td>{lead.get('restaurante', 'N/A')}</td>
                    <td>{lead.get('distrito', 'N/A')}</td>
                    <td>{lead.get('score', 0)}</td>
                    <td><span class="status {estado_class}">{estado}</span></td>
                </tr>"""

    html += """
            </table>
        </div>

        <div class="section">
            <div class="section-title">
                Citas Agendadas
                <span class="badge">""" + str(len(citas)) + """</span>
            </div>
            <table>
                <tr>
                    <th>Restaurante</th>
                    <th>Fecha</th>
                    <th>Hora</th>
                    <th>Estado</th>
                </tr>"""

    # Agregar citas
    for cita in citas:
        html += f"""
                <tr>
                    <td>{cita.get('restaurante', 'N/A')}</td>
                    <td>{cita.get('fecha', 'N/A')}</td>
                    <td>{cita.get('hora', 'N/A')}</td>
                    <td><span class="status cita">{cita.get('estado', 'N/A')}</span></td>
                </tr>"""

    if not citas:
        html += """
                <tr>
                    <td colspan="4" style="text-align: center; opacity: 0.5;">No hay citas agendadas</td>
                </tr>"""

    html += """
            </table>
        </div>

        <div class="footer">
            Powered by Lima Automa &copy; 2026 | Dashboard v1.0
        </div>
    </div>
</body>
</html>"""

    return html


def main():
    print("=" * 60)
    print("  LIMA AUTOMA - Generador de Dashboard")
    print("=" * 60)

    # Cargar datos
    datos = cargar_datos()

    # Generar HTML
    html = generar_dashboard_html(datos)

    # Guardar archivo
    output_file = Path("dashboard.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n  Dashboard generado: {output_file}")
    print("  Abre el archivo en tu navegador para verlo.")


if __name__ == "__main__":
    main()
