<template>
    <el-card>
        <el-button :icon="Plus" type="primary" @click="onAdd">
            新增
        </el-button>
        <Table :request="onRequest" :filters="state.filters">
            <el-table-column label="商品名">
                <template #default="scope">
                    <el-avatar style="vertical-align: middle;margin-right: 15px;" shape="square" :size="60"
                        :src="scope.row.headerPic" />
                    <span>{{ scope.row.title }}</span>
                </template>
            </el-table-column>
            <el-table-column label="原价格" prop="price" />
            <el-table-column label="秒杀价格" prop="costPrice">
                <template #default="scope">
                    <span style="color:red">￥ {{ scope.row.costPrice }}</span>
                </template>
            </el-table-column>
            <el-table-column label="开始时间" prop="startTime" />
            <el-table-column label="结束时间" prop="endTime" />
            <el-table-column label="秒杀商品数量" prop="num" />
            <el-table-column label="商品库存" prop="stockCount" />
            <el-table-column label="商品描述" width="100">
                <template #default="scope">
                    <el-popover placement="bottom" title="商品描述" :width="200" trigger="click">
                        <template #reference>
                            <el-button link>查看</el-button>
                        </template>
                        <div v-html="scope.row.introduction"></div>
                    </el-popover>
                </template>
            </el-table-column>
            <el-table-column align="right" label="操作">
                <template #default="scope">
                    <el-button link @click="onEdit(scope.row)">修改</el-button>
                </template>
            </el-table-column>
        </Table>
       
    </el-card>
    <SeckillForm v-if="state.form" :form="state.form" @cancel="state.form = null"
        @save="state.filters._update = Date.now()" />
    <SeckillForm v-if="state.detailForm" :info="state.detailForm" @cancel="state.detailForm = null" />
</template>
<script setup>
import { reactive } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import axios from '@/utils/axios';
import SeckillForm from './SeckillForm'
import _ from 'lodash'


const state = reactive({
    filters: { _update: Date.now() },
    form: null,
    detailForm: null
})
const onRequest = (params = {}) => {
    return axios.get('seckillGoods/findPage', { params })
}

// 新增
const onAdd = () => {
    state.form = {
        title: '新增',
        data: {}
    }

}
const onEdit = (row) => {
    state.form = {
        title: '编辑',
        data: {
            ..._.cloneDeep(row),
            time:[new Date(row.startTime),new Date(row.endTime)],
            }
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
