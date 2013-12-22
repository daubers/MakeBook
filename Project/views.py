from django.shortcuts import render_to_response

# Create your views here.

def index(request):
    """
        The main index page
    """
    datadict = {}

    return render_to_response('Project/index.html', datadict)