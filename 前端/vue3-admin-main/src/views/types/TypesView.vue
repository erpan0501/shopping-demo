<template>
    <el-card>
        <el-form :inline="true" :model="state.searchForm">
            <el-form-item label="类型名：">
                <el-input v-model="state.searchForm.name" clearable />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSearch">搜索</el-button>
            </el-form-item>
        </el-form>

        <el-button :icon="Plus" type="primary" @click="onAdd">
            新增
        </el-button>
        <el-table ref="table" :data="state.tableData" row-key="id" @expand-change="onExpand" lazy :load="loadChildren"
            stripe border class="result-table">
            <el-table-column prop="name" label="类型名" />

            <el-table-column prop="level" label="类型级别">
                <template #default="scope">
                    <span>{{ scope.row.level }}级</span>
                </template>
            </el-table-column>

            <el-table-column align="right" label="操作">
                <template #default="scope">
                    <el-button link @click="onAdd(scope.row)">新增类型</el-button>
                    <el-button link @click="onEdit(scope.row)">修改</el-button>
                    <DeleteBtn @confirm="onDelete(scope.row)" />

                </template>
            </el-table-column>
        </el-table>
        <el-pagination :current-page="state.pagination.page" background layout="total, prev, pager, next"
            :total="state.total" @current-change="onPageChange" />
    </el-card>
    <TyepsForm v-if="state.form" :form="state.form" @cancel="state.form = null" @save="reloadTree" />
</template>
<script setup>
import { onMounted, reactive, ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import axios from '@/utils/axios';
import TyepsForm from './TypesForm'
import { DeleteBtn } from '@/components';
import { ElMessage } from 'element-plus'
import _ from 'lodash'

const table = ref(null)
const loadMap = new Map();
const state = reactive({
    searchForm: {},
    tableData: [],
    total: 20,
    pagination: { page: 1, size: 10 },
    form: null,
    resolve: null
})
const onGetList = () => {
    axios.get('productType/search', {
        params: {
            page: state.pagination.page,
            size: state.pagination.size,
            name: state.searchForm.name,
            parentId: 0
        }
    }).then(data => {
        const { total, records = [] } = data;
        records.map(item => item.hasChildren = true)
        state.total = total
        state.tableData = records
    })

}

//点击搜索按钮，过滤数据
const onSearch = () => {
    state.pagination = { page: 1, size: 10 }
    onGetList()
}
//切换页码的时候请求列表
const onPageChange = (page) => {
    state.pagination = { page, size: 10 }
    onGetList()

}
// 组件加载完后请求列表
onMounted(onGetList)

const loadChildren = (row, treeNode, resolve) => {
    loadMap.set(row.id, { row, treeNode, resolve });

    axios.get('productType/findByParentId', { params: { parentId: row.id } }).then(data => {

        data.map(item => {
            item.hasChildren = true
            // item.parent = row
        })
        resolve(data)

    })

}
const reloadTree = (parentId) => {
    parentId = parentId ? parseInt(parentId) : 0;
    if (parentId == 0) {
        onGetList()
        return
    }
    const { row, treeNode, resolve } = loadMap.get(parentId);

    // if (table.value.store.states.lazyTreeNodeMap.value[parentId]&&table.value.store.states.lazyTreeNodeMap.value[parentId].length > 1) {
    //     //说明该节点下有多个子节点
    //     table.value.store.states.lazyTreeNodeMap[parentId] = [];
    // } else {
    //说明该节点只有一个节点
    table.value.store.states.lazyTreeNodeMap.value[parentId] = [];
    // }

    loadChildren(row, treeNode, resolve);
}


// 新增管理用户
const onAdd = (row) => {
    state.form = {
        title: '新增',
        data: { parentName: row.name, parentId: row.id || 0 },
    }

}
const onEdit = (row) => {
    state.form = {
        title: '编辑',
        data: _.cloneDeep(row)
    }
}

const onDelete = (row) => {
    axios.delete('productType/delete', { params: { id: row.id } }).then(data => {
        ElMessage.success('操作成功')
        if (row.parentId == 0) {
            onGetList()
            return
        }
        reloadTree(row.parentId)
    })

}


</script>
