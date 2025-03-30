<template>
  <div id="app">
    <OperatorSearch />
  </div>
</template>

<script>
import OperatorSearch from './components/OperatorSearch.vue'

export default {
  name: 'App',
  components: {
    OperatorSearch
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
</style>