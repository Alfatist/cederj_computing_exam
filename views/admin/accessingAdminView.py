import sys
import os

from controllers.admin.confirmDeleteAccountsController import ConfirmDeleteAccountsController
from core.either.left import Left
from core.either.right import Right
from views.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tkinter import messagebox
import tkinter as tk

class AccessingAdminView(ViewModel):
  def __init__(self, argument):
    super().__init__()
    self.print(f"Seja bem vindo a visualização de ADM, {argument}")
    

  def call(self, confirmDeleteAccountsController: ConfirmDeleteAccountsController = ConfirmDeleteAccountsController(), isToNullValues = True):
    
    deleteSolicitations = confirmDeleteAccountsController.getDeleteSolicitations()

    if(type(deleteSolicitations) == Left):
      self.print("Tivemos um erro ao tentar pegar as solicitações de exclusão de contas. Por favor, tente novamente.")


    self.root = tk.Tk()
    self.root.title("Solicitações de Exclusão de Contas")

    tk.Label(self.root, text="Contas que solicitaram exclusão:", font=("Arial", 14, "bold")).pack(pady=10)

    def create_account_frame(account_id, holder_name):
        frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE, padx=10, pady=5)
        frame.pack(pady=5, padx=10, fill="x")

        info = f"ID: {account_id} | Situação: {holder_name}"
        tk.Label(frame, text=info, font=("Arial", 11)).pack(side=tk.LEFT)

        tk.Button(frame, text="Confirmar", fg="green", command=lambda: handle_confirm(account_id, holder_name)).pack(side=tk.RIGHT, padx=5)
        tk.Button(frame, text="Recusar", fg="red", command=lambda: handle_deny(account_id)).pack(side=tk.RIGHT, padx=5)

    def handle_confirm(account_id, holder_name):
        result = confirmDeleteAccountsController.deleteAccount(holder_name, account_id)
        if isinstance(result, Right):
            messagebox.showinfo("Sucesso", f"Conta {account_id} deletada com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível deletar a conta.")
        self.root.destroy()
        self.call(confirmDeleteAccountsController)  # Recarrega a tela

    def handle_deny(account_id):
        result = confirmDeleteAccountsController.denyDeleteAccount(account_id)
        if isinstance(result, Right):
            messagebox.showinfo("Sucesso", f"Solicitação da conta {account_id} negada com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível negar a solicitação.")
        self.root.destroy()
        self.call(confirmDeleteAccountsController)


    def on_submit():
      result = confirmDeleteAccountsController.getAccount(self.account_details.get())
      if(type(result) == Left):
        messagebox.showerror("Erro", "Conta não encontrada.")
      else:
        messagebox.showinfo("Sucesso", f"Conta encontrada: \n===\nTipo: {result["type"]}\nSaldo: {result["balance"]}\nNome do titular: {result["holderName"]}\nEndereço: {result["holderAddress"]}\nAgência: {result["agency"]}\n===")

    for account_id, holder_name in deleteSolicitations.items():
        create_account_frame(account_id, holder_name)
    
    tk.Label(self.root, text="Buscar detalhes da conta: ", font=("Arial", 14, "bold")).pack(pady=10)
    self.account_details = tk.Entry(self.root)
    self.account_details.pack()
    self.search_button = tk.Button(self.root, text="Buscar", command=on_submit)
    self.search_button.pack(pady=10)

    self.root.mainloop()
      
        





    
    
