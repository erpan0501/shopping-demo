<template>
    <a-modal class="modal" :visible="true" :title="modalInfo.title" :footer="null" @cancel="emit('cancel')" width="600px">
        <a-form tri :model="formData" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }" autocomplete="off"
            @finish="onSave">
            <a-form-item label="所在地区" name="areaObj"
                :rules="[{ required: true, message: '所在地区不能为空', validator: validateAreaObj, trigger: 'finish' }]">
                <AreaCascader v-model="formData.areaObj" />
            </a-form-item>
            <a-form-item label="详细地址" name="address" :rules="[{ required: true, message: '详细地址不能为空' }]">
                <Input.TextArea v-model:value="formData.address" />
            </a-form-item>

            <a-form-item label="联系人" name="contact" :rules="[{ required: true, message: '联系人不能为空' }]">
                <a-input v-model:value="formData.contact" />
            </a-form-item>
            <a-form-item label="手机" name="mobile" :rules="[{ required: true, message: '手机不能为空' }]">
                <a-input v-model:value="formData.mobile" />
            </a-form-item>
            <a-form-item label="邮编" name="zipCode" :rules="[{ required: true, message: '邮编不能为空' }]">
                <a-input v-model:value="formData.zipCode" />
            </a-form-item>
            <div class="modalfooter">
                <button @click="emit('cancel')">取消</button>
                <button class="primary" html-type="submit">确定</button>
            </div>

        </a-form>
    </a-modal>

</template>

<script setup>
import { Input } from 'ant-design-vue'
import { AreaCascader } from '@/components'
import { onMounted, reactive } from 'vue';
import { axios } from '@/utils';


const emit = defineEmits(['cancel', 'save'])
const { modalInfo } = defineProps(['modalInfo'])
const formData = modalInfo.data


onMounted(() => {
    if (modalInfo.title == '编辑') {
        axios.get('user/address/findById',{params:{id:formData.id}}).then(data=>{
            
        formData.areaObj = { ...data }
        })
    }
})

const validateAreaObj = (rule, val) => {

    if (!val.provinceName || !val.cityName || !val.areaName) {
        return Promise.reject()
    }
    return Promise.resolve()
}

const onSave = () => {
    const params = {
        provinceName: formData.areaObj.provinceName,
        cityName: formData.areaObj.cityName,
        areaName: formData.areaObj.areaName,
        address: formData.address,
        mobile: formData.mobile,
        contact: formData.contact,
        zipCode: formData.zipCode,
    }
    if (modalInfo.title == '新增') {
        axios.post('user/address/add', params).then(data => {
            emit('save')
        })
        return
    }
    axios.put('user/address/update', { ...params, id: formData.id }).then(data => {
        emit('save')
    })

}





</script>

<style scoped>
.modalfooter {
    text-align: right;
}

.modalfooter button {
    margin-right: 15px;
}
</style>