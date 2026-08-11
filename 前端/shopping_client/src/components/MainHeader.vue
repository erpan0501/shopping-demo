<template>
    <!-- <Nav /> -->
    <div class="header">
        <div class="box">
            <span>
                <img src="../assets/logo-local.svg" alt="商城演示">
                <!-- <h1>商城</h1> -->
            </span>
            <div class="search_box">

                <div class="search">
                    <input type="text" v-model="state.keyword" placeholder="请搜索" @input="onInput" @keyup.enter="onSearch"
                        @focus="state.focused = true">

                    <search-outlined @click="onSearch" />
                </div>
                <div class="words" v-show="state.words.length > 0 && (state.focused)">
                    <p v-for="item in state.words" @click="onSelectWord(item)">{{ item }}</p>

                </div>
                <ul class="hot">
                    <li>热搜词：</li>
                    <li v-for="item in hots" @click="onSelectWord(item)">{{ item }}</li>
                </ul>
                <ul class="type">
                    <li v-for="item in types" @click="onSelectWord(item.name)">{{ item.name }}</li>
                </ul>
            </div>

        </div>

        <slot></slot>
    </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch, watchEffect } from 'vue';
import { SearchOutlined } from '@ant-design/icons-vue';
import { Nav } from '@/components'
import { types } from '@/config'
import { axios } from '@/utils'
import { isDemoMode, searchDemoProducts } from '@/utils/demo'
import { useRoute, useRouter } from 'vue-router';

const emit = defineEmits(['search'])
const hots = ['华为', '平板', '连衣裙', '无线耳机', '手机', '小米', '电脑', '游戏机']
let timer = null
const input = ref()
const state = reactive({
    words: [],
    keyword: sessionStorage.getItem('keyword')

})
const router = useRouter()
const { path } = useRoute()

onMounted(() => {
    window.addEventListener('changeKeyword', (e) => {
        state.keyword = ''
        sessionStorage.setItem('keyword', '')
    })
})
const onInput = (e) => {
    clearTimeout(timer)
    timer = setTimeout(() => {
        if (isDemoMode) {
            state.words = searchDemoProducts(e.target.value).map(item => item.goodsName)
            return
        }
        axios.get('user/goodsSearch/autoSuggest', { params: { keyword: e.target.value } }).then(data => {
            state.words = data
        })
    }, 300)
}

const onSearch = () => {
    state.focused = false
    if (path === '/list') emit('search')
    else router.push('/list')
}

const onSelectWord = (word) => {

    state.keyword = word
    state.focused = false

    onSearch()

}

const keyword = computed(() => state.keyword)
watch(keyword, (val, preVal) => {
    console.log(val, 'watch')
    console.log(preVal, 'watch')
    sessionStorage.setItem('keyword', val)

})


</script>

<style scoped>
.header {
    background: #fff;

}

.search_box {
    margin-left: 50px;
    position: relative;
}

.box {
    width: 60%;
    margin: 0 auto;
    padding: 20px 0 30px 0;
    position: relative;
    box-sizing: border-box;
    display: flex;
    align-items: center;
}

img {
    vertical-align: middle;
    width: 250px;
}

/* h1 {
    display: inline;
    color: var(--primary-color);
    position: relative;
    top: 10px;
} */

.title {
    display: inline;
    color: var(--text-color1);
    font-size: 26px;
    position: relative;
    top: 8px;
    left: 30px;

}

.search {
    width: 560px;
    display: flex;
    align-items: center;
    border: 2px solid var(--primary-color);
    border-radius: 5px;
    height: 40px;
    overflow: hidden;
    padding-left: 10px;
    cursor: pointer;
}

input {
    height: 100%;
    border: none;
    flex: 1
}

input:focus {
    outline: none;
    /* border:none */
}

.anticon-search {
    background-color: var(--primary-color);
    padding: 0 11px;
    color: #fff;
    font-size: 24px;
    height: 100%;
    display: flex;
    align-items: center;
}

ul {
    list-style: none;
    display: flex;
}

.hot li:nth-child(1) {
    color: var(--primary-color)
}

.hot li {
    color: var(--text-color2)
}

ul li {
    margin-right: 15px;
    cursor: pointer;
    color: var(--text-color1);
    font-size: 12px;
}

.type {
    position: relative;
    top: 25px;
}

.type li {
    font-size: 16px;
    font-weight: bold;
    margin-right: 20px;
}

.words {
    position: absolute;
    width: 98%;
    background: #fff;
    border: 1px solid var(--border-color);
    border-top: 0;
    z-index: 10;
}

.words p {
    padding: 5px 10px;
    cursor: pointer;
}

.words p:hover {
    background: #00b68314;
}
</style>
