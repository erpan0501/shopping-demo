<template>
  <Dialog :title="form.title" :visible="form" @close="emit('cancel')" @save="onSave">
    <el-form :model="formData" :rules="rules" label-width="80px" ref="formRef">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="formData.username" autocomplete="off" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="formData.password" autocomplete="off" />
      </el-form-item>

    </el-form>
  </Dialog>
  
</template>

<script setup>
import { ref } from 'vue';
import axios from '@/utils/axios'
import { Dialog } from '@/components'
import { ElMessage } from 'element-plus';

const { form } = defineProps(['form'])
let formData = form.data
const emit = defineEmits(['cancel', 'save'])
const formRef = ref()

// 定义表单的验证规则
const rules = {
  username: [{ required: true, message: '用户名不能为空' }],
  password:form.title=='新增'? [{ required: true, message: '密码不能为空' }]:[],
};
// 保存数据
const onSave = () => {
  const params = { username: formData.username, password: formData.password }
  if (form.title == '新增') {
    formRef.value.validate((valid) => {
      if (valid) {
        axios.post('admin/add', params).then(data => {
          ElMessage.success('操作成功')
          emit('cancel')
          emit('save')
        })
      }
    })
    return
  }
  formRef.value.validate((valid) => {
    if (valid) {
      axios.put('admin/update', { ...params, aid: formData.aid }).then(data => {
        ElMessage.success('操作成功')
        emit('cancel')
        emit('save')
      })
    }
  })

}


</script>