<template>
    <div class="nav">
        <div class="box row">
            <div class="row">
                <p @click="router.push('/')">商城首页</p>
                <p>我的收藏</p>
                <p @click="router.push('/order')">我的订单</p>
            </div>
            <div class="row">
                <p v-if="username">你好，{{ username }}</p>
                <p @click="router.push('/login')" v-else>你好，请登录</p>
                <p @click="router.push('/register')">注册</p>
                <p @click="router.push('/cart')" class="cart">
                    <a-badge :count="count" size="small">
                        <shopping-cart-outlined />
                    </a-badge>
                    <span style="margin-left:10px">购物车</span>
                </p>
                <p v-if="username" @click="onLogout">
                    退出
                    <logout-outlined style="font-size: 12px" />
                </p>
            </div>
        </div>

    </div>
</template>

<script setup>
import { ShoppingCartOutlined, LogoutOutlined } from '@ant-design/icons-vue';
import { useRouter, useRoute } from 'vue-router';
import { Badge as ABadge } from 'ant-design-vue'
import { onBeforeMount, onMounted, ref } from 'vue';
import { axios } from '@/utils'


const router = useRouter()
const { path } = useRoute()
const count = ref(0)
const username = ref('')
const isDemoMode = process.env.VUE_APP_DEMO_MODE !== 'false'
const onGetCarrList = () => {
    if (isDemoMode) {
        count.value = 0
        return
    }
    axios.get('user/cart/findCartList').then((data = []) => {
        count.value = data.reduce((pre, item) => (pre + item.num), 0)

    })
}
const refreshProfile = () => {
    const token=sessionStorage.getItem('token')
    if (token) {
        if (isDemoMode) {
            username.value = sessionStorage.getItem('displayName') || '演示用户'
            count.value = 0
            return
        }
        onGetCarrList()
        axios.get('user/shoppingUser/getName').then(data => {
            username.value = data
        })
    }else{
        count.value = 0
        username.value = ''
    }
}
router.beforeEach(() => {
    refreshProfile()
})


// onBeforeMount(() => {

//     if (path == '/') {
//         return true
//     }
//     onGetCarrList()
//     // 获取登录的用户名
//     axios.get('user/shoppingUser/getName').then(data => {
//         username.value = data

//     })
// })
onMounted(() => {
    refreshProfile()
    window.addEventListener('cartNumChange', (e) => {
        console.log(e.detail)
        if (!e.detail && e.detail !== 0) {
            onGetCarrList()
        } else {

            count.value = e.detail
        }
    })

})
const onLogout = () => {
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('displayName')
    router.push('/login')
}
</script>
<style scoped>
.nav {
    background: #aaaaaa2e;

}

.box {
    width: 60%;
    margin: 0 auto;
    /* color:#fff; */
    justify-content: space-between;
}

p {
    padding: 5px 10px;
    cursor: pointer;
}

p:hover,
p:hover .anticon {
    color: var(--hover-color)
}

.anticon-shopping-cart {
    margin-right: 5px;

}

.cart {
    background: #aaaaaa38;
}

.cart :deep(.ant-badge-count) {
    background: var(--primary-color);
    box-shadow: none;
}
</style>
