<template>
    <div class="container">
        <div class="row">
            <div class="col-12">
                <h4>Link to api</h4>
            </div>
            <div class="col-12">
                <label for="link">Link</label>
                <input v-model="link" type="text" class="form-control" id="link"
                       placeholder="http://127.0.0.1">
            </div>
            <div class="col-12">
                <label for="token">Token</label>
                <input v-model="token" type="text" class="form-control" id="token">
            </div>
        </div>
    </div>

</template>

<script>
  export default {
    name: 'Admin',
    computed: {
      link: {
        get () {
          return localStorage.getItem('link')
        },
        set (val) {
          localStorage.setItem('link', val)
        }
      },
      token: {
        get () {
          return localStorage.getItem('token')
        },
        set (val) {
          localStorage.setItem('token', val)
        }
      }
    },
  }
</script>

<style scoped>

</style>