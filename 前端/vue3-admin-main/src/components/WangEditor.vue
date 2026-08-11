<template>
    <div style="border: 1px solid #ccc">
        {{ aa }}
        <Toolbar style="border-bottom: 1px solid #ccc" :editor="editorRef" :defaultConfig="toolbarConfig" />
        <Editor style="height: 300px; overflow-y: hidden;" v-model="valueHtml" :defaultConfig="editorConfig"
            :mode="mode" @onCreated="handleCreated" @onChange="onChange" />
    </div>
</template>
<script setup>

import { onBeforeUnmount, ref, shallowRef, onMounted, computed, onUpdated, watch } from 'vue'
import '@wangeditor/editor/dist/css/style.css' // 引入 css
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'

const props = defineProps(['defaultValue'])
const emit = defineEmits(['change'])
// 编辑器实例，必须用 shallowRef
const editorRef = shallowRef()

// 内容 HTML
const valueHtml = ref()

// 模拟 ajax 异步获取内容
// onMounted(() => {
//     valueHtml.value = defaultValue

// })
const value = computed(() => {
    return props.defaultValue
})
watch(value, (val, preVal) => {
    console.log(val)
    valueHtml.value=val
})
const toolbarConfig = {}
const editorConfig = {
    placeholder: '请输入内容...',
    MENU_CONF: {}
}
editorConfig.MENU_CONF['uploadImage'] = {
    fieldName:'file',
    server: 'file/uploadImage',
    customInsert(res ,insertFn) {
        // res 即服务端的返回结果

        // 从 res 中找到 url alt href ，然后插图图片
        insertFn(res.data)
    },
}
const onChange = (editor) => {
    emit('change', editor.getHtml())
}

// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
    const editor = editorRef.value
    if (editor == null) return
    editor.destroy()
})

const handleCreated = (editor) => {
    editorRef.value = editor // 记录 editor 实例，重要！

}

</script>    