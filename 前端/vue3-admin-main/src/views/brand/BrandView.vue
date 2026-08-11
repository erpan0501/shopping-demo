<template>
    <el-card>
        <el-form :inline="true" :model="state.filters">
            <el-form-item label="品牌名：">
                <el-input v-model="state.filters.name" clearable />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSearch">搜索</el-button>
            </el-form-item>
        </el-form>
        <el-button :icon="Plus" type="primary" @click="onAdd">
            新增
        </el-button>
        <Table :request="onRequest"  :filters="state.filters">
            <el-table-column prop="name" label="品牌名" />
            <el-table-column align="right" label="操作">
                <template #default="scope">
                    <el-button link @click="onEdit(scope.row)">修改</el-button>
                    <DeleteBtn @confirm="onDelete(scope.row)" />
                </template>
            </el-table-column>
        </Table>
        
    </el-card>
    <BrandForm v-if="state.form" :form="state.form" @cancel="state.form = null" @save="state.filters._update=Date.now()" />
</template>
<script setup>
import {  reactive } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import axios from '@/utils/axios';
import BrandForm from './BrandForm'
import { DeleteBtn ,Table} from '@/components';
import { ElMessage } from 'element-plus'
import _ from 'lodash'

const state = reactive({
    filters: {_update:Date.now()},
    form: null
})
const onRequest=(params)=>{
    return axios.get('brand/search' ,{params})
}

//点击搜索按钮，过滤数据
const onSearch = () => {
    state.filters._update=Date.now()
}

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
        axios.delete('brand/delete', { params: { id: row.id } }).then(data => {
            ElMessage.success('操作成功')
            state.filters._update=Date.now()
        })

}


</script>
