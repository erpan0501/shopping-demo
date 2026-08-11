const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
 
  transpileDependencies: true,
  lintOnSave: false,
  css: {
    loaderOptions: {
      less: {
        lessOptions: {
          modifyVars: {
            'primary-color': "#00b683",
            // 'link-color': '#1DA57A',
            // 'border-radius-base': '2px',
          },
          javascriptEnabled: true,
        },
      },
    },
  },
  devServer: {
    port: 8081,   
    // 代理服务器
    proxy: {
      '/user/seckillGoods': {
        target: 'http://localhost:8090',
        changeOrigin: true,
        // pathRewrite: {
        //   '^/api': ''
        // }
      },
      '/user/shoppingUser': {
        target: 'http://localhost:8090',
        changeOrigin: true,
        // pathRewrite: {
        //   '^/api': ''
        // }
      },
      '/user/category': {
        target: 'http://localhost:8090',
        changeOrigin: true,
        // pathRewrite: {
        //   '^/api': ''
        // }
      },
      '/user/goodsSearch': {
        target: 'http://localhost:8090',
        changeOrigin: true,
        // pathRewrite: {
        //   '^/api': ''
        // }
      },
      '/user/cart': {
        target: 'http://localhost:8090',
        changeOrigin: true,
        // pathRewrite: {
        //   '^/api': ''
        // }
      },
      '/user/(address||orders||payment)': {
        target: 'http://localhost:8090',
        changeOrigin: true,
        // pathRewrite: {
        //   '^/api': ''
        // }
      },
     
    }

  }
})
