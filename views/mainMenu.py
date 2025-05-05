import tkinter as tk
from tkinter import messagebox

def ShowMainMenu():
    selected = {"value": None}

    def on_select(value):
        if value in ("1", "2", "admin", "leave"):
            selected["value"] = value
            window.destroy()
        else:
            messagebox.showerror("Erro", "Valor inválido.")

    window = tk.Tk()
    window.protocol("WM_DELETE_WINDOW", lambda: on_select("leave"))
    window.title("CEDERJ BANK")

    tk.Label(window, text="===================\n\nCEDERJ BANK\n\n===================",
             font=("Courier", 12), justify="center").pack(pady=10, padx=10)

    tk.Label(window, text="Escolha uma opção:", font=("Arial", 11)).pack(pady=5)

    tk.Button(window, text="Entrar (1)", width=20, command=lambda: on_select("1")).pack(pady=5)
    tk.Button(window, text="Cadastre-se (2)", width=20, command=lambda: on_select("2")).pack(pady=5)
    tk.Button(window, text="Admin", width=20, command=lambda: on_select("admin")).pack(pady=5)

    window.mainloop()
    return selected["value"]