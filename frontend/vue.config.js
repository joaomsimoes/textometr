module.exports = {
  devServer: {
    proxy: 'http://backend:8888'
  },
  pwa: {
    name: 'Текстометр',
    themeColor: '#007a7a',
    msTileColor: "#007a7a",
    appleMobileWebAppCache: "yes",
    manifestOptions: {
      background_color: "#ffffff"
    },
    workboxOptions: {
      skipWaiting: true
    }
  }
}
