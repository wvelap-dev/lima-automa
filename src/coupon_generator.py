"""
Lima Automa - Generador de Cupones QR (v2)
==========================================
Crea cupones unicos con QR, tracking y nuevo modelo de negocio.
"""
import json
import hashlib
import random
import string
import base64
from datetime import datetime
from pathlib import Path


def generar_codigo_unico(restaurante_nombre, longitud=8):
    """
    Genera un codigo unico para cada restaurante.
    Ejemplo: CAFE2024, LPAN3K4X, VICT8M2R
    """
    nombre_limpio = "".join(c for c in restaurante_nombre if c.isalnum())[:4].upper()
    caracteres = string.ascii_uppercase + string.digits
    sufijo = "".join(random.choice(caracteres) for _ in range(longitud - 4))
    return f"{nombre_limpio}{sufijo}"


def generar_codigo_cliente(restaurante_nombre):
    """
    Genera un codigo unico por cliente para rastreo.
    Ejemplo: CAFE-2026-8A3F
    """
    nombre_limpio = "".join(c for c in restaurante_nombre if c.isalnum())[:4].upper()
    anho = datetime.now().year
    hash_id = hashlib.md5(f"{restaurante_nombre}{datetime.now().isoformat()}".encode()).hexdigest()[:4].upper()
    return f"{nombre_limpio}-{anho}-{hash_id}"


def crear_cupon(restaurante, descuento_pct=15):
    """
    Crea un cupon completo con QR, codigo y landing page.
    """
    nombre = restaurante.get("nombre", "Restaurante")
    telefono = restaurante.get("telefono", "")

    # Generar codigos
    codigo_rastreo = generar_codigo_unico(nombre)
    codigo_cliente = generar_codigo_cliente(nombre)

    # URL de la landing page (donde cae el cliente al escanear QR)
    landing_url = f"https://lima-aa91.vercel.app/cupon/{codigo_rastreo}"

    cupon = {
        "restaurante": nombre,
        "telefono": telefono,
        "codigo_rastreo": codigo_rastreo,
        "codigo_cliente": codigo_cliente,
        "descuento_pct": descuento_pct,
        "landing_url": landing_url,
        "fecha_creacion": datetime.now().isoformat(),
        "activo": True,
        "usos": 0,
        "clientes_atribuidos": [],
        "balance": 0.0,  # Cuanto le debemos al restaurante
    }

    return cupon


def generar_qr_svg(url, size=200):
    """
    Genera un QR como SVG inline (sin dependencias externas).
    Usa un servicio publico de generacion de QR.
    """
    # Usar API publica de QR Server
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&data={url}&format=svg"
    return f'<img src="{qr_url}" alt="QR Code" width="{size}" height="{size}" />'


