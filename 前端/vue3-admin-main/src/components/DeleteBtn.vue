<template>
    <el-popconfirm @confirm="onConfirm" title="确认要删除吗?">
        <template #reference>
            <el-button  link type="danger" >删除</el-button>
        </template>
    </el-popconfirm>
</template>

<script setup>
// const props=defineProps(['confirmFn'])
const emit=defineEmits(['confirm'])
const onConfirm=()=>{
    // console.log('delete')
    emit('confirm')
}
</script>