<template>
    <div class="col-md-3">
        <h2>{{ title }}</h2>
        <canvas @mousemove="mousemove" @mouseover="mouseover" @mouseleave="mouseup" @mousedown="mousedown"
                @mouseup="mouseup"
                ref="my-canvas" id="canvas1" width="200" height="300"></canvas>
        <p>({{posX}},{{posY}})</p>
    </div>
</template>

<script>
  export default {
    name: 'Face',
    props: {
      w: Number,
      h: Number,
      index: Number,
      title: String,
    },
    data () {
      return {
        width: this.w,
        height: this.h,
        idx: this.index,
        posX: null,
        posY: null,
        xNotShow: null,
        yNotShow: null,
        xShow: null,
        yShow: null,
        mouseDown: false
      }
    },
    computed: {
      ctx: function () {
        return this.$refs['my-canvas'].getContext('2d')
      },
      spaceX: function () {
        return this.width / 4
      },
      spaceY: function () {
        return this.height / 6
      },
      arrayFaceFunction: function () {
        let tab = []
        tab[0] = this.faceCheminee
        tab[1] = this.faceCase
        tab[2] = this.faceToit
        tab[3] = this.faceVitre
        return tab
      },
      link:function () {
        return localStorage.getItem('link')
      },
      token:function () {
        return localStorage.getItem('token')
      }
    },
    methods: {
      drawGrid (notXDraw, notYDraw) {
        let pinceau = this.ctx
        let cptY = 0
        let cptX = 0
        pinceau.clearRect(0, 0, this.width, this.height)
        pinceau.beginPath()
        for (let h = 0; h <= this.height; h += this.spaceY) {
          if (cptY !== notYDraw) {
            pinceau.moveTo(0, h)
            pinceau.lineTo(this.width, h)
          }
          cptY++
        }

        for (let w = 0; w <= this.width; w += this.spaceX) {
          if (cptX !== notXDraw) {
            pinceau.moveTo(w, 0)
            pinceau.lineTo(w, this.height)
          }
          cptX++
        }
        pinceau.stroke()
      },
      mousemove: function (event) {
        if (this.mouseDown) {
          this.pos(event)
          this.notDraw()
          this.drawGrid(this.xNotShow, this.yNotShow)
          this.manageCube()
        }

      },
      mousedown: function () {
        this.mouseDown = true
      },
      mouseover: function () {
        this.notDraw()
      },
      mouseup: function () {
        this.mouseDown = false
        this.drawGrid(-1, -1)
        this.xShow = null
        this.yShow = null
        this.blackoutFace()
      },
      pos: function (event) {
        let rect = this.$refs['my-canvas'].getBoundingClientRect()
        this.posX = event.clientX - rect.left
        this.posY = event.clientY - Math.round(rect.top)
      },
      notDraw: function () {
        this.xNotShow = Math.round(this.posX / this.spaceX)
        this.yNotShow = Math.round(this.posY / this.spaceY)
      },
      manageCube: function () {
        this.arrayFaceFunction[this.idx]()
      },
      faceVitre: function () {
        if (this.xShow !== this.xNotShow) {
          for (let z = 1; z <= 11; z = z + 2) {
            this.axiosXYZ(this.xShow * 2 + 2, 10, z, 0)
          }
          this.xShow = this.xNotShow
          for (let z = 1; z <= 11; z = z + 2) {
            this.axiosXYZ(this.xShow * 2 + 2, 10, z, 15)
          }
        }
        if (this.yShow !== this.yNotShow) {
          for (let x = 3; x <= 9; x = x + 2) {
            this.axiosXYZ(x, 10, 12 - (this.yShow * 2), 0)
          }
          this.yShow = this.yNotShow
          for (let x = 3; x <= 9; x = x + 2) {
            this.axiosXYZ(x, 10, 12 - (this.yShow * 2), 15)
          }
        }
      },
      faceToit: function () {
        if (this.xShow !== this.xNotShow) {
          for (let z = 1; z <= 11; z = z + 2) {
            this.axiosXYZ(10, 10 - this.xShow * 2, z, 0)
          }
          this.xShow = this.xNotShow
          for (let z = 1; z <= 11; z = z + 2) {
            this.axiosXYZ(10, 10 - this.xShow * 2, z, 15)
          }
        }
        if (this.yShow !== this.yNotShow) {
          for (let y = 3; y <= 9; y = y + 2) {
            this.axiosXYZ(10, y, 12 - (this.yShow * 2), 0)
          }
          this.yShow = this.yNotShow
          for (let y = 3; y <= 9; y = y + 2) {
            this.axiosXYZ(10, y, 12 - (this.yShow * 2), 15)
          }
        }
      },
      faceCase: function () {
        if (this.xShow !== this.xNotShow) {
          for (let z = 1; z <= 11; z = z + 2) {
            this.axiosXYZ(10 - (this.xShow * 2 + 2), 0, z, 0)
          }
          this.xShow = this.xNotShow
          for (let z = 1; z <= 11; z = z + 2) {
            this.axiosXYZ(10 - (this.xShow * 2 + 2), 0, z, 15)
          }
        }
        if (this.yShow !== this.yNotShow) {
          for (let x = 1; x <= 7; x = x + 2) {
            this.axiosXYZ(x, 0, 12 - (this.yShow * 2), 0)
          }
          this.yShow = this.yNotShow
          for (let x = 1; x <= 7; x = x + 2) {
            this.axiosXYZ(x, 0, 12 - (this.yShow * 2), 15)
          }
        }
      },
      faceCheminee: function () {
        if (this.xShow !== this.xNotShow) {
          for (let z = 1; z <= 11; z = z + 2) {
            this.axiosXYZ(0, this.xShow * 2, z, 0)
          }
          this.xShow = this.xNotShow
          for (let z = 1; z <= 11; z = z + 2) {
            this.axiosXYZ(0, this.xShow * 2, z, 15)
          }
        }
        if (this.yShow !== this.yNotShow) {
          for (let y = 1; y <= 7; y = y + 2) {
            this.axiosXYZ(0, y, 12 - (this.yShow * 2), 0)
          }
          this.yShow = this.yNotShow
          for (let y = 1; y <= 7; y = y + 2) {
            this.axiosXYZ(0, y, 12 - (this.yShow * 2), 15)
          }
        }
      },
      axiosXYZ: async function (x, y, z, brightness) {
        let form = new FormData()
        form.append('idx_x', x)
        form.append('idx_y', y)
        form.append('idx_z', z)
        form.append('brightness', brightness)
        await this.axios({
          method: 'post',
          url: `${this.link}/xyz`,
          data: form,
          headers: {"Authorization": `Bearer ${this.token}`},
        }).then(function (response) {
          //handle success
          console.log(response)
        })

      }
      ,
      blackoutFace: async function () {
        let form = new FormData()
        form.append('idx_face', this.idx)
        form.append('brightness', 0)
        await this.axios({
          method: 'post',
          url: `${this.link}/face`,
          data: form,
          headers: {"Authorization": `Bearer ${this.token}`},
        }).then(function (response) {
          //handle success
          return console.log(response.data.message)
        })
      }
      ,
    },
    mounted () {

      this.$refs['my-canvas'].width = this.width
      this.$refs['my-canvas'].height = this.height
      this.drawGrid(-1, -1)
    }
  }
</script>

<style scoped>

</style>