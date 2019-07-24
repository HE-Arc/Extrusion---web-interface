<template>
    <div class="container">
        <div class="row">
            <div class="col-12">
                <h4>Number of sequence in queue: {{nb_seq}}</h4>
            </div>
            <div class="col-12">
                <label for="name">Name</label>
                <input v-model="name" type="text" class="form-control" id="name" aria-describedby="emailHelp"
                       placeholder="name">
                <small id="emailHelp" class="form-text text-muted">Name your sequence</small>
            </div>
            <div class="col-12">
                <h4>Sequence</h4>
                <prism-editor v-model="code" language="python" class="my-editor"/>
            </div>
            <div class="col-12">
                <button @click="send" type="button" class="btn btn-dark">send</button>
            </div>
            <div class="col-12">
                <h4>Cube Functions</h4>
            </div>
            <div class="col-12">

                <table class="table">
                    <thead class="thead-dark">
                    <tr>
                        <th scope="col">Function</th>
                        <th scope="col">Description</th>
                        <th scope="col">parameter</th>
                        <th scope="col">Exemple</th>
                        <th scope="col">What exemple do</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <th scope="row">delay([pause_time])</th>
                        <td>Make a pause in sequence</td>
                        <td>pause_time: time in second</td>
                        <td>delay(1)</td>
                        <td>Make a pause of 1 second</td>
                    </tr>
                    <tr>
                        <th scope="row">cube([brightness])</th>
                        <td>ignite the cube</td>
                        <td>brightness: power of ignite (0-15)</td>
                        <td>cube(15)</td>
                        <td>Ignite the cube</td>
                    </tr>
                    <tr>
                        <th scope="row">face([face_index],[brightness])</th>
                        <td>ignite a face</td>
                        <td>face_index: index of face (0-5)<br/>
                            brightness: power of ignite (0-15)</td>
                        <td>face(0,15)</td>
                        <td>Ignite face 0</td>
                    </tr>
                    <tr>
                        <th scope="row">square([face_index],[square_index],[brightness])</th>
                        <td>ignite a square</td>
                        <td>
                            face_index: index of face (0-5)<br/>
                            square_index: index of square (0-23)<br/>
                            brightness: power of ignite (0-15)</td>
                        <td>square(0,0,15)</td>
                        <td>Ignite square 0 of face 0</td>
                    </tr>
                    <tr>
                        <th scope="row">ledstrip([face_index],[square_index],[ledstrip_index],[brightness])</th>
                        <td>ignite a ledstrip</td>
                        <td>
                            face_index: index of face (0-5)<br/>
                            square_index: index of square (0-23)<br/>
                            ledstrip_index_index: index of ledstrip (0-3)<br/>
                            brightness: power of ignite (0-15)</td>
                        <td>ledstrip(0,0,0,15)</td>
                        <td>Ignite the ledstrip 0 of square 0 of face 0</td>
                    </tr>
                    <tr>
                        <th scope="row">ledstrip([face_index],[square_index],[ledstrip_index],[led_index],[brightness])</th>
                        <td>ignite a ledstrip</td>
                        <td>
                            face_index: index of face (0-5)<br/>
                            square_index: index of square (0-23)<br/>
                            ledstrip_index_index: index of ledstrip (0-3)<br/>
                            led_index_index: index of led (0-26)<br/>
                            brightness: power of ignite (0-15)</td>
                        <td>ledstrip(0,0,0,0,15)</td>
                        <td>Ignite the led 0 of ledstrip 0 of square 0 of face 0</td>
                    </tr>
                    <tr>
                        <th scope="row">xyz([x_index],[y_index],[z_index],[brightness])</th>
                        <td>ignite a ledstrip</td>
                        <td>
                            x_index: index x (0-10)<br/>
                            y_index: index y (0-10)<br/>
                            z_index_index: z (0-12)<br/>
                            brightness: power of ignite (0-15)</td>
                        <td>xyz(0,0,0,15)</td>
                        <td>Ignite the ledstrip (0,0,0)</td>
                    </tr>
                    <tr>
                        <th scope="row">xyz_led([x_index],[y_index],[z_index],[led_index],[brightness])</th>
                        <td>ignite a ledstrip</td>
                        <td>
                            x_index: index x (0-10)<br/>
                            y_index: index y (0-10)<br/>
                            z_index_index: z (0-12)<br/>
                            led_index_index: index of led (0-26)<br/>
                            brightness: power of ignite (0-15)</td>
                        <td>xyz(0,0,0,0,15)</td>
                        <td>Ignite the led 0 of the ledstrip (0,0,0)</td>
                    </tr>
                    </tbody>
                </table>


            </div>
        </div>
    </div>
</template>

<script>
  import PrismEditor from 'vue-prism-editor'

  export default {
    name: 'Sequence',
    data () {
      return {
        code: null,
        name: null,
        lineNumbers: true,
        nb_seq: 0,
      }
    },
    computed: {
      link: function () {
        return localStorage.getItem('link')
      },
      token: function () {
        return localStorage.getItem('token')
      },
    },
    methods: {
      getNbSeq: async function () {
        await this.axios({
          method: 'get',
          url: `${this.link}/state`,
          headers: { 'Authorization': `Bearer ${this.token}` },
        })
          .then(response => (this.nb_seq = response.data.nb_seq_in_queue))
      },
      send: async function () {
        let form = new FormData()
        let state = false
        let message = ''
        form.append('name', this.name)
        form.append('code', this.code)
        await this.axios({
          method: 'post',
          url: `${this.link}/seq`,
          data: form,
          headers: { 'Authorization': `Bearer ${this.token}` },
        }).then(function (response) {
          //handle success

          message = response.data.message
          state = response.data.state

        })
        if (state) {
          this.$swal({
            type: 'success',
            text: message
          })
        } else {
          this.$swal({
            type: 'error',
            title: 'Oops...',
            text: message
          })
        }
        this.getNbSeq()
      }
    },
    mounted () {
      this.getNbSeq()
      this.$nextTick(function () {
        window.setInterval(() => {
          this.getNbSeq()
        }, 10000)
      })
    },
    components: {
      PrismEditor,
    },
  }
</script>
