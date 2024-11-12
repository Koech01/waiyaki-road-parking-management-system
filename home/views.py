from django.template import loader
from profiles.models import Profile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def homeView(request):
    profile  = Profile.objects.get(user=request.user)
    template = loader.get_template('home/home.html')
    context  = { "profile": profile }
    return HttpResponse(template.render(context, request))