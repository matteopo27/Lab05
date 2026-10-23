import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView con altezza definita per consentire lo scorrimento
    lista_strumenti = ft.ListView(height=300, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    #TODO

    ## Crea un elemento di testo semplice da usare come titolo
    myText = ft.Text("Aggiungi nuovo strumento", size=20)
    # Crea la casella di testo per inserire il tipo di strumento
    inserisci_tipo = ft.TextField(label="Tipo", width=200)
    # Crea la casella di testo per inserire la marca
    inserisci_marca = ft.TextField(label="Marca", width=200)
    # Crea la casella di testo per inserire l'anno di acquisto
    inserisci_anno = ft.TextField(label="Anno acquisto", width=200)
    # Crea la casella di testo per inserire il valore
    inserisci_valore = ft.TextField(value="0",label="Valore (€)", width=200)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    #TODO

    def handler_minus(e): #funzione per il pulsate -
            print("-")
            v = float(inserisci_valore.value) #Legge il valore attuale e lo trasforma in numero con virgola
            v = v - 5 #Sottrae 5 al valore
            inserisci_valore.value = v
            inserisci_valore.value = str(v) #Converte il risultato in testo e lo inserisce nella casella
            page.update() #Aggiorna la pagina grafica per mostrare il nuovo numero

    def handler_plus(e): #funzione per il pulsate +
            print("+")
            v = float(inserisci_valore.value) #Legge il valore attuale e lo trasforma in numero con virgola
            v = v + 5 #Aggiunge 5 al valore
            inserisci_valore.value = v
            inserisci_valore.value = str(v) #Converte il risultato in testo e lo inserisce nella casella
            page.update() #Aggiorna la pagina grafica per mostrare il nuovo numero


    def handlers(e): #funzion per aggiungere uno strumento
        tipo = inserisci_tipo.value.strip()
        marca = inserisci_marca.value.strip()
        anno = inserisci_anno.value.strip()
        valore = inserisci_valore.value.strip()

        ## Controlla se anche solo uno dei quattro campi è rimasto vuoto
        if not marca or not anno or not tipo or not valore:
            alert.show_alert("Tutti i campi devono essere compilati!") #Mostra l'alert di errore
            return

        #Prova a convertire l'anno in numero intero e il valore in numero con virgola
        try:
            anno_finale = int(anno)
            valore_finale = float(valore)
        #Se la conversione fallisce
        except ValueError:
            alert.show_alert("Anno e Valore devono essere numeri validi!") #Mostra l'alert di errore
            return

        #Chiama il metodo della classe DepositoStrumenti per salvare lo strumento nella lista
        deposito.aggiungi_strumento(tipo, marca, anno_finale, valore_finale)

        # Reset dei campi di testo dopo l'inserimento
        inserisci_tipo.value = ""
        inserisci_marca.value = ""
        inserisci_anno.value = ""
        inserisci_valore.value = "0"

        # Ricarica e mostra la lista degli strumenti aggiornata a schermo
        aggiorna_lista_strumenti()


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    #TODO

    #Crea il pulsante principale per confermare l'inserimento dello strumento e collega l'evento click alla funzione handlers
    button_aggiunta = ft.Button("Aggiungi Strumento", on_click=handlers)
    # Crea il pulsante (-) e collega il click alla funzione handler_minus
    myBtnMinus = ft.IconButton(icon=ft.Icons.REMOVE, icon_size=50, on_click=handler_minus)
    # Crea il pulsante (+) e collega il click alla funzione handler_plus
    myBtnPlus = ft.IconButton(icon=ft.Icons.ADD, icon_size=50, on_click=handler_plus)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(
            spacing=20,
            controls=[input_responsabile, pulsante_conferma_responsabile],
            alignment=ft.MainAxisAlignment.CENTER
        ),

        # Sezione 3
        #TODO
        ft.Divider(),
        ## Mostra il titolo "Aggiungi nuovo strumento"
        myText,
        # Crea una riga orizzontale centrata contenente i campi di testo per tipo, marca e anno
        ft.Row(
            controls=[inserisci_tipo, inserisci_marca, inserisci_anno], # Elenco dei controlli da affiancare
            alignment=ft.MainAxisAlignment.CENTER, # Centra gli elementi al mezzo della pagina
            spacing=5 # Imposta uno spazio di 5 tra i campi
        ),
        # Crea una seconda riga orizzontale centrata per il contatore del valore
        ft.Row(
            controls=[myBtnMinus,inserisci_valore,myBtnPlus], # Affianca il pulsante "-", la casella valore e il pulsante "+"
            alignment=ft.MainAxisAlignment.CENTER, #Centra gli elementi orizzontalmente
            spacing=10 #Imposta uno spazio di 10 tra i bottoni e il campo
        ),
        #Inserisce sotto le due righe il pulsante per confermare l'aggiunta dello strumento
        button_aggiunta,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )

    aggiorna_lista_strumenti()

ft.run(main)