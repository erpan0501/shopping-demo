<template>
    <div class="steps">
        <a-steps :current="current">
            <a-step disabled v-for="item in steps" 
            :key="item.title" :title="item.title" 
            :description="item.description"
            />
        </a-steps>
    </div>
   
    
</template>

<script setup>

const { current ,options} = defineProps(['current','options'])
const steps =options|| [
    { title: '我的购物车' },
    { title: '填写核对订单信息' },
    { title: '成功提交订单' }
]


</script>

<style scoped>
.steps {
    width: 100%
}

.steps :deep(.ant-steps-item-icon) {
    width: 28px;
    height: 28px;
    line-height: 28px;
}

.steps :deep(.ant-steps-item-title) {
    font-size: 14px;
    line-height: 28px;
}
</style>