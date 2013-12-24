from django.shortcuts import render_to_response, HttpResponse, RequestContext
from models import Project, Part, BoMToParts
import json
import datetime
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
    c = RequestContext(request, {
        'projects': projects,
        })
    return render_to_response('Project/projects.html', c)


def new_project(request):
    """
        Create a new project
    """
    c = RequestContext(request)
    return render_to_response('Project/new_project.html', c)


def create_new_project(request):
    """
        Takes in an ajax request to create a new project
    """
    returnDict = {}
    if request.method == 'POST':
        print request.POST
        try:
            datadict = json.loads(request.POST['projectdata'])
            print datadict
            #we have stuff to process
            project = Project()
            project.title = datadict['name']
            project.startDate = datetime.datetime.strptime(datadict['startDate'], "%m/%d/%Y")
            project.category = datadict['category']
            project.complete = False
            project.save()
            returnDict['id'] = project.id
        except Exception, e:
            print e
            returnDict['error'] = e.message
    return HttpResponse(json.dumps(returnDict), content_type="application/json")


def project_detail(request, newid="0"):
    """
        Get's all of the detail for a specific project
    """
    newid = int(newid)
    project = Project.objects.filter(id=newid).get()
    c = RequestContext(request, {'project': project})
    return render_to_response('Project/detail.html', c)