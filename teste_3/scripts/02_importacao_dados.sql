
USE ans_dados_abertos;

LOAD DATA LOCAL INFILE "teste_3\data\cadastrais\Relatorio_cadop.csv"
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(registro_ans, cnpj, razao_social, nome_fantasia, modalidade,
 logradouro, numero, complemento, bairro, cidade, uf, cep,
 ddd, telefone, fax, email, representante, cargo_representante, @data_registro_ans)
SET data_registro_ans = STR_TO_DATE(@data_registro_ans, '%d/%m/%Y');

LOAD DATA LOCAL INFILE "teste_3\data\contabeis\1T2023.csv"
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(registro_ans, @competencia, conta_contabil, descricao, @valor)
SET 
    competencia = STR_TO_DATE(CONCAT('01/', @competencia), '%d/%m/%Y'),
    valor = REPLACE(REPLACE(@valor, '.', ''), ',', '.');