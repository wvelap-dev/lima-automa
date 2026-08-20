# Lima Automa - Sistema de Adquisición de Clientes

## 🎯 Estado Actual

✅ **Sistema completo para encontrar y contactar restaurantes en Lima**

### Herramientas Creadas

1. **Buscador de Clientes** (`buscador_clientes.py`)
   - Encuentra restaurantes reales en Lima
   - Analiza si son buenos candidatos
   - Genera un score de 0-100

2. **Contactador de Clientes** (`contactar_clientes.py`)
   - Genera mensajes personalizados para cada restaurante
   - Crea links de WhatsApp listos para enviar
   - Guarda todo en un archivo JSON

3. **Simulador de Campaña** (`simular_campaña.py`)
   - Simula respuestas de restaurantes (para demostración)
   - Muestra estadísticas de conversión

4. **Dashboard de Campaña** (`dashboard_campana.py`)
   - Genera un dashboard visual en HTML
   - Muestra gráficos y tablas de resultados

## 🚀 Cómo Usar

### Paso 1: Buscar Restaurantes
```bash
python scripts/buscador_clientes.py
```
Esto crea `data/clientes_potenciales.json` con 21 restaurantes.

### Paso 2: Generar Contactos
```bash
python scripts/contactar_clientes.py
```
Esto crea `data/contactos_whatsapp.json` con links de WhatsApp.

### Paso 3: Simular Campaña (Opcional - Modo Demo)
```bash
python scripts/simular_campaña.py
```
Esto simula respuestas para ver cómo funcionaría el sistema.

### Paso 4: Ver Dashboard
```bash
python scripts/dashboard_campana.py
```
Esto genera `dashboard_campana.html` que puedes abrir en tu navegador.

## 📊 Resultados

- **21 restaurantes encontrados** en Lima
- **Todos tienen teléfono** para contacto
- **19 tienen sitio web** (80%)
- **Top candidatos**: Cevicherías, restaurantes con baja calificación

## ⚠️ Modo DEMO

**IMPORTANTE**: Actualmente estamos en modo demostración. No se contactarán restaurantes reales hasta que se establezca la entidad legal.

## 📁 Archivos Importantes

- `data/clientes_potenciales.json` - Lista de restaurantes
- `data/contactos_whatsapp.json` - Links de WhatsApp
- `data/campanas_simuladas.json` - Resultados de simulación
- `dashboard_campana.html` - Dashboard visual

## 🎯 Próximos Pasos

1. **Validar demanda** - Encuesta a restaurantes
2. **Establecer entidad legal** - Antes de contactar clientes
3. **Conectar WhatsApp Business API** - Para automatización real
4. **Ejecutar primera campaña** - Con restaurantes reales

---

*Última actualización: Agosto 2026*
