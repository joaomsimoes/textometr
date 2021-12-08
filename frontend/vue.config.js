const path = require('path')
const PrerenderSPAPlugin = require('prerender-spa-plugin')

module.exports = {
  devServer: {
    proxy: 'http://backend:8888'
  },
  pwa: {
    name: 'Текстометр',
    themeColor: '#007a7a',
    msTileColor: '#007a7a',
    appleMobileWebAppCache: 'yes',
    manifestOptions: {
      background_color: '#ffffff'
    },
    workboxOptions: {
      skipWaiting: true
    }
  },
  configureWebpack: {
    plugins:
      process.env.NODE_ENV === 'production'
        ? [
            new PrerenderSPAPlugin({
              staticDir: path.join(__dirname, 'dist'),
              routes: ['/']
            })
          ]
        : []
  }
}
