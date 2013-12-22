from django.shortcuts import render_to_response
from models import Project, Part, BoMToParts

# Create your views here.


def index(request):
    """
        The main index page
    """
    datadict = {}
    projects = Project.objects.all()[:5]
    orders = BoMToParts.objects.filter(ordered=True).all()[:5]
    deliveries = BoMToParts.objects.filter(ordered=True, arrived=False).all()[:5]
    datadict['projects'] = projects
    datadict['orders'] = orders
    datadict['deliveries'] = deliveries
    return render_to_response('Project/index.html', datadict)