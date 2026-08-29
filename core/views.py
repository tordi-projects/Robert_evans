from django.shortcuts import render

SERVICES = [
    {
        'code': 'PL-01',
        'trade': 'plumbing',
        'name': 'Emergency Repairs',
        'desc': 'Burst pipes, leaks and blockages fixed fast — day or night, no overtime surprises.',
    },
    {
        'code': 'PL-02',
        'trade': 'plumbing',
        'name': 'Installations',
        'desc': 'Water heaters, fixtures, sump pumps and full re-pipes, installed to code.',
    },
    {
        'code': 'PL-03',
        'trade': 'plumbing',
        'name': 'Drain & Sewer',
        'desc': 'Camera inspection, hydro-jetting and trenchless repair for stubborn clogs.',
    },
    {
        'code': 'EL-01',
        'trade': 'electrical',
        'name': 'Panel Upgrades',
        'desc': 'Breaker panel swaps and service upgrades sized for modern loads.',
    },
    {
        'code': 'EL-02',
        'trade': 'electrical',
        'name': 'Wiring & Rewiring',
        'desc': 'New circuits, outlets and full rewires for older homes, done safely.',
    },
    {
        'code': 'EL-03',
        'trade': 'electrical',
        'name': 'Maintenance',
        'desc': 'Inspections and preventative fixes that keep your power flowing reliably.',
    },
]

STEPS = [
    {'label': 'Reach out', 'desc': 'Send your issue through the site — a photo helps.'},
    {'label': 'Get a plan', 'desc': "Robert replies in your dashboard with a fix and a fair quote."},
    {'label': 'We show up', 'desc': "Licensed, insured & bonded — residential or commercial."},
    {'label': 'Flows & power restored', 'desc': "Job done right, follow-up if anything needs a second look."},
]


def home(request):
    context = {
        'services': SERVICES,
        'steps': STEPS,
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')
