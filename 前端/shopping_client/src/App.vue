<template>
  <Nav v-show="hasNav" />
  <a-config-provider :locale="zhCN">
    <router-view />
  </a-config-provider>

</template>

<script setup>
import { ref } from 'vue';
import {  useRouter } from 'vue-router'
import { Nav } from './components';
import zhCN from 'ant-design-vue/es/locale/zh_CN';

const hasNav = ref()
const router = useRouter()
router.beforeEach((to, from) => {
  const { fullPath } = to
  hasNav.value = (fullPath == '/login' || fullPath == '/register') ? false : true

})

</script>

<style>
:root {
  --primary-color: #e2220d;
  --text-color1: #666;
  --border-color: #6c686830;
  --text-color2: #aaa;
  --background-color: #f4f4f4;
  --background-color1: #3f3e3e;
  --hover-color: #ff0000a8
}

html,
body,
#app {
  width: 100%;
  height: 100%;
  color: var(--text-color1);
  /* background-color: var(--background-color); */
}

html,
body,
#app,
div,
p,
li,
ul,
h1,
h2,
h3 {
  padding: 0;
  margin: 0;

}

.container {
  /* height: 100%; */
  background: var(--background-color);
}



button {
  padding: 7px 16px;
  text-align: center;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  height: fit-content;

}

button.block {
  width: 100%
}

button.primary {
  background: var(--primary-color);
  color: #fff;
  font-size: 14px;
}
button.primary[disabled]{
  background:#e2220dbd
}

button h2 {
  color: #fff
}

button:active,
button:focus {
  outline: none;
  border-style: none;
}

.row {
  display: flex;
}

.form-item {
  height: 35px;
  display: flex;
  border: 1px solid var(--border-color);
  margin-bottom: 20px;

}

.form-item label {
  display: block;
  height: 100%;
}

form input {
  border: none;
  flex: 1;
  padding-left: 10px;
  height: 100%;
  width: 100%;
  box-sizing: border-box;
}

form input:focus {
  outline: none
}

.form-control {
  position: relative;
  flex: 1
}

.error {
  position: absolute;
  bottom: -17px;
  left: 0px;
  color: red;
  font-size: 10px;
}

a:hover {
  color: var(--hover-color)
}

a,
a:active,
.ant-steps-item-finish .ant-steps-item-icon>.ant-steps-icon,
.ant-steps .ant-steps-item:not(.ant-steps-item-active)>.ant-steps-item-container[role='button']:hover .ant-steps-item-title,
.ant-steps .ant-steps-item:not(.ant-steps-item-active)>.ant-steps-item-container[role='button']:hover .ant-steps-item-subtitle,
.ant-steps .ant-steps-item:not(.ant-steps-item-active)>.ant-steps-item-container[role='button']:hover .ant-steps-item-description,
.ant-pagination-item-active a,
.ant-pagination-item:hover a,
.ant-modal-confirm-btns .ant-btn:not(.ant-btn-primary):hover,
.ant-radio-button-wrapper-checked:not(.ant-radio-button-wrapper-disabled):active,
.ant-radio-button-wrapper-checked:not(.ant-radio-button-wrapper-disabled),
.ant-radio-button-wrapper:hover,
.ant-radio-button-wrapper-checked:hover .ant-radio-button {
  color: var(--primary-color) !important
}

.ant-radio-button-wrapper-checked:not(.ant-radio-button-wrapper-disabled)::before,
.ant-btn-primary:hover,
.ant-btn-primary,
.ant-checkbox-indeterminate .ant-checkbox-inner::after,
.ant-checkbox-checked .ant-checkbox-inner,
.ant-steps-item-process>.ant-steps-item-container>.ant-steps-item-icon,
.ant-steps-item-process .ant-steps-item-icon,
.ant-steps-item-finish>.ant-steps-item-container>.ant-steps-item-content>.ant-steps-item-title::after,
.ant-steps .ant-steps-item:not(.ant-steps-item-active):not(.ant-steps-item-process)>.ant-steps-item-container[role='button']:hover .ant-steps-item-icon {
  background: var(--primary-color) !important;

}

