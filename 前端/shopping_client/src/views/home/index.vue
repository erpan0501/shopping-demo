<template>
    <div class="container">
        <MainHeader />
        <div class="content">
            <div class="carouselbox">
                <a-carousel effect="fade" autoplay>
                    <img :src="img.pic" alt="" v-for="img in state.imgs" @click="onView(img)">
                </a-carousel>
                <List />
            </div>

            <div style="margin-top:30px;position: relative;">
                <Seckill />
            </div>
            <div style="margin-top:30px;" class="row">
                <SpecialOffer />
                <Brand />
            </div>
            <div style="margin-top:30px;">
                <Recommend />
            </div>
        </div>


    </div>

    <Footer />
    <BackTop/>
        
</template>
<script setup>
import { List, MainHeader, Footer } from '@/components';
import { onBeforeMount, reactive } from 'vue';
import { BackTop } from 'ant-design-vue'
import { axios } from '@/utils'
import Seckill from './Seckill';
import SpecialOffer from './SpecialOffer';
import Brand from './Brand';
import Recommend from './Recommend';

const state = reactive({
    imgs: []
})
const isDemoMode = process.env.VUE_APP_DEMO_MODE !== 'false'

onBeforeMount(() => {
    if (isDemoMode) {
        return
    }
    axios.get('user/category/all').then(data => {
        state.imgs = data
    })
})

const onView = (img) => {

    window.location.href = img.url
}
</script>
<style scoped>
.content {
    width: 60%;
    margin: 0 auto;
    position: relative;
    margin-top: 20px;
}

.carouselbox {
    position: relative;
}

.carouselbox :deep(.ant-carousel) {
    position: absolute;
    left:260px;
    z-index: 0;
    width: calc(100% - 260px);
    height: 100%;




}

.ant-carousel :deep(.slick-slider) {
    height: 100%;
}

.ant-carousel :deep(.slick-list) {
    height: 100%;
    overflow: hidden;
}

.ant-carousel :deep(.slick-slide div),
.ant-carousel :deep(.slick-track),
.ant-carousel :deep(img) {
    height: 100%;

}

</style>
