<template>
  <Dialog :visible="form" :title="form.title" @close="emit('cancel')" @save="onSave">
    <el-form :model="formData" :rules="rules" label-width="100px" ref="formRef">

      <el-form-item label="商品类型：" prop="productTypeId" v-if="form.title == '新增'">
        <el-tree-select check-strictly=true v-model="formData.productTypeId" lazy :load="load" :props="{
          label: 'name',
          value: 'id'
          // children: 'children',
          // isLeaf: 'isLeaf',
        }" />
      </el-form-item>
      <el-form-item label="规格名：" prop="specName">
        <el-input v-model="formData.specName" autocomplete="off" />
      </el-form-item>
    </el-form>

  </Dialog>
</template>

<script setup>
import { ref, reactive } from 'vue';
import axios from '@/utils/axios'
import { Dialog } from '@/components';
import { ElMessage } from 'element-plus';

const { form } = defineProps(['form'])
let formData = form.data
const emit = defineEmits(['cancel', 'save'])
const formRef = ref()

// 定义表单的验证规则
const rules = {
  specName: [{ required: true, message: '规格名不能为空' }],
  productTypeId: [{ required: true, message: '商品类型不能为空' }],
};
// 保存数据
const onSave = () => {
  const params = { specName: formData.specName, productTypeId: formData.productTypeId }
  if (form.title == '新增') {
    formRef.value.validate((valid) => {
      if (valid) {
        axios.post('specification/add', params).then(data => {
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
      axios.put('specification/update', { specName: formData.specName, id: formData.id }).then(data => {
       
       ElMessage.success('操作成功')
       emit('cancel')
        emit('save')
      })
    }
  })

}
const load = (node, resolve) => {
  // if (node.isLeaf) return resolve([])
  console.log(node.data.id)

  axios.get('productType/findByParentId', {params:{parentId: node.data.id || 0}}).then(data => {
    resolve(data)
  })
}

</script>