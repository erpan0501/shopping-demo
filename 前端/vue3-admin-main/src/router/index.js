import { createRouter, createWebHashHistory } from 'vue-router'
import Layout from '@/layout'
import config from '@/config'

const routes = [
  {
    path: '/',
    redirect:'/user/admin',
    component: Layout,
    children: [
      {
        path: '/user/admin',
        name: 'admin',
        component: () => import(/* webpackChunkName: "useradmin" */ '../views/user/UserView.vue')
      },
      {
        path: '/user/role',
        name: 'role',
        component: () => import(/* webpackChunkName: "userrole" */ '../views/role/RoleView.vue')
      },
      {
        path: '/user/permission',
        name: 'permission',
        component: () => import(/* webpackChunkName: "userpermission" */ '../views/permission/PermissionView.vue')
      },
      {
        path: '/product/brand',
        name: 'brand',
        component: () => import(/* webpackChunkName: "probrand" */ '../views/brand/BrandView.vue')
      },
      {
        path: '/product/types',
        name: 'types',
        component: () => import(/* webpackChunkName: "protype" */ '../views/types/TypesView.vue')
      },
      {
        path: '/product/specifi',
        name: 'specifi',
        component: () => import(/* webpackChunkName: "prospecifi" */ '../views/specifi/SpecifiView.vue')
      },
      {
        path: '/product/manage',
        name: 'product',
        component: () => import(/* webpackChunkName: "promanage" */ '../views/good/GoodView.vue')
      },
      {
        path: '/website/advert',
        name: 'advert',
        component: () => import(/* webpackChunkName: "websiteadvert" */ '../views/advert/AdvertView.vue')
      },
      {
        path: '/product/seckill',
        name: 'seckill',
        component: () => import(/* webpackChunkName: "seckill" */ '../views/seckill/SeckillView.vue')
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '../views/Login.vue')
  }]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
