# -*- coding: cp1252 -*-
from Tkinter import *
import random

sorteia=random.choice
x=open('Nomes.txt','r')
lista=x.readlines()
x.close()

palavra=sorteia(lista).split('\n')[0].upper()
lista_letras=[]
lista_traco=[]
lista_erro=[]
digito=[]

for i in range(len(palavra)):
    lista_letras.append(palavra[i])
    lista_traco.append('__ ')

class arquivos:
    def __init__(self, root):
 
        self.canvas=Canvas(root, width=200, height=200)
        self.canvas.pack(side=LEFT)
        self.canvas1=Frame(root)
        self.canvas1.pack()
        self.canvas2=Frame(root)
        self.canvas2.pack()
        self.canvas3=Frame(root)
        self.canvas3.pack()
        self.canvas4=Frame(root)
        self.canvas4.pack()

        self.caixa=StringVar()
        root.title('Jogo da Forca - Isaias Software')

        ret=self.canvas.create_rectangle

        ret(10, 190, 190, 185, fill='black')
        ret(10, 190, 15, 10, fill='black')
        ret(10, 10, 100, 15, fill='black')
        ret(95, 10, 105, 20, fill='black')

        Label(self.canvas1, text='___________________________________________________').pack()
        Label(self.canvas1, text='Letra').pack()
        
        self.nom=Entry(self.canvas1, textvariable=self.caixa)
        self.nom.focus_force()
        self.nom.pack()
        self.nom.bind('<Return>', self.forca)

        Label(self.canvas1, text='___________________________________________________').pack()
        
        self.msg=Label(self.canvas2, text=lista_traco)
        self.msg.pack(side=LEFT)

        Label(self.canvas3, text='Letras Erradas: ').pack(side=LEFT)
        self.msg2=Label(self.canvas3, text=lista_erro)
        self.msg2.pack()
        self.msg3=Label(self.canvas4, text='')
        self.msg3.pack()

    def forca(self, event):

        circulo=self.canvas.create_oval
        lin=self.canvas.create_line
        boca=self.canvas.create_arc
        
        b=str(self.nom.get().upper()[0]) #transforma em string e só pega o primeiro
        #caracter
        for t in range(len(lista_letras)):
            if b == lista_letras[t]:
                lista_traco[t]=lista_letras[t]
                self.msg['text']=lista_traco
                if b not in digito:
                    digito.append(b)#só adciona ao digito se não houver nele
        if b not in lista_letras:
            lista_erro.append(b)
            self.msg2['text']=lista_erro
        self.caixa.set('')
        if len(digito) == len(lista_traco):
            self.msg3['text']='Jogo Ganho! Parabéns!'
            self.msg3['fg']='green'
        if len(lista_erro) == 10:
            self.msg3['text']='10 erros, você perdeu!',lista_letras
            self.msg3['fg']='red'
            self.msg.destroy()
            self.nom.destroy()
            
#Desenhar o bonequinho enforcado        
        if len(lista_erro) == 1:
            circulo(75, 15, 125, 65, fill='orange', outline='black')
        if len(lista_erro) == 2:
            lin(100, 65, 100, 125)
        if len(lista_erro) == 3:
            lin(100, 70, 50, 75)
        if len(lista_erro) == 4:
            lin(100, 70, 150, 75)
        if len(lista_erro) == 5:
            lin(100, 125, 75, 175)
        if len(lista_erro) == 6:
            lin(100, 125, 125, 175)
        if len(lista_erro) == 7:
            circulo(85, 30, 95, 40, fill='green', outline='black')
        if len(lista_erro) == 8:
            circulo(105, 30, 115, 40, fill='green', outline='black')
        if len(lista_erro) == 9:
            circulo(98, 40, 102, 44, fill='white', outline='black')
        if len(lista_erro) == 10:
            boca(65, 50, 115, 60, fill='white')            

    def sair(self):
        janela.destroy()

    def novo(self):       
        pass

    def ocadastra(self):
        import Forca
        
janela=Tk()
arquivos(janela)
janela.mainloop()
