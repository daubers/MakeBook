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


def all_projects(request):
    """
        The main projects page
    """
    datadict = {}
    projects = Project.objects.filter(complete=False).all()
    datadict['projects'] = projects
    return render_to_response('Project/projects.html', datadict)


def new_project(request):
    """
        Create a new project
    """
    datadict = {}
    return render_to_response('Project/new_project.html', datadict)
