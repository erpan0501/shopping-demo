<template>
    <Dialog :visible="info" :title="info.title" :footer="null">
        <el-table :data="info.data" row-key="rid">
            <el-table-column label="权限名" prop="permissionName"/>
            <el-table-column label="资源路径" prop="url"/>
        </el-table>
    </Dialog>
</template>

<script setup>
import { Dialog } from '@/components';
const { info } = defineProps(['info'])
</script>

