from django.shortcuts import render_to_response, HttpResponse, RequestContext, Http404
from models import Project, Part, BoMToParts, BoMtoProject, BoM, TaskToProject, Task, Supplier, SupplierAccount, Order
from models import PartsToOrder
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login


import json
import datetime
# Create your views here.


@login_required()
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

@login_required()
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


@login_required()
def new_project(request):
    """
        Create a new project
    """
    c = RequestContext(request)
    return render_to_response('Project/new_project.html', c)


@login_required()
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


@login_required()
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


@login_required()
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


@login_required()
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
            newpart.number = partdict['number']
            newpart.name = partdict['name']
            newpart.source = partdict['source']
            newpart.description = partdict['description']
            newpart.cost = float(partdict['cost'])
            newpart.save()
            returndict['id'] = newpart.id
        except Exception, e:
            returndict['error'] = e.message

    return HttpResponse(json.dumps(returndict), content_type="application/json")


@login_required()
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


@login_required()
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


@login_required()
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


@login_required()
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


@login_required()
def new_order(request):
    """
        Page for creating a new order
    """
    parts = Part.objects.all()
    suppliers = Supplier.objects.all()
    return render_to_response('Project/new_order.html', {"parts": parts, "suppliers": suppliers, })


@login_required()
def place_order_ajax(request):
    """
        Create a new order
    """
    returnDict = {}
    if request.method == 'POST':
        try:
            #First raise the order as we'll need it for the second part :)
            order_dict = json.loads(request.POST['datadict'])
            order = Order()
            order.supplier = Supplier.objects.filter(id=order_dict['supplier']).get()
            if order_dict['account'] == "none":
                order.account = None
            else:
                order.account = SupplierAccount.objects.filter(id=order_dict['account']).get()
            order.expected_delivery = datetime.datetime.strptime(order_dict['expected_delivery'], "%m/%d/%Y")
            order.date_placed = datetime.datetime.now()
            order.save()
            returnDict['order'] = order.id
            #now add the parts in
            parts_list = []
            for part in order_dict['parts']:

                orderpart = PartsToOrder()
                orderpart.order = order
                orderpart.part = Part.objects.filter(number=part['part_number']).get()
                orderpart.quantity = float(part['quantity'])
                orderpart.save()
                parts_list.append(orderpart.id)
            returnDict['parts_list'] = parts_list
        except Exception, e:
            print e
            returnDict['error'] = e.message
    print returnDict
    return HttpResponse(json.dumps(returnDict), content_type="application/json")


@login_required()
def create_supplier_ajax(request):
    """
        Simple routine to add a supplier
        TODO: finish this :)
    """
    returnDict = {}
    if request.method == 'POST':
        try:
            supplier_dict = json.loads(request.POST['datadict'])
            supplier = Supplier()
            supplier.name = supplier_dict['supplier_name']
            supplier.url = supplier_dict['supplier_url']
            supplier.save()
            returnDict['id'] = supplier.id
        except Exception, e:
            returnDict['error'] = e.message

    return HttpResponse(json.dumps(returnDict), content_type="application/json")


@login_required()
def create_account_ajax(request):
    """
        Simple routine to add an account to a supplier
    """
    returnDict = {}
    if request.method == 'POST':
        try:
            datadict = json.loads(request.POST['datadict'])
            supplier = Supplier.objects.get(id=datadict['supplier_id'])
            account = SupplierAccount()
            account.supplier = supplier
            account.account_number = datadict['account_number']
            account.save()
            returnDict['id'] = account.id
        except Exception, e:
            returnDict['error'] = e.message
    return HttpResponse(json.dumps(returnDict), content_type="application/json")


@login_required()
def get_accounts_ajax(request):
    returnList = []
    if request.method == 'POST':
        try:
            accounts = SupplierAccount.objects.filter(supplier=Supplier.objects.filter(id=request.POST['id']).get()).all()
            for account in accounts:
                tmpDict = {}
                tmpDict['id'] = account.id
                tmpDict['account_number'] = account.account_number
                returnList.append(tmpDict)
        except Exception, e:
            pass
    return HttpResponse(json.dumps(returnList), content_type="application/json")


@login_required()
def orders(request):
    """
        Orders Home Page
    """
    recent_orders = Order.objects.all()[:5]
    all_orders = Order.objects.all()
    recent_arrivals = Order.objects.filter(date_arrived__range=[datetime.datetime.now(), datetime.datetime.now() -
                                                                                        (datetime.timedelta(days=14))])
    return render_to_response('Project/orders.html', {'recent_orders': recent_orders, 'all_orders': all_orders,
                                                      'recent_arrivals': recent_arrivals})


def login(request):
    data = {}
    if "next" in request.GET.keys():
        data['redirect_url'] = request.GET['next']
    return render_to_response('Project/login.html', data)

@csrf_exempt
def login_attempt(request):
    """
        Attempt to login a user
    """
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    returnData = {}
    if user is None:
        returnData['error'] = True
    else:
        if user.is_active:
            auth_login(request, user)
        else:
            returnData['error'] = "Disabled"
    return HttpResponse(json.dumps(returnData), content_type="application/json")


def order_arrived_ajax(request):
    """
        Set an order as arrived
    """
    returnDict = {}
    if request.method == 'POST':
        try:
            datadict = json.loads(request.POST['datadict'])
            order = Order.objects.filter(id=datadict['id']).get()
            order.date_arrived = datetime.datetime.strptime(datadict['arrival_date'], "%m/%d/%Y")
            order.save()
        except Exception, e:
            returnDict['error'] = e.message
    return HttpResponse(json.dumps(returnDict), content_type="application/json")