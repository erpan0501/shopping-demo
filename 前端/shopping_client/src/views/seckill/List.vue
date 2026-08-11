<template>
    <MainHeader />
    <div class="banner">
        <h1>商城秒杀</h1>

    </div>
    <div class="content">

        <img src="../../assets/wang.jpg" alt="" />
        <div class="row">
            <div class="box" v-for="item in state.data">

                <img :src="item.headerPic" alt="">
                <h3>{{ item.title }}</h3>
                <p class="price">￥<i>{{ item.price }}</i></p>
                <p class="row">
                <p style="width:90px">已售{{ (((item.num - item.stockCount) / item.num) * 100).toFixed(0) }}%</p>
                <Progress :showInfo="false" strokeColor="var(--primary-color)"
                    :percent="(((item.num - item.stockCount) / item.num) * 100).toFixed(0)" />
                </p>
                <div class="row" style="justify-content:space-between;align-items: center;margin-top: 10px;">
                    <p style="width:150px">剩余<b class="price">{{ item.stockCount }}</b>件</p>
                    <button class="primary" @click="onDetail(item)">立即抢购</button>
                </div>
            </div>
        </div>

        <div class="pagination">
            <a-pagination v-model:current="state.pagination.page" :total="state.total" show-less-items
                @change="onPageChange" />
        </div>
    </div>
    <Footer />
</template>

<script setup>
import { MainHeader, Footer } from '@/components';
import { onMounted, reactive } from 'vue';
import { Progress } from 'ant-design-vue'
import { axios } from '@/utils'
import { useRouter } from 'vue-router';
import { demoProducts, isDemoMode } from '@/utils/demo'

const router = useRouter()

const state = reactive({
    data: [],
    pagination: { page: 1, size: 40 },
    total: 0
})

const onGetList = () => {
    if (isDemoMode) {
        state.data = demoProducts.map((item, index) => ({
            goodsId: item.id,
            title: item.goodsName,
            price: item.price,
            headerPic: item.headerPic,
            num: 100,
            stockCount: 80 - index * 5,
        }))
        state.total = state.data.length
        return
    }
    axios.get('user/seckillGoods/findPage', { params: { page: state.pagination.page, size: 40 } }).then(data => {
        state.data = data.records;
        state.total = data.total
    })

}
onMounted(() => {
    onGetList()
    window.dispatchEvent(new Event('changeKeyword'))
}
)
const onPageChange = (page) => {
    state.pagination.page = page
    onGetList()
}

const onDetail = (item) => {
    if (isDemoMode) {
        router.push({ path: '/productdetail', query: { id: item.goodsId } })
        return
    }
    router.push('seckilldetail?id='+item.goodsId)
}
</script>

<style scoped>
.content {
    width: 60%;
    margin: 0 auto;
    padding-bottom: 50px;
}

.banner {
    width: 80%;
    margin: 0 auto;
    height: 90px;
    line-height: 90px;
    background: url(../../assets/header_bgV2.png);
    text-align: center;

}

.banner h1 {
    font-size: 30px;
    font-weight: bold;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif
}

.content img {
    width: 100%
}

.content .box {
    width: 25%;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 0px 5px var(--border-color);
    margin: 20;
    margin-top: 20px;
    margin-right: 20px
}

.price {
    font-size: 15px;
    margin: 6px 0
}
</style>
