<template>
  <Dialog :visible="form" :title="form.title" @close="emit('cancel')" @save="onSave">
    <el-form :model="formData" :rules="rules" label-width="80px" ref="formRef">
      <el-form-item label="广告标题" prop="title">
        <el-input v-model="formData.title" autocomplete="off" />
      </el-form-item>
      <el-form-item label="广告链接" prop="url">
        <el-input v-model="formData.url" autocomplete="off" />
      </el-form-item>
      <el-form-item label="图片" prop="pic">
        <UploadFile @change="onImageChange" :defaultFile="formData.pic ? [{ imageUrl: formData.pic }] : []" />
      </el-form-item>
      <el-form-item label="广告状态" prop="status">
        <el-switch size="large" :active-value="1" :inactive-value="0" v-model="formData.status" />
      </el-form-item>
    </el-form>

  </Dialog>
</template>
<script setup>
import { ref } from 'vue';
import axios from '@/utils/axios'
import { ElMessage } from 'element-plus';
// import { Upload } from '@/components';

const { form } = defineProps(['form'])
let formData = form.data
console.log(formData)
const emit = defineEmits(['cancel', 'save'])
const formRef = ref()

// 定义表单的验证规则
const rules = {
  title: [{ required: true, message: '广告标题不能为空' }],
  url: [{ required: true, message: '广告链接不能为空' }],
  pic: [{ required: true, message: '广告图片不能为空' }],
};


const onImageChange = (file) => {
  formData.pic = file[0].imageUrl
}

// 保存数据
const onSave = () => {
  const params = { title: formData.title, url: formData.url, pic: formData.pic, status: formData.status }
  if (form.title == '新增') {
    formRef.value.validate((valid) => {
      if (valid) {
        axios.post('category/add', params).then(data => {
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
      axios.put('category/update', { ...params, id: formData.id }).then(data => {
        ElMessage.success('操作成功')
        emit('cancel')
        emit('save')
      })
    }
  })

}


</script>