from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, HASH_SESSION_KEY
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse

from users.services import UserService


# Create your views here.
def login_view(request):
    if request.method == "GET":
        if isinstance(request.session.get(SESSION_KEY), int):
            return redirect("/")
        request.session.create()
        return render(request, "login.html", {})
    elif request.method == "POST":
        if request.POST.get("username") == "admin" and request.POST.get("password") == "admin":
            if not request.session:
                request.session.create()
            user, _ = UserService().create_user(username=request.session.session_key)
            request.session[SESSION_KEY] = user["pk"]
            request.session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
            request.session[HASH_SESSION_KEY] = "qwerty"
            request.session.modified = True
            return redirect("/")
        return HttpResponse("invalid credentials", status=400)
    raise NotImplementedError


@login_required
def logout_view(request):
    if request.method == "GET":
        request.session.pop(SESSION_KEY)
        request.session.modified = True
        return redirect("/login")
    raise NotImplementedError
