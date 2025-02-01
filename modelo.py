from flask import Flask, render_template, request, jsonify
from itertools import product
from collections import defaultdict

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/calculate', methods=['POST'])
    def calculate():
        data = request.json
        categories = data.get('categories', [])
        
        if not categories:
            return jsonify({"error": "No se proporcionaron categorías"}), 400
        
        # Generar todas las combinaciones posibles
        ranges = [range(1, int(c) + 1) for c in categories]
        combinations = list(product(*ranges))
        total_combinations = len(combinations)  # Total de combinaciones
        
        # Calcular los productos de cada combinación
        results = []
        for comb in combinations:
            product_result = 1
            for num in comb:
                product_result *= num
            results.append(product_result)
        
        # Calcular la distribución de frecuencia
        freq_dist = defaultdict(int)
        for result in results:
            freq_dist[result] += 1
        
        # Ordenar la distribución de frecuencia y calcular la frecuencia relativa
        sorted_freq_dist = []
        for value, freq in sorted(freq_dist.items()):
            rel_freq = freq / total_combinations  # Frecuencia relativa
            sorted_freq_dist.append((value, freq, rel_freq))
        
        # Calcular la distribución acumulada y su frecuencia relativa
        acum_dist = []
        acum = 0
        for value, freq, rel_freq in sorted_freq_dist:
            acum += freq
            acum_rel_freq = acum / total_combinations  # Frecuencia relativa acumulada
            acum_dist.append((value, acum, acum_rel_freq))
        
        return jsonify({
            "freq_dist": sorted_freq_dist,
            "acum_dist": acum_dist,
            "total_combinations": total_combinations
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)