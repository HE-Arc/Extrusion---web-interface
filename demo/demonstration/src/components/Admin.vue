<template>
    <div class="container">
        <div class="row">
            <div class="col-12">
                <h1>Board</h1>
            </div>
        </div>
        <div class="card">
            <div class="card-body">
                
            </div>
        </div>
    </div>
</template>

<script>
  export default {
    name: 'Admin',
    data () {
      return {
        title: '',
      }
    },
    mounted () {
      this.axios
        .get('http://127.0.0.1:5000/state')
        .then(response => (this.title = response.data))
    }

  }
</script>

<style scoped>

</style>