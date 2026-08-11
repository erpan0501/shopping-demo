import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import {Steps,Carousel,Card,Pagination,Tag,Table, ConfigProvider ,
    Popconfirm,Modal,Form,Cascader,Select,Input,Radio,Popover,Dropdown,Menu,Tabs} from 'ant-design-vue'

createApp(App)
.use(router)
.use(Steps)
.use(Carousel)
.use(Card)
.use(Pagination)
.use(Tag)
.use(Table)
.use(ConfigProvider)
.use(Popconfirm)
.use(Modal)
.use(Form)
.use(Cascader)
.use(Select)
.use(Input)
.use(Radio)
.use(Popover)
.use(Dropdown)
.use(Menu)
.use(Tabs)
.mount('#app')
