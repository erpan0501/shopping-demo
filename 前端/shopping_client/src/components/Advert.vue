<template>
    <a-card :title="props.title||'商品精选'" >
        <div v-for="(item, index) in data" class="item">
            <img :src="isDemoMode ? demoProductImages[index % demoProductImages.length] : item.url" alt="商品图片">
            <p class="title">{{ item.name }}</p>
            <b class="price">￥{{ item.price }}</b>
        </div>

    </a-card>
</template>

<script setup>
import { computed } from 'vue';
import { demoProductImages, isDemoMode } from '@/utils/demo'

const props=defineProps(['title','data'])

let data =props.title=='同类型商品'?computed(()=>props.data) :[
    { name: 'realme真我GT Neo3 150W 天玑8100 150W光', price: 2699, url: 'https://img13.360buyimg.com/cms/s190x190_jfs/t1/7785/38/17322/318102/62c7ee20E2e4285e7/b85ddb52cfed19ef.jpg' },
    { name: '海信(Hisense) TOUCH 音乐阅读器 5.84英寸水墨屏', price: 1599, url: 'https://img13.360buyimg.com/cms/s190x190_jfs/t1/205639/2/24417/122330/62c2b295Eeff11e57/9c12061d07899ca1.jpg' },
    { name: '小米12S Pro 骁龙8+处理器 徕卡光学镜头 2K超视', price: 5399, url: 'https://img13.360buyimg.com/cms/s190x190_jfs/t1/218276/1/17334/211505/62cc1e86Eed992bcd/bec05386825bd625.jpg' },
    { name: 'HUAWEI nova 10 【内置66W华为超级快充】 前置6000万超广角镜头', price: 2699, url: 'https://img13.360buyimg.com/cms/s190x190_jfs/t1/76152/15/19931/104718/62c80eb3E8a510bc4/4d926a04edbf4e59.jpg' },
    { name: 'OPPO K9x 天玑810游戏芯 5000mAh长续航', price: 1399, url: 'https://img13.360buyimg.com/cms/s190x190_jfs/t1/107474/6/30249/128908/62c12acbE9693a576/97b3916ecf53734e.jpg' },
    { name: 'Redmi K50 电竞版 全新骁龙8 双VC液冷散热 OLED', price: 2299, url: 'https://img13.360buyimg.com/cms/s190x190_jfs/t1/185897/28/27136/211517/62cc1d77E2ea389e7/29a2d128b130f864.jpg' },
    { name: '科大讯飞录音降噪会议耳机iFLYBUDS Pro 无线蓝牙', price: 899, url: 'https://img13.360buyimg.com/cms/s190x190_jfs/t1/197418/19/25628/132604/62ccf82cE0fde6c11/e23c9550b883633a.jpg' },
]


</script>

<style scoped>
.title{
    overflow: hidden;
}
.item{
    text-align: center;
    margin-bottom: 15px;
    cursor: pointer;
}
.item img{
    width: 100%;
}
.title{
    text-align: left;
}

</style>
