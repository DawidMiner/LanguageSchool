from django.shortcuts import render, redirect
import pyodbc
from django.http import HttpResponse, JsonResponse
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def start(request):
    request.session['email'] = ""
    return render(request, 'home.html')


def home(request):
    return render(request, 'home.html')


def getData(request):
    connection = pyodbc.connect(f'DRIVER=SQL SERVER;Server=LAPTOP-5QFO53LT;Database=School')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM UserData")
    row = cursor.fetchone()
    return render(request, 'register.html', {'row': row})


def signForCourse(request):
    email_login = "testowy418@gmail.com"
    password_login = "fqmmpkuifqeeuswf"
    if request.method == 'POST':
        if len(request.session['email']) > 0:
            email = request.session.get('email', '')
            language = request.POST.get('course', '')
            if language == 'english':
                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=email_login, password=password_login)
                    with open("playground/messages/english_course") as file:
                        letter = MIMEMultipart()
                        letter['From'] = "testowy418@gmail.com"
                        letter['To'] = email
                        letter['Subject'] = "Potwierdzenie zapisu na kurs języka angielskiego"
                        tekst = MIMEText(file.read(), "plain")
                        letter.attach(tekst)
                    connection.sendmail(from_addr="testowy418@gmail.com", to_addrs=email, msg=letter.as_string())
                return render(request, 'signingResult.html', {'email': email, 'language': 'angielskiego'})
            elif language == 'spanish':
                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=email_login, password=password_login)
                    with open("playground/messages/spanish_course") as file:
                        letter = MIMEMultipart()
                        letter['From'] = "testowy418@gmail.com"
                        letter['To'] = email
                        letter['Subject'] = "Potwierdzenie zapisu na kurs języka hiszpańskiego"
                        tekst = MIMEText(file.read(), "plain")
                        letter.attach(tekst)
                    connection.sendmail(from_addr="testowy418@gmail.com", to_addrs=email, msg=letter.as_string())
                return render(request, 'signingResult.html', {'email': email, 'language': 'hiszpańskiego'})
        else:
            return render(request, 'result.html', {'komunikat': 'Aby zapisać się na kurs musisz się najpierw zalogować.'})
    return render(request, 'offer.html')


# def signForSpanishCourse(request):
#     if request.method == 'POST':
#         email = request.session.get('email', '')
#         return render(request, 'signingResult.html', {'email': email, 'language': 'hiszpańskiego'})
#     return render(request, 'offer.html')


def login(request):
    result = ""
    try:
        connection = pyodbc.connect(f'DRIVER=SQL SERVER;Server=LAPTOP-5QFO53LT;Database=School')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM UserData")
        row = cursor.fetchone()
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        loggingData = (email, password)
        canLogIn = False
        while row:
            data = (row[1], row[2])
            if loggingData == data:
                canLogIn = True
            row = cursor.fetchone()
        if request.method == 'POST' and canLogIn:
            request.session['email'] = email
            return render(request, 'loggingResult.html', {'komunikat': 'Logowanie przebiegło pomyślnie'})
        if email and password:
            result = "Nie udało się zalogować. Nie istnieje użytkownik o podanych danych."
    except Exception as e:
        print(e)
    finally:
        if connection:
            connection.close()
    return render(request, 'login.html', {'result': result})


def loggingResult(request):
    return render(request, 'loggingResult.html')


def register(request):
    result = ""
    try:
        connection = pyodbc.connect(f'DRIVER=SQL SERVER;Server=LAPTOP-5QFO53LT;Database=School')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM UserData")
        row = cursor.fetchone()
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        name = request.POST.get('name', '')
        surname = request.POST.get('surname', '')
        canRegister = True
        while row:
            if email == row[1]:
                canRegister = False
            row = cursor.fetchone()
        if request.method == 'POST' and canRegister:
            request.session['email'] = email
            cursor.execute(f"INSERT INTO UserData VALUES('{email}', '{password}', '{name}', '{surname}')")
            connection.commit()
            return render(request, 'registrationResult.html', {'komunikat': 'Konto założone pomyślnie'})
        if email and password:
            result = "Nie udało się zarejestrować. Istnieje już użytkownik o podanym adresie email."
    except Exception as e:
        print(e)
    finally:
        if connection:
            connection.close()
    return render(request, 'register.html', {'result': result})


def registrationResult(request):
    return render(request, 'registrationResult.html')
