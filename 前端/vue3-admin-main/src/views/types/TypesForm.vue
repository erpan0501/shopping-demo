<template>
  <Dialog :visible="form" :title="form.title" @close="emit('cancel')" @save="onSave">
    <el-form :model="formData" :rules="rules" label-width="100px" ref="formRef">
      <el-form-item label="父级类型：" v-if="form.title == '新增'">
        {{ formData.parentName || '无' }}

      </el-form-item>
      <template v-if="form.title == '编辑'">
        <el-form-item label="父级类型：">
          <el-tree-select check-strictly=true v-model="formData.parentId" lazy :load="load" :props="{
            label: 'name',
            value: 'id'
            // children: 'children',
            // isLeaf: 'isLeaf',
          }" />
          <el-button size="small" style="margin-left:20px" link type="primary" @click="onCancelReSelect">取消</el-button>
        </el-form-item>
      </template>

      <el-form-item label="类型名：" prop="name">
        <el-input v-model="formData.name" autocomplete="off" />
      </el-form-item>
    </el-form>

  </Dialog>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from '@/utils/axios'
import { Dialog } from '@/components';
import { ElMessage } from 'element-plus';

const { form } = defineProps(['form'])
let formData = form.data
const parentId = formData.parentId

const emit = defineEmits(['cancel', 'save'])
const formRef = ref()

// 定义表单的验证规则
const rules = {
  name: [{ required: true, message: '类型名不能为空' }]
};
// 保存数据
const onSave = () => {
  console.log(formData.parentId, 'value')
  const params = { name: formData.name, parentId: formData.parentId }
  if (form.title == '新增') {
    formRef.value.validate((valid) => {
      if (valid) {
        axios.post('productType/add', params).then(data => {
          ElMessage.success('操作成功')
          emit('cancel')
          emit('save', formData.parentId)
        })
      }
    })
    return
  }

  formRef.value.validate((valid) => {
    if (valid) {
      axios.put('productType/update', { ...params, id: formData.id }).then(data => {
        ElMessage.success('操作成功')
        emit('cancel')

        if (parentId != formData.parentId) {

          emit('save', parentId)
        }
        emit('save', formData.parentId)
      })
    }
  })

}
// 点击取消回调
const onCancelReSelect = () => {
  // 父级类型恢复默认值
  formData.parentId = parentId

}
// 一进来页面会调用一次，点击上级类型也会调用
const load = (node, resolve) => {
  // 当点击的是无的时候，返回空数组
  if (node.data.id === 0) {
    resolve([])
    return 
     
  }
  axios.get('productType/findByParentId', { params: { parentId: node.data.id||0 } }).then(data => {
// 第一次加载的时候，除了获取第一级的数据再加一个id=0的无
    if ( node.data.id == undefined) {
      data.unshift({ id: 0, name: '无' })
    }
    resolve(data)
  })
}

</script>