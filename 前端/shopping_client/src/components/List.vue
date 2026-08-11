<template>
    <div class="row" @mouseleave="state.current=[]">
        <ul>
            <li v-for="item in types" @mouseover="onView(item)" @click="onSelect(item.name)">
                {{ item.name }}
                <b>
                    <right-outlined />
                </b>

            </li>
        </ul>
        <a-card style="flex:1" v-show="state.current.length>0">
            <div class="box">
                <p v-for="(item, index) in state.current" @click="onSelect(item.name)">
                    <img :src="isDemoMode ? demoProductImages[index % demoProductImages.length] : item.img" alt="商品图片">
                    <b>{{ item.name }}</b>

                </p>
            </div>

        </a-card>
    </div>


</template>
<script setup>
import { RightOutlined } from '@ant-design/icons-vue'
import { reactive } from 'vue';
import {types} from '@/config'
import { useRouter } from 'vue-router'
import { demoProductImages, isDemoMode } from '@/utils/demo'


const state = reactive({
    current: []
})
const router = useRouter()

const onView = (item) => {
    state.current = item.children
}

const onSelect = (keyword) => {
    sessionStorage.setItem('keyword', keyword)
    router.push('/list')
}
</script>

<style scoped>
ul {
    list-style: none;
    width: 260px;
    background: var(--background-color1);
    color: #fff;
    padding: 15px 0;
    z-index: 100;
}

li {
    padding: 8px 20px;
    display: flex;
    justify-content: space-between;
    font-size: 16px;
    cursor: pointer;
}

li:hover {
    background: var(--primary-color)
}

.box {
    display: grid;
    grid-template-columns: repeat(5, 20%);
    grid-template-rows: repeat(3,100px);
    grid-row-gap: 30px;
}
.box p{
    margin:0 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
    cursor: pointer;
}
.box p:hover{
    color:var(--primary-color)
}
</style>
