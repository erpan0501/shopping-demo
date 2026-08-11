<template>
  <div class="container">
    <div class="box">
      <h3>后台管理系统</h3>
      <el-form @keypress.enter="onSubmit" hide-required-asterisk :model="modelForm" ref="form" :rules="rules">
        <el-form-item label="用户名" label-width="60px" prop="username">
          <el-input :prefix-icon="User" type="text" v-model="modelForm.username" />
        </el-form-item>
        <el-form-item label="密码" label-width="60px" prop="password">
          <el-input :prefix-icon="Lock" type="password" v-model="modelForm.password" />
        </el-form-item>
        <el-form-item label-width="60px">
          <el-button type="primary" style="width: 100%" @click="onSubmit">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { User, Lock } from "@element-plus/icons-vue";
import axios from '@/utils/axios'
import { useRouter } from 'vue-router'

const form = ref(null);
const router = useRouter()
const modelForm = reactive({ username: undefined, password: undefined });
const rules = reactive({
  username: [{ required: true, message: '用户名不能为空' }],
  password: [{ required: true, message: '密码不能为空' }],
});
const onSubmit = () => {
  form.value.validate((valid) => {
    if (valid) {
      const form=new FormData()
      form.append('username',modelForm.username)
      form.append('password',modelForm.password)
      axios.post('admin/login', form).then(data => {
        router.push('/')
      })
    }
  });
};


</script>

<style lang="scss" scoped>
.container {
  height: 100%;
  background: url(../assets/video-cover.jpeg);
  color: #fff;
  text-align: center;
}

.box {
  width: 360px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  border-radius: 15px;
  padding: 20px;

  :deep(.el-form-item__label) {
    color: #fff;
  }
}
</style>

