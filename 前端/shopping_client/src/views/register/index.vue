<template>
    <Header title="注册">
        <span class="right">已有账号？<a href="/#/login">登录>></a></span>
    </Header>
    <div class="content">
        <div class="steps">
            <a-steps :current="state.current">
                <a-step v-for="item in steps" :key="item.title" :title="item.title" />
            </a-steps>
            <form v-if="state.current == 0">
                <div class="row">
                    <div style="flex:1">
                        <div class="form-item">
                            <div class="form-control">
                                <input type="text" v-model="state.phone" placeholder="请输入手机号">
                                <span class="error" v-if="state.phoneErr">请输入手机号</span>
                            </div>

                        </div>
                        <div class="form-item ">
                            <div class="form-control">
                                <input type="text" v-model="state.checkCode" placeholder="请输入验证码">
                                <span class="error" v-if="state.checkCodeErr">请输入验证码</span>
                            </div>
                           

                        </div>
                         <Alert type="fail" v-if="state.checkCodeedErr" >
                            {{state.checkCodeedErr}}
                            </Alert>
                    </div>
                    <button :disabled="state.disabled" class="primary" style="margin-left:8px;" @click="onSendMsg">

                        {{ state.disabled ? `重新获取（${state.count}s）` : '获取验证码' }}
                    </button>
                    <Alert v-if="state.sendingMsg === false" style="position: absolute;right: 0;top: 48px">发送成功
                    </Alert>

                </div>

            </form>
            <form v-if="state.current == 1">
                <div class="form-item">
                    <label>用户名</label>
                    <div class="form-control">
                        <input type="text" v-model="state.username">
                        <span class="error" v-if="state.usernameErr">请输入用户名</span>
                    </div>

                </div>
                <div class="form-item">
                    <label>用户密码</label>
                    <div class="form-control">
                        <input type="text" v-model="state.password">
                        <span class="error" v-if="state.passwordErr">请输入密码</span>
                    </div>

                </div>
            </form>
            <div v-if="state.current == 2" class="result">
                恭喜您！注册成功，
                即将为您跳转到登陆页面...

            </div>
            <div class="steps-action">
                <button v-if="state.current < steps.length - 1" class="primary" @click="next">下一步</button>
                <button v-if="state.current == steps.length - 1" class="primary" @click="router.push('/login')">
                    完成
                </button>
                <button v-if="state.current > 0" style="margin-left: 8px" @click="prev">上一步</button>
            </div>

        </div>
    </div>
    <Footer />


</template>

<script setup>
import { Header, Footer, Alert } from '@/components';
import { reactive } from 'vue';
import { axios } from '@/utils'
import { useRouter } from 'vue-router';


const router = useRouter()


const state = reactive({
    current: 0,
    count: 60,
})
const steps = [
    { title: '验证手机号' },
    { title: '填写账号信息' },
    { title: '注册成功' }
]
const next = () => {
    if (state.current == 0) {
        !state.phone ? state.phoneErr = true : state.phoneErr = false
        !state.checkCode ? state.checkCodeErr = true : state.checkCodeErr = false
        if (state.phoneErr || state.checkCodeErr) {
            return
        }
        axios.get('user/shoppingUser/registerCheckCode', {
            params: { checkCode: state.checkCode, phone: state.phone }
        }).then(data => {
            state.current++
        }).catch(e => {
            state.checkCodeedErr=e.message

        })

        return
    }
    if (state.current == 1) {
        onRegister()
    }
};
const prev = () => {
    state.current--

};

// 发送手机验证码
const onSendMsg = () => {
    !state.phone ? state.phoneErr = true : state.phoneErr = false
    if (state.phoneErr) {
        return
    }
    state.sendingMsg = true
    let timer = null
    state.disabled = true
    state.count = 60
    timer = setInterval(() => {
        state.count--
        if (state.count == 0) {
            clearInterval(timer)
            state.disabled = false
        }
    }, 1000)
    axios.get('user/shoppingUser/sendMessage', { params: { phone: state.phone } }).then(data => {
        state.sendingMsg = false

    })
}
// 注册
const onRegister = () => {
    !state.username ? state.usernameErr = true : state.usernameErr = false
    !state.password ? state.passwordErr = true : state.passwordErr = false
    !state.phone ? state.phoneErr = true : state.phoneErr = false
    !state.checkCode ? state.checkCodeErr = true : state.checkCodeErr = false
    if (state.usernameErr || state.phoneErr || state.passwordErr || state.checkCodeErr) {
        return
    }
    axios.post('user/shoppingUser/register?checkCode=' + state.checkCode, { phone: state.phone, username: state.username, password: state.password })
        .then(data => {
            state.current++
            setTimeout(() => {
                router.push('/login')

            }, 2000)
        })
}

</script>

<style scoped>
.right {
    position: absolute;
    right: 0;
    top: 50px;
}


.content {
    width: 100%;
    height: 500px;
    background: url(../../assets/beijingbj.png);
    background-size: auto 100%;
    display: flex;
    justify-content: center;
}

.steps {
    margin-top: 80px;
    width: 600px;
}

form {
    width: 400px;
    margin: 50px auto
}

.form-box {
    width: 405px;
    margin-top: 80px;
}

label {
    display: flex;
    width: 80px;
    align-items: center;
    justify-content: flex-end;
    margin-right: 15px;
}

.form-item {
    border: none
}

input {
    border: 1px solid var(--border-color);
    border-radius: 3px;
}

.steps-action {
    text-align: center;
}

.result {
    font-size: 20px;
    color: var(--primary-color);
    text-align: center;
    line-height: 200px;
}
</style>