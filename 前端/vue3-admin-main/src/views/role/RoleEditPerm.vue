<template>
    <Dialog :visible="info" :title="info.title" @close="emit('cancel')" @save="onSave">
        <el-table ref="multipleTable" :data="allPermissions" row-key="rid" @selection-change="onSelectionChange">
            <el-table-column type="selection" />
            <el-table-column label="权限名" prop="permissionName" />
            <el-table-column label="资源路径" prop="url" />
        </el-table>
    </Dialog>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from '@/utils/axios';
import { Dialog } from '@/components';
import { ElMessage } from 'element-plus';

const { info } = defineProps(['info'])
const emit = defineEmits(['cancel'])
const multipleTable = ref(null)
let pids = []
const allPermissions = ref([])
onMounted(() => {
    // 获取所有角色
    axios.get('permission/findAll').then(data => {
        
        allPermissions.value = data;
        (info.data.permissions || []).map(row => {
            pids.push(row.pid)
            setTimeout(function () {
                // 默认选中该用户拥有的权限
                multipleTable.value.toggleRowSelection(allPermissions.value.find(item => item.pid == row.pid), true);
            }, 0)

        })
    })

})

const onSelectionChange = (keys) => {
    pids = []
    keys.map(item => {
        pids.push(item.pid)
    })

}
const onSave = () => {
    const form=new FormData()
    form.append('rid',info.data.rid)
    form.append('pids',pids)
    axios.put('role/updatePermissionToRole', form).then(data => {
        ElMessage.success('操作成功')
        emit('cancel')
    })
}
</script>
