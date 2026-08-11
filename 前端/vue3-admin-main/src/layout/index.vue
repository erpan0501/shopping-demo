<template>
    <el-aside width="260px">
        <el-menu :router="true" active-text-color="#1BAEAE" background-color="#545c64" class="el-menu-vertical-demo"
            text-color="#fff">
            <template v-for="(menu) in config.menus">
                <el-sub-menu :index="menu.index" v-if="menu.children && menu.children.length">
                    <template #title>
                        <component :is="menu.icon" class="icon"></component>
                        <span>{{ menu.title }}</span>
                    </template>
                    <el-menu-item :index="menu.index + child.index" v-for="(child) in menu.children">
                        {{ child.title }}
                    </el-menu-item>
                </el-sub-menu>

                <el-menu-item v-else>{{ menu.title }}</el-menu-item>
            </template>
        </el-menu>
    </el-aside>
    <el-container>
        <el-header>
            <el-row>
                <el-col :span="20">
                    <el-breadcrumb :separator-icon="ArrowRight">
                        <el-breadcrumb-item v-for="item in breadcrumbs">
                            {{ item }}
                        </el-breadcrumb-item>
                    </el-breadcrumb>
                </el-col>
                <el-col :span="4" style="text-align:right">
                    <span style="margin-right: 20px ">您好：{{ userName }}</span>
                    <el-button link @click="onLogout">
                        <a>
                            退出
                        </a>
                    </el-button>
                </el-col>
            </el-row>
        </el-header>
        <el-main>
            <router-view></router-view>
        </el-main>
    </el-container>
</template>
<script setup>
import { onBeforeMount, onMounted, onUnmounted, onUpdated, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import config from '../config.js'
import { ArrowRight } from '@element-plus/icons-vue'
import axios from '@/utils/axios'

const router = useRouter()
const currentRoute = useRoute()
const breadcrumbs = ref([])
console.log(breadcrumbs, 'breadcrumbts')
const userName = ref('')

const onGetBreadcrumbs = (path) => {
    breadcrumbs.value = []
    // to代表要导航到的路由
    const paths = path.split('/')
    // 获取面包屑需要的数据
    const getBreadcrumb = (menus) => {
        menus.map(menu => {
            paths.map(item => {
                if ('/' + item == menu.index) {
                    breadcrumbs.value.push(menu.title)
                }
            })
            if (menu.children) {
                getBreadcrumb(menu.children)

            }

        })
    }
    getBreadcrumb(config.menus)
}
onBeforeMount(() => {

    onGetBreadcrumbs(currentRoute.path)
})
router.afterEach(to=>{
    onGetBreadcrumbs(to.path)
})
const onLogout = () => {
    axios.post('admin/logout').then(data => {
        router.push('/login')
        // window.location='/#/login'
    })
}
onMounted(() => {
    // 获取登录的用户名
    axios.get('admin/getUsername').then(data => {
        // window.sessionStorage.setItem('user',data)
        userName.value = data
    })
})
onUnmounted(() => {
    // unwatch()
})
</script>

<style lang="scss" scoped>
.el-header {
    --el-header-padding: 20px !important;
    box-shadow: 5px 3px 5px #d1dbe5;
    box-sizing: border-box;
    background-color: #fff;
}

.el-menu {
    height: 100%
}

.icon {
    width: 15px;
    height: 15px;
    margin-right: 6px
}

.el-breadcrumb {
    font-size: inherit;
}
</style>
