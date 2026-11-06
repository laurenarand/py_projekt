
"""
Projekt: Tudengi retseptiabi
Autorid: Lisa siia autorite nimed
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
    """Loob rakenduse graafilise kasutajaliidese."""
    global eelarve_sisend, valikud, tulemused

    aken = tk.Tk()
    aken.title("Tudengi retseptiabi")
    aken.geometry("550x650")
    aken.configure(bg="#f5f5f5")

    tk.Label(
        aken,
        text="Tudengi retseptiabi",
        font=("Arial", 20, "bold"),
        bg="#f5f5f5"
    ).pack(pady=15)

    tk.Label(
        aken,
        text="Vali koostisosad, mis sul olemas on:",
        font=("Arial", 12),
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
        font=("Arial", 12),
        bg="#f5f5f5"
    ).pack(pady=10)

    eelarve_sisend = tk.Entry(aken, font=("Arial", 12))
    eelarve_sisend.pack()
    eelarve_sisend.insert(0, "3")

    tk.Button(
        aken,
        text="Leia retseptid",
        command=leia_retseptid,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=8
    ).pack(pady=15)

    tulemused = tk.Text(
        aken,
        height=12,
        width=55,
        font=("Arial", 10),
        wrap="word"
    )
    tulemused.pack(padx=15, pady=5)

    aken.mainloop()


if __name__ == "__main__":
    main()
