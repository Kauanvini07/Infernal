from tkinter import *
from tkinter import messagebox, ttk

from bancodados import *
from main import Jogo

'''
Um Sistema de login sem nada salvo apenas pra ideda e teste 
de um site que me ensinou sobre tal biblioteca.

faz registro de cliente
e se pro adm no nome na tela de login era na sessão de Admir
'''

with Banco_de_Dados() as banco:
    registro = banco.visualizar_jogadores()  # fiz como global ja que sera usada durante todo codigo

class Menu():
    def __init__(self):
        # configs de tela
        self.login = Tk()

        self.login.title('Tela de login.')
        self.login.geometry('200x300')
        self.login.resizable(width=False, height=False)
        self.configura()
        # função apos confirmar
        


    def arruma(self,var) -> str:
        txt = ''

        for i in var.split(' '):
            txt += f'{i.capitalize()} '

        return txt


    def registrar(self):
        def entrada():
            global registro
            if self.id_t.get() and self.nome_t.get():
                try:
                    with Banco_de_Dados() as banco:
                        banco.adicionar_jogador(idplayer=self.id_t.get(),name=self.nome_t.get(), vida=100, dano=10, Class=1 )
                        registro.append(banco.visualizar_jogador(self.id_t.get()))
                    
                    janela_registro.destroy()
                except Exception as erro:
                    messagebox.showerror(erro.__class__.__name__, erro)
            else:
                messagebox.showerror('Campo Vazio', 'Falta de dados')

        janela_registro = Toplevel()
        janela_registro.transient(self.login)
        janela_registro.focus_force()
        janela_registro.grab_set()
        janela_registro.title('Registros.')
        janela_registro.geometry('200x300')

        janela_registro.resizable(width=False, height=False)
        # totalmente visual da sessão de registro.
        Label(janela_registro, text='Registro', justify='center',
            font='Arial 24', fg='#65cca9').place(x=50, y=0)
        Label(janela_registro, width='40', bg='#65cca9').place(x=0, y=40)

        Label(janela_registro, text='Identidade: ',
            font='Arial 10', fg='#acbfa3').place(x=0, y=70)

        Label(janela_registro, text='Nome: ',
            font='Arial 10', fg='#acbfa3').place(x=0, y=130)

        # interaveis dentro da sessão de resgistro
        self.id_t = Entry(janela_registro, width='17', bg='#dcf4da',
                    font='Arial 14', borderwidth='3', relief='ridge')
        self.id_t.place(x=4, y=100)

        self.nome_t = Entry(janela_registro, width='17', bg='#dcf4da',
                        font='Arial 14', borderwidth='3', relief='ridge')
        self.nome_t.place(x=4, y=160)

        Button(janela_registro, text='Regitra/sair', font='Arial 7',
            bg='#65cca9', fg='black', relief='ridge',
            width=10, height=2, command=entrada).place(x=10, y=250)

        Button(janela_registro, text='Sair', font='Arial 7',
            bg='#65cca9', fg='black', relief='ridge',
            width=10, height=2, command=janela_registro.destroy).place(x=100, y=250)

        janela_registro.mainloop()


    def logar(self):
        global registro
        print(registro)
        if registro:  # checa se Há registros.
            # caso falte algum dado de entrada ele retorna sem tirar nada.
            if not self.nome.get():
                messagebox.showerror('Campo Vazio', 'Campo nome vazio')
                return

            if not self.id.get():
                messagebox.showerror('Campo Vazio', 'Campo Senha vazio')
                return

            # Checa os dados registrados
            if int(self.id.get()) in [int(i['idplayer']) for i in registro]:
                game = Jogo(idplayer=int(self.id.get()))
                self.login.destroy()
                game.run()
                messagebox.showwarning('Fail Login', 'Não temos esse usuario.')

            self.nome.delete(0, END)
            self.senha.delete(0, END)
        else:
            messagebox.showwarning('Não ha nada cadatrado por aqui', 'Sem cadastro')

    def configura(self):
        # visual não interagivel
        Label(self.login, text='Login', justify='center',
            font='Arial 24', fg='#65cca9').place(x=60, y=0)
        Label(self.login, width='40', bg='#65cca9').place(x=0, y=40)

        Label(self.login, text='Identificador: ', font='Arial 10', fg='#acbfa3').place(x=0, y=70)

        Label(self.login, text='Nome_Player: ', font='Arial 10', fg='#acbfa3').place(x=0, y=130)


        # interagiveis de Nome, login e confirmação:flat, groove,
        # raised, ridge, solid, or sunken

        self.id = Entry(self.login, width='17', bg='#dcf4da',
                    font='Arial 14', borderwidth='3', relief='ridge')
        self.id.place(x=4, y=100)

        # senha correta 12345
        self.nome = Entry(self.login, show='*',
                    width='17', bg='#dcf4da',
                    font='Arial 14', borderwidth='3', relief='ridge')
        self.nome.place(x=4, y=160)

        Button(self.login, text='Registrar', font='Arial 10',
            bg='#65cca9', fg='black', relief='ridge',
            width=10, height=2, command=self.registrar).place(x=5, y=200)

        Button(self.login, text='Confirmar', font='Arial 10',
            bg='#65cca9', fg='black', relief='ridge',
            width=10, height=2, command=self.logar).place(x=105, y=200)

        Button(self.login, text='sair', font='Arial 10',
            bg='#65cca9', fg='black', relief='ridge',
            width=10, height=2, command=self.login.destroy).place(x=50, y=250)

        self.login.mainloop()
 
Menu()