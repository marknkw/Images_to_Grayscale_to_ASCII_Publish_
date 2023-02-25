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
        if verificar_imagem("Resources/quadra.jpg"):
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
        time.sleep(0.01)


def verificar_tamanho_imagem(imagem):
    return (Image.open(imagem)).size


def salvar_imagem(imagem, tamanho, coordenadas_cinza):
    """imagem_bytes = bytes(imagem)
    print(imagem_bytes)
    imagem_cinza_nova = Image.frombytes("L", tamanho, imagem_bytes)"""
    imagem_cinza_nova = Image.new("L", tamanho)
    """print(imagem)"""
    for i in range(0, tamanho[0]*tamanho[1]):
        imagem_cinza_nova.putpixel((coordenadas_cinza[i]), imagem[i])

    """print(imagem_cinza_nova.size)"""
    """imagem_cinza_nova.show()"""
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


def pixel_para_lista_resize(l_imagem):
    imagem_cinza_ascii = []
    coordenadas_cinza = []
    tamanho = (x, y) = l_imagem.size
    """print(tamanho)"""

    for j in range(0, y - 1):
        linha = ""
        for i in range(0, x - 1):
            coordenadas = i, j
            luminancia = l_imagem.getpixel(coordenadas)
            valor_luminancia = int((luminancia * 69 / 255)) - 1
            linha += escala_cinza_um[valor_luminancia] + " "
            coordenadas_cinza.append(coordenadas)
        imagem_cinza_ascii.append(linha)
    """print(len(imagem_cinza_ascii))
    print(len(coordenadas_cinza))"""

    return imagem_cinza_ascii, coordenadas_cinza


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
        r, g, b = importar_imagem("quadra.jpg")
        l_im, a_im = verificar_tamanho_imagem("Resources/quadra.jpg")
        return r, g, b, l_im, a_im

    else:
        print("Pasta não existe...")
        exit()


def definir_tamanho_divisivel(largura, altura):
    mod_l, mod_a = (largura % 12), (altura % 12)
    largura_divisivel = largura
    altura_divisivel = altura

    if mod_l != 0:
        if mod_l <= 5:
            largura_divisivel = largura - mod_l
        elif mod_l > 5:
            largura_divisivel = (12-mod_l)+largura
    elif mod_l == 0:
        largura_divisivel = largura/12

    if mod_a != 0:
        if mod_a <= 5:
            altura_divisivel = altura - mod_a
        elif mod_a > 5:
            altura_divisivel = (12-mod_a)+altura
    elif mod_a == 0:
        altura_divisivel = altura/12
    return largura_divisivel, altura_divisivel


def imagem_cinza_para_ascii(imagem, coordenadas, coordenadas_cinza):
    imagem_ascii = []
    imagem_ascii_redimensionada = []
    imagem_l, imagem_a = int(coordenadas[0]/12), int(coordenadas[1]/12)
    imagem_l_r, imagem_a_r = definir_tamanho_divisivel(imagem_l, imagem_a)

    valor_index = 0
    for i in range(coordenadas[0]):
        for j in range(coordenadas[1]):
            valor_luminancia = int((math.floor(imagem[valor_index]*69)/255))
            imagem_ascii.append(escala_cinza_um[valor_luminancia])
            valor_index = valor_index+1


def salvar_imagem_ascii(diretorio, imagem):
    with open(diretorio + "/" + "imagem_ascii.txt", 'w+') as txt:
        for i in imagem:
            txt.write(i + "\n")
        txt.close()
        exit()


def imagem_redimensionada(coordenadas):
    imagem_cinza_local = Image.open("Resources/grayscale.png")
    imagem_l, imagem_a = coordenadas[0] / 12, coordenadas[1] / 12
    imagem_l_r, imagem_a_r = definir_tamanho_divisivel(imagem_l, imagem_a)
    imagem_cinza_redimensionada = imagem_cinza_local.resize((int(imagem_l_r), int(imagem_a_r)))
    imagem_cinza_redimensionada.save("Resources/grayscale_redimensionada.png")
    imagem_redimensionada_luminancia, coordenadas_luminancia = pixel_para_lista_resize(imagem_cinza_redimensionada)
    return imagem_l_r, imagem_a_r, imagem_redimensionada_luminancia


def imagem_cinza_para_ascii_com_resize(coordenadas):
    imagem_redimensionada_luminancia = []
    imagem_ascii_redimensionada = []
    imagem_l_r, imagem_a_r, imagem_redimensionada_luminancia_ascii = imagem_redimensionada(coordenadas)
    coordenadas_r = imagem_l_r, imagem_a_r
    return imagem_redimensionada_luminancia_ascii, coordenadas_r


def reverter_ramps(string):
    return string[::-1]


escala_cinza_dois = r"@%#*+=-:. "
escala_cinza_um = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'. "
r_out, g_out, b_out, l_im_out, a_im_out = canaistamanho_imagem()
"""r_out.show(), g_out.show(), b_out.show()"""
"""print(l_im_out, a_im_out)"""
coordenadas_globais = [int(l_im_out), int(a_im_out)]
imagem_cinza_out, coordenadas_cinza_globais = media_dos_pixels(r_out, b_out, g_out, l_im_out, a_im_out)
imagem_cinza_final = salvar_imagem(imagem_cinza_out, coordenadas_globais, coordenadas_cinza_globais)
nome_diretorio_ascii = []

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

"""imagem_cinza_para_ascii(imagem_cinza_out, coordenadas_globais, coordenadas_cinza_globais)"""
imagem_ascii_redimensionada_global, coordenadas_redimensionadas = imagem_cinza_para_ascii_com_resize(coordenadas_globais)
salvar_imagem_ascii(nome_diretorio_ascii, imagem_ascii_redimensionada_global)

"""if salvar_bool:
    print_digitado("Imagem salva em " + nome_diretorio_ascii + "...\n")
    exit()
else:
    print_digitado("Não foi possível salvar a imagem...")"""