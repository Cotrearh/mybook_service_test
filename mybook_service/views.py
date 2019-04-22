from django.shortcuts import render, redirect
import requests
import json
from .forms import LoginForm
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
	if 'mybook_authorization_cookie' in request.COOKIES:
		authorized = True
		jar = requests.cookies.RequestsCookieJar()
		jar.set('session', request.COOKIES['mybook_authorization_cookie'], domain='.mybook.ru')
		headers = { 'Accept': 'application/json; version=5'}
		g = requests.get('https://mybook.ru/api/bookuserlist/', cookies=jar, headers=headers)
		books = []
		for obj in g.json()['objects']:
			books.append({'name': obj['book']['name'], 'authors': obj['book']['authors_names'], 
				'cover': 'https://i3.mybook.io/c/256x426/' + obj['book']['default_cover']})
		return render(request, 'index.html', { 'authorized': authorized, 'books': books })
	else:
		authorized = False
		form = LoginForm()
		return render(request, 'index.html', { 'authorized': authorized, 'form': form })

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			r = requests.post('https://mybook.ru/api/auth/', 
				json = 	{
							"email": form.cleaned_data['e_mail'], 
							"password": form.cleaned_data['password']
						}
					)
			if r.status_code == requests.codes.ok:
				auth_cookie = r.cookies.get('session', domain='.mybook.ru')
				response = HttpResponseRedirect('/mybook_service')
				response.set_cookie('mybook_authorization_cookie', auth_cookie, 3600 * 24 * 365 * 2)
				return response
			else:
				print(r.json())
				try:
					form.add_error('e_mail', r.json()['email'][0])
				except KeyError:
					pass
					# Email is valid, no error msg
				except:
					form.add_error('e_mail', 'Неизвестная ошибка')
				try:
					form.add_error('password', r.json()['password'][0])
				except KeyError:
					pass
					# Password is valid, no error msg
				except:
					form.add_error('e_mail', 'Неизвестная ошибка')
				return render(request, 'index.html', { 'authorized': False, 'form': form })
		else:
			return render(request, 'index.html', { 'authorized': False, 'form': form })
	else:
		return redirect('index')

def logout(request):
        response = HttpResponseRedirect('/mybook_service')
        response.delete_cookie('mybook_authorization_cookie')
        return response
