# Instruções de Uso - Processamento de Dados ANS

## Configuração Inicial

1. **Instale o Python** (versão 3.8 ou superior)  
   - Download oficial: [python.org/downloads](https://www.python.org/downloads)

2. **Instale o Google Chrome**  
   - Disponível em: [google.com/chrome](https://www.google.com/chrome)

3. **Instale as dependências** executando no terminal:  
   ```bash
   pip install -r requirements.txt
   ```

---

## Execução do Processo

É fundamental executar os scripts na ordem. O script ```teste_transformacao_dados.py``` utiliza o caminho do PDF dinamicamente, quando for baixado pelo script ```teste_web_scraping.py```.

Caso os scripts sejam executados em ordem inversa, um erro tratado será lançado: ```"Erro: Execute primeiro o teste_web_scraping.py"```.

---

### Etapa 1: Coleta de Arquivos
Execute o seguinte comando:

```bash
python teste_web_scraping.py
```

**O que faz:**
- ✅ Acessa automaticamente o portal da ANS
- ✅ Faz download dos PDFs com o Rol de Procedimentos
- ✅ Gera e armazena na pasta `downloaded_pdfs`
- ✅ Gera arquivo ZIP com todos os PDFs

⏳ **Tempo estimado:** 5-10 minutos

---

### Etapa 2: Processamento de Dados
Execute o seguinte comando:

```bash
python teste_transformacao_dados.py
```

**O que faz:**
- ✅ Extrai tabelas do primeiro PDF baixado
- ✅ Padroniza e organiza os dados
- ✅ Gera arquivo final `Teste_Vitor.zip` contendo:
  - `Rol_de_Procedimentos.csv` (dados estruturados)

⏳ **Tempo estimado:** 2-5 minutos

---

## Localização dos Arquivos
- 📂 **Arquivos baixados:** Pasta `downloaded_pdfs`
- 📂 **Resultado final:** `Teste_Vitor.zip` na raiz do projeto