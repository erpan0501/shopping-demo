<template>

    <div class="row" style="z-index:1">
        <div class="small" ref="small" @mousemove.prevent="mousemove" @mouseleave="mouseleave">
            <img :src="imgUrl" alt="" />
            <div class="mask" :style="{ 'left': state.left + 'px', 'top': state.top + 'px', }" ref="mask"></div>
        </div>
        <div style="position:relative">
        <div class="big" ref="big">
            <img ref="bigimg" :src="imgUrl" alt=""
                :style="{ 'left': state.imgX + 'px', 'top': state.imgY + 'px', }" />
        </div></div>
        
    </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue';
const props=defineProps(['imgUrl'])
const imgUrl=computed(()=>props.imgUrl)
const small = ref()
const big = ref()
const mask = ref()
const bigimg = ref()
const state = reactive({
    left: 0,
    top: 0,
    imgX: 0,
    imgY: 0

})
const mousemove = (e) => {
    const pointX = e.pageX - small.value.offsetLeft
    const pointY = e.pageY - small.value.offsetTop

    let maskX = pointX - mask.value.offsetWidth / 2
    let maskY = pointY - mask.value.offsetHeight / 2
    // console.log(maskX)
    maskX = maskX < 0 ? 0 : maskX;
    maskY = maskY < 0 ? 0 : maskY;

    maskX = maskX > small.value.offsetWidth - mask.value.offsetWidth ? small.value.offsetWidth - mask.value.offsetWidth : maskX;
    maskY = maskY > small.value.offsetHeight - mask.value.offsetHeight ? small.value.offsetHeight - mask.value.offsetHeight : maskY;
    // console.log(maskX)
    state.left = maskX
    state.top = maskY

    state.imgX = -maskX * (big.value.offsetWidth/mask.value.offsetWidth)
    state.imgY = -maskY * (big.value.offsetWidth/mask.value.offsetWidth)
    mask.value.style.display = 'block'
    big.value.style.visibility = 'visible'

}

const mouseleave = (e) => {
    mask.value.style.display = 'none'
    big.value.style.visibility = 'hidden'
}
</script>

<style scoped>

.small {
    width: 450px;
    height: 450px;
    border: 1px solid var(--border-color);
    position: relative;
}

.small img {
    width: 100%;
    /* height: 100% */
}

.small .mask {
    width: 300px;
    height: 300px;
    background: #eee;
    display: none;
    position: absolute;
    left: 0;
    top: 0;
    cursor: move;
    background: rgba(255, 255, 0, 0.4);
}

.big {
    width: 600px;
    height: 600px;
    border: 1px solid var(--border-color);
    position: absolute;
    visibility: hidden;
    overflow: hidden;
    background:#fff
}

.big img {
    width: 900px;
    /* height: 900px; */
    position: absolute;
    top: 0;
    left: 0
}
</style>