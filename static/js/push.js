// push.js — registers this device to receive message alerts, once the
// visitor is logged in. Runs once per page load; a device only ever
// re-subscribes if it doesn't already have an active subscription.

(function () {
  function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
    const rawData = atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; i++) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
  }

  function postJSON(url, body) {
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify(body),
    });
  }

  async function enablePushNotifications() {
    if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
      return; // browser doesn't support it — fail quietly, site works fine without it
    }
    if (!window.VAPID_PUBLIC_KEY) return;

    try {
      const registration = await navigator.serviceWorker.register('/sw.js');

      let permission = Notification.permission;
      if (permission === 'default') {
        permission = await Notification.requestPermission();
      }
      if (permission !== 'granted') return;

      let subscription = await registration.pushManager.getSubscription();
      if (!subscription) {
        subscription = await registration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: urlBase64ToUint8Array(window.VAPID_PUBLIC_KEY),
        });
      }

      await postJSON('/inbox/push/subscribe/', subscription.toJSON());
    } catch (err) {
      console.warn('Push notification setup skipped:', err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enablePushNotifications);
  } else {
    enablePushNotifications();
  }
})();
