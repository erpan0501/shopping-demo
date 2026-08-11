<template>
    <Header>
        <h3 class="right" @click="router.push('/')">
            <home-outlined />首页
        </h3>
    </Header>
    <div class="content">

        <h4>订单中心 > 订单：{{ state.detail.id }}</h4>
        <div class="card">
            <h3>
                <monitor-outlined />订单状态
            </h3>
            <Steps :options="options" :current="state.detail.status-1" />
        </div>
        <div class="card">
            <h3>
                <issues-close-outlined />订单信息
            </h3>
            <div class="row info">
                <div class="box">
                    <b>收货人信息</b>
                    <p>
                        <label>收货人：</label>
                        <span>{{ state.detail.receiver }}</span>
                    </p>
                    <p>
                        <label>收货地址：</label>
                        <span>{{ state.detail.receiverAreaName }}</span>
                    </p>
                    <p>
                        <label>手机号码：</label>
                        <span>{{ state.detail.receiverMobile }}</span>
                    </p>
                </div>
                <div class="box">
                    <b>付款信息</b>
                    <p>
                        <label>付款方式：</label>
                        <span>{{ ['', '微信支付', '支付宝支付'][state.detail.paymentType] }}</span>
                    </p>
                    <p>
                        <label>付款时间：</label>
                        <span>{{ state.detail.paymentTime }}</span>
                    </p>

                </div>
                <div class="box">
                    <b>配送信息</b>
                    <p>
                        <label>物流名称：</label>
                        <span>{{ state.detail.shippingName }}</span>
                    </p>
                    <p>
                        <label>物流单号：</label>
                        <span>{{ state.detail.shippingCode }}</span>
                    </p>

                </div>
            </div>
        </div>
        <div class="card">
            <h3>
                <unordered-list-outlined />订单清单
            </h3>
            <a-table :pagination="false" :columns="state.columns" :data-source="state.detail.cartGoods">
                <template #bodyCell="{ column, record }">
                    <template v-if="column.dataIndex == 'goodsName'">
                        <div class="row" style="align-items:center">
                            <img :src="record.headerPic" alt="" style="width:100px">
                            <p>{{ record.goodsName }}</p>
                        </div>

                    </template>
                    <template v-else-if="column.dataIndex == 'price'">
                        ￥{{ record.price }}
                    </template>


                    <template v-if="column.dataIndex == 'action'">
                        <a @click="onBuy(record)">再次购买</a>

                    </template>
                </template>
            </a-table>
            <div class="total">
                商品总额：<i>￥{{ state.detail.payment }}</i>
                <p class="price">实付款：<i>￥{{ state.detail.payment }}</i></p>
            </div>

        </div>

    </div>
    <Footer/>
</template>

<script setup>
import {  Header, Steps ,Footer} from '@/components'
import { HomeOutlined, UnorderedListOutlined, IssuesCloseOutlined, MonitorOutlined } from '@ant-design/icons-vue';
import { onMounted, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { axios } from '@/utils'
const { query } = useRoute()
const router=useRouter()

const state = reactive({
    detail: {},
    columns: [
        {
            title: '商品',
            dataIndex: 'goodsName',
            width: 400
        },
        {
            title: '商品编号',
            dataIndex: 'goodId',
        },
        {
            title: '商品价格',
            dataIndex: 'price',
        },
        {
            title: '商品数量',
            dataIndex: 'num',
        },
        {
            title: '操作',
            dataIndex: 'action',
        },
    ]
})
const options = [
    { title: "提交订单", description: state.detail.createTime },
    { title: "付款成功" },
    { title: "商品出库" },
    { title: "等待收货" },
    { title: "完成" }
]
onMounted(() => {
    axios.get('user/orders/findById', { params: { id: query.id } }).then(data => {
        state.detail = data
    })

})

const onBuy = (item) => {
    
    router.push('productdetail?id='+item.goodId)

}
</script>

<style scoped>
.content {
    width: 50%;
    margin: 0 auto;
    padding: 15px 0
}

h3:hover {
    color: var(--hover-color)
}

h3 .anticon {
    margin-right: 10px;
    font-size: 14px;
    position: relative;
    top: -2px;
}

h4 {
    margin: 15px 0;
    background: var(--background-color);
    padding: 10px;
    color: #666
}

h3:not(.right) {
    margin-bottom: 20px;

}

.card {
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 0px 5px var(--border-color);
    margin: 20px 0
}

.info {
    justify-content: space-between;
    padding: 15px;

    line-height: 32px;
}

h3:not(.right) .anticon {
    font-size: 23px;
    color: var(--hover-color);
    position: relative;
    top: 3px;
}
.total{
    text-align: right;
    margin-top: 15px;
    line-height: 25px;
    font-weight: bold;
}
.total i{
    margin-left: 20px;
}
</style>