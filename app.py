from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import random

app = Flask(__name__)
CORS(app)

coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754, -103.346253),
    'Monterrey': (25.691611, -100.321838),
    'QuintanaRoo': (21.163111, -86.802315),
    'Michohacan': (19.701400, -101.208296),
    'Aguascalientes': (21.876410, -102.264386),
    'CDMX': (19.432713, -99.133183),
    'QRO': (20.597194, -100.386670)
}

def distancia(coord1, coord2):
    latitud1, longitud1 = coord1
    latitud2, longitud2 = coord2
    return math.sqrt((latitud1 - latitud2) ** 2 + (longitud1 - longitud2) ** 2)

def evalua_ruta(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total += distancia(coord[ciudad1], coord[ciudad2])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])
    return total

def simulated_annealing(ruta):
    T = 20.0
    T_MIN = 0.1
    V_enfriamiento = 100
    mejor_ruta = ruta[:]
    mejor_distancia = evalua_ruta(ruta)
    
    while T > T_MIN:
        for _ in range(V_enfriamiento):
            i = random.randint(0, len(ruta) - 1)
            j = random.randint(0, len(ruta) - 1)
            nueva_ruta = ruta[:]
            nueva_ruta[i], nueva_ruta[j] = nueva_ruta[j], nueva_ruta[i]
            
            nueva_distancia = evalua_ruta(nueva_ruta)
            delta = nueva_distancia - mejor_distancia
            
            if delta < 0 or random.random() < math.exp(-delta / T):
                ruta = nueva_ruta[:]
                mejor_distancia = nueva_distancia
                mejor_ruta = nueva_ruta[:]
        
        T *= 0.95

    return mejor_ruta, mejor_distancia

@app.route('/api/tsp', methods=['GET'])
@app.route('/api/tsp', methods=['GET'])
def resolver_tsp():
    ciudades = list(coord.keys())
    random.shuffle(ciudades)
    ruta_inicial = ciudades[:]
    distancia_inicial = evalua_ruta(ruta_inicial)
    
    mejor_ruta, mejor_distancia = simulated_annealing(ciudades)
    
    return jsonify({
        'ruta_inicial': ruta_inicial,
        'distancia_inicial': round(distancia_inicial, 4),
        'ruta_optima': mejor_ruta,
        'distancia_optima': round(mejor_distancia, 4)
    })
if __name__ == '__main__':
    app.run(debug=True, port=5000)