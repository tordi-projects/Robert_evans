from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

SERVICES = [
    {
        'trade': 'plumbing',
        'name': 'Emergency Repairs',
        'desc': (
            "Burst pipes, active leaks, and blocked lines don't wait for business hours, "
            "and neither do we. Our team is on call around the clock to stop the damage "
            "fast, with no overtime surprises tacked onto the bill."
        ),
    },
    {
        'trade': 'plumbing',
        'name': 'Installations',
        'desc': (
            "From a single new water heater to a full re-pipe of an older home, our "
            "installations are done to current code and backed by our workmanship "
            "guarantee, so you're not calling us back for the same problem twice."
        ),
    },
    {
        'trade': 'plumbing',
        'name': 'Drain & Sewer Service',
        'desc': (
            "We use camera inspection to see exactly what's causing a clog before we "
            "touch anything, then clear it with hydro-jetting or trenchless repair "
            "methods that avoid tearing up your yard whenever possible."
        ),
    },
    {
        'trade': 'electrical',
        'name': 'Panel Upgrades',
        'desc': (
            "Older homes often have panels that were never built for today's appliance "
            "load. We size and install upgraded breaker panels and service entrances "
            "so your circuits aren't working overtime — or tripping when you least want them to."
        ),
    },
    {
        'trade': 'electrical',
        'name': 'Wiring & Rewiring',
        'desc': (
            "New circuits for a renovation, additional outlets for a home office, or a "
            "full rewire of a decades-old property — all handled by licensed electricians "
            "who know how to work safely inside walls that have seen better days."
        ),
    },
    {
        'trade': 'electrical',
        'name': 'Inspections & Maintenance',
        'desc': (
            "A yearly electrical checkup catches small issues — loose connections, aging "
            "wiring, overloaded circuits — long before they become a fire risk or an "
            "expensive emergency call."
        ),
    },
]

STEPS = [
    {
        'label': 'Tell us what\'s going on',
        'desc': 'Create a free account and describe the issue in your own words — a photo helps, but isn\'t required.',
    },
    {
        'label': 'Get a straight answer',
        'desc': 'Robert reviews it personally and replies in your dashboard with next steps and an honest, upfront quote.',
    },
    {
        'label': 'We show up on time',
        'desc': 'Licensed, insured, and bonded technicians arrive in the window we agreed on — residential or commercial.',
    },
    {
        'label': 'We follow up',
        'desc': 'If anything needs a second look after the job is done, you message us the same way you always have.',
    },
]

REVIEWS = [
    {
        'initials': 'JM',
        'name': 'Janet M.',
        'meta': 'Residential · Water heater replacement',
        'body': (
            "Called about a leaking water heater on a Sunday morning and had someone at "
            "my door within two hours. Fair price, no upsell pressure, and they cleaned "
            "up better than they found it."
        ),
    },
    {
        'initials': 'DO',
        'name': 'David O.',
        'meta': 'Commercial · Panel upgrade',
        'body': (
            "We needed a panel upgrade for our shop without shutting down for more than "
            "a day. Robert's crew planned it out ahead of time and it went exactly to "
            "schedule. Would use them again without a second thought."
        ),
    },
    {
        'initials': 'AK',
        'name': 'Amara K.',
        'meta': 'Residential · Drain cleaning',
        'body': (
            "The messaging system alone is worth it — I could describe the clog, send a "
            "photo, and get a real answer back the same evening instead of playing phone tag."
        ),
    },
]

FAQS = [
    {
        'q': 'Do you charge for estimates?',
        'a': (
            "No. Send us the details through your dashboard and we'll give you an honest, "
            "written estimate before any work begins — there's never a charge just to hear "
            "what a job will cost."
        ),
    },
    {
        'q': 'Are you licensed and insured?',
        'a': (
            "Yes. We're fully licensed, insured, and bonded for both plumbing and electrical "
            "work, for residential and commercial properties alike. Proof of coverage is "
            "available on request."
        ),
    },
    {
        'q': 'How fast can someone get to me for an emergency?',
        'a': (
            "For active leaks, no power, or anything that can't wait, we prioritize same-day "
            "dispatch and are reachable 24/7 by phone. For non-urgent work we'll schedule a "
            "time that fits your calendar."
        ),
    },
    {
        'q': 'Do you handle both plumbing and electrical on the same job?',
        'a': (
            "Often, yes — that's the whole idea behind having one crew for both trades. A "
            "water heater swap that also needs a dedicated circuit, for example, doesn't "
            "need two separate contractors and two separate invoices."
        ),
    },
    {
        'q': "Why do I need to create an account to message you?",
        'a': (
            "An account gives you a private, permanent thread with us — you can see every "
            "past conversation, get replies without checking email or missing a call, and "
            "(if you enable it) get an alert the moment we reply, even when the site isn't open."
        ),
    },
]


def home(request):
    context = {
        'services': SERVICES,
        'steps': STEPS,
        'reviews': REVIEWS,
        'faqs': FAQS,
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def service_worker(request):
    """Serves sw.js from the site root (not /static/) so its default scope
    covers the whole site — required for push notifications to work from
    any page, not just wherever the file happens to be hosted."""
    path = settings.BASE_DIR / 'static' / 'js' / 'sw.js'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='application/javascript')
