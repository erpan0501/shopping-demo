<template>
    <Dialog :visible="info" :title="info.title" width="700px" @close="emit('cancel')" @save="onSave">
        <el-table ref="singleTableRef" :data="state.tableData" highlight-current-row @row-click="onSelect">
            <el-table-column type="index" />
            <el-table-column property="date" label="商品">
                <template #default="scope">
                    <!-- <el-avatar style="vertical-align: middle;margin-right: 15px;" shape="square" :size="60"
                        :src="scope.row.headerPic" /> -->
                    <span>{{ scope.row.goodsName }}</span>
                </template>
            </el-table-column>
            <el-table-column align="right">
                <template #default="scope">
                    <el-icon v-if="scope.row.id == state.selected.id"
                        style="color:var(--el-color-primary);font-size: 20px;font-weight: bold;">
                        <Check />
                    </el-icon>
                </template>

            </el-table-column>

        </el-table>
        <el-pagination :current-page="state.pagination.page" background layout="total, prev, pager, next"
            :total="state.total" @current-change="onPageChange" />
       
    </Dialog>
</template>
  

  <script setup>
  import { onMounted, reactive, ref } from 'vue';
  import axios from '@/utils/axios'
  
  const { info } = defineProps(['info'])
  const emit = defineEmits(['cancel', 'save'])
  const singleTableRef = ref()
  const state = reactive({
      tableData: [],
      total: 0,
      pagination: { page: 1, size: 10 },
      selected: {},
      total:0
  })
  const onGetList = () => {
      axios.get('goods/search', {params:{ page: state.pagination.page, size: state.pagination.size }}).then(data => {
          state.tableData = data.records
          state.total=data.total
  
      })
  }
  onMounted(onGetList)
  //切换页码的时候请求列表
  const onPageChange = (page) => {
      state.pagination = { page, size: 10 }
      onGetList()
  
  }
  const onSelect = (row) => {
      singleTableRef.value.setCurrentRow(row)
      state.selected = row
  }
  const onSave = () => {
      emit('cancel')
      emit('save', state.selected)
  }
  </script>