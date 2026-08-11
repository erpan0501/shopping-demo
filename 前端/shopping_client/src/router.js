import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import(/* webpackChunkName: "home" */ './views/home/index.vue')
  },
  {
    path: '/list',
    name: 'list',
    component: () => import(/* webpackChunkName: "list" */ './views/product/List.vue')
  },
  {
    path: '/cart',
    name: 'cart',
    component: () => import(/* webpackChunkName: "cart" */ './views/product/Cart.vue')
  },
  {
    path: '/orderinfo',
    name: 'orderinfo',
    component: () => import(/* webpackChunkName: "cart" */ './views/product/OrderInfo.vue')
  },
  {
    path: '/pay',
    name: 'pay',
    component: () => import(/* webpackChunkName: "pay" */ './views/product/Pay.vue')
  },
  {
    path: '/order',
    name: 'order',
    component: () => import(/* webpackChunkName: "order" */ './views/product/Order.vue')
  },
  {
    path: '/orderdetail',
    name: 'orderdetail',
    component: () => import(/* webpackChunkName: "orderdetail" */ './views/product/OrderDetail.vue')
  },
  {
    path: '/productdetail',
    name: 'productdetail',
    component: () => import(/* webpackChunkName: "productdetail" */ './views/product/ProductDetail.vue')
  },
  {
    path: '/seckill',
    name: 'seckill',
    component: () => import(/* webpackChunkName: "seckill" */ './views/seckill/List.vue')
  },
  {
    path: '/seckilldetail',
    name: 'seckilldetail',
    component: () => import(/* webpackChunkName: "seckilldetail" */ './views/seckill/Detail.vue')
  },
  {
    path: '/seckillorderinfo',
    name: 'seckillorderinfo',
    component: () => import(/* webpackChunkName: "seckillorderinfo" */ './views/seckill/OrderInfo.vue')
  },
  {
    path: '/seckillpay',
    name: 'seckillpay',
    component: () => import(/* webpackChunkName: "seckillpay" */ './views/seckill/Pay.vue')
  },
  
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ './views/login/index.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import(/* webpackChunkName: "register" */ './views/register/index.vue')
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
