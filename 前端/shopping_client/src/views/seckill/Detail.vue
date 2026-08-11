<template>
    <div class="con">
        <MainHeader />
        <div class="content">
            <div class="info row">
                <Viewer :imgUrl="detail.headerPic" />
                <div class="inforight">
                    <h3>{{ detail.title }}</h3>
                    <div class="downtime">
                        <span>抢购秒杀</span>
                        <span>
                            <clock-circle-outlined />抢购剩余：
                            <i>{{ downTime }}</i>
                        </span>
                    </div>
                    <p class="pricebox">

                        <label>秒杀价</label>
                        <span class="price">￥<i>{{ detail.costPrice }}</i></span>
                        <span>原价：{{ detail.price }}</span>
                    <p>
                        <label>剩余库存</label>
                        <i>{{ detail.stockCount }}</i>
                    </p>
                    </p>
                    <p style="margin-bottom:10px">
                        <label>服务</label>
                        <a>送货上门</a>
                        <a>七天无理由退货</a>
                        <a>赠送运费险</a>
                    </p>
                    <p>
                        <label>物流</label>
                        <label>现在下单</label>
                        <label>预计明天到达</label>
                    </p>
                    <div class="row opera">
                        <Count @changes="onChangeCount" :value="1" />
                        <button class="primary" @click="onBuy">立即抢购</button>
                    </div>

                </div>
            </div>
            <div class="row">
                <div class="sametype">
                    <Advert title='推荐商品'  />
                </div>
                <div style="flex:1">
                    <a-tabs type="card">
                        <a-tab-pane key="1" tab="商品介绍">
                            <p style="margin:15px 0">
                                <label>品牌：{{ detail.brand }}</label>
                            </p>
                            <div class="box">
                                <p>
                                    <label>商品名称：</label>
                                    <span>{{ detail.title }}</span>
                                </p>
                                <p>
                                    <label>商品类型：</label>
                                    <span>{{ }}</span>
                                </p>
                                <p>
                                    <label>商品编号：</label>
                                    <span>{{ detail.goodsId }}</span>
                                </p>
                                <p>
                                    <label>商品描述：</label>
                                    <span v-html="detail.introduction"/>
                                </p>
                                <p v-for="item in detail.specifications">
                                    <label>{{ item.specName }}</label>
                                    <span>{{ item.specificationOptions.map(item => item.optionName).join('/')
                                    }}</span>
                                </p>


                            </div>

                            <p v-for="item in detail.images" style="text-align:center">
                                <img :src="item.imageUrl" alt="">
                            </p>

                        </a-tab-pane>
                        <!-- <a-tab-pane key="2" tab="商品规格">
                            <p v-for="item in detail.specifications">
                                <label>{{ item.specName }}</label>
                                <span>{{ item.specificationOptions.map(item => item.optionName).join('/') }}</span>
                            </p>
                        </a-tab-pane> -->
                    </a-tabs>
                </div>

            </div>

        </div>
    </div>
    <Footer />

</template>

<script setup>
import { Viewer, MainHeader, Count, Advert, Footer } from '@/components'
import { onMounted, onUnmounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router'
import { ClockCircleOutlined } from '@ant-design/icons-vue'
import { axios, times } from '@/utils'

const { query } = useRoute()
const router = useRouter()
const detail = ref({})
const downTime = ref()
const count = ref(1)
let timer = null

onMounted(() => {
    axios.get('user/seckillGoods/findById', { params: { id: query.id } }).then(data => {
        detail.value = data
        timer = setInterval(() => {
            const { day, hours, minutes, seconds } = times(data.endTime)
            downTime.value = (day <= 0 ? '' : day + ' 天 ') + (hours < 0 ? 0 : hours) + ' 小时 ' + (minutes < 0 ? 0 : minutes) + ' 分 ' + (seconds < 0 ? 0 : seconds) + ' 秒 '

        }, 1000)

    })
})

onUnmounted(() => clearInterval(timer))

const onChangeCount = (e) => {
    console.log(e)
    count.value = e
}


const onBuy = () => {

    router.push({ name: 'seckillorderinfo', params: { ...detail.value, num: count.value } })
}
</script>


<style scoped>
.content {
    width: 70%;
    margin: 30px auto;
}

.con :deep(.header) {
    border-bottom: 2px solid var(--primary-color);
}

.inforight {
    flex: 1;
    margin-left: 40px;


}

.inforight h3 {
    font-weight: 700;
    margin-bottom: 10px;
    font-size: 16px;
}

.pricebox {
    background: #f3f3f3;
    padding: 0px 10px;
    line-height: 32px;
    margin-bottom: 10px;
}

.pricebox span:nth-child(3) {
    color: var(--text-color2);
    text-decoration: line-through;
    margin-left: 15px;
    font-size: 12px;

}

.price i {
    font-size: 22px;
}

.inforight label {
    color: var(--text-color2);
    margin-right: 15px;
    margin-bottom: 15px;
}

.inforight a {
    color: #646fb0 !important;
    margin-right: 8px;
}

.opera {
    align-items: center;
    margin: 15px 0;

}

.opera button {
    margin-left: 20px;
}

.sametype {
    width: 200px;
    border: 1px solid var(--border-color);
    margin-right: 15px;
}

.info {
    margin-bottom: 20px;
}

.content :deep(.ant-tabs-tabpane.ant-tabs-tabpane-active) {
    padding: 15px 20px
}

.content .box {
    line-height: 25px;
    margin-bottom: 40px;
}

.downtime {
    display: flex;
    padding: 10px 8px;
    justify-content: space-between;
    color: #fff;
    background: var(--primary-color)
}

.downtime .anticon {
    margin-right: 5px;

}

.downtime i {
    color: #ffe134
}
</style>