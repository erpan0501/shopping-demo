<template>
    <el-table  :data="state.data" stripe border class="result-table">
        <slot></slot>
    </el-table>
    <el-pagination 
    background layout="total, prev, pager, next" 
    :total="state.total" 
    @current-change="onPageChange"
    :current-page="state.pagination.page"
     />
</template>
<script setup>
import { computed, onMounted, reactive, watch } from 'vue'

const { request, filters = {} } = defineProps(['request', 'filters'])
const state = reactive({
    data: [],
    total:0,
    pagination: { page: 1, size: 10 },

})
//请求列表数据
const onGetData = () => {
    request({
        ...filters,
        page: state.pagination.page,
        size: state.pagination.size
    }).then(data => {
        state.data = data.records;
        state.total = data.total
    })
}
//切换页码的时候请求列表
const onPageChange = (page) => {
    state.pagination = { page, size: 10 }
    onGetData()

}
//在变更（不是替换）对象或数组时，新值与旧值相同，
//因为他们指向同一数组或对象，Vue不会保留变更前值的副本。
//所以我们这里利用计算属性来使其保留
const copyFilters=computed(()=>JSON.parse(JSON.stringify(filters)))
watch(copyFilters, (val,preval) => {
    console.log(val)
    if(val._update!=preval._update){
        state.pagination = { page:1, size: 10 }
        onGetData()
    }
    
})

onMounted(onGetData)
</script>