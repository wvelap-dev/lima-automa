"""
Lima Automa - Generar Mensajes para Top 5
"""
import sys
sys.path.insert(0, 'src')

from scraper_restaurantes import buscar_restaurantes, calcular_score_prioridad
from message_generator import generar_mensaje_whatsapp, generar_mensaje_seguimiento
from analyzer import generar_informe
import json

# Buscar restaurantes
all_restaurants = []
for district in ['Miraflores', 'San Isidro', 'Barranco']:
    restaurants = buscar_restaurantes(district)
    for r in restaurants:
        calcular_score_prioridad(r)
    all_restaurants.extend(restaurants)

# Ordenar por score
all_restaurants.sort(key=lambda x: x.get('score', 0), reverse=True)

# Generar mensajes para los TOP 5
print('=' * 60)
print('  MENSAJES PERSONALIZADOS - TOP 5')
print('=' * 60)

messages_data = []
for i, r in enumerate(all_restaurants[:5], 1):
    msg = generar_mensaje_whatsapp(r)
    nombre = r['nombre']
    score = r['score']
    
    print(f'\n--- {i}. {nombre} (Score: {score}) ---')
    print(msg)
    seg1 = generar_mensaje_seguimiento(r, 1)
    print(f'\n--- SEGUIMIENTO ---')
    print(f'Dia 1: {seg1}')
    
    messages_data.append({
        'restaurante': nombre,
        'telefono': r.get('telefono', ''),
        'score': score,
        'mensaje_inicial': msg,
        'seguimiento_dia1': generar_mensaje_seguimiento(r, 1),
        'seguimiento_dia3': generar_mensaje_seguimiento(r, 3),
        'seguimiento_dia7': generar_mensaje_seguimiento(r, 7),
    })

# Guardar mensajes
with open('data/mensajes_personalizados.json', 'w', encoding='utf-8') as f:
    json.dump(messages_data, f, ensure_ascii=False, indent=2)

print(f'\nMensajes guardados en data/mensajes_personalizados.json')
