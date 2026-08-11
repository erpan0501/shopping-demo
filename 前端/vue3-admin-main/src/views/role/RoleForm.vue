<template>
  <Dialog :visible="form" :title="form.title" @close="emit('cancel')" @save="onSave">
    <el-form :model="formData" :rules="rules" label-width="80px" ref="formRef">
      <el-form-item label="角色名" prop="roleName">
        <el-input v-model="formData.roleName" autocomplete="off" />
      </el-form-item>
      <el-form-item label="角色描述" prop="roleDesc">
        <el-input  type="textarea" v-model="formData.roleDesc"  />
      </el-form-item>
    </el-form>
  </Dialog>
</template>

<script setup>
import { ref } from 'vue';
import axios from '@/utils/axios'
import { Dialog } from '@/components';

const { form } = defineProps(['form'])
let formData = form.data
const emit = defineEmits(['cancel', 'save'])
const formRef = ref()

// 定义表单的验证规则
const rules = {
  roleName: [{ required: true, message: '角色名不能为空' }],
};
// 保存数据
const onSave = () => {
  const params={roleName:formData.roleName,roleDesc:formData.roleDesc}
  if (form.title == '新增') {
    formRef.value.validate((valid) => {
      if (valid) {
        axios.post('role/add', params).then(data => {
          emit('cancel')
          emit('save')
        })
      }
    })
    return
  }
  formRef.value.validate((valid) => {
    if (valid) {
      axios.put('role/update', { ...params,rid:formData.rid }).then(data => {
        emit('cancel')
        emit('save')
      })
    }
  })

}


</script>