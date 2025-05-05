import consume_data
from flask import request, jsonify
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/championships', methods=['GET', 'POST'])
def get_championships():
    consulta_csv = consume_data.consulta_csv()
    if consulta_csv is not None:
        if request.method == 'GET':
            return consulta_csv.to_json(orient='records')
        elif request.method == 'POST':
            filters = request.get_json()
            if not filters:
                return jsonify({'error': 'No filters provided'}), 400

            filtered_data = consulta_csv
            for field, value in filters.items():
                if field in filtered_data.columns:
                    filtered_data = filtered_data[filtered_data[field] == value]
                else:
                    return jsonify({'error': f'Field "{field}" does not exist in the dataset'}), 400

            if not filtered_data.empty:
                return filtered_data.to_json(orient='records')
            else:
                return jsonify({'message': 'No data found for the given filters'}), 404
    else:
        return 'Error loading data', 500
    return 'Get Championships'

@app.route('/championships/<int:n>')
def get_top_5_championships(n):
    consulta_csv = consume_data.consulta_csv()

    if consulta_csv is not None:
        top_n = consulta_csv.head(n)
        return top_n.to_json(orient='records')

    return 'Get Top Championships'

@app.route('/championships/<string:championship_name>', methods=['GET'])
def get_championship_by_name(championship_name):
    consulta_csv = consume_data.consulta_csv()

    if consulta_csv is not None:
        championship = consulta_csv[consulta_csv['Tournament'] == championship_name]
        if not championship.empty:
            return championship.to_json(orient='records')
        else:
            return 'Championship not found', 404
    return 'Get Championship by Name'

@app.route('/insert-championship', methods=['POST'])
def insert_championship():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    consume_data.inserir_championship(data)
    return 'Campeonato Inserido', 201

@app.route('/update-championship', methods=['PUT'])
def update_championship():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    resultado = consume_data.atualizar_championship(data)

    return jsonify({'mensagem': resultado['mensagem']}), resultado['status_code']

@app.route('/delete-championship', methods=['DELETE'])
def delete_championship():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    resultado = consume_data.deletar_championship(data)

    return jsonify({'mensagem': resultado['mensagem']}), resultado['status_code']

if __name__ == '__main__':
    app.run(debug=True)