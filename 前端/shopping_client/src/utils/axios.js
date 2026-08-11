import axios from 'axios'
import router from '@/router'

// 请求拦截器
axios.interceptors.request.use(function (config) {
    // 在发送请求之前做些什么
    sessionStorage.getItem('token') ? config.headers.Authorization = sessionStorage.getItem('token') : null
    return config;
});

// 响应拦截器
axios.interceptors.response.use(res => {
    const { data = {}, status } = res
    if(status == 200){
        return data.data
    }
},error =>{
    if(error.response?.status == 401){
      router.push('/login')
    }
    return Promise.reject(error)
})

export default axios
