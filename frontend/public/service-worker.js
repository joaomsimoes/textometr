if (typeof navigator !== 'undefined') {
  navigator.serviceWorker.getRegistrations().then(function (registrations) {
    for (const registration of registrations) {
      registration.unregister()
    }
  })
}
