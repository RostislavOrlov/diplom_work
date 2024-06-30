const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    // proxy: 'http://localhost:8000/offer',
    // host: '192.168.1.123',
    host: '0.0.0.0',
    port: 8080,
    // https: true,
    // hotOnly: false
  }
})
