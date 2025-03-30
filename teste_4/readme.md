# Manual de Instruções - API de Consulta de Operadoras ANS

## 1. Pré-requisitos
Antes de começar, verifique se seu ambiente possui:  
- **Python**: Versão 3.8 ou superior  
- **Node.js**: Versão 16+ (para o frontend)  
- **Postman** (para testar a API)  

---

## 2. Configuração Inicial

### 2.1 Estrutura de Arquivos

```
teste_4/
├── backend/
│ ├── app.py
│ ├── requirements.txt
│ ├── data/
│ │ └── Relatorio_cadop.csv
│ └── .env
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ │ └── OperatorSearch.vue
│ │ ├── App.vue
│ │ └── main.js
│ ├── package.json
│ └── vite.config.js
└── postman_collection.json
```

### 2.2 Configuração do Ambiente  
Edite o arquivo `.env` na pasta `backend` com:  

```ini
PORT=5000
HOST=0.0.0.0
DEBUG=true
MAX_RESULTS=20
MIN_SEARCH_LENGTH=2
```

---

## 3. Instalação e Execução

### 3.1 Backend (API Flask)
**Instalação:**  
```bash
cd backend
pip install -r requirements.txt
```

**Execução:**  
```bash
python app.py
```
A API estará disponível em: [http://localhost:5000](http://localhost:5000)

### 3.2 Frontend (Vue.js)
**Instalação:**  
```bash
cd frontend
npm install
```

**Execução:**  
```bash
npm run dev
```
O frontend estará disponível em: [http://localhost:3000](http://localhost:3000)

---

## 4. Endpoints da API

### 4.1 Busca de Operadoras
```
GET /api/operators?q=<termo_de_busca>
```
**Parâmetros:**  
- `q`: Termo para busca (mínimo 2 caracteres)  

**Exemplo:**  
```bash
curl "http://localhost:5000/api/operators?q=saude"
```

### 4.2 Health Check
```
GET /api/healthcheck
```
Verifica o status da API e quantidade de registros carregados.

---

## 5. Testando com Postman
1. Importe o arquivo `postman_collection.json`.  
2. Execute as requisições de exemplo:  
   - **Health Check**  
   - **Busca por termo**  
   - **Busca inválida** (termo curto)  

---

## 6. Solução de Problemas

### Problema 1: Arquivo CSV não encontrado  
**Solução:**  
- Verifique se `Relatorio_cadop.csv` está em `backend/data/`.  
- Confira o caminho absoluto no código se necessário.  

### Problema 2: Erros de CORS  
**Solução:**  
- Certifique-se que `CORS(app)` está habilitado no `app.py`.  
- No frontend, verifique o proxy configurado no `vite.config.js`.  

### Problema 3: Frontend não conecta à API  
**Solução:**  
- Verifique se ambas as aplicações estão rodando.  
- Confira as URLs configuradas no `frontend/src/main.js`.  

---

## 7. Atualizações

Para atualizar os dados cadastrais:  
1. Substitua o arquivo `Relatorio_cadop.csv`.  
2. Reinicie a aplicação Flask.  

---

## 8. Personalização

### Alterar limites de busca:  
Edite no `.env`:  

```ini
MAX_RESULTS=50  # Número máximo de resultados
MIN_SEARCH_LENGTH=3  # Tamanho mínimo do termo de busca
```

### Modificar campos de busca:  
Edite no `app.py` a variável `SEARCH_FIELDS` para incluir novos campos.  

---

## 9. Considerações Finais

Esta solução fornece:  
✅ **API REST robusta** para consulta de operadoras  
✅ **Interface web moderna** com Vue.js  
✅ **Pronta para desenvolvimento e produção**  
✅ **Fácil integração com outros sistemas**  

### Para deploy em produção, considere usar:  
- **Gunicorn** (backend)  
- **Nginx** (proxy reverso)  
- **Docker** (containerização)  

---