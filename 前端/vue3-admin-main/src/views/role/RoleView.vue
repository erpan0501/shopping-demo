<template>
    <el-card>
        <el-button :icon="Plus" type="primary" @click="onAdd">
            新增
        </el-button>
        <Table :request="onRequest" :filters="state.filters">
            <el-table-column prop="roleName" label="角色名" />
            <el-table-column prop="roleDesc" label="角色描述" />
            <el-table-column align="right" label="操作">
                <template #default="scope">
                    <el-button link @click="onEdit(scope.row)">修改</el-button>
                    <el-button link @click="onViewPerm(scope.row)">查看权限</el-button>
                    <el-button link @click="onEditPerm(scope.row)">修改权限</el-button>
                    <DeleteBtn @confirm="onDelete(scope.row)" />

                </template>
            </el-table-column>
        </Table>

    </el-card>
    <RoleForm v-if="state.form" :form="state.form" @cancel="state.form = null"
        @save="state.filters._update = Date.now()" />
    <RolePerms v-if="state.permDialog" :info="state.permDialog" />
    <RoleEditPerm v-if="state.permForm" :info="state.permForm" @cancel="state.permForm = null" />
</template>
<script setup>
import { reactive } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import axios from '@/utils/axios';
import RoleForm from './RoleForm'
import RolePerms from './RolePerms'
import RoleEditPerm from './RoleEditPerm'
import { DeleteBtn } from '@/components';
import { ElMessage } from 'element-plus'
import _ from 'lodash'

const state = reactive({
    form: null,
    permDialog: null,
    permForm: null,
    filters: { _update: Date.now() }
})
const onRequest = (params = {}) => {
    return axios.get('role/search', { params })

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

    axios.delete('role/delete', { params: { rid: row.rid } }).then(data => {
        ElMessage.success('操作成功')
        state.filters._update = Date.now()
    })


}
// 查看权限
const onViewPerm = (row) => {
    axios.get('role/findById', { params: { rid: row.rid } }).then(data => {
    state.permDialog = {
        title: "权限",
        data: data.permissions
    }
    })

}
// 修改权限
const onEditPerm = (row) => {

    axios.get('role/findById', { params: { rid: row.rid } }).then(data => {
        
    state.permForm = {
        title: '修改权限',
        data: { rid: row.rid, permissions: data.permissions }
    }
    })



}

</script>
