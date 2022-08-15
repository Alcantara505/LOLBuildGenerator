from tkinter import *
from PIL import Image, ImageTk
import banco
import json


def buscar(busca):
    global imagem_campeao, imagem_logo2, imagem_item0, imagem_item1, imagem_item2, imagem_item3, imagem_item4, imagem_item5
    global imagem_item6, imagem_item7, imagem_item8, imagem_item9
    try:
        busca_campeao = busca.title()

        if busca_campeao == 'Jarvan Iv':
            busca_campeao = 'Jarvan IV'

        if busca_campeao == 'Leblanc':
            busca_campeao = 'LeBlanc'

        sql = f"SELECT * FROM tb_champions WHERE T_NOMECHAMPION = '{busca_campeao}'"
        dados_campeao = banco.selecionar(sql)
        nome = None
        blurb = None
        build = []

        for dados in dados_campeao:
            nome = dados[1]
            blurb = dados[2]
            build = json.loads(dados[4])

        janela_campeao = Toplevel()
        janela_campeao.configure(bg='#444')
        largura = 1140
        altura = 660
        largura_screen = janela_campeao.winfo_screenwidth()
        altura_screen = janela_campeao.winfo_screenheight()
        posx = (largura_screen / 2) - (largura / 2)
        posy = (altura_screen / 2) - (altura / 2)
        janela_campeao.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))

        janela_campeao.resizable(0, 0)

        frame_campeao = Frame(janela_campeao, bd=0, bg='#444')
        label0 = Label(frame_campeao,
                       text=f'{nome}',
                       font='Heveltica 20 bold',
                       fg='white',
                       bg='#444')
        label0.pack()

        label_blurb = Label(frame_campeao,
                            text=f'{blurb}\n',
                            font='Heveltica 15 italic',
                            fg='white',
                            bg='#444')
        label_blurb.pack()
        imagem_campeao = ImageTk.PhotoImage(Image.open(f'loading\\{nome.replace(" ", "")}_0.jpg'))
        label = Label(frame_campeao, image=imagem_campeao, bg='#444')
        label.pack()

        frame_campeao.pack(side=LEFT)

        imagem_logo2 = ImageTk.PhotoImage(Image.open('league-of-Legends-logo.png'))
        label_logo2 = Label(janela_campeao, image=imagem_logo2, anchor=CENTER, bg='#444')
        label_logo2.pack()

        frame_miticos = LabelFrame(janela_campeao, text='Itens Míticos', bg='#444', fg='white')
        frame_lendaros = LabelFrame(janela_campeao, text='Itens Lendários', bg='#444', fg='white')
        frame_botas = LabelFrame(janela_campeao, text='Botas', bg='#444', fg='white')

        def itemizar(item, imagem):
            if item == 0:
                print('Nada aqui')
            else:
                sql = f"SELECT * FROM tb_itens WHERE T_IDITEM ='{item}'"
                dados_item = banco.selecionar(sql)
                tipo_item = None
                nome_item = None

                for teste in dados_item:
                    tipo_item = teste[2]
                    nome_item = teste[1]

                if tipo_item == 'MÍTICO':
                    frame_item = Frame(frame_miticos, bg='#444')
                    label = Label(frame_item, image=imagem, bg='#444')
                    label.pack()
                    label_item = Label(frame_item, text=f'{nome_item}', font='Heveltica 7 italic', fg='white', bg='#444')
                    label.pack()
                    label_item.pack()
                    frame_item.pack(side=LEFT)
                elif tipo_item == 'LENDARIO':
                    frame_item = Frame(frame_lendaros, bg='#444')
                    label = Label(frame_item, image=imagem, bg='#444')
                    label.pack()
                    label_item = Label(frame_item, text=f'{nome_item}', font='Heveltica 7 italic', fg='white', bg='#444')
                    label.pack()
                    label_item.pack()
                    frame_item.pack(side=LEFT)
                else:
                    frame_item = Frame(frame_botas, bg='#444')
                    label = Label(frame_item, image=imagem, bg='#444')
                    label.pack()
                    label_item = Label(frame_item, text=f'{nome_item}', font='Heveltica 7 italic', bg='#444', fg='white')
                    label.pack()
                    label_item.pack()
                    frame_item.pack(side=LEFT)

        contador = 0
        for item in build:
            if contador == 0:
                imagem_item0 = ImageTk.PhotoImage(Image.open(f'item\\{item}.png'))
                itemizar(item, imagem_item0)
            elif contador == 1:
                imagem_item1 = ImageTk.PhotoImage(Image.open(f'item\\{item}.png'))
                itemizar(item, imagem_item1)
            elif contador == 2:
                imagem_item2 = ImageTk.PhotoImage(Image.open(f'item\\{item}.png'))
                itemizar(item, imagem_item2)
            elif contador == 3:
                imagem_item3 = ImageTk.PhotoImage(Image.open(f'item\\{item}.png'))
                itemizar(item, imagem_item3)
            elif contador == 4:
                imagem_item4 = ImageTk.PhotoImage(Image.open(f'item\\{item}.png'))
                itemizar(item, imagem_item4)
            elif contador == 5:
                imagem_item5 = ImageTk.PhotoImage(Image.open(f'item\\{item}.png'))
                itemizar(item, imagem_item5)
            elif contador == 6:
                imagem_item6 = ImageTk.PhotoImage(Image.open(f'item\\{item}.png'))
                itemizar(item, imagem_item6)
            elif contador == 7:
                imagem_item7 = ImageTk.PhotoImage(Image.open(f'item\\{item}.png'))
                itemizar(item, imagem_item7)
            elif contador == 8:
                imagem_item8 = ImageTk.PhotoImage(Image.open(f'item\\{item}.png'))
                itemizar(item, imagem_item8)
            elif contador == 9:
                imagem_item9 = ImageTk.PhotoImage(Image.open(f'item\\{item}.png'))
                itemizar(item, imagem_item9)
            contador += 1

        frame_miticos.place(x=330, y=100, width=800, height=150)
        frame_lendaros.place(x=330, y=300, width=800, height=150)
        frame_botas.place(x=330, y=500, width=800, height=150)

    except Exception as ex:
        print(ex)
        janela_campeao.destroy()