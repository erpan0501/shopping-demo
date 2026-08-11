const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // 保存文件的时候不进行eslink检查
  lintOnSave: false,
  // 开发环境
  devServer: {
    // 本地商城演示后端使用 8090，管理端使用 8082
    port: 8082,
    // 代理服务器
    proxy: {
      '/': {
        target: 'http://localhost:8090',
        changeOrigin: true,
        // pathRewrite: {
        //   '^/api': ''
        // }
      },
    }

  }
})
