<template>
    <div class="con">
        <MainHeader />
        <div class="content">
            <div class="info row">
                <Viewer :imgUrl="detail.headerPic" />
                <div class="inforight">
                    <h3>{{ detail.goodsName }}</h3>
                    <p class="pricebox">
                        <label>商城价</label>
                        <span class="price">￥<i>{{ detail.price }}</i></span>
                    <p>
                        <label>好评率</label>
                        <i>98%</i>
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
                        <button class="primary" @click="onAddCart">加入购物车</button>
                    </div>

                </div>
            </div>
            <div class="row">
                <div class="sametype">
                    <Advert title='同类型商品' :data="sametypeProduct" />
                </div>
                <div style="flex:1">
                    <a-tabs type="card">
                        <a-tab-pane key="1" tab="商品介绍">
                            <p style="margin:15px 0">
                                <label>品牌：{{ detail.brand.name }}</label>
                            </p>
                            <div class="box">
                                <p>
                                    <label>商品名称：</label>
                                    <span>{{ detail.goodsName }}</span>
                                </p>
                                <p>
                                    <label>商品类型：</label>
                                    <span>{{ `
                                    ${detail.productType1.name}/
                                    ${detail.productType2.name}/
                                    ${detail.productType3.name}` 
                                    }}</span>
                                </p>
                                <p>
                                    <label>商品编号：</label>
                                    <span>{{ detail.id }}</span>
                                </p>
                                <p v-for="item in detail.specifications">
                                    <label>{{ item.specName }}：</label>
                                    <span>{{ item.specificationOptions.map(item => item.optionName).join('/')
                                    }}</span>
                                </p>


                            </div>

                            <p v-for="item in detail.images" style="text-align:center">
                                <img :src="item.imageUrl" alt="" style="width:100%">
                            </p>

                        </a-tab-pane>
                        <a-tab-pane key="2" tab="商品规格">
                            <p v-for="item in detail.specifications">
                                <label>{{ item.specName }}：</label>
                                <span>{{ item.specificationOptions.map(item => item.optionName).join('/') }}</span>
                            </p>
                        </a-tab-pane>
                    </a-tabs>
                </div>

            </div>

        </div>
    </div>
    <Footer />

</template>

<script setup>
import { Viewer, MainHeader, Count, Advert, Footer } from '@/components'
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router'
import { axios } from '@/utils'
import { addDemoCart, demoProducts, findDemoProduct, isDemoMode } from '@/utils/demo'

const {query} = useRoute()

const router = useRouter()
const detail = ref({brand:{},productType3:{},productType2:{},productType1:{}})
const sametypeProduct = ref([])
const count = ref(1)

onMounted(() => {
    if (isDemoMode) {
        const product = findDemoProduct(query.id)
        detail.value = {
            ...product,
            brand: { name: product.brand },
            productType1: { name: '本地演示' },
            productType2: { name: product.category },
            productType3: { name: '精选商品' },
            specifications: [{ specName: '服务说明', specificationOptions: [{ optionName: '本地演示' }, { optionName: '七天退换' }] }],
            images: [{ imageUrl: product.headerPic }],
        }
        sametypeProduct.value = demoProducts.filter(item => item.id !== product.id).slice(0, 4).map(item => ({ name: item.goodsName, price: item.price, url: item.headerPic }))
        return
    }
    axios.get('/user/goodsSearch/findDesc', { params: { id: query.id } }).then(data => {
        
        detail.value = data
        
        axios.post('user/goodsSearch/search', { keyword: data.productType3.name ,page:1,size:10}).then(({goodsPage}) => {
            const result = goodsPage.records.map(item => {
                return { name: item.goodsName, price: item.price, url: item.headerPic }
            })
            
            sametypeProduct.value = result
        })
    })
})

const onChangeCount = (e) => {
    console.log(e)
    count.value = e
}

const onAddCart = () => {
    if (isDemoMode) {
        addDemoCart(detail.value, count.value)
        router.push('/cart')
        return
    }
    axios.post('user/cart/addCart', {
        goodId: detail.value.id,
        goodsName: detail.value.goodsName,
        price: detail.value.price,
        headerPic: detail.value.headerPic,
        num: count.value
    }).then(data => {
        router.push('/cart')
    })
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
</style>
