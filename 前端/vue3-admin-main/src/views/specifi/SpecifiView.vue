<template>
    <el-card>
        <el-button :icon="Plus" type="primary" @click="onAdd">
            新增
        </el-button>
        <el-button :icon="Delete" @click="onDelete(state.ids)">
            删除
        </el-button>
        <el-table :data="state.tableData" stripe border class="result-table" @selection-change="onSelectionChange">
            <el-table-column type="selection" />
            <el-table-column prop="specName" label="规格名" />
            <el-table-column prop="productType" label="商品类型" />
            <el-table-column align="right" label="操作">
                <template #default="scope">
                    <el-button link @click="onEdit(scope.row)">修改</el-button>
                    <el-button link @click="onAddItems(scope.row)">新增规格项</el-button>
                    <el-button link @click="onViewItems(scope.row)">查看规格项</el-button>
                    <DeleteBtn @confirm="onDelete([scope.row.id])" />

                </template>
            </el-table-column>
        </el-table>
        <el-pagination background layout="total, prev, pager, next" :total="state.total"
            @current-change="onPageChange" />
    </el-card>
    <SpecifiForm v-if="state.form" :form="state.form" @cancel="state.form = null" @save="onGetList" />
    <SpecifiItemForm v-if="state.itemsForm" :form="state.itemsForm" @cancel="state.itemsForm = null" />
    <SpecifiItems v-if="state.items" :info="state.items" @cancel="state.items = null" />
</template>
<script setup>
import { onMounted, reactive, toRefs } from 'vue'
import { Plus, Delete } from '@element-plus/icons-vue'
import axios from '@/utils/axios';
import SpecifiForm from './SpecifiForm'
import SpecifiItemForm from './SpecifiItemForm'
import SpecifiItems from './SpecifiItems'
import { DeleteBtn } from '@/components';
import { ElMessage } from 'element-plus'
import _ from 'lodash'


const state = reactive({
    searchForm: {},
    tableData: [],
    total: 0,
    pagination: { page: 1, size: 10 },
    form: null,
    ids: [],
    itemsForm: null,
    items: null
})
const onGetList = () => {
    axios.get('specification/search', {
        params: {
            page: state.pagination.page,
            size: state.pagination.size,
        }
    }).then(data => {
        const { total, records = [] } = data;
        state.total = total
        state.tableData = records
    })
}

//切换页码的时候请求列表
const onPageChange = (page) => {
    state.pagination = { page, size: 10 }
    onGetList()

}
// 组件加载完后请求列表
onMounted(onGetList)
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

const onDelete = (ids) => {
    if (!ids || !ids.length) {
        ElMessage.warning('请先勾选要删除的数据！')
        return
    }

    let url = 'specification/delete?'
    ids.map((item, index) => {
        url += 'ids=' + item + (index < ids.length - 1 ? '&' : '')
    })
    axios.delete(url).then(data => {
        ElMessage.success('操作成功')
        onGetList()
    })
}
// 勾选数据回调
const onSelectionChange = (rows) => {
    state.ids = rows.map(item => item.id)

}
// 为规格添加规格项
const onAddItems = (row) => {
    console.log(row.specName)
    state.itemsForm = {
        title: '新增规格项',
        data: { specId: row.id, specName: row.specName }
    }
}

const onViewItems = (row) => {
    state.items = {
        title: '查看规格项',
        data: { id: row.id }
    }

}


</script>
