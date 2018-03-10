from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from tron import brain
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError




def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context,request))


def checkUrl(request):
    if request.method == "GET":
        url = request.GET['kappa']
        url = brain.stripHttp(url)
        siteHash = brain.getSiteHash(url)
        result = ""
        if brain.isSiteChanged(url,siteHash):
            result = "true"
            date = brain.getLastChange(url)
            brain.updateSavedTime(url)
            
        else:
            result = "false"
            date = brain.getLastChange(url)
        brain.updateSavedHash(url,siteHash)
        return HttpResponse('{"url":"%s","change":%s,"date": "%s"}' % (url,result,date))
    else:
        return HttpResponse(status=404)