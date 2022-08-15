from tkinter import *
from PIL import ImageTk, Image
import gui_campeao
import data_lol
import os


pasta = os.path.dirname(__file__)
root = Tk()

root.title('League Personal Assistent')

largura = 710
altura = 400
largura_screen = root.winfo_screenwidth()
altura_screen = root.winfo_screenheight()
posx = (largura_screen/2) - (largura/2)
posy = (altura_screen/2) - (altura/2)
root.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))
root['bg'] = '#444'
root.resizable(False, False)

imagem = ImageTk.PhotoImage(Image.open('logo.png'))
lb = Label(root, image=imagem, bg='#444')
lb.pack(side=TOP)

label_orientacao = Label(root, text='Campeão', font='Heveltica 14 italic', bg='#444', fg='white').place(x=268, y=280)
text_box_campeao = Entry(root)
text_box_campeao.place(x=270, y=310)

imagem_lupa = ImageTk.PhotoImage(Image.open('search.png'))
botao = Button(root, image=imagem_lupa, bg='#444', relief='flat', command=lambda: gui_campeao.buscar(text_box_campeao.get())).place(x=434, y=300)

barradeMenus = Menu(root)
menuAtualizar = Menu(barradeMenus, tearoff=0)
menuAtualizar.add_command(label='Resetar DB', command=data_lol.resetar_DB)
menuAtualizar.add_command(label='Atualizar DB', command=data_lol.atualizar_DB)
barradeMenus.add_cascade(label='Manutenção', menu=menuAtualizar)
root.config(menu=barradeMenus)
root.mainloop()
