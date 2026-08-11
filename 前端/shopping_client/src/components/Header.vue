<template>
    <!-- <div class="con"> -->
    <div class="header">
        <img src="../assets/logo-local.svg" alt="商城演示">
        <!-- <h1>商城</h1> -->
        <div class="title">欢迎{{ title }}</div>
        <slot></slot>

    </div>
    <div class="shadow" v-if="!hideShadow"></div>
    <!-- </div> -->

</template>

<script setup>
const { title, hideShadow } = defineProps(['title', 'hideShadow'])
</script>

<style scoped>
.header {
    width: 50%;
    height: 100px;
    margin: 0 auto;
    padding: 20px 0;
    position: relative;
    box-sizing: border-box;

}

img {
    vertical-align: middle;
    width: 250px;
}

h1 {
    display: inline;
    color: var(--primary-color);
    position: relative;
    top: 10px;
}

.title {
    display: inline;
    color: var(--text-color1);
    font-size: 26px;
    position: relative;
    top: 8px;
    left: 10px;

}

.shadow {
    width: 100%;
    height: 10px;
    border-bottom: 2px solid var(--primary-color);
}

.header :deep(.right) {
    position: absolute;
    right: 0;
    top: 50px;
    cursor: pointer;
}
</style>