.ant-steps-item-process .ant-steps-item-icon,
.ant-pagination-item-active,
.ant-pagination-item-active:hover,
.ant-pagination-item:hover,
.ant-checkbox-checked .ant-checkbox-inner,
.ant-steps-item-finish .ant-steps-item-icon,
.ant-btn-primary,
.ant-modal-confirm-btns .ant-btn:hover,
.ant-radio-button-wrapper-checked:not(.ant-radio-button-wrapper-disabled),
.ant-radio-button-wrapper-checked:not(.ant-radio-button-wrapper-disabled):active,
.ant-radio-button-wrapper-checked:not(.ant-radio-button-wrapper-disabled):first-child,
.ant-radio-button-wrapper-checked:not([class*=' ant-radio-button-wrapper-disabled']).ant-radio-button-wrapper:first-child {
  border-color: var(--primary-color);
}

.ant-steps-item-wait:hover>.ant-steps-item-container {
  color: #fff
}

.price {
  color: #e4393c
}

.pagination {
  margin-top: 40px;
  text-align: right;
}



.ant-table-thead>tr>th,
.ant-table-tbody>tr>td,
.ant-table tfoot>tr>th,
.ant-table tfoot>tr>td {
  padding: 6px
}

.modal .ant-modal-confirm-body {
  height: 130px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}

.modal .ant-modal-confirm-body>.anticon {
  margin-right: 0;
  font-size: 45px;
}

.modal .ant-modal-confirm-body .ant-modal-confirm-title {
  color: var(--text-color1);
  font-size: 18px;
  font-weight: 700;
}

.modal .ant-modal-confirm-content {
  color: var(--text-color2)
}

.modal.ant-modal-confirm .ant-modal-confirm-btns {
  float: initial;
  text-align: center;
}

.modal .ant-modal-confirm-body>.anticon+.ant-modal-confirm-title+.ant-modal-confirm-content {
  margin-left: 0;
}

.modal .ant-modal-content {
  border: 4px solid var(--text-color2)
}

.scroll::-webkit-scrollbar {
  width: 8px;
}

/* 外层轨道 */
.scroll::-webkit-scrollbar-track {
  background: var(--border-color);
  border-radius: 20px;
}

/* 滚动条可以拖动的那部分 */
.scroll::-webkit-scrollbar-thumb {
  background: var(--text-color2);
  border-radius: 20px;
}

.opera {
  cursor: pointer;
}

.opera:hover,
.ant-tabs-tab:hover .ant-tabs-tab-btn {
  color: var(--hover-color)
}

.ant-tabs {
  color: inherit
}

.ant-tabs-card>.ant-tabs-nav .ant-tabs-tab-active,
.ant-tabs-card>div>.ant-tabs-nav .ant-tabs-tab-active {
  background: var(--primary-color);

}

.ant-tabs-tab .ant-tabs-tab-btn {
  padding: 0 15px
}

.ant-tabs-tab.ant-tabs-tab-active .ant-tabs-tab-btn {
  color: #fff;
}

.ant-tabs-card.ant-tabs-top>.ant-tabs-nav .ant-tabs-tab+.ant-tabs-tab,
.ant-tabs-card.ant-tabs-bottom>.ant-tabs-nav .ant-tabs-tab+.ant-tabs-tab,
.ant-tabs-card.ant-tabs-top>div>.ant-tabs-nav .ant-tabs-tab+.ant-tabs-tab,
.ant-tabs-card.ant-tabs-bottom>div>.ant-tabs-nav .ant-tabs-tab+.ant-tabs-tab {
  margin-left: 0px;
}

.ant-tabs-card>.ant-tabs-nav .ant-tabs-tab,
.ant-tabs-card>div>.ant-tabs-nav .ant-tabs-tab {
  border: none
}

.ant-tabs-nav-wrap {
  border-bottom: 1px solid var(--primary-color);
  background: #f7f7f7
}
</style>
