<template>
    <el-card>
        <el-form :inline="true" :model="state.filters">
            <el-form-item label="商品名：">
                <el-input v-model="state.filters.goodsName" clearable />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSearch">搜索</el-button>
            </el-form-item>
        </el-form>

        <el-button :icon="Plus" type="primary" @click="onAdd">
            新增
        </el-button>
        <Table :request="onRequest" :filters="state.filters">
            <el-table-column label="商品名">
                <template #default="scope">
                    <el-avatar style="vertical-align: middle;margin-right: 15px;" shape="square" :size="60"
                        :src="scope.row.headerPic" />
                    <span>{{ scope.row.goodsName }}</span>
                </template>
            </el-table-column>
            <el-table-column label="副标题" prop="caption" />
            <el-table-column label="价格" prop="price">
                <template #default="scope">
                    <span style="color:red">￥ {{ scope.row.price }}.00</span>
                </template>
            </el-table-column>
            <el-table-column label="是否上架" prop="isMarketable">
                <template #default="scope">
                    {{ scope.row.isMarketable ? '是' : '否' }}
                </template>
            </el-table-column>

            <el-table-column align="right" label="操作">
                <template #default="scope">
                    <el-button link @click="onView(scope.row)">查看</el-button>
                    <el-button link @click="onEdit(scope.row)">修改</el-button>
                    <el-button link @click="onOperate(scope.row)">{{ scope.row.isMarketable ? '下架' : '上架' }}</el-button>

                </template>
            </el-table-column>
        </Table>

    </el-card>
    <GoodForm v-if="state.form" :form="state.form" @cancel="state.form = null" @save="state.filters._update=Date.now()" />
    <GoodDetail v-if="state.detailForm" :info="state.detailForm" @cancel="state.detailForm = null" />
</template>
<script setup>
import { reactive } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import axios from '@/utils/axios';
import GoodForm from './GoodForm'
import GoodDetail from './GoodDetail'
import { ElMessage } from 'element-plus'
import _ from 'lodash'


const state = reactive({
    filters: { _update: Date.now() },
    form: null,
    detailForm: null
})
const onRequest = (params = {}) => {
    return axios.get('goods/search', { params })
}
//点击搜索按钮，过滤数据
const onSearch = () => {
    state.filters._update = Date.now()
}

const onOperate = (row) => {
    axios.put('goods/putAway?id='+row.id+'&isMarketable='+(row.isMarketable ? false : true) ).then(data => {
        ElMessage.success('操作成功')
        state.filters._update = Date.now()
    })
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
        data: {id:row.id}
    }
}


const onView = (row) => {
    state.detailForm = {
        title: '详情',
        data: { id: row.id }
    }
}


</script>

<style>
.el-avatar--square {
    background: none;
}

.el-avatar>img {
    width: 100%;
    height: auto;
}
</style>
