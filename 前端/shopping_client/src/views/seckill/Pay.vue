<template>
    <Header>
        <div class="right">
            <Steps :current="2" />
        </div>
    </Header>
    <div class="content">
        <div class="total">应付金额：<b class="price">￥{{ params.payment }}</b></div>
        <h4>订单编号：{{ params.id }}</h4>
        <div class="box">
            <div style="width:50%;text-align:center">
                <template v-if="!payeResult">
                    <button class="primary" @click="onPay">立即付款</button>
                    <p>距离订单过期还有：{{ downTime }}</p>
                </template>
                <template v-else>
                   <p style="margin-top: 200px;">
                    <check-circle-outlined v-if="payeResult=='成功'" style="font-size: 28px;color:#52c41a;position: relative;top:4px"/> 
                    <close-circle-outlined v-else style="font-size: 28px;color:var(--primary-color);position: relative;top:4px"/> 
                    支付{{payeResult}}</p>
                </template>
                

            </div>
           
        </div>

    </div>
    <Footer />
</template>

<script setup>
import { Header, Steps, Footer } from '@/components'
import { useRoute } from 'vue-router';
import { onBeforeMount, onUnmounted, ref } from 'vue';
import { axios, times } from '@/utils'
import { CheckCircleOutlined,CloseCircleOutlined } from '@ant-design/icons-vue'

const { params } = useRoute()
const downTime = ref()
const payeResult = ref()

let timer = null
onBeforeMount(() => {
    timer = setInterval(() => {
        const { day, hours, minutes, seconds } = times(params.expire)
        downTime.value = (day <= 0 ? '' : day + ' 天 ') + (hours < 0 ? 0 : hours) + ' 小时 ' + (minutes < 0 ? 0 : minutes) + ' 分 ' + (seconds < 0 ? 0 : seconds) + ' 秒 '
    }, 1000)
})
onUnmounted(() => {
    clearInterval(timer)
})

const onPay = () => {
    axios.get('user/seckillGoods/pay', { params: { id: params.id } }).then(data => {
        payeResult.value ='成功' 
    }).catch(e=>{
        
        payeResult.value =e.message||'失败' 
    })
}
</script>

<style scoped>
.right {
    position: absolute;
    top: 50px;
    right: 0
}

.content {
    width: 50%;
    margin: 15px auto
}

.total {
    text-align: right;
    font-size: 15px;
}

.total .price {
    font-size: 18px;
}

.box {
    width: 100%;
    height: 500px;
    border: 1px solid var(--border-color);
    background: url(../../assets/scan.jpg) no-repeat;
    background-position: 400px;
}

.box button {
    margin-top: 200px;
    font-size: 16px;
    margin-bottom: 20px;

}

.box p {
    font-size: 20px;
    font-weight: bold;
}





h3 {
    margin-top: 20px;
    margin-left: 20px;
    color: var(--primary-color);
}
</style>