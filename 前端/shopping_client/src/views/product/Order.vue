<template>
    <Header>
        <h3 class="right" @click="router.push('/')">
            <home-outlined />首页
        </h3>
    </Header>
    <div class="content row">
        <div class="left">
            <div class="box">
                <p><b>订单中心</b></p>
                <span>我的订单</span>
            </div>
            <div class="box">
                <p><b>设置</b></p>
                <span >收货地址</span>
            </div>
        </div>
        <div class="right">
            <h3>我的订单</h3>
            <div class="thead row">
                <p class="th">订单详情</p>
                <p class="th">收货人</p>
                <p class="th">金额</p>
                <p class="th">
                    <a-dropdown :trigger="['click']">
                        <span style="cursor:pointer" @click.prevent>
                            全部状态
                            <DownOutlined />
                        </span>
                        <template #overlay>
                            <a-menu @click="onGetOrder">
                                <p v-for="(item, index) in statuses">
                                    <a-menu-item :key="index">
                                        {{ item }}
                                    </a-menu-item>
                                    <!-- <a-menu-divider /> -->
                                </p>
                            </a-menu>
                        </template>
                    </a-dropdown>
                </p>
                <p class="th">操作</p>
            </div>
            <div v-for="order in state.data" class="orderbox">
                <p class="des">
                    {{ order.createTime }}
                    <span>订单号：<i>{{ order.id }}</i></span>
                </p>
                <div class="row tr">
                    <p class="td">
                        <template v-for="item in order.cartGoods">
                            <div class="row" @click="router.push({ path: '/productdetail', query: { id: item.goodId } })">
                                <img :src="item.headerPic" style="width:80px">
                                <span class="name">{{ item.goodsName }}</span>
                                <span class="num">x{{ item.num }}</span>
                            </div>
                        </template>

                    </p>
                    <p class="td">
                        <a-popover>
                            <template #content>
                                <p>{{ order.receiver }}

                                </p>
                                <p>{{ order.receiverAreaName }}</p>
                                <p>{{ order.receiverMobile }}</p>
                            </template>
                            <i>{{ order.receiver }}
                                <user-outlined />
                            </i>
                        </a-popover>
                    </p>
                    <p class="td">
                        ￥{{ order.payment }}
                    </p>
                    <p class="td">
                        {{ statuses[order.status] }}
                    </p>
                    <p class="td">
                        <a class="" @click="onDetail(order)">订单详情</a><br />
                        <a v-if="order.status==1" @click="onPay(order)">立即付款</a><br />
                    </p>
                </div>
            </div>
        </div>
    </div>
    <Footer />
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import {  Header, Footer } from '@/components'
import { HomeOutlined, DownOutlined } from '@ant-design/icons-vue';
import { useRouter } from 'vue-router';
import { UserOutlined } from '@ant-design/icons-vue'
import { axios } from '@/utils'
import { getDemoOrders, isDemoMode } from '@/utils/demo'

const router = useRouter()
const statuses = ['', '未付款', '已付款', '未发货', '已发货', '交易成功', '交易关闭', '待评价']
const state = reactive({
    data: []
})

const onGetOrder = (item = {}) => {
    if (isDemoMode) {
        state.data = getDemoOrders()
        return
    }
    axios.get('user/orders/findUserOrders',{params:{status:item.key}}).then(data=>{
    state.data=data

    })

}
onMounted(onGetOrder)

const onDetail=(item)=>{
    
    router.push('orderdetail?id='+item.id)
}

const onPay=(item)=>{
    router.push({name:'pay',params:{orderId:item.id,payment:item.payment,paymentType:item.paymentType}})
}

</script>

<style scoped>
h3:hover {
    color: var(--hover-color)
}

h3 .anticon {
    margin-right: 10px;
    font-size: 14px;
    position: relative;
    top: -2px;
}

.td .anticon {
    margin-left: 5px;
}

.box {
    margin: 15px;
    line-height: 25px;
}

.box span:hover {
    cursor: pointer;
    color: var(--hover-color)
}

.content {
    width: 60%;
    margin: 0 auto;
    margin-top: 15px;


}

.content .left {
    width: 110px
}

.content .right {
    flex: 1
}

.right h3 {
    margin: 15px 0;

}

.orderbox {
    border: 1px solid var(--border-color);
    margin-bottom: 15px;
    background: #fff;
}

.thead {
    justify-content: space-between;
    background: #f5f5f5;
    height: 32px;
    line-height: 32px;
    color: #666;
    padding: 0 10px;
    margin-bottom: 15px;
}

.tr {
    padding: 0 10px
}

.des {
    background: #f5f5f5;
    height: 31px;
    line-height: 31px;
    padding: 0 10px;
    color: #aaa
}

.des span {
    margin-left: 15px;

}

.des span i {
    color: initial;

}

.tr {
    align-items: center;
}

.tr .td,
.thead .th {
    flex: 1;
    /* text-align: center; */
}

.tr .td:nth-child(1),
.thead .th:nth-child(1) {
    min-width: 500px
}

.tr .td:nth-child(1) .row {
    justify-content: space-around;
    align-items: center;
    padding-right: 15px;
    cursor: pointer;
}

.tr .td:last-child {
    font-size: 12px;
}

.tr .td .name {
    display: block;
    width: 250px;
}
.tr .td .name:hover{
    color:var(--hover-color)
}
.td{
    padding:8pxc
}
</style>
