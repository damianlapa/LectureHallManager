from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from managerapp.models import LectureHall, Reservation
import datetime


class AddLectureHall(View):
    def get(self, request):
        return render(request, 'add.html')

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')

        projector_availability = False
        if projector:
            projector_availability = True

        LectureHall.objects.create(name=name, capacity=capacity, projector=projector_availability)

        statement = "Hall {} added".format(name)
        return render(request, "statement.html", {"statement": statement})


class AddReservation(View):
    def get(self, request):
        halls = LectureHall.objects.all()
        return render(request, 'add_reservation.html', {'halls': halls})

    def post(self, request):
        hall_name = request.POST.get("hall")
        date = request.POST.get("date")
        comment = request.POST.get("comment")

        if datetime.datetime.strptime(date, '%Y-%m-%d') < datetime.datetime.today():
            statement = "Reservation can be made only for further dates!"
            return render(request, "statement.html", {"statement": statement})

        hall = LectureHall.objects.get(name=hall_name)

        if Reservation.objects.filter(date=date).filter(lecture_hall_id= hall.id):
            statement = "Hall already reserved!"
            return render(request, "statement.html", {"statement": statement})

        Reservation.objects.create(lecture_hall=hall, date=date, comment=comment)

        statement = "Reservation created!"
        return render(request, "statement.html", {"statement": statement})


class ShowAllHalls(View):
    def get(self, request):
        halls = LectureHall.objects.all()
        return render(request, 'halls.html', {'halls': halls})


class HallsAvailability(View):
    def get(self, request):
        halls = LectureHall.objects.all()
        reservations = Reservation.objects.all()
        return render(request, 'halls_availability.html')

    def post(self, request):
        date = request.POST.get('date')
        halls = LectureHall.objects.all()
        reservations = Reservation.objects.all().filter(date=date)
        return render(request, 'halls_availability_check.html', context={'halls': halls, 'reservations': reservations,
                                                                         "date": date})


class EditHall(View):
    def get(self, request, hall_id):
        hall = LectureHall.objects.get(id=hall_id)
        return render(request, "edit_hall.html", {"hall": hall})

    def post(self, request, hall_id):
        hall = LectureHall.objects.get(id=hall_id)
        hall.name = request.POST.get("name")
        hall.capacity = request.POST.get("capacity")
        hall_projector = request.POST.get("projector")
        if hall_projector:
            hall.projector = True
        else:
            hall.projector = False
        hall.save()
        statement = "Hall {} edited".format(hall.name)
        return render(request, "statement.html", {"statement": statement})


class DeleteHall(View):
    def get(self, request, hall_id):
        hall = LectureHall.objects.get(id=hall_id)
        name = hall.name
        hall.delete()
        statement = "Hall {} deleted".format(name)
        return render(request, "statement.html", {"statement": statement})


class HallSearch(View):
    def get(self, request):
        return render(request, 'search_form.html')

    def post(self, request):
        name = request.POST.get('name')
        capacity_min = request.POST.get('capacity_min')
        capacity_max = request.POST.get('capacity_max')
        projector = request.POST.get('projector')
        date = request.POST.get('date')

        halls = LectureHall.objects.all()
        reservations = Reservation.objects.all()

        if name:
            halls = halls.filter(name=name)
        if capacity_min:
            halls = halls.filter(capacity__gte=capacity_min)
        if capacity_max:
            halls = halls.filter(capacity__lte=capacity_max)
        if projector:
            halls = halls.filter(projector=True)
        else:
            halls = halls.filter(projector=False)
        if date:
            occupied_halls = []
            reservations = reservations.filter(date=date)
            for r in reservations:
                occupied_halls.append(r.lecture_hall_id)

            for num in occupied_halls:
                halls = halls.exclude(id=num)

        return render(request, 'halls.html', {'halls': halls})