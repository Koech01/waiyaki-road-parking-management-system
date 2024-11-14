from django.template import loader
from profiles.models import Profile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import ParkingGrid, Reservation
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone


# Create your views here.
@login_required
def homeView(request):
    profile     = Profile.objects.get(user=request.user)
    parkingGrid = ParkingGrid.objects.all().order_by('row', 'column')
    
    parkingCells = {}
    for slot in parkingGrid:
        if slot.row not in parkingCells:
            parkingCells[slot.row] = []
        parkingCells[slot.row].append(slot)

    template    = loader.get_template('home/home.html')
    context     = { "profile": profile , "parkingCells": parkingCells }
    return HttpResponse(template.render(context, request))


@login_required
def createParkingGrid(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST' and profile.user.is_superuser:
        newParkingSlot = ParkingGrid()
        newParkingSlot.save()
    return redirect('home:home')


@login_required
def reserveParkingGrid(request, slotId):
    profile     = Profile.objects.get(user=request.user)
    parkingGrid = get_object_or_404(ParkingGrid, id=slotId)
    
    # Check if the parking grid is available
    if not parkingGrid.isAvailable:
        pass
    
    if request.method == 'POST':
        startTime = timezone.now()  # Example, use form data for actual start time
        endTime   = startTime + timezone.timedelta(hours=1)  # Example, 1 hour reservation
        
        Reservation.objects.create(
            user        = profile,
            parkingSlot = parkingGrid,
            startTime   = startTime,
            endTime     = endTime,
            isActive    = True
        )
        
        # Mark the ParkingGrid as reserved
        parkingGrid.isAvailable = False
        parkingGrid.save()
        
        return redirect('home:home')
    return redirect('home:home')