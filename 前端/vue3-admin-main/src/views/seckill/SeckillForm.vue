<template>
  <Dialog :visible="form" :title="form.title" width="700px" @close="emit('cancel')" @save="onSave">
    <el-scrollbar max-height="600px">
      <el-form class="form" :model="state.formData" :rules="rules" label-width="110px" ref="formRef"
        style="overflow:hidden">
        <el-form-item label="商品" prop="title">
          <el-button link type="primary" @click="onSelectGood">请选择商品</el-button>
        </el-form-item>
        <template v-if="state.formData.title">

          <el-form-item label="商品名">
            {{ state.formData.title }}
          </el-form-item>
          <el-form-item label="商品主图">
            <img :src="state.formData.headerPic" alt="" style="width:80px;height: auto;">
          </el-form-item>

          <el-form-item label="商品描述">
            <div v-html="state.formData.introduction"></div>
          </el-form-item>

          <el-row>
            <el-col :span="12">
              <el-form-item label="商品原价">
                <b>{{ state.formData.price }}</b>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="秒杀价" prop="costPrice">
                <el-input-number v-model="state.formData.costPrice" :min="0" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="秒杀商品数" prop="num">
                <el-input-number v-model="state.formData.num" :min="0" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="剩余库存数" prop="stockCount">
                <el-input-number v-model="state.formData.stockCount" :min="0" />
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="活动时间" prop="time">
            <el-date-picker v-model="state.formData.time" type="datetimerange" range-separator="至"
              start-placeholder="秒杀开始时间" end-placeholder="秒杀结束时间" />
          </el-form-item>

        </template>

      </el-form>
    </el-scrollbar>

  </Dialog>
  <TableDialog v-if="state.tableDialog" :info="state.tableDialog" @cancel="state.tableDialog = null"
    @save="onGetSelected" />
</template>

<script setup>
import { ref, reactive } from 'vue';
import axios from '@/utils/axios'
import { ElMessage } from 'element-plus';
import TableDialog from './TableDialog'

const { form } = defineProps(['form'])

const emit = defineEmits(['cancel', 'save'])
const formRef = ref()
const state = reactive({
  tableDialog: null,
  formData: form.data

})
// 定义表单的验证规则
const rules = {
  title: [{ required: true, message: '请先选择一个商品' }],
  costPrice: [{ required: true, message: '秒杀价不能为空' }],
  time: [{ required: true, message: '活动时间不能为空' }],
  num: [{ required: true, message: '秒杀商品数不能为空' }],
  stockCount: [{ required: true, message: '库存数量不能为空' }],


};
const onSelectGood = () => {
  state.tableDialog = {
    title: '选择商品'
  }
}
const onGetSelected = (good) => {
  state.formData.goodsId = good.id
  state.formData.title = good.goodsName
  state.formData.headerPic = good.headerPic
  state.formData.price = good.price
  state.formData.introduction = good.introduction
}

const translateDate = (date) => {
  return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate() + ' ' + date.getHours() + ':' + date.getMinutes() + ":" + date.getSeconds()

}

// 保存数据
const onSave = () => {
  const { formData } = state
  console.log(formData)


  formRef.value.validate((valid) => {
    if (valid) {
      const params = {
        goodsId: formData.goodsId,
        title: formData.title,
        price: formData.price,
        headerPic: formData.headerPic,
        introduction: formData.introduction,
        costPrice: formData.costPrice,
        startTime: translateDate(formData.time[0]),
        endTime: translateDate(formData.time[1]),
        num: formData.num,
        stockCount: formData.stockCount

      }

      if (form.title == '新增') {
        axios.post('seckillGoods/add', params).then(data => {
          ElMessage.success("操作成功")
          emit('cancel')
          emit('save')
        })
        return
      }
      axios.put('seckillGoods/update', { ...params, id: formData.id }).then(data => {
        ElMessage.success("操作成功")
        emit('cancel')
        emit('save')
      })

    }
  })

}



</script>
<style scoped lang="scss">
.form {
  :deep(.el-input-number) {
    width: 100%
  }
}
</style>
