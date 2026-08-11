<template>
 <el-dialog v-model="visible" :title="title" :width="width||'600px'" destroy-on-close @close="onClose">
    <slot></slot> 
    <template #footer v-if="footer!==null">
      <span class="dialog-footer">
        <el-button @click="onClose">取消</el-button>
        <el-button type="primary" @click="onSave">
          确定
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>
<script setup>
const {visible,title,width,footer}=defineProps(['visible','title','width','footer'])

const emit=defineEmits(['close','save'])
const onClose=()=>{
    emit('close')
}
const onSave=()=>{
    emit('save')
}
</script>