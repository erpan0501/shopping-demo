<template>
    <div class="address">
        <h4>填写收货人信息</h4>
        <a class="addBtn" @click="onAddAddress">新增收货地址</a>
        <p v-if="!state.addresses.length" style="color:var(--primary-color);line-height:60px;text-align:center">暂无收货地址，请先新增</p>
        <template v-if="!!state.collapse&&state.addresses.length">
            <div class="row active">
                <p>{{ state.receiver }}</p>
                <p>
                    {{ state.receiverAreaName }}&nbsp;&nbsp;
                    {{ state.receiverMobile }}

                </p>
                <a @click.stop="onEditAddress(selectedAdd)">编辑</a>
                <a @click.stop="onRemoveAddress(selectedAdd)">删除</a>

            </div>
            <span @click="state.collapse = false" class="opera">
                更多地址
                <down-outlined />
            </span>
        </template>
        <template v-else-if="state.addresses.length">
            <div class="scroll">
                <div class="row" :class="{ active: selectedAdd.id == item.id }" v-for="item in state.addresses"
                    @click="onSelectAddress(item)">
                    <p>{{ item.contact }}</p>
                    <p>
                        <!-- {{ item.contact }}&nbsp;&nbsp; -->
                        {{ item.provinceName }}&nbsp;
                        {{ item.cityName }}&nbsp;
                        {{ item.areaName }}&nbsp;
                        {{ item.address }}&nbsp;
                        {{ item.mobile }}&nbsp;
                    </p>
                    <a @click.stop="onEditAddress(item)">编辑</a>
                    <a @click.stop="onRemoveAddress(item)">删除</a>
                </div>
            </div>

            <span @click="state.collapse = true" class="opera">
                收起地址
                <up-outlined />
            </span>
        </template>

    </div>
    <AddressForm v-if="state.modal" :modalInfo="state.modal" @cancel="state.modal = null" @save="onCloseAddForm" />
</template>

<script setup>
import { reactive, watch, ref, onMounted ,createVNode} from 'vue';
import { axios } from '@/utils'
import { Modal } from 'ant-design-vue';
import { UpOutlined, DownOutlined,ExclamationCircleOutlined } from '@ant-design/icons-vue'
import AddressForm from './AddressForm.vue';

const emit = defineEmits(['changes'])
const selectedAdd = ref({})
const state = reactive({
    addresses: [],
    collapse: true,
    modal: null,
    receiverAreaName: '',
    receiver: '',
    receiverMobile: '',
    receiverZipCode: ''
})

const onGetAddressList = () => {
    axios.get('user/address/findByUser').then(data => {
    state.addresses =data
    selectedAdd.value = state.addresses[0]
    })
}
watch(selectedAdd, (val) => {
    if (val) {
        state.receiver = val.contact
        state.receiverMobile = val.mobile
        state.receiverZipCode = val.zipCode
        state.receiverAreaName = `${val.provinceName} ${val.cityName} ${val.areaName} ${val.address}`
        emit('changes',{
            receiver:state.receiver,
            receiverMobile:state.receiverMobile,
            receiverZipCode:state.receiverZipCode,
            receiverAreaName:state.receiverAreaName

            })
    }
}, { immediate: true }
)
const onCloseAddForm = () => {
    state.modal = null;
    onGetAddressList()

}
// 选择收货地址
const onSelectAddress = (item) => {
    selectedAdd.value = item
    state.collapse = true
}
// 编辑收货地址
const onEditAddress = (item) => {
    state.modal = {
        title: '编辑',
        data: { ...item }
    }
}

// 新增收货地址
const onAddAddress = () => {
    state.modal = {
        title: '新增',
        data: {}
    }
}

// 删除收货地址
const onRemoveAddress = (item) => {
    Modal.confirm({
        title: '删除',
        icon: createVNode(ExclamationCircleOutlined),
        content: createVNode('div', {}, '确认要删除该地址吗?'),
        onOk() {
            axios.delete('user/address/delete', { params: { id: item.id } }).then(data => {
                onGetAddressList()

            })
        },
        okText: '确认',
        cancelText: '取消',
        class: 'modal',
    });

}

onMounted(onGetAddressList)
</script>

<style scoped>
.address{
    position: relative;
}
.address .row {
    margin-left: 15px;
    align-items: center;
    margin-top: 15px;
    cursor: pointer;
    padding-right: 15px;
}

.address .row p:nth-child(1) {
    width: 120px;
    height: 28px;
    font-size: 15px;
    border: 1px solid var(--border-color);
    text-align: center;
}
.address .row.active p:nth-child(1),
.address .row:hover p:nth-child(1) {
    border: 2px solid var(--primary-color);
    background: #fff
}

.address .row p:nth-child(2) {
    flex: 1;
    padding: 3px 15px
}

.address .row:hover {
    background: rgb(234, 238, 234);

}

.address .row a {
    display: none;
    margin-right: 8px;
}

.address .row:hover a {
    display: block;

}
.addBtn {
    position: absolute;
    right: 10px;
    top: 0px
}
.address .opera {
    position: relative;
    top: 10px;
    margin-left: 15px;
    cursor: pointer;
}

.address .opera .anticon {
    font-size: 12px;
}


</style>