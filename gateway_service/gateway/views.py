import json

import jwt
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import status

from .forms import LoginForm, UserRegistrationForm, NewLibrary, NewBook, NewLibraryBook, DeleteBook
import requests
import re

from gateway_service.settings import JWT_KEY

# LIBRARY_URL = "http://127.0.0.1:9001/api/v1/library"
# BOOK_URL = "http://127.0.0.1:9002/api/v1/book"
# SESSION_URL = "http://127.0.0.1:9003/api/v1/session"
# REPORT_URL = "http://127.0.0.1:9004/api/v1/report"
# RATING_URL = "http://127.0.0.1:9005/api/v1/rating"
# CONTROL_URL = "http://127.0.0.1:9006/api/v1/control"

LIBRARY_URL = "https://darzhain-library.herokuapp.com/api/v1/library"
BOOK_URL = "https://darzhain-book.herokuapp.com/api/v1/book"
SESSION_URL = "https://darzhain-session.herokuapp.com/api/v1/session"
REPORT_URL = "https://darzhain-report.herokuapp.com/api/v1/report"
RATING_URL = "https://darzhain-rating.herokuapp.com/api/v1/rating"
CONTROL_URL = "https://darzhain-control.herokuapp.com/api/v1/control"


def cookies(request):
    is_authenticated = False
    session = requests.get(f"{SESSION_URL}/validate", cookies=request.COOKIES)
    if session.status_code != 200:
        pass
        # if session.status_code == 403:
        #     session = requests.get("http://localhost:8001/api/v1/session/refresh", cookies=request.COOKIES)
        #     is_authenticated = True
        # elif session.status_code == 401:
        #     pass
        # else:
        #     request.delete_cookie('jwt')
    else:
        is_authenticated = True
    return is_authenticated, request, session


def auth(request):
    token = request.COOKIES.get('jwt')

    if not token:
        return
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=['HS256'], options={"verify_exp": False})
    except jwt.DecodeError:
        return None
    return payload


def signup(request):
    error = None
    form = UserRegistrationForm()
    form.fields['library'].choices = get_libraries_for_form()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        form.fields['library'].choices = get_libraries_for_form()

        # validation
        if form.data['password'] != form.data['password2']:
            return render(request, 'signup.html', {'form': form, 'error': 'Password mismatch'})
        # if not re.compile("^([A-Za-z0-9]+)+$").match(form.data['username']):
        #     return render(request, 'signup.html', {'form': form, 'error': 'No valid login'})
        session = requests.post(f'{SESSION_URL}/signup',
                                json={"username": form.data['username'],
                                      "password": form.data['password'],
                                      "library_id": form.data['library']
                                      })
        error = 'success'
        if session.status_code != status.HTTP_201_CREATED:
            session = session.content.decode('utf8').replace("'", '"')
            error = "email is not unique" if 'email' in session else "username is not unique"

    return render(request, 'signup.html', {'form': form, 'error': error})


def make_login(request):
    error = None
    if request.method == "GET":
        form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        session = requests.post(f'{SESSION_URL}/login',
                                json={"username": request.POST.get('username'),
                                      "password": request.POST.get('password')})
        if session.status_code == 200:
            response = HttpResponseRedirect('/index')
            response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True)
            return response
        else:
            session = session.content.decode('utf8').replace("'", '"')
            error = json.loads(session)['detail']
    return render(request, 'login.html', {'form': form, 'error': error})


def make_logout(request):
    session = requests.post(f"{SESSION_URL}/logout", cookies=request.COOKIES)
    if session.status_code == 200:
        response = HttpResponseRedirect('/index')
        response.delete_cookie('jwt')
        return response
    return render(request, 'libraries.html')


def get_libraries_response(request, data):
    libraries = requests.get(f"{LIBRARY_URL}/").json()
    if len(libraries) != 0:
        title = "Библиотеки в городах"
        response = render(request, 'libraries.html', {'libraries': libraries, 'title': title,
                                                      'user': data})
    else:
        title = "Нет библиотек"
        response = render(request, 'libraries.html', {'title': title, 'user': data})
    return response


def index(request):
    is_authenticated, request, session = cookies(request)
    data = auth(request)

    if not is_authenticated or data['role'] == 'admin':
        response = get_libraries_response(request, data)
    else:
        response = HttpResponseRedirect(f"/library/{data['library_id']}/books")
        response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True)
        return response

    response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True) \
        if is_authenticated else response.delete_cookie('jwt')
    return response


