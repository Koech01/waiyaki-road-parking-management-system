from .models import Profile
from .forms import EditForm
from django.template import loader
from django.http import HttpResponse
from home.models import Notification
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def profileView(request):
    profile       = Profile.objects.get(user=request.user)
    notifications = Notification.objects.filter(user=profile).order_by('-timestamp')
    template      = loader.get_template('profiles/profile.html')
    context       = { 'profile' : profile, "notifications": notifications }
    return HttpResponse(template.render(context, request))


@login_required
def editProfile(request):
    profile  = Profile.objects.get(user=request.user)
    form     = EditForm(request.POST or None, request.FILES or None, instance=profile)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()  
            return redirect('profiles:profile')
    
    template = loader.get_template('profiles/editProfile.html')
    context = { 'profile': profile, 'form' :form }
    return HttpResponse(template.render(context, request))