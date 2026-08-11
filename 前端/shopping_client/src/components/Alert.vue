<template>
    <div  :style="style" class="alert">
    <b v-if="!type||type=='success'">✔</b>
    <b v-else>✖</b>
    &nbsp;
    <slot></slot>
    </div>
</template>
<script setup>
import { onMounted, reactive } from 'vue';
const {style , type} = defineProps(['style','type'])

onMounted(()=>{
    setTimeout(()=>{
        document.getElementsByClassName("alert")[0].style.display='none';
     },3000)
})
</script>
<style scoped>
div{
    color: var(--text-color2);
    font-size: 12px;

}
div b{
    color:var(--primary-color)
}
</style>