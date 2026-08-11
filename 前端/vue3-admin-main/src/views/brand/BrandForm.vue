<template>
  <Dialog :visible="form" :title="form.title" @close="emit('cancel')" @save="onSave">
    <el-form :model="formData" :rules="rules" label-width="80px" ref="formRef">
      <el-form-item label="品牌名" prop="name">
        <el-input v-model="formData.name" autocomplete="off" />
      </el-form-item>
    </el-form>
    
  </Dialog>
</template>

<script setup>
import { ref ,reactive} from 'vue';
import axios from '@/utils/axios'
import { Dialog } from '@/components';

const { form } = defineProps(['form'])
let formData =form.data
const emit = defineEmits(['cancel', 'save'])
const formRef = ref()

// 定义表单的验证规则
const rules = {
  name: [{ required: true, message: '品牌名不能为空' }]
};
// 保存数据
const onSave = () => {
  const params={name:formData.name}
  if (form.title == '新增') {
    formRef.value.validate((valid) => {
      if (valid) {
        axios.post('brand/add', params).then(data => {
          emit('cancel')
          emit('save')
        })
      }
    })
    return
  }
  formRef.value.validate((valid) => {
    if (valid) {
      axios.put('brand/update', { ...params,id:formData.id }).then(data => {
        emit('cancel')
        emit('save')
      })
    }
  })

}


</script>