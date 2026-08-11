<template>
    <Header>
        <div class="right">
            <Steps :current="1" />
        </div>
    </Header>
    <div class="content">
        <h3>填写并核对订单信息</h3>
        <div class="box">
            <Address v-if="!isDemoMode" @changes="onAddressChange" />
            <p v-else class="demo-address">演示收货信息：演示用户，13800000000，本地演示地址</p>
        </div>
        <div class="box">
            <h4>支付方式</h4>
            <a-radio-group v-model:value="state.paymentType">
                <a-radio-button :value="1">
                    <wechat-outlined />微信支付
                </a-radio-button>
                <a-radio-button :value="2">
                    <alipay-outlined />支付宝
                </a-radio-button>
            </a-radio-group>

        </div>
        <div class="box list">
            <h4>送货清单</h4>
            <a class="addBtn" @click="router.push('/cart')">返回修改购物车信息</a>
            <div v-for="item in selected" class="row">
                <span><img :src="item.headerPic">
                    {{ item.goodsName }}</span>

                <b class="price">￥{{ item.price }}</b>
                X{{ item.num }}

            </div>

        </div>
        <div class="box msg">
            <h4>留言</h4>
            <Input.TextArea v-model:value="state.buyerMessage" placeholder="请输入给商家的留言" />
        </div>
        <div class="total">商品总金额：<b>￥{{ state.payment }}</b></div>
        <div class="footerbar">
            <p>应付总额：<b class="price">￥{{ state.payment }}</b></p>
            <span>寄送至：{{ state.address.receiverAreaName }}</span>
            <span>收货人：{{ state.address.receiver }}&nbsp;{{ state.address.receiverMobile }}</span>
        </div>
        <button class="primary" @click="onSubmitOrder">提交订单</button>

    </div>
    <Footer />
</template>

<script setup>
import { Nav, Header, Steps, Footer, Address } from '@/components';
import { reactive, ref } from 'vue'
import { axios } from '@/utils'
import { Input } from 'ant-design-vue';
import { useRouter } from 'vue-router';
import { WechatOutlined, AlipayOutlined } from '@ant-design/icons-vue'
import { createDemoOrder, isDemoMode } from '@/utils/demo'

const router = useRouter()
const selected = JSON.parse(sessionStorage.getItem('selectedGoods') || '[]')
const state = reactive({
    address: isDemoMode ? { receiverAreaName: '本地演示地址', receiverMobile: '13800000000', receiverZipCode: '000000', receiver: '演示用户' } : {},
    paymentType: 1,
    payment: selected.reduce((pre, item) => (pre + item.num * item.price), 0),
})


const onAddressChange = (e) => {
    state.address = e
}


// 提交订单
const onSubmitOrder = () => {
    const { address } = state
    if (isDemoMode) {
        createDemoOrder(selected, state.payment, state.paymentType)
        sessionStorage.setItem('selectedGoods', JSON.stringify([]))
        router.push('/order')
        return
    }
    axios.post('user/orders/add',
        {
            cartGoods: selected,
            payment: state.payment,
            paymentType: state.paymentType,
            buyerMessage: state.buyerMessage,
            receiverAreaName: address.receiverAreaName,
            receiverMobile: address.receiverMobile,
            receiverZipCode: address.receiverZipCode,
            receiver: address.receiver,
        }).then(data => {
            sessionStorage.setItem('selectedGoods', JSON.stringify([]))
            window.dispatchEvent( new CustomEvent('cartNumChange'))
            router.push({ name: 'pay', params: { orderId: data.id, payment: data.payment, paymentType: state.paymentType } })

        })
}
</script>

<style scoped>
.content {
    width: 50%;
    margin: 0 auto;
    padding-bottom: 20px;
    position: relative;

}

.right {
    position: absolute;
    top: 50px;
    right: 0
}

h3 {
    margin: 15px 0
}

.box {
    border: 1px solid var(--border-color);
    padding: 20px;
    position: relative;
    border-bottom: none;
}



.box.address .row {
    margin-left: 15px;
    align-items: center;
    margin-top: 15px;
    cursor: pointer;
    padding-right: 15px;
}

.demo-address {
    padding: 12px 0;
    color: var(--text-color2);
}

.box .addBtn {
    position: absolute;
    right: 10px;
    top: 20px
}


.box h4 {
    font-weight: bold;
}

.scroll {
    max-height: 260px;
    overflow-y: auto;
}


.box :deep(.ant-radio-button-wrapper) {
    margin: 10px 15px
}

.box :deep(.ant-radio-button-wrapper .anticon) {
    margin-right: 5px;
}

.box :deep(.anticon-wechat) {
    color: #10a63ed1
}

.box :deep(.anticon-alipay) {
    color: #1890ff
}

.msg {
    border-bottom: 1px solid var(--border-color);
}


.list .row {
    justify-content: space-around;
    align-items: center;
}

.list .row img {
    width: 100px;
}

.total {
    text-align: right;
    margin: 15px 5px
}

.total b {
    margin-left: 20px;
}

.footerbar {
    padding: 15px;
    background: var(--background-color);
    text-align: right;
    line-height: 28px;
}

.footerbar .price {
    margin-left: 15px;
    font-size: 20px;
}

.footerbar span {
    margin-left: 20px;
    color: #999
}

button.primary {
    position: absolute;
    right: 0;
    margin-top: 5px;
    font-size: 16px;
    font-weight: bold;
}
</style>
