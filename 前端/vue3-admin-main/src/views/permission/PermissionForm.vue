<template>
  <Dialog :visible="form" :title="form.title" @close="emit('cancel')" @save="onSave">
    <el-form :model="formData" :rules="rules" label-width="80px" ref="formRef">
      <el-form-item label="权限名" prop="permissionName">
        <el-input v-model="formData.permissionName" autocomplete="off" />
      </el-form-item>
      <el-form-item label="资源路径" prop="url">
        <el-input   v-model="formData.url"  autocomplete="off"/>
      </el-form-item>

    </el-form>
    
  </Dialog>
</template>

<script setup>
import { ref } from 'vue';
import axios from '@/utils/axios'
import { Dialog } from '@/components';
import { ElMessage } from 'element-plus';

const { form } = defineProps(['form'])
let formData = form.data
const emit = defineEmits(['cancel', 'save'])
const formRef = ref()

// 定义表单的验证规则
const rules = {
  permissionName: [{ required: true, message: '权限名不能为空' }],
  url: [{ required: true, message: '资源路径不能为空' }],
};
// 保存数据
const onSave = () => {
  const params={permissionName:formData.permissionName,url:formData.url}
  if (form.title == '新增') {
    formRef.value.validate((valid) => {
      if (valid) {
        axios.post('permission/add', params).then(data => {
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
      axios.put('permission/update', { ...params,pid:formData.pid }).then(data => {
        ElMessage.success('操作成功')
        emit('cancel')
        emit('save')
      })
    }
  })

}


</script>