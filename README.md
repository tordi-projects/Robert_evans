# Robert Evan's Plumbing & Electrician — Django site

A full site for the business: a friendly, conventional marketing site (trust
badges, reviews, FAQ), customer accounts, two-way in-dashboard messaging, and
real phone/desktop push notifications when a new message arrives.

## What's included

- **Public site** — home page (hero, trust bar, services, how-it-works,
  reviews, FAQ, contact CTA) and an about page. Clean, bright, conventional
  trade-business design: blue/gold palette, rounded cards, plenty of plain
  reassuring copy — no jargon, no gimmicks.
- **Accounts** — registration (name, email, username, password, optional
  phone/address) and login/logout, using Django's standard auth system.
- **Customer dashboard** (`/inbox/dashboard/`) — a customer's private thread
  with Robert. They start a ticket (topic + description), then send/receive
  replies on the same page.
- **Robert's inbox** (`/inbox/admin/`) — staff-only. Lists every customer
  conversation (search by name/email, unread badges), click into one to read
  the full thread and reply.
- **Django admin** (`/django-admin/`) — full data admin as a backup/raw view.
- **Push notifications** — once a customer or Robert is logged in and grants
  permission, their browser registers for Web Push. The instant the other
  side sends a message, a real OS-level notification (with sound, via the
  browser/OS default) pops up on that device — even if the site isn't open
  in a tab. This uses the standard Web Push API + a service worker
  (`static/js/sw.js`), no third-party push service required.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # this account = Robert / staff = admin inbox access
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

- Log in with the superuser account you created → you land in **Robert's
  inbox** at `/inbox/admin/`.
- Register a normal account (e.g. in an incognito window) → that account
  lands in the **customer dashboard** at `/inbox/dashboard/`. Send a
  message, then log back in as the superuser to see it and reply.

Any user with `is_staff=True` is "Robert" / an admin who can see and reply
to all conversations. Promote more staff/dispatcher accounts from
`/django-admin/` → Users → check "Staff status".

## Push notifications — how it works, and what to know

A working VAPID key pair is already generated and committed
(`vapid_private_key.pem` + the matching public key in `settings.py`), so
push notifications work out of the box on your machine. For production:

1. Generate your own key pair (don't reuse the sample one publicly):
   ```bash
   openssl ecparam -genkey -name prime256v1 -noout -out vapid_private_key.pem
   openssl ec -in vapid_private_key.pem -pubout -outform DER | tail -c 65 | base64 | tr -d '=' | tr '/+' '_-'
   ```
   The second command prints your public key — set it as the `VAPID_PUBLIC_KEY`
   environment variable. Point `VAPID_PRIVATE_KEY_PATH` at wherever you keep
   the `.pem` (keep it out of version control) and set `VAPID_CLAIMS_EMAIL`
   to `mailto:you@yourdomain.com`.
2. Push **requires HTTPS** in production (localhost is exempt, so local dev
   works without it). Deploy behind TLS.
3. **Sound**: browsers don't let a website supply a custom sound file for
   notifications — but as long as the notification isn't marked `silent`
   (ours isn't), the OS plays its normal system notification sound
   automatically. That's as close to "make a sound" as the open web spec
   allows, and it works the same way native apps' notifications do.
4. **iOS Safari** only supports Web Push if the site has been added to the
   Home Screen (iOS 16.4+). Desktop Chrome/Edge/Firefox and Android Chrome
   support it directly in the browser, no install needed.
5. If a user's device stops responding to push (uninstalled, permission
   revoked, etc.), we detect that on the next failed send and quietly
   remove that subscription — no manual cleanup needed.

## Project layout

```
accounts/    registration form + Profile (phone/address) extending Django's User
core/        public marketing pages (home, about) + business info context processor
messaging/   Conversation + Message + PushSubscription models, dashboards, push sending
templates/   base.html + one template per page
static/css/  the entire design system in a single stylesheet
static/js/   push.js (subscribes the browser) + sw.js (service worker that shows alerts)
```

## Notes for going to production

- Set `DJANGO_DEBUG=False` and a real `DJANGO_SECRET_KEY` /
  `DJANGO_ALLOWED_HOSTS` as environment variables before deploying.
- Swap SQLite for Postgres by changing `DATABASES` in `plumbing_site/settings.py`.
- Run `python manage.py collectstatic` and serve `staticfiles/` via your web
  server or a service like WhiteNoise.
- Consider adding email notifications as a fallback for devices that never
  granted push permission.
