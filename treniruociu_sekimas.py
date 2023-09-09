# 1 Dalis Einaras
# Duomenų lentelės atvaizdavimas: Pagrindinėje programos dalyje turėsime lentelę
# kuri atvaizduos sportininko treniruočių duomenis. 
# Lentelė gali būti sudaryta iš stulpelių,
# kuriuose bus pateikti šie duomenys: data, atlikti pratimai, pakartojimų skaičius, 
# kilogramai arba kilogramais atlikti pratimai ir pan.


# 2 Dalis Lukas
#Įvedimo, redagavimo ir trynimo funkcionalumas (CRUD):
#Leiskite naudotojui įvesti naujas treniruotes į lentelę,
#redaguoti esamas, trinti nepageidaujamus įrašus ir peržiūrėti turimus įrašus. 
#Tai įgyvendins CRUD funkcionalumą (Create, Read, Update, Delete).


# 3 Dalis Eimantas
#Duomenų saugojimas į failą ir atkūrimas (JSON/Pickle):
#Sukurkite funkcijas, kurios leis naudotojui išsaugoti treniruočių duomenis į failą, 
#naudojant JSON arba Pickle formatą. 
#Be to, reikės funkcijų, kurios atkuria duomenis iš šio failo į programos lentelę.


# 4 Dalis Dainius 
#Duomenų apdorojimo funkcija:
#Sukurkite funkciją, kuri apdoros sportininko treniruočių duomenis. 
#Pavyzdžiui, galite šią funkciją panaudoti, kad apskaičiuotumėte, 
#kokia buvo vidutinė treniruočių trukmė, sumažinote svorius arba kilogramus per tam tikrą laikotarpį ir panašiai. 



import PySimpleGUI as sg
import json


### 3 Dalis Eimantas

# Funkcijos, kurios leis išsaugoti ir atkurti treniruočių duomenis į JSON failą

def save_to_json(data):
    with open('treniruotes.json', 'w') as file:
        json.dump(data, file, indent=4)

def load_from_json():
    try:
        with open('treniruotes.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

# PySimpleGUI

sg.theme('DarkBlue3')

layout = [
    [sg.Button('Pridėti'), sg.Button('Išsaugoti'), sg.Button('Atkurti')],
    [sg.Table(values=[], headings=['Data', 'Pratimai', 'Pakartojimai', 'Svoris'], auto_size_columns=False, justification='right', num_rows=10, key='table')],
]

window = sg.Window('Treniruočių Duomenys', layout, resizable=True)

data = load_from_json()

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == 'Pridėti':
        data.append({
            'Data': values['data'],
            'Pratimai': values['pratimai'],
            'Pakartojimai': values['pakartojimai'],
            'Svoris': values['svoris']
        })
        window['table'].update(values=data)

    if event == 'Išsaugoti':
        save_to_json(data)
        sg.popup('Duomenys išsaugoti')

    if event == 'Atkurti':
        data = load_from_json()
        window['table'].update(values=data)

window.close()