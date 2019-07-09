<template>
    <div class="container">
        <div class="row mt-5">
            <Face v-bind:index="3" v-bind:w="200" v-bind:h="300"></Face>
        </div>
    </div>
</template>

<script>
  import Face from './Face'

  export default {
    name: 'Game',
    components: {
      Face,
    },
    data () {
      return {}
    },
    mounted () {

    }

  }
</script>

<style scoped>

</style>