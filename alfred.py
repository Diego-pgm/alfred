import pyttsx3
import speech_recognition as sr
import webbrowser as wb
import datetime
import wikipedia
import smtplib
import os
import random
import pyautogui
import psutil
import pyjokes

alfred = pyttsx3.init()

def hablar(audio):
    alfred.setProperty('rate', 175)
    voices = alfred.getProperty('voices')
    alfred.setProperty('voice', voices[3].id)
    alfred.say(audio)
    alfred.runAndWait()

def hora():
    tiempo = datetime.datetime.now().strftime("%I:%M:%S")
    hablar("La hora es:")
    hablar(tiempo)

def fecha():
    anio = int(datetime.datetime.now().year)
    mes = int(datetime.datetime.now().month)
    dia = int(datetime.datetime.now().day)
    hablar("La fecha es:")
    hablar(dia)
    hablar(mes)
    hablar(anio)

def saludo():
    hablar("Bienvenido de nuevo maestro Diego")
    hora = datetime.datetime.now().hour
    if hora >= 6 and hora <12:
        hablar("Buenos días")
    elif hora >=12 and hora < 18:
        hablar("Buenas tardes")
    else:
        hablar("Buenas noches")

    hablar("Alfred esta a tu disposición, ¿en qué puedo ayudarte?")

def tomar_comando():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.energy_threshold = 4000
        r.dynamic_energy_threshold = True
        r.pause_threshold = 0.5
        audio = r.listen(source)
    try:
        print("Reconociendo voz...")
        query = r.recognize_google(audio, language='es-mx')
        print(query)
    except Exception as e:
        print(e)
        hablar("Comando no reconocido, vuelva a intentar")
        return "None"
    return query

def mandar_mail(para, contenido):
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.ehlo()
    servidor.starttls()
    #servidor.login("cuenta_gmail", "contraseña")
    servidor.sendmail("mitm.onetwo23@gmail.com", para, contenido)

def tomar_screenshot():
    imagen = pyautogui.screenshot()
    imagen.save('C:\\Users\\diego\\Pictures\\ss.png')

def cpu():
    usage = str(psutil.cpu_percent())
    hablar("CPU tiene un uso de:"+usage+"por ciento")
    bateria = (psutil.sensors_battery())
    hablar("El porcentaje de la batería es: ")
    hablar(bateria.percent)
    hablar("por ciento")

def chistes():
    hablar(pyjokes.get_joke(language='es'))

if __name__ == "__main__":
    saludo()
    while True:
        query = tomar_comando().lower()
        if 'hora' in query:
            hora()
        elif 'fecha' in query:
            fecha()
        elif 'wikipedia'in query:
            hablar("Buscando...")
            try:
                query = query.replace("wikipedia","")
                wikipedia.set_lang("es")
                resultado = wikipedia.summary(query, sentences=2)
                print(resultado)
                hablar(resultado)
            except Exception:
                pass

        elif 'manda un mail' in query:
            try:
                hablar("Que mensaje quieres mandar?")
                contenido = tomar_comando()
                #para = "email al que se enviara el mensaje" 
                mandar_mail(para, contenido)
                hablar("Mail enviado.")
            except Exception as e:
                print(e)
                hablar("No se pudo enviar el mail")

        elif 'abre en chrome' in query:
            hablar("Qué debo abrir en chrome?")
            chromepath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            buscar = tomar_comando().lower()
            wb.get(chromepath).open(buscar+'.com')

        elif 'música' in query:
            hablar("Reproduciendo música.")
            dir_canciones = 'C:\\Users\\diego\\Music'
            canciones = os.listdir(dir_canciones)
            can = random.randint(0,100)
            os.startfile(os.path.join(dir_canciones, canciones[can]))

        elif 'recordatorio' in query:
            hablar("Qué deseas que te recuerde?")
            data = tomar_comando()
            hablar("Me pides que te recuerde:"+data)
            recordatorio = open("data.txt", "a")
            recordatorio.write(data+"\n")
            recordatorio.close()

        elif 'tienes algo que recordarme' in query:
            recordar = open("data.txt", "r")
            hablar("Me pediste que te recordara que:" +recordar.read())

        elif 'screenshot' in query:
            tomar_screenshot()
            hablar("Screenshot guardado.")

        elif 'chiste' in query:
            chistes()

        elif 'batería' in query:
            cpu()

        elif 'desconéctate' in query:
            hablar("Hasta luego maestro Diego")
            quit()

        elif 'cerrar sesion' in query:
            os.system("shutdown -l")
        
        elif 'reiniciar' in query:
            os.system("shutdown /r /t 1")

        elif 'apagar computadora' in query:
            os.system("shutdown /s /t 1")
        
