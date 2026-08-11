<template>
    <Dialog :visible="info" :title="info.title" @close="emit('cancel')" @save="onSave">
        <el-table ref="multipleTable" :data="allRoles" row-key="rid" @selection-change="onSelectionChange">
            <el-table-column type="selection" :reserve-selection="true" />
            <el-table-column label="角色名" prop="roleName" />
            <el-table-column label="角色描述" prop="roleDesc" />
        </el-table>
    </Dialog>
</template>

<script setup>
import { onMounted, ref, reactive } from 'vue'
import axios from '@/utils/axios';
import { Dialog } from '@/components';
import { ElMessage } from 'element-plus';

const { info } = defineProps(['info'])
const emit = defineEmits(['cancel'])
const multipleTable = ref(null)
let rids = []
const allRoles = ref([])
onMounted(() => {
    // 获取所有角色
    axios.get('role/findAll').then(data => {
        allRoles.value = data;
        (info.data.roles || []).map(row => {
            rids.push(row.rid)
            // setTimeout(function () {
                // 默认选中该用户拥有的权限
                multipleTable.value.toggleRowSelection(allRoles.value.find(item => item.rid == row.rid), true);
            // }, 0)

        })
    })

})

const onSelectionChange = (keys) => {
    rids = []
    keys.map(item => {
        rids.push(item.rid)
    })

}
const onSave = () => {
    const form=new FormData()
    form.append('aid',info.data.aid)
    form.append('rids',rids)
    axios.put('admin/updateRoleToAdmin', form).then(data => {
        ElMessage.success('操作成功')
        emit('cancel')
    })
}
</script>
