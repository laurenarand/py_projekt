
"""
Projekt: Tudengi retseptiabi
Autorid: Lauren Arand ja Betti Kallus
Kirjeldus: Retseptide soovitamine olemasolevate
koostisosade ja eelarve põhjal.

Käivitamine:
Ava fail main.py Thonnys ja vajuta Run. 
Terminalis käivitamiseks kirjuta: python main.py

Allikad:
Koostisosade hinnad on võetud Coopist.
Hinnad on ligikaudsed ja võivad muutuda olenevalt poest.
"""

import tkinter as tk
from tkinter import messagebox


hinnad = { #hinnad Coop poest
    "muna": 1.90,
    "juust": 1.80,
    "kurk": 1.38,
    "tomat": 2.00,
    "lehtsalat": 1.80,
    "piim": 0.60,
    "toidukoor": 1.50,
    "makaronid": 0.90,
    "riis": 1.50,
    "kartul": 0.79,
    "tatar": 1.20,
    "hakkliha": 2.00,
    "kana": 3.50,
    "kodujuust": 1.40,
    "leib": 0.60,
    "sai": 0.70,
    "või": 1.35,
    "merevaik": 2.00,
    "sibul": 0.50
}

retseptid = {
    "Juustuomlett": {
        "koostisosad": ["muna", "juust", "piim"],
        "aeg": 10
    },
    "Makaronid juustuga": {
        "koostisosad": ["makaronid", "juust", "piim"],
        "aeg": 15
    },
    "Tomati-munapuder": {
        "koostisosad": ["muna", "tomat", "sibul"],
        "aeg": 10
    },
    "Praekartulid": {
        "koostisosad": ["kartul", "sibul"],
        "aeg": 25
    }
}


def leia_retseptid():  #leiame eelarvega sobivad retseptid ning kuvame puuduvad koostisosad
    try:
        eelarve = float(eelarve_sisend.get().replace(",", "."))  #kasutaja sisestab oma eelarve ja get() võtab sisestatud väärtuse

        if eelarve <= 0:
            messagebox.showerror("Viga", "Vale väärtus on sisestatud")
            return
    except ValueError:
        messagebox.showerror("Viga", "Vale väärtus on sisestatud")
        return
    
    tulemused.delete("1.0", tk.END) #nullib kõik eelmised retseptid ära

    leitud = 0 #sobivad retseptid

    for nimi in retseptid:
        puuduvad = []  #asjad mida kasutajal kodus pole
        maksumus = 0  

        for koostisosa in retseptid[nimi]["koostisosad"]:
            if not valikud[koostisosa].get():  #kontrollib, kas toiduaine kastike on valitud(True) või valimata(False)
                puuduvad.append(koostisosa) #kui eelmine tuli False siis lisatakse see puuduvatesse
                maksumus = maksumus + hinnad[koostisosa] #ning liidetakse uus hind

        if maksumus <= eelarve: #kui on piisavalt raha retsepti jaoks k.a puuduvad koostisosad
            leitud = leitud + 1 #suurendatakse sobivate retseptide arvu
            
            tulemused.insert(tk.END, f"{nimi}\n") 

            aeg = retseptid[nimi]["aeg"]
            tulemused.insert(tk.END, f"Valmistamisaeg: {aeg} min\n")

            if not puuduvad:
                tulemused.insert(tk.END, f"Osta juurde: Mitte midagi\n")
            else:
                tulemused.insert(tk.END, f"Osta juurde:\n")

                for asi in puuduvad:
                    tulemused.insert(tk.END, f"{asi}\n")

            tulemused.insert(tk.END, f"Juurde ostmise maksumus: {maksumus:.2f} €\n\n") #\n\n jätab järgmise retsepti ette tühja rea ja .2f kuvab arvu kahe komakohaga 
    
    if leitud == 0:
        tulemused.insert(tk.END, f"Sobivaid retsepte ei leitud.")

def main():
    #Loob rakenduse graafilise kasutajaliidese ja käivitab rakenduse.
    global eelarve_sisend, valikud, tulemused

    aken = tk.Tk() #programmi põhiaken
    aken.title("Vaese tudengi retseptid")

    akna_laius = 550
    akna_korgus = 650

    ekraani_laius = aken.winfo_screenwidth() #meetod, mis võimaldab leida vastava ekraani laiuse ja pikkuse, et aken avaneks alati keskel
    ekraani_korgus = aken.winfo_screenheight()

    x = int((ekraani_laius - akna_laius) / 2)
    y = int((ekraani_korgus - akna_korgus) / 2)

    aken.geometry(f"{akna_laius}x{akna_korgus}+{x}+{y}") #akna suurus ja asukoht ekraanil
    aken.configure(bg="#f5f5f5")

    tk.Label( #tkinteri Label klass, et teha tekstikasti aknasse
        aken,
        text="Vaese tudengi retseptid",
        font=("Segoe UI", 20, "bold"),
        bg="#f5f5f5"
    ).pack(pady=15) #pady=15 jätab 15 pikslit ruumi üleval ja all

    tk.Label(
        aken,
        text="Vali koostisosad, mis sul on kodus olemas:",
        font=("Segoe UI", 12),
        bg="#f5f5f5"
    ).pack(pady=5)

    valikud = {}  #koostisosad, mis on valitud/valimata

    raam = tk.Frame(aken, bg="#f5f5f5")  #loome akna sisse eraldi ala, et paigutada koostisosad
    raam.pack()

    rida = 0
    veerg = 0

    for koostisosa in hinnad:
        muutuja = tk.BooleanVar() #jätab meelde, kas märkeruut on valitud või mitte
        valikud[koostisosa] = muutuja #siis salvestatakse märkeruudu olek

        tk.Checkbutton(
            raam,
            text=koostisosa.capitalize(),
            variable=muutuja,
            bg="#f5f5f5"
        ).grid(row=rida, column=veerg, sticky="w", padx=30, pady=3)  #grid paigutab märkeruudud ridadesse ja veergudesse

        rida = rida + 1

        if rida == 10: #programm paneb koostisosad järgmisesse veergu, kui täis on saanud 10 koostisosa
            rida = 0
            veerg = 1

    tk.Label(
        aken,
        text="Eelarve, palju maksaksid juurde (€):",
        font=("Segoe UI", 12),
        bg="#f5f5f5"
    ).pack(pady=10)

    eelarve_sisend = tk.Entry(aken, font=("Segoe UI", 12)) #eelarve sisestamine
    eelarve_sisend.pack()
    
    tk.Button( #leiab retseptid
        aken,
        text="Leia retseptid",
        command=leia_retseptid,  #nupp kasutab seda funktsiooni
        bg="#4CAF50", #taustavärv
        fg="white", #tekstivärv
        font=("Segoe UI", 12, "bold"),
        padx=20, #ruum teksti kõrvale
        pady=8 #ruum üles-alla
    ).pack(pady=15)

    tulemused = tk.Text(  #luuakse suurem kast, kuhu hakatakse kuvama retsepte
        aken,
        height=12,
        width=55,
        font=("Segoe UI", 10),
        wrap="word"  #kui tekst ei mahu ühele reale, viiakse see sõna järgmisele reale
    )
    tulemused.pack(padx=15, pady=5)  #paigutab tulemuste kasti aknasse

    aken.mainloop() #käivitab tkinteri sündmuste tsükli


if __name__ == "__main__":
    main()
