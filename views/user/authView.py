import sys
import os

from views.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.user.authUserController import AuthUserController
import tkinter as tk


class AuthView(ViewModel):
    def __init__(self, argument):
      super().__init__()
      
    
    def call(self):
        self.result = None
        self.authUserController = AuthUserController()
        self.root = tk.Tk()
        self.root.title("Autenticação - CEDERJ BANK")
        self.root.geometry("350x240")

        self.message_var = tk.StringVar()
        self.build_ui()
        self.root.mainloop()
        return self.result

    def build_ui(self):
        tk.Label(self.root, text="Insira seus dados para login", font=("Arial", 12)).pack(pady=10)
        
        tk.Label(self.root, text="Conta:").pack()
        self.login_entry = tk.Entry(self.root)
        self.login_entry.pack()

        tk.Label(self.root, text="Agência:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.message_label = tk.Label(self.root, textvariable=self.message_var, fg="red")
        self.message_label.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Entrar", command=self.on_submit)
        self.login_button.pack(pady=10)

    def on_submit(self):
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()

        if not login or not password:
            self.message_var.set("Por favor, preencha todos os campos.")
            return

        self.authUserController.setName(login)
        self.authUserController.setPassword(password)
        self.handle_auth()
        return self.result

    def handle_auth(self):
        result = self.authUserController.auth()

        match result:
            case -1:
                
                self.result = ["5", f"{self.authUserController.getName()};{self.authUserController.getResultAccount()}"]
                self.root.destroy()
            case 1:
                self.message_var.set("Erro: usuário não encontrado.")
                self.clear_password()
            case 2:
                self.message_var.set("Agência inválida. Tente novamente.")
                self.clear_password()
            case _:
                self.message_var.set("Erro interno. Tente novamente.")
                self.clear_inputs()

    def clear_inputs(self):
        self.login_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def clear_password(self):
        self.password_entry.delete(0, tk.END)

    def __call__(self):
        return self.result