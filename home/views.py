from django.template import loader
from .forms import ReservationForm
from django.shortcuts import render
from django.http import HttpResponse
from profiles.models import Profile, CarPlate
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ParkingGrid, Reservation, ParkingColumn, Notification


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

    # Get the car plates for the current profile
    carPlates    = CarPlate.objects.filter(profile=profile)
    totalColumns = ParkingColumn.objects.first().totalColumn
    columnCount  = list(range(totalColumns))

    template    = loader.get_template('home/home.html')
    context     = { 
        "profile"     : profile , 
        "parkingCells": parkingCells,
        "carPlates"   : carPlates,
        "columnCount" : columnCount,
        "totalColumns": totalColumns
    }
    return HttpResponse(template.render(context, request))


@login_required
def createParkingGrid(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST' and profile.user.is_superuser:
        lastParkingGrid = ParkingGrid.objects.last()
        totalColumns    = ParkingColumn.objects.first().totalColumn

        if lastParkingGrid:
            lastRow = lastParkingGrid.row
            lastColumn = lastParkingGrid.column

            # Determine the next row and column
            if lastColumn >= totalColumns:
                nextRow = lastRow + 1
                nextColumn = 1
            else:
                nextRow = lastRow
                nextColumn = lastColumn + 1
        else:
            # Initialize row and column for the first slot
            nextRow = 1
            nextColumn = 1

        # Create the new parking grid with the calculated slot
        slotNo = f"R{nextRow}C{nextColumn}"
        ParkingGrid.objects.create(row=nextRow, column=nextColumn, slotNo=slotNo)
    return redirect('home:home')


@login_required
def removeParkingGrid(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST' and profile.user.is_superuser:
        lastParkingGrid = ParkingGrid.objects.last()

        if lastParkingGrid.isAvailable == True:
            lastParkingGrid.delete()
        return redirect('home:home')


@login_required
def increaseParkingColumns(request):
    parkingColumn = ParkingColumn.objects.first()
    profile       = Profile.objects.get(user=request.user)
    if request.method == 'POST' and profile.user.is_superuser and parkingColumn.totalColumn < 15: 
        parkingColumn.totalColumn += 1
        parkingColumn.save()
    return redirect('home:home')


@login_required
def decreaseParkingColumns(request):
    parkingColumn = ParkingColumn.objects.first()
    profile       = Profile.objects.get(user=request.user)
    if request.method == 'POST' and profile.user.is_superuser and parkingColumn.totalColumn > 0: 
        parkingColumn.totalColumn -= 1
        parkingColumn.save()
    return redirect('home:home')


def reserveParkingGrid(request, slotId):
    profile     = Profile.objects.get(user=request.user)
    parkingSlot = get_object_or_404(ParkingGrid, id=slotId, isAvailable=True)

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation      = form.save(commit=False)
            reservation.user = profile
            reservation.slot = parkingSlot
            reservation.save()

            parkingSlot.user        = profile
            parkingSlot.isAvailable = False
            parkingSlot.save()

            # Send reservation notification
            Notification.objects.create(
                user      = profile,
                carPlate  = reservation.carPlate,
                startTime = reservation.startTime,
                endTime   = reservation.endTime,
                message   = f"Reservation confirmed for slot {parkingSlot.slotNo}."
            )
            return redirect("home:home")
        else:
            print(form.errors) 
    else:
        form = ReservationForm()

    return render(request, 'home/reservation.html', {'form': form, 'parkingSlot': parkingSlot})


def reservationDetail(request, slotId):
    profile     = Profile.objects.get(user=request.user)
    parkingSlot = get_object_or_404(ParkingGrid, id=slotId)
    reservation = Reservation.objects.filter(slot_id=parkingSlot.id, isActive=True).first()


    template    = loader.get_template('home/reservationInfo.html')
    context     = { 
        "profile"    : profile , 
        "reservation": reservation
    }
    return HttpResponse(template.render(context, request))


@login_required
def cancelReservation(request, slotId):
    profile     = Profile.objects.get(user=request.user)
    parkingSlot = get_object_or_404(ParkingGrid, id=slotId)
    reservation = get_object_or_404(Reservation, slot_id=slotId, user=profile)

    parkingSlot.user        = None
    parkingSlot.isAvailable = True
    parkingSlot.save() 

    Notification.objects.create(
        user        = profile,
        carPlate    = reservation.carPlate,
        startTime   = reservation.startTime,
        endTime     = reservation.endTime,
        message     = f"Reservation cancelled for slot {parkingSlot.slotNo}.",
        isCancelled = True
    )
    return redirect('home:home')