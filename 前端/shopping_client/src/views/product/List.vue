<template>
    <div class="container">
        <MainHeader @search="onGetList"/>
        <div class="content">
            <div class="hasSelected">
                已选：<a-tag color="var(--primary-color)" v-if="state.filters.brand" closable @close="onRemoveBrand">
                    品牌：{{ state.filters.brand }}
                </a-tag>
                <a-tag color="var(--primary-color)" closable @close="onRemoveSpec(key)"
                    v-for="[key, val] in Object.entries(state.filters.specificationOption)">
                    {{ key }}：{{ val }}
                </a-tag>
            </div>

            <div class="search-box">
                <div class="type row">
                    <p class="title">商品类型：</p>

                    <div class="content">{{ state.productType.join('/') }}</div>
                </div>
                <div class="brand row">
                    <p class="title">品牌：</p>
                    <div class="content">
                        <p :class="{ selected: state.filters.brand == item }" v-for="item in state.brands"
                            @click="onSelectBrand(item)">{{ item }}</p>
                    </div>
                </div>
                <div class="spec">
                    <div class="row" v-for="[key, val] in Object.entries(state.specifications)">
                        <p class="title">{{ key }}：</p>
                        <div class="content row">
                            <p :class="{ selected: state.filters.specificationOption[key] == item }" v-for="item in val"
                                @click="onSelectSpec(key, item)">{{ item }}</p>
                        </div>
                    </div>
                </div>

            </div>
            <div class="row">
                <div style="width:200px;margin-right: 10px;">
                    <Advert />
                </div>

                <div style="flex:1">
                    <SearchNav :total="state.total" @changes="onChange" />
                    <div class="list">

                        <div v-for="item in state.data" class="itembox" @click="router.push('productdetail?id='+item.id)">
                            <img :src="item.headerPic" alt="">
                            <div>
                                <p class="price">
                                    <i>￥</i>
                                    {{ item.price }}

                                </p>
                                <p class="name">{{ item.goodsName }}</p>
                            </div>

                        </div>
                    </div>
                    <div class="pagination">
                        <a-pagination v-model:current="state.pagination.page" page-size="30" :total="state.total"
                            :show-total="total => `共 ${total} 条数据`" />
                    </div>
                </div>
            </div>

        </div>

    </div>


</template>

<script setup>
import { MainHeader, SearchNav, Advert } from '@/components'
import axios from '@/utils/axios'
import { onMounted, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { isDemoMode, searchDemoProducts } from '@/utils/demo'

const router=useRouter()
const state = reactive({

    brands: [

    ],
    productType: [],
    specifications: {},
    data: [],
    total: 0,
    pagination: {
        page: 1,
        size: 30
    },
    filters: { specificationOption: {} }
})

const onGetList = () => {
    const { filters, pagination } = state;
    if (isDemoMode) {
        const products = searchDemoProducts(sessionStorage.getItem('keyword')).filter(item => !filters.brand || item.brand === filters.brand)
        state.data = products
        state.total = products.length
        state.brands = [...new Set(searchDemoProducts().map(item => item.brand))]
        state.specifications = { 分类: [...new Set(searchDemoProducts().map(item => item.category))] }
        state.productType = ['本地演示商品']
        return
    }
    axios.post('user/goodsSearch/search', {
        keyword: sessionStorage.getItem('keyword'),
        brand: filters.brand,
        specificationOption: filters.specificationOption,
        highPrice: filters.highPrice,
        lowPrice: filters.lowPrice,
        sort: filters.sort,
        sortFiled: filters.sortFiled,
        page: pagination.page,
        size: pagination.size,

    }).then(({ goodsPage, brands, specifications, productType }) => {
        state.data = goodsPage.records
        state.total = goodsPage.total
        state.brands = brands
        state.specifications = specifications
        state.productType = productType

    })
}
onMounted(onGetList)

const onSelectBrand = (brand) => {
    state.filters.brand = brand
    onGetList()

}
const onRemoveBrand = () => {
    state.filters.brand = undefined
    onGetList()
}
const onSelectSpec = (key, val) => {
    state.filters.specificationOption[key] = val
    onGetList()
}
const onRemoveSpec = (key) => {
    delete state.filters.specificationOption[key]
    onGetList()
}

const onChange = (options) => {

    state.filters.highPrice = options.highPrice
    state.filters.lowPrice = options.lowPrice
    state.filters.sort = options.sort
    state.filters.sortFiled = options.sortFiled
    onGetList()
}

</script>

<style scoped>
.container {
    height: 100%;
    background-color: #fff;
}

.container :deep(.header) {
    border-bottom: 2px solid var(--primary-color);
    margin-bottom: 15px;
}

.content {
    width: 70%;
    margin: 0 auto
}

.search-box {
    border: 1px solid var(--border-color);
    border-top: none;
    margin-bottom: 15px;
}

.title {
    width: 150px;
    text-align: right;
    background: var(--background-color);
    padding-right: 10px;
    line-height: 40px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    font-weight: bold;
    border-top: 1px solid var(--border-color);

}

.search-box .content {
    flex: 1;
    line-height: 40px;
    padding-left: 10px;
    color: #005aa0;
    cursor: pointer;
    border-top: 1px solid var(--border-color);

}

.search-box .content p:hover {
    color: var(--primary-color)
}



.brand div {
    display: flex;
    flex-wrap: wrap;
    padding: 10px 0
}

.brand div p {
    width: 100px;
    height: 55px;
    line-height: 60px;
    text-align: center;
    border: 1px solid var(--border-color);
    margin: -1px -1px 0 0;

}

.type .content {
    color: var(--primary-color)
}

.spec .content p {
    margin-right: 15px;
}

.list {
    display: flex;
    flex-wrap: wrap;
    margin-top: 15px;
}

.itembox {
    width: 20%;
    height: 280px;
    padding: 10px;
    text-align: center;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: space-around;

}

.itembox img {
    width: 100%;
    /* flex:1 */
}

.itembox:hover {
    box-shadow: 0px 0px 5px #ccc;
    border-radius: 5px;
}


.price {
    font-size: 18px;
    font-weight: bold;
}

.price i {
    font-size: 14px;
}

.search-box .brand .selected {
    border-color: var(--primary-color);
}

.search-box .spec .selected,
.search-box .brand .selected {
    color: var(--primary-color)
}

.hasSelected {
    margin: 15px 0 5px 150px
}
</style>