def library_books(request, library_id):
    is_authenticated, request, session = cookies(request)
    data = auth(request)
    books = requests.get(f"{LIBRARY_URL}/{library_id}/books", cookies=request.COOKIES).json()
    library = requests.get(f"{LIBRARY_URL}/{library_id}", cookies=request.COOKIES).json()

    control = requests.get(f"{CONTROL_URL}/get", cookies=request.COOKIES).json()
    if control['current_count'] < control['max_count']:
        action = 'take'
    else:
        action = 'no'

    if len(books) != 0:
        response = render(request, 'library_books.html',
                          {'books': books,
                           'title': library['city'],
                           'user': data,
                           'library_id': library_id,
                           'action': action})

    else:
        title = "Нет книг"
        response = render(request, 'libraries.html', {'title': title, 'user': data})

    response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True) \
        if is_authenticated else response.delete_cookie('jwt')
    return response


def admin(request):
    is_authenticated, request, session = cookies(request)
    data = auth(request)
    if data['role'] != 'admin':
        response = HttpResponseRedirect('/index')
        response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True)
        return response
    response = render(request, 'admin.html', {'user': data})
    response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True) \
        if is_authenticated else response.delete_cookie('jwt')
    return response


def add_library_admin(request):
    error = None
    is_authenticated, request, session = cookies(request)
    data = auth(request)

    if request.method == "GET":
        form = NewLibrary()
    if request.method == "POST":
        form = NewLibrary(data=request.POST)
        new_library = requests.post(f"{LIBRARY_URL}/",
                                    json={'city': form.data['city']},
                                    cookies=request.COOKIES)
        error = 'success'
        if new_library.status_code != status.HTTP_201_CREATED:
            error = new_library.json()['message']

    response = render(request, 'new_library.html', {'form': form, 'error': error, 'user': data})

    response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True) \
        if is_authenticated else response.delete_cookie('jwt')
    return response


def get_authors_for_form():
    authors = requests.get(f"{BOOK_URL}/author")
    form_list = []
    for author in authors.json():
        form_list.append((author['id'], f"{author['firstname']} {author['lastname']}"))
    return form_list


def add_book_admin(request):
    error = None
    is_authenticated, request, session = cookies(request)
    data = auth(request)

    if request.method == "GET":
        form = NewBook()
        form.fields['author'].choices = get_authors_for_form()
    if request.method == "POST":
        form = NewBook(data=request.POST)
        form.fields['author'].choices = get_authors_for_form()

        new_book = requests.post(f"{BOOK_URL}/",
                                 json={'name': form.data['name'],
                                       'genre': form.data['genre'],
                                       'author': form.data['author']},
                                 cookies=request.COOKIES)
        error = 'success'
        if new_book.status_code != status.HTTP_201_CREATED:
            error = new_book.json()['message']
    response = render(request, 'new_book.html', {'form': form, 'error': error, 'user': data})

    response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True) \
        if is_authenticated else response.delete_cookie('jwt')
    return response


def get_books_for_form():
    books = requests.get(f"{BOOK_URL}/")
    form_list = []
    for book in books.json():
        form_list.append((book['id'], f"{book['name']} ({book['author']['firstname']} {book['author']['lastname']})"))
    return form_list


def get_libraries_for_form():
    libraries = requests.get(f"{LIBRARY_URL}/")
    form_list = []
    for library in libraries.json():
        form_list.append((library['id'], f"{library['city']}"))
    return form_list


def add_library_book(request):
    error = None
    is_authenticated, request, session = cookies(request)
    data = auth(request)

    if request.method == "GET":
        form = NewLibraryBook()

        form.fields['book'].choices = get_books_for_form()
        form.fields['library'].choices = get_libraries_for_form()

    if request.method == "POST":
        form = NewLibraryBook(data=request.POST)

        form.fields['book'].choices = get_books_for_form()
        form.fields['library'].choices = get_libraries_for_form()

        new_book = requests.post(
            f"{LIBRARY_URL}/{form.data['library']}/book/{form.data['book']}",
            cookies=request.COOKIES)
        error = 'success'
        if new_book.status_code != status.HTTP_201_CREATED:
            error = new_book.json()['message']

    response = render(request, 'add_library_book.html', {'form': form, 'error': error, 'user': data})
    response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True) \
        if is_authenticated else response.delete_cookie('jwt')
    return response


def delete_book(request):
    error = None
    is_authenticated, request, session = cookies(request)
    data = auth(request)

    if request.method == "GET":
        form = DeleteBook()

        form.fields['book'].choices = get_books_for_form()

    if request.method == "POST":
        form = DeleteBook(data=request.POST)

        service_response = requests.delete(
            f"{BOOK_URL}/{form.data['book']}",
            cookies=request.COOKIES)
        error = 'success'
        # if service_response.status_code != status.HTTP_204_NO_CONTENT:
        #     error = service_response.json()['message']

        form.fields['book'].choices = get_books_for_form()

    response = render(request, 'delete_book.html', {'form': form, 'error': error, 'user': data})
    response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True) \
        if is_authenticated else response.delete_cookie('jwt')
    return response


