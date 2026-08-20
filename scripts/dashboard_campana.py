"""
Lima Automa - Dashboard de Campaña
====================================
Genera un dashboard visual de las campañas.
"""
import json
from pathlib import Path


def cargar_campanas():
    """Carga las campañas simuladas."""
    campanas_file = Path("data/campanas_simuladas.json")
    if campanas_file.exists():
        with open(campanas_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def generar_dashboard_html(campanas):
    """Genera un dashboard HTML visual."""
    
    # Calcular estadísticas
    total = len(campanas)
    interes_alto = sum(1 for c in campanas if c["estado"] == "interes_alto")
    interes_medio = sum(1 for c in campanas if c["estado"] == "interes_medio")
    sin_respuesta = sum(1 for c in campanas if c["estado"] == "sin_respuesta")
    no_interesado = sum(1 for c in campanas if c["estado"] == "no_interesado")
    
    # Porcentajes
    pct_alto = (interes_alto / total * 100) if total > 0 else 0
    pct_medio = (interes_medio / total * 100) if total > 0 else 0
    pct_sin = (sin_respuesta / total * 100) if total > 0 else 0
    pct_no = (no_interesado / total * 100) if total > 0 else 0
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard de Campaña - Lima Automa</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: white; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1 {{ text-align: center; color: #00d4ff; margin: 20px 0; }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            border: 1px solid #00d4ff;
        }}
        
        .stat-card h3 {{ color: #00d4ff; margin-bottom: 10px; font-size: 14px; }}
        .stat-card .number {{ font-size: 36px; font-weight: bold; }}
        .stat-card .percentage {{ color: #888; margin-top: 5px; }}
        
        .high {{ color: #00ff88; }}
        .medium {{ color: #ffaa00; }}
        .none {{ color: #ff6b6b; }}
        .low {{ color: #ff4444; }}
        
        .chart-container {{
            background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
        }}
        
        .bar-chart {{
            display: flex;
            align-items: flex-end;
            justify-content: space-around;
            height: 200px;
            padding: 20px 0;
        }}
        
        .bar {{
            width: 60px;
            background: linear-gradient(180deg, #00d4ff 0%, #0066cc 100%);
            border-radius: 5px 5px 0 0;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
            transition: all 0.3s;
        }}
        
        .bar:hover {{ transform: scale(1.05); }}
        .bar-label {{ margin-top: 10px; text-align: center; }}
        .bar-value {{ color: #00d4ff; font-weight: bold; }}
        
        .leads-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
        }}
        
        .leads-table th, .leads-table td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #333;
        }}
        
        .leads-table th {{
            background: #16213e;
            color: #00d4ff;
        }}
        
        .leads-table tr:hover {{ background: #16213e; }}
        
        .status-badge {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .badge-alto {{ background: #00ff88; color: #000; }}
        .badge-medio {{ background: #ffaa00; color: #000; }}
        .badge-sin {{ background: #666; color: #fff; }}
        .badge-no {{ background: #ff4444; color: #fff; }}
        
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Dashboard de Campaña - Lima Automa</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>TOTAL CONTACTADOS</h3>
                <div class="number">{total}</div>
            </div>
            <div class="stat-card">
                <h3>INTERÉS ALTO</h3>
                <div class="number high">{interes_alto}</div>
                <div class="percentage">{pct_alto:.1f}%</div>
            </div>
            <div class="stat-card">
                <h3>INTERÉS MEDIO</h3>
                <div class="number medium">{interes_medio}</div>
                <div class="percentage">{pct_medio:.1f}%</div>
            </div>
            <div class="stat-card">
                <h3>SIN RESPUESTA</h3>
                <div class="number none">{sin_respuesta}</div>
                <div class="percentage">{pct_sin:.1f}%</div>
            </div>
            <div class="stat-card">
                <h3>NO INTERESADOS</h3>
                <div class="number low">{no_interesado}</div>
                <div class="percentage">{pct_no:.1f}%</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h2 style="color: #00d4ff; margin-bottom: 20px;">Distribución de Respuestas</h2>
            <div class="bar-chart">
                <div class="bar" style="height: {pct_alto * 2}px;">
                    <span class="bar-value">{interes_alto}</span>
                </div>
                <div class="bar" style="height: {pct_medio * 2}px;">
                    <span class="bar-value">{interes_medio}</span>
                </div>
                <div class="bar" style="height: {pct_sin * 2}px;">
                    <span class="bar-value">{sin_respuesta}</span>
                </div>
                <div class="bar" style="height: {pct_no * 2}px;">
                    <span class="bar-value">{no_interesado}</span>
                </div>
            </div>
            <div class="bar-chart" style="height: 40px;">
                <div class="bar-label">Interés Alto</div>
                <div class="bar-label">Interés Medio</div>
                <div class="bar-label">Sin Respuesta</div>
                <div class="bar-label">No Interesados</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h2 style="color: #00d4ff; margin-bottom: 20px;">Detalle por Restaurante</h2>
            <table class="leads-table">
                <thead>
                    <tr>
                        <th>Restaurante</th>
                        <th>Distrito</th>
                        <th>Estado</th>
                        <th>Respuesta</th>
                        <th>Acción</th>
                    </tr>
                </thead>
                <tbody>"""
    
    for campana in campanas:
        estado = campana["estado"]
        if estado == "interes_alto":
            badge_class = "badge-alto"
            badge_text = "Interés Alto"
        elif estado == "interes_medio":
            badge_class = "badge-medio"
            badge_text = "Interés Medio"
        elif estado == "sin_respuesta":
            badge_class = "badge-sin"
            badge_text = "Sin Respuesta"
        else:
            badge_class = "badge-no"
            badge_text = "No Interesado"
        
        respuesta = campana["respuesta"]["mensaje"] or "-"
        accion = campana["respuesta"]["accion"].replace("_", " ").title()
        
        html += f"""
                    <tr>
                        <td>{campana['restaurante']}</td>
                        <td>{campana['distrito']}</td>
                        <td><span class="status-badge {badge_class}">{badge_text}</span></td>
                        <td>{respuesta}</td>
                        <td>{accion}</td>
                    </tr>"""
    
    html += f"""
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Lima Automa - Simulador de Campaña</p>
            <p>Modo DEMO - No se contactaron restaurantes reales</p>
        </div>
    </div>
</body>
</html>"""
    
    return html


def main():
    """Función principal."""
    print("=" * 60)
    print("  LIMA AUTOMA - Dashboard de Campaña")
    print("=" * 60)
    
    # Cargar campañas
    campanas = cargar_campanas()
    
    if not campanas:
        print("\n  No hay campañas para mostrar.")
        print("  Ejecuta primero: python scripts/simular_campaña.py")
        return
    
    print(f"\n  Campañas cargadas: {len(campanas)}")
    
    # Generar HTML
    print("\n  Generando dashboard...")
    html = generar_dashboard_html(campanas)
    
    # Guardar archivo
    output_file = Path("dashboard_campana.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\n  Dashboard generado: {output_file}")
    print("\n  ¡Listo! Abre el archivo en tu navegador.")


if __name__ == "__main__":
    main()
