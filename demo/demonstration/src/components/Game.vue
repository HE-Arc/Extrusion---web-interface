<template>
    <div class="container">
        <div class="row mt-5">
            <Face title="Face Cheminée" v-bind:index="0" v-bind:w="200" v-bind:h="300"></Face>
            <Face title="Face Case" v-bind:index="1" v-bind:w="200" v-bind:h="300"></Face>
            <Face title="Face Vitre" v-bind:index="3" v-bind:w="200" v-bind:h="300"></Face>
            <Face title="Face Toit" v-bind:index="2" v-bind:w="200" v-bind:h="300"></Face>
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