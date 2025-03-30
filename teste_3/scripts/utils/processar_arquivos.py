import os
import pymysql
from dotenv import load_dotenv
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('importacao_dados.log'),
        logging.StreamHandler()
    ]
)

def carregar_arquivos_contabeis():
    load_dotenv()
    
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'ans_dados_abertos'),
        'local_infile': True
    }
    
    base_path = os.path.join('teste_3', 'data', 'contabeis')
    processed_files = 0
    
    try:
        conn = pymysql.connect(**db_config)
        
        with conn.cursor() as cursor:
            for filename in sorted(os.listdir(base_path)):
                if filename.endswith('.csv') and filename.startswith(('1T', '2T', '3T', '4T')):
                    filepath = os.path.abspath(os.path.join(base_path, filename))
                    
                    quarter = filename[0]
                    year = filename[2:6]
                    
                    logging.info(f"Processando: {filename} (T{quarter} {year})")
                    
                    sql = f"""
                    LOAD DATA LOCAL INFILE '{filepath}'
                    INTO TABLE demonstracoes_contabeis
                    CHARACTER SET latin1
                    FIELDS TERMINATED BY ';'
                    ENCLOSED BY '"'
                    LINES TERMINATED BY '\\n'
                    IGNORE 1 ROWS
                    (registro_ans, @competencia, conta_contabil, descricao, @valor)
                    SET 
                        competencia = STR_TO_DATE(CONCAT('01/', @competencia), '%d/%m/%Y'),
                        valor = REPLACE(REPLACE(@valor, '.', ''), ',', '.');
                    """
                    
                    try:
                        start_time = datetime.now()
                        cursor.execute(sql)
                        processed_files += 1
                        duration = (datetime.now() - start_time).total_seconds()
                        logging.info(f"Arquivo {filename} processado com sucesso em {duration:.2f}s")
                    except pymysql.Error as e:
                        logging.error(f"Erro ao processar {filename}: {e}")
                        continue
            
            conn.commit()
            logging.info(f"Importação concluída. {processed_files} arquivos processados com sucesso.")
            
    except pymysql.Error as e:
        logging.error(f"Falha na conexão com o banco de dados: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()
            logging.info("Conexão com o banco de dados encerrada.")
            
if __name__ == '__main__':
    logging.info("Iniciando processo de importação de dados contábeis da ANS")
    carregar_arquivos_contabeis()
    logging.info("Processo finalizado")