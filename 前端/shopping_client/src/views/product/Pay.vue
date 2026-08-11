<template>
    <Header>
        <div class="right">
            <Steps :current="2" />
        </div>
    </Header>
    <div class="content">
        <div class="total">应付金额：<b class="price">￥{{ params.payment }}</b></div>
        <h4>订单编号：{{ params.orderId }}</h4>
        <div class="box">
            <h3><i>{{ params.paymentType == 1 ? '微信支付' : '支付宝支付' }}</i></h3>
            <div class="qrcode">
                <qrcode-vue :value="state.imgUrl" :size="260" level="H" foreground="#2d2828"/>
                <div>
                    <scan-outlined />
                    {{ params.paymentType == 1 ? '请使用微信扫描二维码付款' : '请使用支付宝扫描二维码付款' }}
                </div>
            </div>

        </div>
    </div>
    <Footer />
</template>

<script setup>
import {  Header, Steps, Footer } from '@/components'
import { useRoute } from 'vue-router';
import QrcodeVue from "qrcode.vue"
import { onMounted, reactive, ref } from 'vue';
import {ScanOutlined} from  '@ant-design/icons-vue'
import { axios } from '@/utils'

const { params } = useRoute()
const state = reactive({
    imgUrl: ''
})
onMounted(() => {
    axios.post('user/payment/pcPay?orderId='+params.orderId).then(data => {
    state.imgUrl = data

    })
})
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

.qrcode {
    position: relative;
    top: 40px;
    left: 100px
}

.qrcode div {
    width: 260px;
    padding: 20px 0;
    font-size: 16px;
    background: var(--primary-color);
    color: #fff;
    margin-top: 15px;
    display: flex;
    align-items: center;
    padding:10px 20px

}
.qrcode div .anticon{
    font-size: 40px;
    margin-right: 16px;

}
h3{
    margin-top:20px;
    margin-left: 20px;
    color: var(--primary-color);
}
</style>