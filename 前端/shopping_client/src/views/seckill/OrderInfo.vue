<template>
    <Header>
        <div class="right">
            <Steps :current="1" />
        </div>
    </Header>
    <div class="content">
        <h3>填写并核对订单信息</h3>
        <div class="box">
            <Address @changes='state.address = $event' />

        </div>
        <div class="box">
            <h4>支付方式</h4>
            <a-radio-group :value="2">
                <!-- <a-radio-button :value="1">
                    <wechat-outlined />微信支付
                </a-radio-button> -->
                <a-radio-button :value="2">
                    <alipay-outlined />支付宝
                </a-radio-button>
            </a-radio-group>

        </div>
        <div class="box list">
            <h4>送货清单</h4>
            <div class="row">
                <span><img :src="detail.headerPic" style="width:100px">
                    {{ detail.title }}</span>

                <b class="price">￥{{ detail.costPrice }}</b>
                X{{ detail.num }}

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
import {  Header, Steps, Footer, Address } from '@/components';
import { reactive } from 'vue'
import { axios } from '@/utils'
import { Input } from 'ant-design-vue';
import { useRouter, useRoute } from 'vue-router';
import { AlipayOutlined } from '@ant-design/icons-vue'


const router = useRouter()
const { params: detail } = useRoute()

const state = reactive({
    paymentType: 2,
    payment: detail.num * detail.costPrice,
    address: {}

})




// 提交订单
const onSubmitOrder = () => {
    const { address } = state
    axios.post('user/seckillGoods/add',
        {
            cartGoods: [{
                goodId: detail.goodsId,
                goodsName: detail.title,
                headerPic: detail.smallPic,
                price: detail.costPrice,
                num: detail.num
            }],
            payment: state.payment,
            paymentType: state.paymentType,
            buyerMessage: state.buyerMessage,
            receiverAreaName: address.receiverAreaName,
            receiverMobile: address.receiverMobile,
            receiverZipCode: address.receiverZipCode,
            receiver: address.receiver,
        }).then(data => {
            router.push({ name: 'seckillpay', 
            params:  data})

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

.box .addBtn {
    position: absolute;
    right: 10px;
    top: 20px
}

.box.address .row p:nth-child(1) {
    width: 120px;
    height: 28px;
    font-size: 15px;
    border: 1px solid var(--border-color);
    text-align: center;
}

.box.address .row.active p:nth-child(1),
.box.address .row:hover p:nth-child(1) {
    border: 2px solid var(--primary-color);
    background: #fff
}

.box.address .row p:nth-child(2) {
    flex: 1;
    padding: 3px 15px
}

.box.address .row:hover {
    background: rgb(234, 238, 234);

}

.box.address .row a {
    display: none;
    margin-right: 8px;
}

.box.address .row:hover a {
    display: block;

}

.box h4 {
    font-weight: bold;
}

.scroll {
    max-height: 260px;
    overflow-y: auto;
}

.opera {
    position: relative;
    top: 10px;
    margin-left: 15px;
    cursor: pointer;
}

.opera .anticon {
    font-size: 12px;
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
    width: 80px;
    height: 80px;
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