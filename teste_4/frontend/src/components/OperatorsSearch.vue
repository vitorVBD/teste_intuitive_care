<template>
  <div class="operator-search">
    <h1>Busca de Operadoras de Saúde</h1>
    
    <div class="search-box">
      <input
        v-model="searchTerm"
        @input="handleSearch"
        placeholder="Digite nome, CNPJ ou cidade..."
      />
      <button @click="searchOperators">Buscar</button>
    </div>
    
    <div v-if="loading" class="status">Carregando...</div>
    <div v-if="error" class="error">{{ error }}</div>
    
    <div v-if="results.length > 0">
      <h2>Resultados ({{ totalResults }})</h2>
      <div class="results-grid">
        <div v-for="operator in results" :key="operator.registro_ans" class="operator-card">
          <h3>{{ operator.nome_fantasia || operator.razao_social }}</h3>
          <p><strong>Registro ANS:</strong> {{ operator.registro_ans }}</p>
          <p><strong>CNPJ:</strong> {{ formatCnpj(operator.cnpj) }}</p>
          <p><strong>Localização:</strong> {{ operator.cidade }}/{{ operator.uf }}</p>
        </div>
      </div>
    </div>
    
    <div v-else-if="searchTerm && !loading" class="status">
      Nenhuma operadora encontrada para "{{ searchTerm }}"
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      searchTerm: '',
      results: [],
      loading: false,
      error: null,
      totalResults: 0,
      searchTimeout: null
    }
  },
  methods: {
    async searchOperators() {
      if (this.searchTerm.length < 2) {
        this.results = []
        return
      }
      
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('/api/operators', {
          params: { q: this.searchTerm }
        })
        
        this.results = response.data.results
        this.totalResults = response.data.count
      } catch (err) {
        this.error = 'Erro ao buscar operadoras. Tente novamente.'
        console.error('Search error:', err)
      } finally {
        this.loading = false
      }
    },
    handleSearch() {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {
        this.searchOperators()
      }, 300)
    },
    formatCnpj(cnpj) {
      if (!cnpj) return ''
      return cnpj.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5')
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.search-box {
  display: flex;
  gap: 1rem;
  margin: 2rem 0;
}

.search-box input {
  flex: 1;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-box button {
  padding: 0 2rem;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.card {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 1.5rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card h3 {
  margin-top: 0;
  color: #2c3e50;
}

.status, .error {
  padding: 2rem;
  text-align: center;
  font-size: 1.2rem;
}

.error {
  color: #e74c3c;
}
</style>