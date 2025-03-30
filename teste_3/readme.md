# Manual de Instruções - Sistema de Análise de Dados ANS

## 1. Pré-requisitos
Antes de começar, verifique se seu ambiente possui:
- **Banco de dados**: MySQL 8.0+
- **Python**: Versão 3.8 ou superior
- **Acesso administrativo** ao banco de dados

---

## 2. Configuração Inicial

### 2.1 Preparação dos Arquivos
- Todos os arquivos trimestrais devem estar na pasta `data/contabeis` no formato `XTAAAA.csv` (ex: `1T2023.csv`)
- O arquivo cadastral deve estar em `data/cadastrais/Relatorio_cadop.csv`

### 2.2 Configuração do Banco
Edite o arquivo `.env` na pasta `utils` com:

```ini
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=ans_dados_abertos
```

---

## 3. Execução do Sistema

### 3.1 Criar Estrutura do Banco

```bash
mysql -u seu_usuario -p < scripts/01_criacao_tabelas.sql
```

### 3.2 Importar Dados

**Dados Cadastrais**:

```bash
mysql -u seu_usuario -p < scripts/02_importacao_dados.sql
```

**Dados trimestrais (automático)**:

```bash
pip install pymysql python-dotenv
python utils/processar_arquivos.py
```

---

## 4. Consultas Analíticas

Para gerar relatórios:

```bash
mysql -u seu_usuario -p ans_dados_abertos < scripts/03_queries_analiticas.sql
```

**Resultados obtidos**:

- Top 10 operadoras com maiores despesas no último trimestre
- Top 10 operadoras com maiores despesas no último ano

---

## 5. Solução de Problemas

### Problema 1: Arquivo não encontrado

**Solução**:

- Verifique os caminhos dos arquivos CSV
- Use caminhos absolutos se necessário

### Problema 2: Falha na importação

**Solução**:

- Verifique o encoding dos arquivos (deve ser Latin1)
- Confirme que os delimitadores são ";" (ponto e vírgula)

### Problema 3: Permissões no MySQL

**Solução**:

```sql
SET GLOBAL local_infile = 1;
GRANT FILE ON *.* TO 'seu_usuario'@'localhost';
```

---

## 6. Atualização de Dados

Para adicionar novos dados:

1.Coloque os novos arquivos CSV em ```data/contabeis/```
2.Execute:

```bash
python utils/processar_arquivos.py
```