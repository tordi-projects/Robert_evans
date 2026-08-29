# Robert Evan's Plumbing & Electrician — Django site

A full site for the business: marketing home page, customer accounts, and a
two-way messaging system — every message a customer sends lands in Robert's
inbox, and his replies show up in the customer's own dashboard. Built with
plain Django (no JS framework needed).

## What's included

- **Public site** — home page, services (plumbing + electrical), about page.
- **Accounts** — registration (name, email, username, password, optional
  phone/address) and login/logout, using Django's standard auth system.
- **Customer dashboard** (`/inbox/dashboard/`) — a customer's private thread
  with Robert. They start a ticket (pick a topic + describe the issue), then
  send/receive replies on the same page.
- **Robert's inbox** (`/inbox/admin/`) — only visible to staff accounts.
  Lists every customer conversation (search by name/email, unread badges),
  click into one to read the full thread and reply.
- **Django admin** (`/django-admin/`) — full data admin for conversations,
  messages, and customer profiles, in case Robert wants raw DB access too.
- A custom, from-scratch visual design (copper/brass/patina palette, "work
  order ticket" card motif) — not a default Bootstrap/Tailwind template.

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

- Log in with the superuser account you created → you'll land in **Robert's
  inbox** at `/inbox/admin/` (staff accounts always go there).
- Register a normal account (e.g. from an incognito window) → that account
  lands in the **customer dashboard** at `/inbox/dashboard/`. Send a message,
  then log back in as the superuser to see it in the inbox and reply.

Any user with `is_staff=True` is treated as "Robert" / an admin who can see
and reply to all conversations. You can promote more staff/dispatcher
accounts later from `/django-admin/` → Users → check "Staff status".

## Project layout

```
accounts/    registration form + Profile (phone/address) extending Django's User
core/        public marketing pages (home, about) + business info context processor
messaging/   Conversation + Message models, customer dashboard, admin inbox
templates/   base.html + one template per page
static/css/  the entire design system in a single stylesheet
```

## Notes for going to production

- Set `DJANGO_DEBUG=False` and a real `DJANGO_SECRET_KEY` / `DJANGO_ALLOWED_HOSTS`
  as environment variables before deploying.
- Swap SQLite for Postgres by changing `DATABASES` in `plumbing_site/settings.py`.
- Run `python manage.py collectstatic` and serve `staticfiles/` via your web
  server or a service like WhiteNoise.
- Consider adding email notifications (Django's `django.core.mail`) so Robert
  gets pinged when a new message arrives, and hooking the reply form up to
  WebSockets/HTMX if you want live updates without a page refresh.
