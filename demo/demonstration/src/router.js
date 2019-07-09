import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const router = new VueRouter({
    mode: 'history',
    routes:[
      {
        path:'/admin',
        component: r => require.ensure([],() => r(require('./components/Admin'))),
        name:'admin'
      },
      {
        path:'/game',
        component: r => require.ensure([],() => r(require('./components/Game'))),
        name:'game'
      },
    ]

  }
)
export default router