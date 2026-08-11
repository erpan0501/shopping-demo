<template>
    <Dialog :visible="form" :title="form.title" @close="emit('cancel')" @save="onSave">
        <el-form :model="formData" labelWidth="120px">
            <el-form-item style="align-items:center" v-for="(item, index) in items" :key="item.key" :prop="item.value"
                :label="index == 0 ? formData.specName + '：' : ''">
                <el-row :gutter="10" style="width:100%;align-items: flex-end;">
                    <el-col :span="20">
                        <el-input v-model="items[index].value" />
                    </el-col>
                    <el-col :span="4">
                        <el-icon v-if="items.length > 1">
                            <Delete color="#e51313" @click="onRemoveItem(item)" />
                        </el-icon>
                    </el-col>
                </el-row>
            </el-form-item>
            <div style="text-align:center">
                <el-button :icon="Plus" type="primary" @click="onAddItem">添加</el-button>
            </div>
        </el-form>

    </Dialog>

</template>

<script setup>
import { reactive } from 'vue'
import { ElMessage  } from 'element-plus'
import { Delete } from '@element-plus/icons-vue'
import axios from 'axios';
import { Dialog } from '@/components';

const { form } = defineProps(['form'])
const emit = defineEmits(['cancel'])
const formData = form.data
const items = reactive([{ key: Date.now(), value: '' }])

const onAddItem = () => {
    items.push({ key: Date.now(), value: '' })
}

const onRemoveItem = (item) => {

    const index = items.indexOf(item)
    if (index !== -1) {
        items.splice(index, 1)
    }
}

const onSave = () => {
    const optionName = []
    items.map(item => {
        if (item.value) {
            optionName.push(item.value)
        }
    })
    if (optionName.length == 0) {
        ElMessage.warning('请至少填写一项！')
        return
    }
    axios.post('specification/addOption', { specId: formData.specId, optionName }).then(data => {
        ElMessage.success('操作成功')
        emit('cancel')
    })
}
</script>