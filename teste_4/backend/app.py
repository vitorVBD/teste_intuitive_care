from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)

load_dotenv()

app = Flask(__name__)
CORS(app)

MIN_SEARCH_LENGTH = 2
MAX_RESULTS = 20
SEARCH_FIELDS = ['razao_social', 'nome_fantasia', 'cnpj', 'cidade', 'uf']

try:
    df = pd.read_csv(
        'data/Relatorio_cadop.csv', 
        sep=';', 
        encoding='iso-8859-1',
        dtype={'cnpj': str, 'registro_ans': str}
    )
    df.fillna('', inplace=True)
    logging.info(f"Dados carregados com sucesso. Total de registros: {len(df)}")
except Exception as e:
    logging.error(f"Erro ao carregar arquivo CSV: {str(e)}")
    raise

@app.route('/api/operators', methods=['GET'])
def search_operators():
    """Endpoint para busca de operadoras de saúde"""
    start_time = datetime.now()
    search_term = request.args.get('q', '').strip()
    
    if len(search_term) < MIN_SEARCH_LENGTH:
        logging.warning(f"Termo de busca muito curto: '{search_term}'")
        return jsonify({
            'error': f'O termo de busca deve conter pelo menos {MIN_SEARCH_LENGTH} caracteres',
            'status': 400
        }), 400
    
    try:
        logging.info(f"Iniciando busca por: '{search_term}'")
        
        mask = df[SEARCH_FIELDS].apply(
            lambda col: col.str.contains(search_term, case=False, regex=False)
        ).any(axis=1)
        
        results = df[mask].head(MAX_RESULTS).to_dict('records')
        
        duration = (datetime.now() - start_time).total_seconds()
        logging.info(f"Busca concluída em {duration:.2f}s. Resultados: {len(results)}")
        
        return jsonify({
            'search_term': search_term,
            'results': results,
            'count': len(results),
            'status': 'success'
        })
        
    except Exception as e:
        logging.error(f"Erro na busca: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Ocorreu um erro interno no servidor',
            'status': 500
        }), 500

@app.route('/api/healthcheck', methods=['GET'])
def health_check():
    """Endpoint para verificação do status da API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'records_loaded': len(df)
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    logging.info(f"Iniciando servidor na porta {port}")
    app.run(host=host, port=port, debug=debug)