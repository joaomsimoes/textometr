caches.keys().then(function (names) {
  for (const name of names) caches.delete(name)
})

self.addEventListener('activate', function () {
  self.registration
    .unregister()
    .then(function () {
      return self.clients.matchAll()
    })
    .then(function (clients) {
      clients.forEach((client) => {
        if (client.url && 'navigate' in client) {
          client.navigate(client.url)
        }
      })
    })
})
