"""
Lima Automa - Dashboard de Transacciones
==========================================
Panel de control financiero con ventas, comisiones y pagos.
"""
import sys
sys.path.insert(0, 'src')

import json
from pathlib import Path
from datetime import datetime


def cargar_transacciones():
    """Carga todas las transacciones del sistema."""
    transacciones_file = Path("data/transacciones.json")
    if transacciones_file.exists():
        with open(transacciones_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def calcular_estadisticas(transacciones):
    """Calcula estadísticas financieras."""
    stats = {
        "total_transacciones": 0,
        "total_ingresos": 0,
        "total_comisiones": 0,
        "total_pagado_restaurantes": 0,
        "ganancia_neta": 0,
        "por_servicio": {},
        "por_metodo_pago": {},
        "por_restaurante": {},
        "por_dia": {},
        "ticket_promedio": 0,
    }

    for txn in transacciones:
        if txn.get("estado") != "COMPLETADO":
            continue

        stats["total_transacciones"] += 1
        monto = txn.get("monto_cliente", 0)
        comision = txn.get("comision_monto", 0)
        pagado = txn.get("monto_restaurante", 0)
        servicio = txn.get("servicio", "otro")
        metodo = txn.get("metodo_pago", "otro")
        restaurante = txn.get("restaurante", "otro")
        fecha = txn.get("fecha", "sin_fecha")

        stats["total_ingresos"] += monto
        stats["total_comisiones"] += comision
        stats["total_pagado_restaurantes"] += pagado

        # Por servicio
        if servicio not in stats["por_servicio"]:
            stats["por_servicio"][servicio] = {"cantidad": 0, "monto": 0, "comision": 0}
        stats["por_servicio"][servicio]["cantidad"] += 1
        stats["por_servicio"][servicio]["monto"] += monto
        stats["por_servicio"][servicio]["comision"] += comision

        # Por método de pago
        if metodo not in stats["por_metodo_pago"]:
            stats["por_metodo_pago"][metodo] = {"cantidad": 0, "monto": 0}
        stats["por_metodo_pago"][metodo]["cantidad"] += 1
        stats["por_metodo_pago"][metodo]["monto"] += monto

        # Por restaurante
        if restaurante not in stats["por_restaurante"]:
            stats["por_restaurante"][restaurante] = {"cantidad": 0, "monto": 0, "comision": 0}
        stats["por_restaurante"][restaurante]["cantidad"] += 1
        stats["por_restaurante"][restaurante]["monto"] += monto
        stats["por_restaurante"][restaurante]["comision"] += comision

        # Por día
        if fecha not in stats["por_dia"]:
            stats["por_dia"][fecha] = {"cantidad": 0, "monto": 0}
        stats["por_dia"][fecha]["cantidad"] += 1
        stats["por_dia"][fecha]["monto"] += monto

    # Ticket promedio
    if stats["total_transacciones"] > 0:
        stats["ticket_promedio"] = stats["total_ingresos"] / stats["total_transacciones"]

    # Ganancia neta
    stats["ganancia_neta"] = stats["total_comisiones"]

    return stats


def generar_dashboard_html(transacciones, stats):
    """Genera el HTML del dashboard de transacciones."""

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lima Automa - Dashboard de Transacciones</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 36px;
            margin-bottom: 10px;
        }}
        .header h1 span {{ color: #00d9ff; }}
        .header p {{ opacity: 0.7; font-size: 14px; }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            color: white;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s;
        }}
        .stat-card:hover {{ transform: translateY(-5px); }}
        .stat-icon {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: 700;
            color: #00d9ff;
        }}
        .stat-label {{
            font-size: 13px;
            opacity: 0.7;
            margin-top: 5px;
        }}
        .stat-card.success .stat-value {{ color: #00e676; }}
        .stat-card.warning .stat-value {{ color: #ffab00; }}
        .stat-card.danger .stat-value {{ color: #ff5252; }}
        
        .section {{
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            border: 1px solid rgba(255,255,255,0.08);
        }}
        .section-title {{
            color: white;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .badge {{
            background: #00d9ff;
            color: #0f0c29;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 24px;
            margin-bottom: 24px;
        }}
        .chart-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 24px;
            color: white;
            border: 1px solid rgba(255,255,255,0.08);
        }}
        .chart-title {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #00d9ff;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            color: white;
        }}
        th, td {{
            padding: 14px 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }}
        th {{
            font-weight: 600;
            opacity: 0.7;
            font-size: 13px;
            text-transform: uppercase;
        }}
        td {{ font-size: 14px; }}
        tr:hover {{ background: rgba(255,255,255,0.03); }}
        
        .status {{
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        .status.completado {{ background: rgba(0,230,118,0.2); color: #00e676; }}
        .status.pendiente {{ background: rgba(255,171,0,0.2); color: #ffab00; }}
        .status.cancelado {{ background: rgba(255,82,82,0.2); color: #ff5252; }}
        
        .service-badge {{
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 600;
        }}
        .service-badge.traemos {{ background: rgba(0,217,255,0.2); color: #00d9ff; }}
        .service-badge.automatizacion {{ background: rgba(156,39,176,0.2); color: #ce93d8; }}
        .service-badge.agente {{ background: rgba(255,171,0,0.2); color: #ffab00; }}
        
        .bar {{
            display: flex;
            align-items: center;
            margin: 12px 0;
        }}
        .bar-label {{
            width: 140px;
            font-size: 13px;
            color: white;
        }}
        .bar-container {{
            flex: 1;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            height: 24px;
            overflow: hidden;
        }}
        .bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #00d9ff, #00e676);
            border-radius: 10px;
            transition: width 0.5s ease;
        }}
        .bar-fill.comision {{ background: linear-gradient(90deg, #ffab00, #ff6d00); }}
        .bar-value {{
            width: 80px;
            text-align: right;
            font-size: 14px;
            color: white;
            font-weight: 600;
        }}
        
        .footer {{
            text-align: center;
            color: rgba(255,255,255,0.4);
            margin-top: 40px;
            font-size: 12px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Lima<span>Automa</span> Finanzas</h1>
            <p>Dashboard de Transacciones | {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-value">S/ {stats['total_ingresos']:,.2f}</div>
                <div class="stat-label">Ingresos Totales</div>
            </div>
            <div class="stat-card success">
                <div class="stat-icon">📈</div>
                <div class="stat-value">S/ {stats['total_comisiones']:,.2f}</div>
                <div class="stat-label">Comisiones Ganadas</div>
            </div>
            <div class="stat-card warning">
                <div class="stat-icon">🏪</div>
                <div class="stat-value">S/ {stats['total_pagado_restaurantes']:,.2f}</div>
                <div class="stat-label">Pagado a Restaurantes</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-value">{stats['total_transacciones']}</div>
                <div class="stat-label">Total Transacciones</div>
            </div>
            <div class="stat-card success">
                <div class="stat-icon">💵</div>
                <div class="stat-value">S/ {stats['ticket_promedio']:,.2f}</div>
                <div class="stat-label">Ticket Promedio</div>
            </div>
            <div class="stat-card danger">
                <div class="stat-icon">🎯</div>
                <div class="stat-value">S/ {stats['ganancia_neta']:,.2f}</div>
                <div class="stat-label">Ganancia Neta</div>
            </div>
        </div>

        <div class="charts-grid">
            <div class="chart-card">
                <div class="chart-title">Ingresos por Servicio</div>"""

    # Gráfico por servicio
    max_servicio = max((s["monto"] for s in stats["por_servicio"].values()), default=1)
    servicio_labels = {
        "traemos_clientes": "Traemos Clientes",
        "automatizacion": "Automatización",
        "agente_propio": "Agente Propio",
        "automatizacion_setup": "Auto. Setup",
        "automatizacion_mensual": "Auto. Mensual",
        "agente_propio_setup": "Agente Setup",
        "agente_propio_mensual": "Agente Mensual",
    }
    for servicio, data in stats["por_servicio"].items():
        width = (data["monto"] / max_servicio) * 100 if max_servicio > 0 else 0
        label = servicio_labels.get(servicio, servicio)
        html += f"""
                <div class="bar">
                    <div class="bar-label">{label}</div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: {width}%"></div>
                    </div>
                    <div class="bar-value">S/ {data['monto']:,.2f}</div>
                </div>"""

    html += """
            </div>
            <div class="chart-card">
                <div class="chart-title">Comisiones por Restaurante</div>"""

    # Gráfico de comisiones por restaurante
    max_restaurante = max((r["comision"] for r in stats["por_restaurante"].values()), default=1)
    for restaurante, data in sorted(stats["por_restaurante"].items(), key=lambda x: x[1]["comision"], reverse=True):
        width = (data["comision"] / max_restaurante) * 100 if max_restaurante > 0 else 0
        html += f"""
                <div class="bar">
                    <div class="bar-label">{restaurante[:20]}</div>
                    <div class="bar-container">
                        <div class="bar-fill comision" style="width: {width}%"></div>
                    </div>
                    <div class="bar-value">S/ {data['comision']:,.2f}</div>
                </div>"""

    html += """
            </div>
        </div>

        <div class="charts-grid">
            <div class="chart-card">
                <div class="chart-title">Métodos de Pago</div>
                <table>
                    <tr>
                        <th>Método</th>
                        <th>Cantidad</th>
                        <th>Monto</th>
                    </tr>"""

    for metodo, data in stats["por_metodo_pago"].items():
        html += f"""
                    <tr>
                        <td>{metodo}</td>
                        <td>{data['cantidad']}</td>
                        <td>S/ {data['monto']:,.2f}</td>
                    </tr>"""

    html += """
                </table>
            </div>
            <div class="chart-card">
                <div class="chart-title">Ventas por Día</div>
                <table>
                    <tr>
                        <th>Fecha</th>
                        <th>Pedidos</th>
                        <th>Monto</th>
                    </tr>"""

    for fecha, data in sorted(stats["por_dia"].items(), reverse=True):
        html += f"""
                    <tr>
                        <td>{fecha}</td>
                        <td>{data['cantidad']}</td>
                        <td>S/ {data['monto']:,.2f}</td>
                    </tr>"""

    html += """
                </table>
            </div>
        </div>

        <div class="section">
            <div class="section-title">
                Últimas Transacciones
                <span class="badge">""" + str(stats['total_transacciones']) + """</span>
            </div>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Fecha</th>
                    <th>Restaurante</th>
                    <th>Cliente</th>
                    <th>Pedido</th>
                    <th>Monto</th>
                    <th>Comisión</th>
                    <th>Restaurante</th>
                    <th>Pago</th>
                    <th>Estado</th>
                </tr>"""

    # Últimas 15 transacciones
    for txn in transacciones[-15:]:
        servicio = txn.get("servicio", "")
        servicio_class = "traemos" if "traemos" in servicio else "automatizacion" if "automatizacion" in servicio else "agente"
        estado = txn.get("estado", "PENDIENTE")
        estado_class = "completado" if estado == "COMPLETADO" else "pendiente" if estado == "PENDIENTE" else "cancelado"

        html += f"""
                <tr>
                    <td>{txn.get('id', 'N/A')}</td>
                    <td>{txn.get('fecha', 'N/A')}</td>
                    <td>{txn.get('restaurante', 'N/A')}</td>
                    <td>{txn.get('cliente', 'N/A') or 'N/A'}</td>
                    <td>{str(txn.get('pedido', 'N/A'))[:30]}</td>
                    <td>S/ {txn.get('monto_cliente', 0):,.2f}</td>
                    <td>S/ {txn.get('comision_monto', 0):,.2f}</td>
                    <td>S/ {txn.get('monto_restaurante', 0):,.2f}</td>
                    <td><span class="service-badge {servicio_class}">{txn.get('metodo_pago', 'N/A')}</span></td>
                    <td><span class="status {estado_class}">{estado}</span></td>
                </tr>"""

    html += f"""
            </table>
        </div>

        <div class="footer">
            Powered by Lima Automa &copy; 2026 | Dashboard de Transacciones v1.0
        </div>
    </div>
</body>
</html>"""

    return html


def main():
    print("=" * 60)
    print("  LIMA AUTOMA - Dashboard de Transacciones")
    print("=" * 60)

    # Cargar transacciones
    transacciones = cargar_transacciones()
    print(f"\n  Transacciones cargadas: {len(transacciones)}")

    # Calcular estadísticas
    stats = calcular_estadisticas(transacciones)

    # Generar HTML
    html = generar_dashboard_html(transacciones, stats)

    # Guardar archivo
    output_file = Path("dashboard_finanzas.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n  Dashboard generado: {output_file}")
    print("  Abre el archivo en tu navegador para verlo.")

    # Resumen
    print("\n" + "=" * 60)
    print("  RESUMEN FINANCIERO")
    print("=" * 60)
    print(f"  Ingresos totales:     S/ {stats['total_ingresos']:,.2f}")
    print(f"  Comisiones ganadas:   S/ {stats['total_comisiones']:,.2f}")
    print(f"  Pagado a restaurantes: S/ {stats['total_pagado_restaurantes']:,.2f}")
    print(f"  Ticket promedio:      S/ {stats['ticket_promedio']:,.2f}")
    print(f"  Transacciones:        {stats['total_transacciones']}")


if __name__ == "__main__":
    main()
