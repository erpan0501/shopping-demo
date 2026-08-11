<template>
    <el-card>
        <el-button :icon="Plus" type="primary" @click="onAdd">
            新增
        </el-button>
        <Table :request="onRequest" :filters="state.filters">
            <el-table-column prop="username" label="用户名" />
            <el-table-column align="right" label="操作">
                <template #default="scope">
                    <el-button link @click="onEdit(scope.row)">修改</el-button>
                    <el-button link @click="onViewRole(scope.row)">查看角色</el-button>
                    <el-button link @click="onEditRole(scope.row)">修改角色</el-button>
                    <DeleteBtn @confirm="onDelete(scope.row)" />
                </template>
            </el-table-column>
        </Table>

    </el-card>
    <UserForm v-if="state.form" :form="state.form" @cancel="state.form = null"
        @save="state.filters._update = Date.now()" />
    <UserRoles v-if="state.roleDialog" :info="state.roleDialog" />
    <UserEditRole v-if="state.roleForm" :info="state.roleForm" @cancel="state.roleForm = null" />
</template>
<script setup>
import { onMounted, reactive, toRefs } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import axios from '@/utils/axios';
import UserForm from './UserForm'
import UserRoles from './UserRoles'
import UserEditRole from './UserEditRole'
import { DeleteBtn } from '@/components';
import { ElMessage } from 'element-plus'
import _ from 'lodash'

const state = reactive({
    filters: { _update: Date.now() },
    form: null,
    roleDialog: null,
    roleForm: null,
})
const onRequest = (params = {}) => {
    return axios.get('admin/search', { params })

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
        // data: {username:row.username,password:row.password,aid:row.aid} 
        data: { username: row.username, aid: row.aid }
    }
}

const onDelete = (row) => {
    axios.delete('admin/delete', { params: { aid: row.aid } }).then(data => {
        ElMessage.success('操作成功')
        state.filters._update = Date.now()
    })

}
// 查看角色权限
const onViewRole = (row) => {
    axios.get('admin/findById', { params: { aid: row.aid } }).then(data => {
        state.roleDialog = {
            title: "角色与权限",
            data: data.roles
        }
    })

}
// 修改角色
const onEditRole = (row) => {

    axios.get('admin/findById', { params: { aid: row.aid } }).then(data => {
        state.roleForm = {
            title: '修改角色',
            data: { aid: row.aid, roles: data.roles }
        }
    })



}

</script>
