import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import LoginForm


# Create your views here.

def index(request):
    if 'mybook_authorization_cookie' in request.COOKIES:
        authorized = True
        jar = requests.cookies.RequestsCookieJar()
        jar.set('session', request.COOKIES['mybook_authorization_cookie'], domain='.mybook.ru')
        headers = {'Accept': 'application/json; version=5'}
        books = []
        books.extend(get_books('', jar, headers))
        return render(request, 'index.html', {'authorized': authorized, 'books': books})
    else:
        authorized = False
        form = LoginForm()
        return render(request, 'index.html', {'authorized': authorized, 'form': form})


def get_books(next, jar, headers):
    books = []
    if next == '':
        adress = 'https://mybook.ru/api/bookuserlist/'
    else:
        adress = 'https://mybook.ru' + next
    g = requests.get(adress, cookies=jar, headers=headers)
    for obj in g.json()['objects']:
        books.append({'name': obj['book']['name'], 'authors': obj['book']['authors_names'],
                      'cover': 'https://i3.mybook.io/c/256x426/' + obj['book']['default_cover']})
    if g.json()['meta']['next'] is not None:
        books.extend(get_books(g.json()['meta']['next'], jar, headers))
    return books


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            r = requests.post('https://mybook.ru/api/auth/',
                              json={
                                  "email": form.cleaned_data['e_mail'],
                                  "password": form.cleaned_data['password']
                              }
                              )
            if r.status_code == requests.codes.ok:
                auth_cookie = r.cookies.get('session', domain='.mybook.ru')
                response = HttpResponseRedirect('/')
                response.set_cookie('mybook_authorization_cookie', auth_cookie, 3600 * 24 * 365 * 2)
                return response
            else:
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
                return render(request, 'index.html', {'authorized': False, 'form': form})
        else:
            return render(request, 'index.html', {'authorized': False, 'form': form})
    else:
        return redirect('index')


def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('mybook_authorization_cookie')
    return response

