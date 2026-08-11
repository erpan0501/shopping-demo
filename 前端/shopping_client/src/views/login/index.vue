<template>
    <Header title="登录">
        <h3 @click="router.push('/')">
           <home-outlined />首页
        </h3>
    </Header>
    <div class="content">
        <div class="form-box">
            <ul>
                <li @click="state.selected = USER_LOGIN" :class="{ active: state.selected == USER_LOGIN }">
                    账户登录
                </li>
                <li @click="state.selected = PHONE_LOGIN" :class="{ active: state.selected == PHONE_LOGIN }">手机验证登录
                </li>
            </ul>
            <form v-if="state.selected == USER_LOGIN" @submit.prevent="onLoginByUser">
                <div class="form-item">
                    <label />
                    <div class="form-control">
                        <input type="text" v-model="state.username" placeholder="请输入用户名">
                        <span class="error" v-if="state.usernameErr">请输入用户名</span>
                    </div>

                </div>
                <div class="form-item">
                    <label />
                    <div class="form-control">
                        <input type="password" v-model="state.password" placeholder="请输入密码">
                        <span class="error" v-if="state.passwordErr">请输入密码</span>
                    </div>

                </div>
                <div class="warn" @click="router.push('/register')">还没有账号？立即注册>></div>
                <button type="submit" class="primary block">
                    <h2>登录</h2>
                </button>
            </form>
            <form v-if="state.selected == PHONE_LOGIN" @submit.prevent="onLoginByCheckCode">
                <div class="row" style="position:relative">
                    <div style="flex:1">
                        <div class="form-item form-control">
                            <input type="text" v-model="state.phone" placeholder="请输入手机号">
                            <span class="error" v-if="state.phoneErr">请输入手机号</span>
                        </div>
                        <div class="form-item form-control">
                            <input type="text" v-model="state.checkCode" placeholder="请输入验证码">
                            <span class="error" v-if="state.checkCodeErr">请输入验证码</span>
                        </div>
                    </div>
                    <button type="button" :disabled="state.disabled" class="primary" style="margin-left:8px;" @click="onSendMsg">
                       {{state.disabled?`重新获取（${state.count}s）`:'获取验证码'}} 
                    </button>
                    <Alert v-if="state.sendingMsg === false" style="position: absolute;right: 0;top: 48px">发送成功</Alert>

                </div>
                <div class="warn" @click="router.push('/register')">还没有账号？立即注册>></div>
                <button type="submit" class="primary block" :disabled="!state.phone || !state.checkCode">
                    <h2>登录</h2>
                </button>
            </form>
        </div>
    </div>
    <Footer />
</template>
<script setup>
import { Header, Alert, Footer } from '@/components'
import { reactive } from 'vue';
import { axios } from '@/utils'
import { useRouter } from 'vue-router'
import { HomeOutlined } from '@ant-design/icons-vue'

const USER_LOGIN = 1;
const PHONE_LOGIN = 2;
const isDemoMode = process.env.VUE_APP_DEMO_MODE !== 'false'
const state = reactive({
    selected: USER_LOGIN,
    disabled:false,
    count:60
})

const router = useRouter()
// 用户名密码登录
const onLoginByUser = () => {
    !state.username ? state.usernameErr = true : state.usernameErr = false
    !state.password ? state.passwordErr = true : state.passwordErr = false
    if (state.usernameErr || state.passwordErr) {
        return
    }
    if (isDemoMode) {
        sessionStorage.setItem('token', 'demo-token')
        sessionStorage.setItem('displayName', state.username)
        router.push('/')
        return
    }
    axios.post('user/shoppingUser/loginPassword', { username: state.username, password: state.password }).then(data => {
        
        sessionStorage.setItem('token', 'Bearer '+data)
        router.push('/')
    })
}

// 发送手机验证码
const onSendMsg = () => {
    !state.phone ? state.phoneErr = true : state.phoneErr = false
    if (state.phoneErr) {
        return
    }

    state.sendingMsg = true
    let timer=null
    state.disabled=true
    state.count=60
    timer=setInterval(()=>{
        state.count--
        if(state.count==0){
            clearInterval(timer)
            state.disabled=false
        }
    },1000)
    axios.get('user/shoppingUser/sendLoginCheckCode', { params: { phone: state.phone } }).then(data => {
        state.sendingMsg = false
    })
}
// 通过手机验证码登录
const onLoginByCheckCode = () => {
    !state.phone ? state.phoneErr = true : state.phoneErr = false
    !state.checkCode ? state.checkCodeErr = true : state.checkCodeErr = false
    if (state.phoneErr || state.checkCodeErr) {
        return
    }
    if (isDemoMode) {
        sessionStorage.setItem('token', 'demo-token')
        sessionStorage.setItem('displayName', state.phone)
        router.push('/')
        return
    }
    axios.post('user/shoppingUser/loginCheckCode?phone='+state.phone+'&&checkCode='+state.checkCode ).then(data => {
        sessionStorage.setItem('token', data)
        router.push('/')
    })
}

</script>

<style scoped>
.content {
    width: 100%;
    height: 500px;
    background: url(../../assets/beijingbj.png);
    background-size: auto 100%;
    display: flex;
    align-items: center;
    justify-content: flex-end;
}

.form-box {
    width: 350px;
    border-radius: 10px;
    background: #fff;
    overflow: hidden;
    box-shadow: 0 0 15px #ddd;
    margin-right: 240px;
    padding-bottom: 30px;
}

ul {
    display: flex;
    list-style: none;
    border-bottom: 1px solid var(--border-color);
}

ul li {
    flex: 1;
    text-align: center;
    font-size: 18px;
    padding: 20px 0;
    font-weight: 500;
    cursor: pointer;
}

.active {
    color: var(--primary-color);

}

form {
    padding: 25px
}


.form-item label {
    /* display: block; */
    width: 35px;
    /* height: 100%; */
}

form .form-item:nth-child(1) label {
    background: url(../../assets/pwd-icons-new.png);
}

form .form-item:nth-child(2) label {
    background: url(../../assets/pwd-icons-new.png);
    background-position: -48px 0px;
}

form input {
    border: none;
    flex: 1;
    padding-left: 10px;
    height: 100%;
}


form input:focus {
    outline: none
}

.warn {
    color: var(--primary-color);
    cursor: pointer;
    text-align: right;
    font-size: 12px;
    text-decoration: underline;
    margin-bottom: 20px;
}



h2 {
    font-weight: normal;
}

h3 {
    position: absolute;
    right: 0;
    top: 50px;
    cursor: pointer;
}
h3:hover{
    color:var(--hover-color)
}

h3 .anticon {
    margin-right: 10px;
    font-size: 14px;
    position: relative;
    top: -2px;
    

}
</style>
