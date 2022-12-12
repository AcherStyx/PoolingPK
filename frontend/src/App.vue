<template>
  <div id="app">
    <h1>Game AI Web Display</h1>
    <PoolingPK msg="display"/>
  </div>
</template>

<script>
import PoolingPK from './components/PoolingPK.vue'

export default {
  name: 'App',
  components: {
    PoolingPK
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  margin-left: 60px;
  margin-right: 60px;
}
</style>
