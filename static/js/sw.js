// sw.js — Robert Evan's Plumbing & Electrician
// Runs in the background once registered; the browser/OS wakes it up when a
// push arrives, even if no tab is open. showNotification() triggers the
// device's normal notification sound/vibration unless `silent: true` is set
// (we don't set it, so the OS default sound plays).

self.addEventListener('install', function (event) {
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('push', function (event) {
  let data = {};
  try {
    data = event.data ? event.data.json() : {};
  } catch (e) {
    data = { title: "Robert Evan's Plumbing & Electrician", body: event.data ? event.data.text() : 'You have a new message.' };
  }

  const title = data.title || "Robert Evan's Plumbing & Electrician";
  const options = {
    body: data.body || 'You have a new message.',
    tag: 'plumbing-message',
    renotify: true,
    vibrate: [200, 100, 200],
    data: { url: data.url || '/' },
  };

  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  const targetUrl = (event.notification.data && event.notification.data.url) || '/';

  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (clientList) {
      for (const client of clientList) {
        if (client.url.indexOf(targetUrl) !== -1 && 'focus' in client) {
          return client.focus();
        }
      }
      if (self.clients.openWindow) {
        return self.clients.openWindow(targetUrl);
      }
    })
  );
});
