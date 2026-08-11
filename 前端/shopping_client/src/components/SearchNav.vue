<template>
    <div class="row">
        <a @click="onSelect('ALL')" :class="{ active: state.selected == 'ALL' }">综合</a>
        <a class="updown" @click="onSelect('NEW')" :class="{ active: state.selected == 'NEW' }">新品
            <em>
                <caret-up-outlined @click="onChangeSort('NEW', 'ASC')" :class="{ selected: state.NEW == 'ASC' }" />
                <caret-down-outlined @click="onChangeSort('NEW', 'DESC')" :class="{ selected: state.NEW == 'DESC' }" />
            </em>
        </a>
        <a class="updown" @click="onSelect('PRICE')" :class="{ active: state.selected == 'PRICE' }">
            价格
            <em>
                <caret-up-outlined @click="onChangeSort('PRICE', 'ASC')" :class="{ selected: state.PRICE == 'ASC' }" />
                <caret-down-outlined @click="onChangeSort('PRICE', 'DESC')" :class="{ selected: state.PRICE == 'DESC' }" />
            </em>
        </a>
        <div class="pricerange">
            <input type="number" placeholder="￥" v-model="state.lowPrice">
            —
            <input type="number" placeholder="￥" v-model="state.highPrice">
            <button @click="onClearPrice">清除</button>
            <button @click="onSavePrice">确定</button>
        </div>
        <div class="total">
            共计 <u>{{ total }}</u> 件商品
        </div>
    </div>

</template>
<script setup>
import { CaretUpOutlined, CaretDownOutlined } from '@ant-design/icons-vue'
import { reactive } from 'vue';

const { total } = defineProps(['total'])
const emit = defineEmits('changes')
const state = reactive({
    selected: 'ALL',
    highPrice: undefined,
    lowPrice: undefined
})

const onSelect = (type) => {
    state.selected = type
    if(type=='ALL'){

        emit('changes', { sortFiled: undefined, sort:undefined })
    }
}

const onChangeSort = (type, sort) => {
    
    state[type] = sort
    emit('changes', { sortFiled: type, sort })
}

const onSavePrice = () => {
    
    emit('changes', {
        sortFiled: state.selected,
        sort: state[state.selected],
        highPrice: state.highPrice,
        lowPrice: state.lowPrice
    })
}

const onClearPrice=()=>{
    state.highPrice=undefined
    state.lowPrice=undefined
     emit('changes', {
        sortFiled: state.selected,
        sort: state[state.selected],
       
    })
}





</script>
<style scoped>
.row {
    position: relative;
    background: var(--background-color);
    padding: 6px 8px
}

.row a {
    display: block;
    padding: 0 9px;
    height: 23px;
    border: 1px solid #CCC;
    margin-right: -1px;
    background: #FFF;
    color: #333;

}

.updown {
    display: flex !important;
    justify-content: space-between;
}

em {
    display: flex;
    flex-direction: column;
    font-size: 12px;
    margin-left: 5px;
}

.anticon-caret-up {
    position: relative;
    top: 2px
}

.anticon-caret-down {
    position: relative;
    top: -2px
}

.row a.active {
    background: var(--primary-color);
    color: #fff !important
}

.active .anticon:not(.selected) {
    color: #aaa
}

.active .anticon.selected {
    color: #fff
}

.pricerange {
    display: flex;
    margin-left: 10px;
    color: var(--text-color2);
    align-items: center;
}

.pricerange input {
    width: 50px;
    height: 23px;
    border: 1px solid var(--border-color);
    margin: 0 4px;
    color: var(--text-color1)
}

.pricerange input:focus {
    border: none;
    outline: none;
}

.total {
    position: absolute;
    right: 10px
}

u {
    color: var(--primary-color)
}

button {
    border: 1px solid var(--border-color);
    background: #fff;
    padding: 2px 7px;
    font-size: 12px;
}
</style>