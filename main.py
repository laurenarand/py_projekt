
"""
Projekt: Tudengi retseptiabi
Autorid: Lauren Arand ja Betti Kallus
Kirjeldus: Retseptide soovitamine olemasolevate
koostisosade ja eelarve põhjal.
"""

import tkinter as tk
from tkinter import messagebox


# Näitlikud hinnad eurodes
hinnad = {
    "muna": 0.30,
    "juust": 1.50,
    "piim": 1.00,
    "makaronid": 1.20,
    "tomat": 0.80,
    "kartul": 0.90,
    "sibul": 0.40
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


def leia_retseptid():
    """Leiab eelarvesse sobivad retseptid."""
    try:
        eelarve = float(eelarve_sisend.get().replace(",", "."))
        if eelarve < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Viga", "Sisesta korrektne mittenegatiivne eelarve!"
        )
        return

    olemas = {
        nimi for nimi, muutuja in valikud.items()
        if muutuja.get()
    }

    tulemused.delete("1.0", tk.END)
    leitud = 0

    for nimi, andmed in retseptid.items():
        puuduvad = [
            asi for asi in andmed["koostisosad"]
            if asi not in olemas
        ]

        maksumus = sum(hinnad[asi] for asi in puuduvad)

        if maksumus <= eelarve:
            leitud += 1
            tulemused.insert(tk.END, f"{nimi}\n")
            tulemused.insert(
                tk.END,
                f"Valmistamisaeg: {andmed['aeg']} min\n"
            )
            tulemused.insert(
                tk.END,
                "Osta juurde: "
                + (", ".join(puuduvad) if puuduvad else "Mitte midagi")
                + "\n"
            )
            tulemused.insert(
                tk.END, f"Lisakulu: {maksumus:.2f} €\n\n"
            )

    if leitud == 0:
        tulemused.insert(
            tk.END, "Selle eelarvega sobivaid retsepte ei leitud."
        )


def main():
    #Loob rakenduse graafilise kasutajaliidese.
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
        text="Vali koostisosad, mis sul olemas on:",
        font=("Segoe UI", 12),
        bg="#f5f5f5"
    ).pack(pady=5)

    valikud = {}

    for koostisosa in hinnad:
        muutuja = tk.BooleanVar()
        valikud[koostisosa] = muutuja

        tk.Checkbutton(
            aken,
            text=koostisosa.capitalize(),
            variable=muutuja,
            bg="#f5f5f5"
        ).pack(anchor="w", padx=100)

    tk.Label(
        aken,
        text="Sinu eelarve (€):",
        font=("Segoe UI", 12),
        bg="#f5f5f5"
    ).pack(pady=10)

    eelarve_sisend = tk.Entry(aken, font=("Segoe UI", 12))
    eelarve_sisend.pack()
    eelarve_sisend.insert(0, "3")

    tk.Button(
        aken,
        text="Leia retseptid",
        command=leia_retseptid,
        bg="#4CAF50",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        padx=20,
        pady=8
    ).pack(pady=15)

    tulemused = tk.Text(
        aken,
        height=12,
        width=55,
        font=("Segoe UI", 10),
        wrap="word"
    )
    tulemused.pack(padx=15, pady=5)

    aken.mainloop() #käivitab tkinteri sündmuste tsükli


if __name__ == "__main__":
    main()
