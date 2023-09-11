import PySimpleGUI as psg
import json

def atkurti_duomenis():
    try:
        with open('duomenys.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

def issaugoti_duomenis(duomenys):
    with open('duomenys.json', 'w') as file:
        json.dump(duomenys, file)

def atliekamu_pratimu_vidurkis(duomenys):
    trukmes = [int(irasas[3]) for irasas in duomenys]
    if len(trukmes) > 0:
        vidutine_trukme = sum(trukmes) / len(trukmes)
        return vidutine_trukme
    else:
        return 0

def skaiciuoti_svorio_pokyti(duomenys):
    if len(duomenys) > 0:
        pradinis_svoris = float(duomenys[0][4])
        paskutinis_svoris = float(duomenys[-1][4])
        svorio_pokytis = pradinis_svoris - paskutinis_svoris
        return svorio_pokytis
    else:
        return 0
    
def ivesti_pratima(data, pratimo_pavadinimas, atlikti_kartai, svoris, duomenys):
    try:
        id = max(duomenys, key=lambda x: x[0])[0] + 1
    except ValueError:
        id = 1

    try:
        atlikti_kartai = int(atlikti_kartai)
        svoris = float(svoris)
    except (ValueError, TypeError):
        psg.popup_error('Netinkamas skaičiaus formatas')
        return

    naujas_irasas = (id, data, pratimo_pavadinimas, atlikti_kartai, svoris)
    duomenys.append(naujas_irasas)

def redaguoti_irasas(duomenys, indeksas):
    layout = [
        [psg.Text('Data', size=20), psg.Input(key='-DATA-', size=20, default_text=duomenys[indeksas][1])],
        [psg.Text('Pratimas', size=20), psg.Input(key='-PRATIMAS-', size=20, default_text=duomenys[indeksas][2])],
        [psg.Text('Atlikti Kartai', size=20), psg.Input(key='-ATLIKTIKARTAI-', size=20, default_text=duomenys[indeksas][3])],
        [psg.Text('Svoris', size=20), psg.Input(key='-SVORIS-', size=20, default_text=duomenys[indeksas][4])],
        [psg.Button('Atnaujinti', key='-ATNAUJINTI-', size=20, button_color='blue')],
    ]

    window = psg.Window('Redaguoti Irasa', layout)
    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED:
            break
        elif event == '-ATNAUJINTI-':
            try:
                duomenys[indeksas][1] = values['-DATA-']
                duomenys[indeksas][2] = values['-PRATIMAS-']
                duomenys[indeksas][3] = int(values['-ATLIKTIKARTAI-'])
                duomenys[indeksas][4] = float(values['-SVORIS-'])
            except (ValueError, TypeError):
                psg.popup_error('Netinkamas skaičiaus formatas')
                continue
            issaugoti_duomenis(duomenys)
            psg.popup('Irasas atnaujintas')
            window.close()
            break
    window.close()

def pagrindinis_langas(duomenys):
    psg.set_options(font=("Arial Bold", 14))
    toprow = ['ID', 'Data', 'Pratimas', 'Atlikti Kartai', 'Svoris(Kg)']
    tbl1 = psg.Table(values=duomenys, headings=toprow,
        auto_size_columns=True,
        display_row_numbers=False,
        justification='center', key='-TABLE-',
        selected_row_colors='red on yellow',
        enable_events=True,
        expand_x=True,
        expand_y=True,
        enable_click_events=True)
    layout = [
        [tbl1],
        [psg.Text('Data', size=20), psg.Input(key='-DATA-', size=20)],
        [psg.Text('Pratimas', size=20), psg.Input(key='-PRATIMAS-', size=20)],
        [psg.Text('Atlikti Kartai', size=20), psg.Input(key='-ATLIKTIKARTAI-', size=20)],
        [psg.Text('Svoris', size=20), psg.Input(key='-SVORIS-', size=20)],
        [psg.Button('Prideti', key='-PRIDETI-'), psg.Button('Redaguoti', key='-REDAGUOTI-'), psg.Button('Istrinti', key='-ISTRINTI-'), psg.Button('Uzdaryti', key='-EXIT-')],
        [psg.Button('Išsaugoti'), psg.Button('Atkurti')],
        [psg.Button("Apskaičiuoti atliekamų pratimų vidurkį"), psg.Button("Apskaičiuoti svorio pokytį")],
    ]
    
    window = psg.Window("Pagrindinis", layout, size=(900, 600), resizable=True)
    
    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED or event == '-EXIT-':
            break
        if event == '-PRIDETI-':
            data = values['-DATA-']
            pratimas = values['-PRATIMAS-']
            atlikti_kartai = values['-ATLIKTIKARTAI-']
            svoris = values['-SVORIS-']
            ivesti_pratima(data, pratimas, atlikti_kartai, svoris, duomenys)
            window['-TABLE-'].update(values=duomenys)
            issaugoti_duomenis(duomenys)
            window['-DATA-'].update('')
            window['-PRATIMAS-'].update('')
            window['-ATLIKTIKARTAI-'].update('')
            window['-SVORIS-'].update('')
        elif event == '-REDAGUOTI-':
            selected_rows = values['-TABLE-']
            if selected_rows:
                selected_row_index = selected_rows[0]
                redaguoti_irasas(duomenys, selected_row_index)
                window['-TABLE-'].update(values=duomenys)
        elif event == '-ISTRINTI-':
            selected_rows = values['-TABLE-']
            if selected_rows:
                selected_row_index = selected_rows[0]
                del duomenys[selected_row_index]
                issaugoti_duomenis(duomenys)
                window['-TABLE-'].update(values=duomenys)

        elif event == "Apskaičiuoti atliekamų pratimų vidurkį":
            vidutine_trukme = atliekamu_pratimu_vidurkis(duomenys)
            psg.popup(f"Atliekamų pratimų vidurkis: {vidutine_trukme:.2f} kartais")

        elif event == "Apskaičiuoti svorio pokytį":
            svorio_pokytis = skaiciuoti_svorio_pokyti(duomenys)
            psg.popup(f"Svorio pokytis: {svorio_pokytis:.2f} kg")
            
        elif event == 'Išsaugoti':
            issaugoti_duomenis(duomenys)
            psg.popup('Duomenys išsaugoti')

        elif event == 'Atkurti':
            data = atkurti_duomenis()
            window['-TABLE-'].update(values=data)    
    window.close()

duom_json = atkurti_duomenis()
pagrindinis_langas(duom_json)
