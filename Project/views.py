from django.shortcuts import render_to_response, HttpResponse, RequestContext, Http404
from models import Project, Part, BoMToParts, BoMtoProject, BoM, TaskToProject, Task

import json
import datetime
# Create your views here.


def index(request):
    """
        The main index page
    """
    datadict = {}
    projects = Project.objects.all()[:5]
    #orders = BoMToParts.objects.filter(ordered=True).all()[:5]
    #deliveries = BoMToParts.objects.filter(ordered=True, arrived=False).all()[:5]
    datadict['projects'] = projects
    #datadict['orders'] = orders
    #datadict['deliveries'] = deliveries
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
    boms = BoMtoProject.objects.filter(project=project).all()
    tasks_links = TaskToProject.objects.filter(project=project).all()
    tasks = [i.task for i in tasks_links]
    c = RequestContext(request, {'project': project,
                                 'BoMs': boms,
                                 'tasks': tasks
    })
    return render_to_response('Project/detail.html', c)


def create_bom(request):
    """
        Create a new bill of materials
    """
    #We should have been posted a project id to start with.....
    if request.method == 'POST':
        project = Project.objects.filter(id=request.POST['projid']).get()
        parts = Part.objects.all()
        c = RequestContext(request, {'projid': project.id,
                                     'parts': parts
                                     })
        return render_to_response('Project/new_bom.html', c)
    else:
        raise Http404()


def new_part(request):
    """
        Ajax method to create a new part
        returns the new parts id on success and false on failure
    """
    returndict = {}
    if request.method == 'POST':
        try:
            partdict = json.loads(request.POST['newpart'])
            newpart = Part()
            newpart.name = partdict['name']
            newpart.source = partdict['source']
            newpart.description = partdict['description']
            newpart.cost = float(partdict['cost'])
            newpart.save()
            returndict['id'] = newpart.id
        except Exception, e:
            returndict['error'] = e.message

    return HttpResponse(json.dumps(returndict), content_type="application/json")


def create_bom_ajax(request):
    """
        Method to create a new bom
    """
    returnDict = {}
    if request.method == 'POST':
        try:
            bomdict = json.loads(request.POST['bomdict'])
            bom = BoM()
            bom.name = bomdict['name']
            bom.description = bomdict['description']
            bom.save()

            for part in bomdict['parts']:
                mainpart = Part.objects.filter(id=part['id']).get()
                bomtoparts = BoMToParts()
                bomtoparts.bom = bom
                bomtoparts.part = mainpart
                bomtoparts.quantity = part['quantity']
                bomtoparts.save()

            bomtoproject = BoMtoProject()
            bomtoproject.bom = bom
            bomtoproject.project = Project.objects.filter(id=bomdict['projid']).get()
            bomtoproject.save()

            returnDict['id'] = bom.id
        except Exception, e:
            returnDict['error'] = e.message

    return HttpResponse(json.dumps(returnDict), content_type="application/json")


def bom_detail(request, bomid):
    """
        Shows all the bom details
    """
    bom = BoM.objects.filter(id=bomid).get()
    parts = BoMToParts.objects.filter(bom=bom).all()
    c = RequestContext(request, {
        'bom': bom,
        'parts': parts
    })
    return render_to_response('Project/bom_detail.html', c)


def add_task_ajax(request, id):
    """
        Simple routine to add a task to a project
        TODO: finish this :)
    """
    returnDict = {}
    if request.method == 'POST':
        try:
            taskdict = json.loads(request.POST['datadict'])
            task = Task()
            task.completed = False
            task.date_added = datetime.datetime.now()
            task.title = taskdict['task_title']
            task.description = taskdict['task_description']
            task.save()

            link = TaskToProject()
            link.task = task
            link.project = Project.objects.filter(id=id).get()
            link.save()

            returnDict['id'] = task.id
        except Exception, e:
            returnDict['error'] = e.message

    return HttpResponse(json.dumps(returnDict), content_type="application/json")


def toggle_task(request, id, projid):
    """
        Toggles a tasks completion status
    """
    task = Task.objects.filter(id=id).get()
    if task.completed:
        task.completed = False
    elif not task.completed:
        task.completed = True
    task.save()
    return HttpResponse(json.dumps({}), content_type="application/json")


def new_order(request):
    """
        Page for creating a new order
    """

    return render_to_response('Project/new_order.html', {})