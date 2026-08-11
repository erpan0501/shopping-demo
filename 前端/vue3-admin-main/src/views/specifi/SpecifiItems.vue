<template>
    <Dialog :visible="info" :title="info.title" :footer="null" @close="emit('cancel')">
        <el-button size="small" type="primary" :icon="Delete" @click="onRemove">删除</el-button>
        <el-table class="result-table" :data="state.tableData" @selection-change="onSelectionChange" max-height="350">
            <el-table-column type="selection" />
            <el-table-column prop="optionName" label="规格项" />

        </el-table>
    </Dialog>

</template>

<script setup>
import { onMounted, reactive } from 'vue';
import axios from '@/utils/axios'
import { Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { Dialog } from '@/components';

const { info } = defineProps(['info'])
const emit = defineEmits(['cancel'])
let state = reactive({
    tableData: [],
    ids: []
})
const onGetList = () => {
    axios.get('specification/findById', { params: { id: info.data.id } }).then(data => {
        state.tableData = data.specificationOptions
    })
}
onMounted(() => {
    console.log(2222);
    onGetList()

}
)


const onSelectionChange = (rows) => {
    state.ids = rows.map(item => item.id)
}

const onRemove = () => {
    if (!state.ids.length) {
        ElMessage.warning('请先勾选要删除的数据！')
        return
    }
    let url = 'specification/deleteOption?'
    state.ids.map((item, index) => {
        url += 'ids=' + item + (index < state.ids.length - 1 ? '&' : '')
    })
    axios.delete(url).then(data => {
        ElMessage.success('操作成功')
        onGetList()
    })

}

</script>