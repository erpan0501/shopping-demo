<template>
    <el-card>
        <el-button :icon="Plus" type="primary" @click="onAdd">
            新增
        </el-button>
        <Table :request="onRequest" :filters="state.filters">
            <el-table-column prop="title" label="广告标题" />
            <el-table-column prop="url" label="广告链接" />
            <el-table-column prop="pic" label="图片">
                <template #default="scope">
                    <img :src="scope.row.pic" style="height:60px" />
                </template>
            </el-table-column>
            <el-table-column prop="status" label="状态">
                <template #default="scope">
                    <el-switch size="large" :active-value="1" :inactive-value="0" v-model="scope.row.status"
                        inline-prompt active-text="启用" inactive-text="未启用" />
                </template>
            </el-table-column>
            <el-table-column align="right" label="操作">
                <template #default="scope">
                    <el-button link @click="onEdit(scope.row)">修改</el-button>
                    <DeleteBtn @confirm="onDelete(scope.row)" />
                </template>
            </el-table-column>
        </Table>
    </el-card>
    <AdvertForm v-if="state.form" :form="state.form" @cancel="state.form = null" @save="state.filters._update=Date.now()" />
</template>
<script setup>
import { reactive } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import axios from '@/utils/axios';
import AdvertForm from './AdvertForm'
import { DeleteBtn } from '@/components';
import { ElMessage } from 'element-plus'
import _ from 'lodash'

const state = reactive({
    form: null,
    filters:{_update:Date.now()}
})
const onRequest = (params = {}) => {
   return  axios.get('category/search', { params })
      
}

// 新增管理用户
const onAdd = () => {
    state.form = {
        title: '新增',
        data: { status: 1 }
    }

}
const onEdit = (row) => {
    state.form = {
        title: '编辑',
        data: _.cloneDeep(row)
    }
}
const onDelete = (row) => {
        axios.delete('category/delete?ids='+row.id).then(data => {
            ElMessage.success('操作成功')
            state.filters._update=Date.now()
        })
}

</script>
