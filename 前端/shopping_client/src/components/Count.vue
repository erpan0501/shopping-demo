<template>
    <div class="count">
        <plus-outlined @click="onAdd" />
        <input type="text" v-model="inputVal">
        <minus-outlined @click="onMin" :class="{disabled:inputVal<=1}"/>
    </div>
</template>

<script setup>
import { PlusOutlined, MinusOutlined } from '@ant-design/icons-vue'
import { ref, watch } from 'vue';

const emit = defineEmits(['changes'])
const { value=0 } = defineProps(['value'])
const inputVal = ref(value)
let timer = null


watch(inputVal, (val) => {
    clearTimeout(timer)
    timer = setTimeout(() => {
        emit('changes', val)
    }, 600)
})


const onAdd = () => {
    inputVal.value++
}
const onMin = () => {
    if (inputVal.value == 1) {
        return
    }
    inputVal.value--
}
</script>

<style scoped>
.count {
    display: flex;
    align-items: center;
    height: 23px;
}

input {
    border: 1px solid var(--border-color);
    width: 60px;
    height: 100%;
    text-align: center
}

input:focus {
    outline: none;
}

.count .anticon {
    display: block;
    height: 100%;
    color: var(--text-color1);
    background: #b3dbcc6e;
    line-height: 24px;
    padding: 0 5px;
    font-size: 12px;
    cursor: pointer;
}
.count .disabled.anticon{
    background:#ccc;
    user-select: none;
}
</style>