def crear_landing_page_html(cupon):
    """
    Genera el HTML de la landing page con tracking y nuevo modelo de negocio.
    """
    restaurante = cupon["restaurante"]
    descuento = cupon["descuento_pct"]
    codigo = cupon["codigo_cliente"]
    codigo_rastreo = cupon["codigo_rastreo"]
    landing_url = cupon["landing_url"]

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oferta Exclusiva - {restaurante}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .coupon {{
            background: white;
            border-radius: 24px;
            padding: 0;
            max-width: 420px;
            text-align: center;
            box-shadow: 0 25px 80px rgba(0,0,0,0.4);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
            padding: 30px 20px;
            color: white;
        }}
        .logo-placeholder {{
            width: 80px;
            height: 80px;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            margin: 0 auto 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            font-weight: bold;
        }}
        .restaurant-name {{
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        .restaurant-subtitle {{
            font-size: 12px;
            opacity: 0.9;
        }}
        .discount-section {{
            padding: 30px 20px;
            background: #f8f9fa;
        }}
        .discount-label {{
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .discount-value {{
            font-size: 80px;
            font-weight: 700;
            color: #e94560;
            line-height: 1;
            margin: 10px 0;
        }}
        .discount-suffix {{
            font-size: 24px;
            color: #e94560;
            font-weight: 600;
        }}
        .code-section {{
            padding: 20px;
        }}
        .code-label {{
            font-size: 12px;
            color: #999;
            margin-bottom: 8px;
        }}
        .code-value {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #00d9ff;
            padding: 15px 25px;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 3px;
            font-family: monospace;
        }}
        .instructions {{
            padding: 20px;
            background: white;
        }}
        .step {{
            display: flex;
            align-items: center;
            text-align: left;
            margin: 12px 0;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        .step-number {{
            width: 28px;
            height: 28px;
            background: #e94560;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: bold;
            margin-right: 12px;
            flex-shrink: 0;
        }}
        .step-text {{
            font-size: 13px;
            color: #333;
            line-height: 1.4;
        }}
        .footer {{
            padding: 15px;
            background: #f8f9fa;
            border-top: 1px solid #eee;
        }}
        .validity {{
            font-size: 11px;
            color: #999;
        }}
        .powered {{
            font-size: 10px;
            color: #ccc;
            margin-top: 8px;
        }}
        .qr-section {{
            padding: 20px;
            background: white;
            border-top: 1px solid #eee;
        }}
        .qr-placeholder {{
            width: 150px;
            height: 150px;
            margin: 0 auto;
            background: #f0f0f0;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="coupon">
        <div class="header">
            <div class="logo-placeholder">{restaurante[0]}</div>
            <div class="restaurant-name">{restaurante}</div>
            <div class="restaurant-subtitle">Oferta exclusiva para ti</div>
        </div>

        <div class="discount-section">
            <div class="discount-label">Tu descuento</div>
            <div class="discount-value">{descuento}%</div>
            <div class="discount-suffix">de descuento</div>
        </div>

        <div class="code-section">
            <div class="code-label">Tu codigo unico</div>
            <div class="code-value">{codigo}</div>
        </div>

        <div class="instructions">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-text">Muestra este codigo al momento de pagar en <strong>{restaurante}</strong></div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-text">El descuento se aplicara automaticamente en tu cuenta</div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-text">Paga menos y disfruta la mejor experiencia gastronomica</div>
            </div>
        </div>

        <div class="footer">
            <div class="validity">Vigencia: 30 dias desde hoy | Lima Automa</div>
            <div class="powered">Powered by Lima Automa</div>
        </div>
    </div>

    <script>
        // Tracking: registrar apertura de la pagina
        (function() {{
            const data = {{
                codigo_rastreo: '{codigo_rastreo}',
                restaurante: '{restaurante}',
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent,
                language: navigator.language,
                platform: navigator.platform,
                screen: screen.width + 'x' + screen.height,
                referrer: document.referrer || 'direct'
            }};

            // Enviar a nuestro endpoint de tracking
            fetch('/api/tracking', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(data)
            }}).catch(err => console.log('[Lima Automa] Tracking error:', err));

            console.log('[Lima Automa] Apertura registrada:', data);
        }})();
    </script>
</body>
</html>"""

    return html


def registrar_uso_cupon(cupon, cliente_info=None):
    """
    Registra cuando un cliente usa el cupon.
    """
    cupon["usos"] += 1
    cupon["clientes_atribuidos"].append({
        "fecha": datetime.now().isoformat(),
        "cliente": cliente_info or "Sin info",
    })
    return cupon


def registrar_pago_restaurante(cupon, monto, cliente_info=None):
    """
    Registra un pago al restaurante por cliente traído.
    """
    cupon["balance"] -= monto
    cupon["pagos_realizados"] = cupon.get("pagos_realizados", [])
    cupon["pagos_realizados"].append({
        "fecha": datetime.now().isoformat(),
        "monto": monto,
        "cliente": cliente_info or "Sin info",
    })
    return cupon


def generar_reporte_cupones(cupones):
    """
    Genera un reporte de uso de cupones.
    """
    reporte = {
        "total_cupones": len(cupones),
        "cupones_activos": sum(1 for c in cupones if c["activo"]),
        "total_usos": sum(c["usos"] for c in cupones),
        "clientes_atribuidos": sum(len(c["clientes_atribuidos"]) for c in cupones),
        "balance_total": sum(c.get("balance", 0) for c in cupones),
        "por_restaurante": [],
    }

    for cupon in cupones:
        reporte["por_restaurante"].append({
            "restaurante": cupon["restaurante"],
            "codigo": cupon["codigo_cliente"],
            "usos": cupon["usos"],
            "clientes": len(cupon["clientes_atribuidos"]),
            "balance": cupon.get("balance", 0),
        })

    return reporte


# === TESTING ===
if __name__ == "__main__":
    print("=" * 60)
    print("  LIMA AUTOMA - Generador de Cupones QR v2")
    print("=" * 60)

    # Ejemplo de uso
    restaurante_ejemplo = {
        "nombre": "Cafe de Lima",
        "telefono": "+5112425555",
    }

    cupon = crear_cupon(restaurante_ejemplo, descuento_pct=15)

    print(f"\n  Restaurante: {cupon['restaurante']}")
    print(f"  Codigo rastreo: {cupon['codigo_rastreo']}")
    print(f"  Codigo cliente: {cupon['codigo_cliente']}")
    print(f"  Landing URL: {cupon['landing_url']}")

    # Generar landing page HTML
    html = crear_landing_page_html(cupon)
    print(f"\n  Landing page generada ({len(html)} bytes)")
    print(f"  Guardar como: data/landing_{cupon['codigo_rastreo']}.html")
