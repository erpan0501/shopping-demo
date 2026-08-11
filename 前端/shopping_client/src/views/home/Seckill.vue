<template>
    <div class="row" >
        <h1 @click="router.push('/seckill')">
            <p>正在秒杀</p>
            <h5>点击进入秒杀会场</h5>
            <p class="warn">
                <b>20:00</b>点场&nbsp;距结束
            </p>
            <p class="timer">
                <span class="unit">{{ time.hours }}</span>
                <b>:</b>
                <span class="unit">{{ time.minutes }}</span>
                <b>:</b>
                <span class="unit">{{ time.seconds }}</span>

            </p>
        </h1>
        <!-- <div style="flex:1"> -->
        <a-carousel :arrows="true">
            <template #prevArrow>
                <div class="custom-slick-arrow" style="left:5px">
                    <left-outlined />
                </div>
            </template>
            <template #nextArrow>
                <div class="custom-slick-arrow" style="right: 5px">
                    <right-outlined />
                </div>
            </template>
            <div>
                <div class="row">
                    <div v-for="item in data" class="item" @click="onView(item)">
                        <img :src="item.url" alt="">
                        <span class="title">{{ item.name }}</span>
                        <span class="price">￥{{ item.price }}</span>

                    </div>
                </div>
            </div>
            <div>
                <div class="row">
                    <div v-for="item in data" class="item" @click="onView(item)">
                        <img :src="item.url" alt="">
                        <span class="title">{{ item.name }}</span>
                        <span class="price">￥{{ item.price }}</span>

                    </div>
                </div>
            </div>


        </a-carousel>
        <!-- </div> -->



    </div>

</template>

<script setup>
import { LeftOutlined, RightOutlined } from "@ant-design/icons-vue"
import { times } from '@/utils'
import { onBeforeMount, onUnmounted, reactive } from "vue";
import { useRouter } from "vue-router";
import { demoProducts } from '@/utils/demo'

const router=useRouter()
const time = reactive({
    hours: 0,
    minutes: 0,
    seconds: 0,
})
let timer = null
onBeforeMount(() => {
    timer = setInterval(() => {
        const now = new Date()
        const { hours, minutes, seconds } = times(`${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()} 23:59:59`)

        time.hours = hours < 10 ? '0' + hours : hours
        time.minutes = minutes < 10 ? '0' + minutes : minutes
        time.seconds = seconds < 10 ? '0' + seconds : seconds
    }, 1000)

})

onUnmounted(() => {
    clearInterval(timer)
})

const data = demoProducts.slice(1, 5).map(item => ({ id: item.id, name: item.goodsName, price: item.price, url: item.headerPic }))

const onView = (item) => router.push({ path: '/productdetail', query: { id: item.id } })
</script>

<style scoped>
.row {
    background: #fff;
    height: 240px;
    justify-content: space-between;

}

.row :deep(.ant-carousel) {
    /* flex: 1; */
    width: calc(100% - 190px);
    overflow: hidden;

}

.row :deep(.ant-carousel .slick-arrow.custom-slick-arrow) {
    width: 35px;
    height: 35px;
    text-align: center;
    line-height: 35px;
    border-radius: 35px;
    color: #fff;
    background-color: #bfbfbfe0;
    z-index: 1;
    font-size: 20px;
}

.row :deep(.ant-carousel .custom-slick-arrow:before) {
    display: none;
}

.row :deep(.ant-carousel .custom-slick-arrow:hover) {
    opacity: 0.5;
}

h1 {
    width: 210px;
    text-align: center;
    font-size: 30px;
    font-weight: 700;
    padding-top: 31px;
    background: url(../../assets/seckill.png);
    color: #fff;
    cursor: pointer;
}

.item {
    /* width: 25%; */
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 18px 5px;
    cursor: pointer;
}

.price {
    color: red;
    font-size: 15px;
}

img {
    height: 150px;
}

.timer {
    text-align: center;
    font-size: 16px;
}

.unit {
    display: inline-block;
    position: relative;
    width: 30px;
    height: 30px;
    line-height: 30px;
    text-align: center;
    background-color: #2f3430;
    margin: 10px;
    color: white;
    font-size: 16px;
}
.warn{
    font-size: 14px;
    margin-top: 80px;
}
h5{
    font-size: 12px;
    color:#fff;
    margin-top: -5px;
}
</style>
