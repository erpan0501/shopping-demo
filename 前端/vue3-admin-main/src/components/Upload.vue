<template>
    <el-upload ref="upload"  action="file/uploadImage" list-type="picture-card"
        :on-success="onUploadSuccess" :before-upload="onBeforeUpload"
         :file-list="state.fileList" :on-remove="onRemove"
        :limit="limit" :on-exceed="onExceed">
        <el-icon>
            <Plus />
        </el-icon>
    </el-upload>
</template>
<script setup>
import { computed, reactive, ref, watch } from 'vue';
import { ElMessage } from 'element-plus';

const props = defineProps(['defaultFile', 'limit'])
console.log(props.defaultFile,'defulatFile')
const {limit=1}=props
const emit = defineEmits(['change'])
const upload = ref(null)
const state = reactive({
    files: [],//所有图片
    // 默认展示的图片
    fileList: []
})
const defaultObj = computed(() =>props.defaultFile)
watch(defaultObj, (val, preVal) => {
    console.log(val,'val')
    console.log(preVal,'preVal')
    if (val&&val.length ) {
        state.fileList = val.map(item => ({ name: item.imageTitle, url: item.imageUrl }))
        state.files = val
    }
},{immediate:true})
const onUploadSuccess = (
    response,
    uploadFile
) => {
    const { name, response: res } = uploadFile
    state.files.push({ imageTitle: name, imageUrl: res.data })
    if (limit == 1) {
        state.files = [{ imageTitle: name, imageUrl: res.data }]
    }
    emit('change', state.files)
}
const onRemove = (file, files) => {
    const { response = {} } = file
    const removeFile = state.files.find(item => item.imageUrl == (file.url || response.data))
    const index = state.files.indexOf(removeFile)
    state.files.splice(index, 1)
    emit('change', state.files)
}

const onBeforeUpload = (rawFile) => {
    const { type } = rawFile
    if (type !== 'image/jpeg' && type !== 'image/png' && type !== 'image/jpg') {
        ElMessage.error('不是正确的图片格式')
        return false
    } else if (rawFile.size > 1024 * 1024 * 10) {
        ElMessage.error('图片大小不能超过 10MB!')
        return false
    }
    return true
}
const onExceed = (files, uploadFiles) => {
    ElMessage.warning('最多只能上传' + limit + "张图片")
}
</script>