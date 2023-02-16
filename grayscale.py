from PIL import Image
import os
import math
import time
import sys


def verificar_imagem(nome):
    if os.path.isfile(nome):
        return True
    else:
        return False


def verificar_diretorio(nome):
    caminho = os.path.exists(nome)
    if caminho:
        if verificar_imagem("Resources/morango.png"):
            return True
        else:
            return False
    else:
        return False


def verificar_diretorio_ascii(nome):
    diretorio_base = os.path.join(os.getcwd(), nome)
    caminho = os.path.exists(diretorio_base)
    print(diretorio_base)
    if caminho:
        return False

    else:
        try:
            os.mkdir(diretorio_base)
            return True
        except FileExistsError:
            return False


def print_digitado(frase):
    for i in frase:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.1)



def verificar_tamanho_imagem(imagem):
    return (Image.open(imagem)).size


def salvar_imagem(imagem, tamanho, coordenadas_cinza):
    """imagem_bytes = bytes(imagem)
    print(imagem_bytes)
    imagem_cinza_nova = Image.frombytes("L", tamanho, imagem_bytes)"""
    imagem_cinza_nova = Image.new("L", tamanho)
    print(imagem)
    for i in range(0, tamanho[0]*tamanho[1]):
        imagem_cinza_nova.putpixel((coordenadas_cinza[i]), imagem[i])

    print(imagem_cinza_nova.size)
    imagem_cinza_nova.show()
    imagem_cinza_nova.save("Resources/grayscale.png")
    return imagem_cinza_nova


def media_dos_pixels(r, g, b, l_im, a_im):
    imagem_cinza = []
    coordenadas_cinza = []
    for i in range(0, l_im):
        for j in range(0, a_im):
            coordenadas = i, j
            red, green, blue = float(r.getpixel(coordenadas)), float(g.getpixel(coordenadas)), float(b.getpixel(coordenadas))
            media_das_cores = 0.2989 * red + 0.5870 * green + 0.1140 * blue
            if (media_das_cores % 1) == 0:
                imagem_cinza.append(int(media_das_cores))
                coordenadas_cinza.append((coordenadas[0], coordenadas[1]))
            elif media_das_cores == 0:
                imagem_cinza.append(int(media_das_cores))
                coordenadas_cinza.append((coordenadas[0], coordenadas[1]))
            elif (media_das_cores % 1) >= 0.5:
                imagem_cinza.append((int(math.ceil(media_das_cores))))
                coordenadas_cinza.append((coordenadas[0], coordenadas[1]))
            elif (media_das_cores % 1) < 0.5:
                imagem_cinza.append((int(math.floor(media_das_cores))))
                coordenadas_cinza.append((coordenadas[0], coordenadas[1]))
    """print(len(imagem_cinza))
    print(len(coordenadas_cinza))"""

    return imagem_cinza, coordenadas_cinza


def importar_imagem(imagem):
    imagem_inicial = "Resources/" + imagem
    """print(imagem_inicial)"""
    with Image.open(imagem_inicial) as imagem_canais:
        print("imagem bands ", Image.Image.getbands(imagem_canais))
        canais_convertidos = imagem_canais.convert('RGB')
        r, g, b = canais_convertidos.split()
        return r, g, b


def canaistamanho_imagem():

    if verificar_diretorio("Resources"):
        r, g, b, = importar_imagem("morango.png")
        l_im, a_im = verificar_tamanho_imagem("Resources/morango.png")
        return r, g, b, l_im, a_im

    else:
        print("Pasta não existe...")
        exit()

"""def imagem_cinza_para_ascii(imagem):
    
    """
escala_cinza_dois = "@%#*+=-:. "
escala_cinza_um = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'. "

r_out, g_out, b_out, l_im_out, a_im_out = canaistamanho_imagem()
"""r_out.show(), g_out.show(), b_out.show()"""
"""print(l_im_out, a_im_out)"""
coordenadas_globais = [int(l_im_out), int(a_im_out)]
imagem_cinza_out, coordenadas_cinza_globais = media_dos_pixels(r_out, b_out, g_out, l_im_out, a_im_out)
imagem_cinza_final = salvar_imagem(imagem_cinza_out, coordenadas_globais, coordenadas_cinza_globais)

while True:
    print_digitado("Digite o nome do diretório ASCII que deseja criar: ")
    nome_diretorio_ascii = input()
    if nome_diretorio_ascii.isalpha():
        if nome_diretorio_ascii == "sair":
            exit()
        bool_diretorio = verificar_diretorio_ascii(nome_diretorio_ascii)
        if bool_diretorio:
            print_digitado("Diretório criado...\n")
            break
        else:
            print_digitado("Diretório já existe...\n")
            break
    elif nome_diretorio_ascii.lower().isalpha() == "sair":
        exit()
    else:
        print_digitado("O nome do diretório contém caracteres não permitidos...\n" +
                       "Por favor, use somente letras de A até Z...\n" +
                       "Caso queira sair, digite 'sair'...\n")

