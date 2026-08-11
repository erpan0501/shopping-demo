<template>
    <Header>
        <div class="right">
            <Steps :current="0" />
        </div>

    </Header>
    <div class="content">
        <h3 class="title"><b>购物车商品</b></h3>
        <a-table :pagination="false" row-key="goodId"
            :row-selection="{ selectedRowKeys: state.selectedKeys, onChange: onSelectChange }" :columns="state.columns"
            :data-source="state.data">
            <template #bodyCell="{ column, record }">
                <template v-if="column.dataIndex == 'goodsName'">
                    <div class="name">
                        <img :src="record.headerPic" alt="">
                        <p>{{ record.goodsName }}</p>
                    </div>

                </template>
                <template v-else-if="column.dataIndex == 'price'">
                    ￥{{ record.price }}
                </template>
                <template v-else-if="column.dataIndex == 'num'">
                    <Count :value="record.num" @changes="onUpdateNum(record.goodId, $event)" />
                </template>
                <template v-else-if="column.dataIndex == 'total'">
                    <b class="price">￥{{ record.num * record.price }}</b>
                </template>
                <template v-if="column.dataIndex == 'id'">
                    <span class="opera" @click="onRemove(record.goodId)">删除</span>

                </template>
            </template>
        </a-table>
    </div>
    <div class="bar">
        <div class="box">
            <h3>已选<u>{{ state.count }}</u>件商品</h3>
            <h3>总价：<b class="price">￥{{ state.total }}</b></h3>
            <button class="primary" @click="onCreateOrder">结算</button>
        </div>
    </div>
    <Footer />
</template>

<script setup>
import { Header, Count, Nav, Footer, Steps } from '@/components';
import { onMounted, reactive, createVNode, watch, computed } from 'vue';
import { axios } from '@/utils'
import { Modal } from 'ant-design-vue';
import { ExclamationCircleOutlined } from '@ant-design/icons-vue'
import { useRouter } from 'vue-router';
import { getDemoCart, isDemoMode, removeDemoCart, updateDemoCart } from '@/utils/demo'

const router = useRouter()
const state = reactive({
    columns: [
        {
            title: '商品',
            dataIndex: 'goodsName',
            width: 600
        },
        {
            title: '单价',
            dataIndex: 'price',
        },
        {
            title: '数量',
            dataIndex: 'num',
        },
        {
            title: '小计',
            dataIndex: 'total',
        },
        {
            title: '操作',
            dataIndex: 'id',
        },
    ],
    data: [],
    count: 0,
    total: 0,
    selectedKeys: [],
    selected: JSON.parse(sessionStorage.getItem('selectedGoods') || '[]')
})
const selected = computed(() => state.selected)
watch(selected, (val) => {
    console.log(val, 'watch')
    if (val) {
        state.count = 0;
        state.total = 0
        state.selectedKeys = []


        val.map(item => {
            state.count += item.num
            state.total += item.num * item.price
            state.selectedKeys.push(item.goodId)
        })

        sessionStorage.setItem('selectedGoods', JSON.stringify(state.selected))

    }

}, { immediate: true, deep: true })


const onGetList = () => {
    if (isDemoMode) {
        state.data = getDemoCart()
        return
    }
    axios.get('user/cart/findCartList').then(data => {
        state.data = data
        window.dispatchEvent(
            new CustomEvent('cartNumChange',{detail:data.reduce((pre, item) => (pre + item.num), 0)}),
            )

        state.selected.map((item, index) => {
            data.map(good => {
                if (item.goodId == good.goodId) {
                    state.selected[index].num = good.num

                }

            })

        })


    })

}
onMounted(onGetList)

const onUpdateNum = (goodId, num) => {
    if (isDemoMode) {
        updateDemoCart(goodId, num)
        onGetList()
        return
    }
    axios.get('user/cart/handleCart', { params: { goodId, num } }).then(data => {
        onGetList()
    })
}

const onSelectChange = (keys, rows) => {
    state.selected = rows
}

const onRemove = (goodId) => {
    Modal.confirm({
        title: '删除',
        icon: createVNode(ExclamationCircleOutlined),
        content: createVNode('div', {}, '确认要删除该商品吗?'),
        onOk() {
            if (isDemoMode) {
                removeDemoCart(goodId)
                const index = state.selectedKeys.findIndex((item) => item == goodId)
                if (index !== -1) state.selectedKeys.splice(index, 1)
                onGetList()
                return
            }
            axios.delete('user/cart/deleteCart', { params: { goodId } }).then(data => {

                const index = state.selectedKeys.findIndex((item) => item == goodId)
                index !== -1 ? state.selectedKeys.splice(index, 1) : null
                onGetList()
            })
        },
        okText: '确认',
        cancelText: '取消',
        class: 'modal',
    });
}

const onCreateOrder = () => {
    if (state.count == 0) {
        Modal.warning({
            title: '请至少选择一种商品',
            content: '',
            okText: '知道了',
            class: 'modal'

        });

        return
    }


    router.push({ name: 'orderinfo' })

}
</script>

<style scoped>
.title {
    margin-bottom: 15px;
}

.content {
    width: 50%;
    margin: 15px auto;
}


input {
    border: 1px solid var(--border-color)
}

input:focus {
    outline: none
}

.name {
    display: flex;
    align-items: center;
}

.name img {
    margin-right: 8px;
    width: 100px
}

.bar {
    width: 100%;
    position: sticky;
    bottom: 0px;
    left: 0;
    background: #fff;
    box-shadow: 0 -1px 8px rgba(0, 1, 1, .08);

}

.box {
    width: 50%;
    height: 50px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: flex-end;
}

.box h3 {
    margin-right: 16px;
}

.price {
    font-size: 20px;
}

u {
    font-size: 20px;
    margin: 0 5px
}

.right {
    position: absolute;
    right: 0;
    top: 50px
}
</style>
