<template>
    <Dialog :title="info.title" :visible="info" :footer="null">
        <el-table :data="info.data" row-key="rid">
            <el-table-column type="expand">
                <template #default="scope" :style="{ padding: '0 30px' }">
                    <el-table :data="scope.row.permissions" border :style="{ marginLeft: '50px', width: '500px' }">
                        <el-table-column label="权限名" prop="permissionName"/>
                        <el-table-column label="权限资源路径" prop="url"/>
                    </el-table>
                </template>
            </el-table-column>
            <el-table-column label="角色名" prop="roleName"/>
            <el-table-column label="角色描述" prop="roleDesc"/>
        </el-table>
    </Dialog>
</template>

<script setup>
import { Dialog } from '@/components';
const { info } = defineProps(['info'])
</script>

