if (typeof navigator !== 'undefined') {
  navigator.serviceWorker.getRegistrations().then(function (registrations) {
    for (const registration of registrations) {
      registration.unregister()
    }
  })
}

caches.keys().then(function (names) {
  for (const name of names) caches.delete(name)
})
