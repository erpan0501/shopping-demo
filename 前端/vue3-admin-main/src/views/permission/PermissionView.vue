<template>
    <el-card>
        <el-button :icon="Plus" type="primary" @click="onAdd">
            新增
        </el-button>
        <Table :request="onRequest" :filters="state.filters">
            <el-table-column prop="permissionName" label="权限名"/>
            <el-table-column prop="url" label="资源路径"/>
            <el-table-column align="right" label="操作">
                <template #default="scope">
                    <el-button link @click="onEdit(scope.row)">修改</el-button>
                    <DeleteBtn @confirm="onDelete(scope.row)" />

                </template>
            </el-table-column>
        </Table>
       
    </el-card>
    <PermissionForm v-if="state.form" :form="state.form" @cancel="state.form = null" @save="state.filters._update=Date.now()" />
</template>
<script setup>
import {  reactive } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import axios from '@/utils/axios';
import PermissionForm from './PermissionForm'
import { DeleteBtn } from '@/components';
import { ElMessage } from 'element-plus'
import _ from 'lodash'

const state = reactive({
    tableData: [],
    total: 0,
    form: null,
    filters:{_update:Date.now()}
})
const onRequest = (params = {}) => {
    return  axios.get('permission/search', { params})
    

}

// 新增管理用户
const onAdd = () => {
    state.form = {
        title: '新增',
        data: {}
    }

}
const onEdit = (row) => {
    state.form = {
        title: '编辑',
        data: _.cloneDeep(row)
    }
}

const onDelete = (row) => {
        axios.delete('permission/delete', { params: { pid: row.pid } }).then(data => {
            ElMessage.success('操作成功')
            state.filters._update=Date.now()
        })

}


</script>