def take_book(request, library_id, book_id):
    is_authenticated, request, session = cookies(request)
    data = auth(request)
    take_response = requests.post(f"{LIBRARY_URL}/{library_id}/book/{book_id}/take",
                                  cookies=request.COOKIES)

    # todo check response status code

    response = HttpResponseRedirect(f'/library/{library_id}/books')
    response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True)
    return response

    # продумать как сделать кнопку вместо взять, уже взята, надо ходить по taken_book from library
    books = requests.get(f"{LIBRARY_URL}/{library_id}/books").json()
    if len(books) != 0:
        title = "Книги"
        response = render(request, 'library_books.html',
                          {'books': books, 'title': title, 'user': data, 'library_id': library_id})
    else:
        title = "Нет библиотек"
        response = render(request, 'libraries.html', {'title': title})

    response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True) \
        if is_authenticated else response.delete_cookie('jwt')
    return response


def user_books(request):
    is_authenticated, request, session = cookies(request)
    data = auth(request)
    library_id = data['library_id']
    # todo поменять запрос на получение списка взятых книг
    books = requests.get(f"{LIBRARY_URL}/taked_books", cookies=request.COOKIES).json()
    # library = requests.get(f"http://{LIBRARY_URL}/{library_id}").json()

    if len(books) != 0:
        response = render(request, 'library_books.html',
                          {'books': books,
                           'title': 'Мои книги',
                           'user': data,
                           'library_id': library_id,
                           'action': 'return',
                           })
    else:
        title = "Нет книг"
        response = render(request, 'libraries.html', {'title': title})

    response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True) \
        if is_authenticated else response.delete_cookie('jwt')
    return response


def return_book(request, book_id):
    is_authenticated, request, session = cookies(request)
    data = auth(request)
    library_id = data['library_id']
    take_response = requests.post(f"{LIBRARY_URL}/{library_id}/book/{book_id}/return",
                                  cookies=request.COOKIES)

    # todo check response status code

    response = HttpResponseRedirect(f'/user_books/')
    response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True)
    return response


def genre_stat(request):
    is_authenticated, request, session = cookies(request)
    data = auth(request)
    report_response = requests.get(f"{REPORT_URL}/genre_stat",
                                   cookies=request.COOKIES)

    # todo check response status code
    response = render(request, 'genre_stat.html', {'genres': report_response.json(), 'user': data})
    # response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True)
    return response


def user_stat(request):
    is_authenticated, request, session = cookies(request)
    data = auth(request)
    report_response = requests.get(f"{REPORT_URL}/user_stat",
                                   cookies=request.COOKIES)


    # todo check response status code
    response = render(request, 'user_stat.html', {'users': report_response.json(), 'user': data})
    return response


def delete_library_book(request, library_id, book_id):
    is_authenticated, request, session = cookies(request)
    data = auth(request)
    service_response = requests.delete(f"{LIBRARY_URL}/{library_id}/book/{book_id}",
                                       cookies=request.COOKIES)

    # todo check response status code

    response = HttpResponseRedirect(f'/library/{library_id}/books')
    response.set_cookie(key='jwt', value=session.cookies.get('jwt'), httponly=True)
    return response


def user_rating(request):
    is_authenticated, request, session = cookies(request)
    data = auth(request)
    rating_response = requests.get(f"{RATING_URL}/",
                                   cookies=request.COOKIES)
    control_response = requests.get(f"{CONTROL_URL}/get",
                                    cookies=request.COOKIES)

    # todo check response status code
    response = render(request, 'user_stat.html', {'rating': rating_response.json(), 'user': data,
                                                  'control': control_response.json()})
    return response


def search(request):
    is_authenticated, request, session = cookies(request)
    data = auth(request)

    # todo check response status code
    response = render(request, 'search.html', {'user': data})
    return response


def search_by_book_name(request):
    is_authenticated, request, session = cookies(request)
    data = auth(request)
    form_data = request.POST

    book_response = requests.get(f"{BOOK_URL}/search_by_book_name/{form_data['book_name']}",
                                 cookies=request.COOKIES)
    # response = requests.get(f"http://{RATING_URL}/", cookies=request.COOKIES)

    # todo check response status code
    response = render(request, 'books.html', {'books': book_response.json(), 'user': data})
    return response


def search_by_author(request):
    is_authenticated, request, session = cookies(request)
    data = auth(request)
    form_data = request.POST

    book_response = requests.get(f"{BOOK_URL}/search_by_author/{form_data['author']}",
                                 cookies=request.COOKIES)

    # todo check response status code
    response = render(request, 'books.html', {'books': book_response.json(), 'user': data})
    return response
