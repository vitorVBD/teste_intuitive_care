
CREATE DATABASE IF NOT EXISTS ans_dados_abertos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE ans_dados_abertos;

CREATE TABLE IF NOT EXISTS operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(5),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    email VARCHAR(100),
    representante VARCHAR(100),
    cargo_representante VARCHAR(100),
    data_registro_ans DATE,
    INDEX idx_nome_fantasia (nome_fantasia),
    INDEX idx_cidade (cidade),
    INDEX idx_uf (uf)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registro_ans VARCHAR(20),
    competencia DATE,
    conta_contabil VARCHAR(50),
    descricao VARCHAR(255),
    valor DECIMAL(15, 2),
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans),
    INDEX idx_competencia (competencia),
    INDEX idx_conta_contabil (conta_contabil),
    INDEX idx_descricao (descricao(50)),
    INDEX idx_registro_competencia (registro_ans, competencia)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;