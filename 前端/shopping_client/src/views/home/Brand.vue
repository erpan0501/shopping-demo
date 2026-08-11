<template>
    <div class="box">
        <h1 @click="router.push('/list')">品牌闪购
            <right-circle-outlined/>
        </h1>
        <div class="row">
            <p class="left" @click="onView('5')">
                <h3>{{ data[0].name }}</h3>
                {{ data[0].des }}<br>
                <img :src="demoProductImages[4]" alt="商品图片">
            </p>
            <div class="right row">
                <p v-for="(item, index) in data.slice(1,7)" @click="onView(String((index % 6) + 1))">
                    
                        {{ item.name }}<br>
                    
                        <img :src="demoProductImages[index % demoProductImages.length]" alt="商品图片">
                   
                </p>
            </div>
        </div>
    </div>

</template>

<script setup>
import { reactive } from 'vue';
import { RightCircleOutlined } from '@ant-design/icons-vue';
import { useRouter } from 'vue-router'
import { demoProductImages } from '@/utils/demo'

const router = useRouter()
const onView = (id) => router.push({ path: '/productdetail', query: { id } })

const { data } = reactive({
    data: [{
        url: 'https://img14.360buyimg.com/seckillcms/s390x390_jfs/t1/131098/2/16614/154830/5fb5eaedEfdfebc77/e6bb1b1886ffe585.jpg!cc_130x130.webp',
        name: 'STL闪购专场',
        des:'配镜低至79元 仅剩2天',
    },
    {
        url: 'https://img20.360buyimg.com/seckillcms/s300x150_jfs/t1/110948/11/28345/5452/62d64363Ed21651ca/a95481f8d85cf72f.png!cc_300x150.webp',
        name: '四季沐歌品牌秒杀',
        price: 1298
    },
    {
        url: 'https://img13.360buyimg.com/seckillcms/s300x150_jfs/t1/36165/15/16798/4066/62d7a06fE03e8abf2/e232bc358a9e4372.png!cc_300x150.webp',
        name: '舒福佳品牌闪购',
        price: 198
    },
        {
            url: 'https://img11.360buyimg.com/seckillcms/s300x150_jfs/t1/212052/23/20828/11194/62ca7e88E3df5b7e4/c5f0a10f9940a1a1.png!cc_300x150.webp',
            name: 'MLB品牌闪购',
            price: 9
        },
    {
        url: 'https://img12.360buyimg.com/seckillcms/s300x150_jfs/t1/194573/9/27422/7356/62d6728bE10b9499c/17d231e1268a8f06.png!cc_300x150.webp',
        name: '万和家电闪购专场',
        price: 1298
    },
    {
        url: 'https://img11.360buyimg.com/seckillcms/s300x150_jfs/t1/28042/16/17853/11365/62d7a9a2E2a27304b/459f7436c5c61d2f.png!cc_300x150.webp',
        name: '万和家电闪购专场',
        price: 1298
    },
    {
        url: 'https://img12.360buyimg.com/seckillcms/s300x150_jfs/t1/194573/9/27422/7356/62d6728bE10b9499c/17d231e1268a8f06.png!cc_300x150.webp',
        name: '美的华凌狂欢购',
        price: 1298
    },
    ]
})
</script>

<style scoped>
.box{
    background: #fff;
    padding:10px;
    margin-right: 10px;
    font-weight: 600;
}
.box h1{
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 10px;
}
.box h1, .left { cursor: pointer; }

.left{
    text-align: center;
    margin-right: 15px;
    padding:20px;
    background:#fcf8f8
}
h1 .anticon {
    color:var(--primary-color);
    font-size: 20px;
}
.left img{
    width:100%;
    margin-top: 10px;
}
.right {
    flex-wrap: wrap;
}
.right p{
    width:50%;
    /* height: 100px; */
    box-sizing: border-box;
    justify-content: space-between;
    
    margin-top: 15px;
    padding-right: 10px;
}
.right p img{
    width:80px
}
.right p:hover{
    color:var(--hover-color)
}
.price i{
    font-size: 15px;

}
</style>
