<template>
    <div class="title">
        <h1>为你推荐</h1>
        <div class="row">
            <p v-for="(item, index) in data" @click="onView(index)">
                <img :src="demoProductImages[index % demoProductImages.length]" alt="商品图片">
            <h3>{{ item.name }}</h3>
            <span class="price">￥<b>{{ item.price }}</b></span>
            </p>
        </div>
    </div>

</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { demoProductImages } from '@/utils/demo'

const router = useRouter()

const data = ref([
    {
        url: 'https://img10.360buyimg.com/jdcms/s150x150_jfs/t1/220975/35/14871/129629/623044c2E147ea0eb/738319279e918159.jpg.webp',
        name: '长虹洗衣机全自动中小型迷你儿童母婴家用宿舍智能波轮洗衣机带甩干机脱水风干节能蓝光洗衣机全自动波轮 8公斤智能风干强力电机 推荐1-3人使用',
        price: 568
    },
    {
        url: 'https://img11.360buyimg.com/jdcms/s150x150_jfs/t1/118332/33/27439/48524/62ac2577E7cf4d3a4/3eafa1a07c7aef7d.jpg.webp',
        name: '小米Redmi红米K405G智能游戏手机 幻境 8GB+128GB ',
        price: 9999
    },
    {
        url: 'https://img13.360buyimg.com/jdcms/s150x150_jfs/t1/216379/5/13599/132040/621c7a3aEb6f1ecef/5967a2781473479b.jpg.webp',
        name: '荣耀Magic4 全新一代骁龙8 双曲屏设计 LTPO屏幕 潜望式长焦摄像头 7P广角主摄 全网通版 5G 12GB+256GB 流金',
        price: 4988
    },
    {
        url: 'https://img10.360buyimg.com/jdcms/s150x150_jfs/t1/87400/22/24585/130257/622867baE8f860c00/60574bb382d1cd67.jpg.webp',
        name: 'Apple iPhone 13 (A2634) 128GB 蓝色 支持移动联通电信5G 双卡双待手机',
        price: 5999
    },
    {
        url: 'https://img12.360buyimg.com/babel/s150x150_jfs/t1/111100/30/20008/49142/5f8619caEeb536ff2/f50369e925acbd4e.jpg.webp',
        name: 'Apple iPhone 12 (A2404) 128GB 红色 支持移动联通电信5G 双卡双待手机',
        price: 4999
    },
    {
        url: 'https://img30.360buyimg.com/babel/s150x150_jfs/t1/181881/11/27486/382703/62da51e0Ec26b5d89/dd50e10d4944d801.jpg.webp',
        name: '小米电视 Redmi A43 2022款 43英寸 全高清 金属全面屏  双扬声器立体声 智能电视机L43R8-A ',
        price: 899
    },
    {
        url: 'https://img20.360buyimg.com/babel/s150x150_jfs/t1/127981/20/26329/161313/6232a961Ed02d77a1/76199ef1aa3fa51f.jpg.webp',
        name: '荣耀Magic4 至臻版 全新一代骁龙8 四曲屏设计 LTPO屏幕 潜望式长焦摄像头 全网通版 12GB+512GB 陶瓷黑',
        price: 7999
    },
    {
        url: 'https://img14.360buyimg.com/babel/s150x150_jfs/t1/153998/21/19009/84932/6035f334Ed2b110e2/709b7e700e762ff3.jpg.webp',
        name: ' 小草屋 小风扇迷你usb手持户外随身便携式可充电轻音大风力办公室学生桌面宿舍可爱台式小电扇 小风扇迷你【暗夜绿】',
        price: 32
    },
    {
        url: 'https://img13.360buyimg.com/babel/s150x150_jfs/t1/200422/35/9589/161711/614c35cfEb8976cbc/f66338cf82edb286.jpg.webp',
        name: '碧云泉（bewinch） G3纯水净水器 台式家用加热一体机直饮免安装反渗透自来水过滤净水器净饮机 G3Pro-慕可:套装版',
        price: 3999
    }, {
        url: 'https://img20.360buyimg.com/babel/s150x150_jfs/t1/218388/17/12291/107641/620703ebEf24edb8b/27eb43a94a0eebae.jpg.webp',
        name: '哈玛森鲜奶机H73商用10升大容量搅拌机私房奶油机打蛋机奶盖机台式10L商用打蛋机 经典白 10升奶油机',
        price: 2500
    },
    {
        url: 'https://img30.360buyimg.com/babel/s150x150_jfs/t1/209044/1/15572/128183/61dc6f10Ee80a0714/47ff92b2c0a705c8.jpg.webp',
        name: '【准新品】19寸20寸22寸 24寸27英寸电脑显示器 24寸显示器带点',
        price: 365
    },
     {
        url: 'https://img12.360buyimg.com/babel/s150x150_jfs/t1/192287/17/22572/105535/624c4d7bE18de581e/8f92fdb4a032f847.jpg.webp',
        name: '【全新】vivoiqooZ5无线蓝牙耳机高颜值可爱降噪游戏半入耳式Z3/NEO3适用运动型超长续航 【樱花粉】智能触控#自动配对超长续航环绕高音质 标配 ',
        price: 118
    },
     {
        url: 'https://img13.360buyimg.com/babel/s150x150_jfs/t1/75515/26/20182/64948/62a99f78E5cf9fb1b/62b54a11ca3acf89.jpg.webp',
        name: '松典（SONGDIAN）DC302L 数码卡片照相机 学生入门级便携高清 罗兰紫 32G 内存卡',
        price: 368
    },
     {
        url: 'https://img30.360buyimg.com/babel/s150x150_jfs/t1/217747/35/4858/106895/61960c0dE7e07dbb5/e935e08084413c57.jpg.webp',
        name: '惠威（Swan）汽车音响前门6.5英寸F1600MKIII二分频套装喇叭 无损改装车载扬声器通用型音箱可接功放低音炮',
        price: 2690
    },
     {
        url: 'https://img11.360buyimg.com/babel/s150x150_jfs/t1/223826/37/1312/86003/61c6c4fcE98d525dd/684c2004a27d735d.jpg.webp',
        name: 'MS苹果无线蓝牙耳机套iphone3代卡通蜡笔小新pro保护套1代2代收纳盒硅胶防摔软壳可爱保护套 AirPodspro耳机套【透明】230353',
        price: 22
    },

])

const onView = (index) => router.push({ path: '/productdetail', query: { id: String((index % 6) + 1) } })
</script>


<style scoped>
h1 {
    width: 200px;
    margin: 0 auto;
    position: relative;
    text-align: center;
    margin-bottom: 30px;
}

h1:before {
    content: "";
    display: block;
    width: 25px;
    height: 20px;
    position: absolute;
    top: 50%;
    margin-top: -10px;
    background-image: none;
    background-position: 0 0;
    left: -20px;

}

h1:after {
    content: "";
    display: block;
    width: 25px;
    height: 20px;
    position: absolute;
    top: 50%;
    margin-top: -10px;
    background-image: none;
    background-position: -25px 0;
    right: -20px;

}

.row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-column-gap: 10px;
    grid-row-gap: 10px;
    padding-bottom:100px
}

.row p {
    background: #fff;
    padding: 20px;
    cursor: pointer;

}

.row p img {
    width: 100%
}

.row p h3 {
    margin: 10px 0;
    word-break: break-all;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical
}
</style>
