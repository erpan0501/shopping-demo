<template>
    <div class="box">
        <h1 @click="onView('1')">每日特价 <right-circle-outlined/></h1>
        <div class="row">
            <p class="left" @click="onView('2')">
                <img :src="demoProductImages[0]" alt="商品图片">
                {{ data[0].name }}<br>
                <p class="price" style="text-align:center ;">￥ <i>{{ data[0].price }}</i></p>
            </p>
            <div class="right row">
                <p v-for="(item, index) in data.slice(1,5)" class="row" @click="onView(String(index + 3))">
                    <img :src="demoProductImages[(index + 1) % demoProductImages.length]" alt="商品图片">
                    <p>
                         {{ item.name }}<br>
                    <span class="price">￥ <i>{{ item.price }}</i></span>
                    </p>
                   
                </p>
            </div>
        </div>
    </div>

</template>

<script setup>
import { reactive } from 'vue';
import {RightCircleOutlined} from '@ant-design/icons-vue'
import { useRouter } from 'vue-router'
import { demoProductImages } from '@/utils/demo'

const router = useRouter()
const onView = (id) => router.push({ path: '/productdetail', query: { id } })

const { data } = reactive({
    data: [{
        url: 'https://img14.360buyimg.com/seckillcms/s144x144_jfs/t1/152568/17/24557/52398/62a882b8E101d64b7/d8c4d468f4ac1711.jpg!q70.jpg.webp',
        name: '荣耀Play6T全网通手机',
        price: 1259
    },
    {
        url: 'https://img10.360buyimg.com/seckillcms/s144x144_jfs/t1/14162/26/17505/18495/62ce856aE74987f82/e4a8c0d40e27dbb5.png!q70.jpg.webp',
        name: '海尔全自动10KG波轮洗衣机',
        price: 1298
    },
    {
        url: 'https://img20.360buyimg.com/seckillcms/s144x144_jfs/t1/185753/12/26093/124550/62be98d2E9be8035c/014dbe8344598901.jpg!q70.jpg.webp',
        name: '扬子  整屋扇空气循环扇',
        price: 198
    },
        {
            url: 'https://img14.360buyimg.com/seckillcms/s144x144_jfs/t1/53186/10/19542/58812/62bfa885E8b279cbe/fffdcea3b7e4ef2d.jpg!q70.jpg.webp',
            name: '新品经典色花荷瓣江山美人特价',
            price: 9
        },
    {
        url: 'https://img13.360buyimg.com/seckillcms/s144x144_jfs/t1/220002/23/12800/663808/621207daE79f33fc3/237d35829f42f3e9.png!q70.jpg.webp',
        name: '小天鹅除菌洗衣机',
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
    margin-right: 15px;
    padding:20px;
    background:var(--background-color)
}
h1 .anticon {
    color:var(--primary-color);
    font-size: 20px;
}
.left img{
    width:100%
}
.right {
    flex-wrap: wrap;
}
.right p{
    width:50%;
    /* height: 100px; */
    box-sizing: border-box;
    justify-content: space-around;
    margin-top: 15px;
    padding-right: 10px;
}
.right p img{
    width:90px
}
.right p:hover{
    color:var(--hover-color)
}
.price i{
    font-size: 15px;

}
</style>
