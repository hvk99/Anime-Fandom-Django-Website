from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Character, Genre, Anime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm

# Create your views here.

def single_slug(request, single_slug):

	genres = [g.genre for g in Genre.objects.all()]

	if single_slug in genres:
		matching_anime = Anime.objects.filter(genre__slug=single_slug.lower())

		anime_urls = {}
		for a in matching_anime.all():
			episode = Character.objects.filter(anime__anime=a.anime).earliest("name")
			anime_urls[a] = episode.slug

		return render(request, 'main/genre.html',
					  {"urls":anime_urls})

	characters = [c.slug for c in Character.objects.all()]

	if single_slug in characters:

		this_character = Character.objects.get(slug=single_slug)
		characters_from_anime = Character.objects.filter(anime__anime=this_character.anime).order_by("name")
		this_character_idx = list(characters_from_anime).index(this_character)

		return render(request, 'main/character.html',
					  {"character":this_character,
					   "sidebar":characters_from_anime,
					   "this_character_idx":this_character_idx})

	return HttpResponse(f"'{single_slug}' does not correspond to anything we know of!")

def homepage(request):
	return render(request=request,
				  template_name="main/genres.html",
				  context={"genres": Genre.objects.all})

def register(request):

	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"New account created: {username}")
			login(request, user)
			messages.info(request, f"You are now logged in as {username}")
			return redirect("main:homepage")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages[msg]}")

	form = NewUserForm
	return render(request,
				  "main/register.html",
				  context={"form":form})

def logout_request(request):

	logout(request)
	messages.info(request, "You have been logged out succesfully")
	return redirect("main:homepage")

def login_request(request):

	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}")
				return redirect("main:homepage")
			else:
				messages.error(request, "Invalid username or password")
		else:
			messages.error(request, "Invalid username or password")

	form = AuthenticationForm()
	return render(request,
				  "main/login.html",
				  context={"form":form})