import pygame
import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
import math
import random

# Inicialização do Pygame
pygame.init()

# Configurações da janela Pygame
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SPACE MARKER")
pygame.display.set_icon(pygame.image.load('assets/icone _Copia.ico'))  

# Carregar imagens de fundo
start_screen_bg = pygame.image.load(os.path.join('assets', 'bg.jpg')).convert()
start_screen_bg = pygame.transform.scale(start_screen_bg, (screen_width, screen_height))

game_screen_bg = pygame.image.load(os.path.join('assets', 'espaco.png')).convert()
game_screen_bg = pygame.transform.scale(game_screen_bg, (screen_width, screen_height))

exit_screen_bg = pygame.image.load(os.path.join('assets', 'sideral.jpg')).convert()
exit_screen_bg = pygame.transform.scale(exit_screen_bg, (screen_width, screen_height))

som_fundo = pygame.mixer.Sound(os.path.join('assets', "space.wav"))
som_fundo.play(-1)

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Estrutura para armazenar as marcações
marcacoes = []
constelacoes_salvas = []

# Variável para controlar o estado do jogo
in_game = False

# Função para abrir caixa de diálogo e obter nome da estrela usando Tkinter
def get_star_name():
    root = tk.Tk()
    root.withdraw()
    star_name = simpledialog.askstring("Nome da Estrela", "Digite o nome da estrela:")
    root.destroy()
    return star_name if star_name else "Desconhecido"

# Função para gerar cor aleatória para os planetas
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Função para desenhar marcadores na tela
def draw_markers():
    for marcacao in marcacoes:
        posicao = marcacao['posicao']
        nome = marcacao['nome']
        cor = random_color()  # Gera cor aleatória para cada planeta
        pygame.draw.circle(screen, cor, posicao, 10)  # Desenha círculo com cor aleatória
        font = pygame.font.Font(None, 20)
        text_surface = font.render(nome, True, WHITE)
        screen.blit(text_surface, (posicao[0] + 15, posicao[1] - 7))  # Posiciona o texto ao lado do marcador

    # Desenhar linhas entre os planetas marcados
    if len(marcacoes) > 1:
        for i in range(len(marcacoes) - 1):
            p1 = marcacoes[i]['posicao']
            p2 = marcacoes[i + 1]['posicao']
            pygame.draw.line(screen, WHITE, p1, p2, 2)  # Desenha linha branca entre os marcadores

            # Calcular distância em pixels
            distancia_pixels = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
            # Supondo que 1 pixel = 1 ano-luz
            distancia_anos_luz = int(distancia_pixels)

            font = pygame.font.Font(None, 23)
            cor = random_color()
            text_surface = font.render(f"{distancia_anos_luz} Anos-luz", True, cor)
            screen.blit(text_surface, ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2))

# Função para salvar as constelações em um arquivo JSON
def save_constellation():
    global constelacoes_salvas
    constelacoes_salvas.append(list(marcacoes))  # Salva uma cópia das marcações
    with open('constelacoes.json', 'w') as f:
        json.dump(constelacoes_salvas, f)
    messagebox.showinfo("Salvar", "Constelação salva com sucesso ;)")

# Função para carregar constelações salvas de um arquivo JSON
def load_constellations():
    global constelacoes_salvas, marcacoes
    if os.path.exists('constelacoes.json'):
        with open('constelacoes.json', 'r') as f:
            constelacoes_salvas = json.load(f)
        if constelacoes_salvas:
            marcacoes = constelacoes_salvas[-1]  # Carrega a última constelação salva
            display_constellation()  # Exibe a constelação carregada na tela
            messagebox.showinfo("Carregar", "Constelação carregada com sucesso ;)")
    else:
        messagebox.showwarning("Carregar", "Nenhuma constelação salva encontrada.")

# Função para limpar todas as marcações da tela
def clear_markers():
    global marcacoes
    marcacoes = []
    messagebox.showinfo("Limpar", "Todas as marcações foram removidas.")

# Função para inicializar o Pygame e iniciar o loop principal
def run_game():
    global in_game
    in_game = True
    running = True
    while running:
        screen.blit(game_screen_bg, (0, 0))  # Desenha o fundo do jogo

        # Botões centralizados na parte inferior da tela
        button_width = 100
        button_height = 50
        margin = 20
        save_button = pygame.Rect((screen_width - button_width) // 2 - button_width - margin, screen_height - button_height - margin, button_width, button_height)
        load_button = pygame.Rect((screen_width - button_width) // 2, screen_height - button_height - margin, button_width, button_height)
        clear_button = pygame.Rect((screen_width - button_width) // 2 + button_width + margin, screen_height - button_height - margin, button_width, button_height)
        quit_button = pygame.Rect((screen_width - button_width) // 2, screen_height - button_height - margin * 2 - button_height, button_width, button_height)

        # Desenha os botões
        pygame.draw.rect(screen, BLACK, save_button)
        pygame.draw.rect(screen, BLACK, load_button)
        pygame.draw.rect(screen, BLACK, clear_button)
        pygame.draw.rect(screen, BLACK, quit_button)

        # Texto nos botões
        font = pygame.font.Font(None, 30)
        text_surface = font.render("Salvar", True, WHITE)
        screen.blit(text_surface, (save_button.x + 15, save_button.y + 15))

        text_surface = font.render("Carregar", True, WHITE)
        screen.blit(text_surface, (load_button.x + 5, load_button.y + 15))

        text_surface = font.render("Limpar", True, WHITE)
        screen.blit(text_surface, (clear_button.x + 15, clear_button.y + 15))

        text_surface = font.render("Sair", True, WHITE)
        screen.blit(text_surface, (quit_button.x + 30, quit_button.y + 15))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_constellation()  # Salva as constelações antes de sair
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Verifica se os botões foram clicados
                if save_button.collidepoint(mouse_pos):
                    save_constellation()
                elif load_button.collidepoint(mouse_pos):
                    load_constellations()
                elif clear_button.collidepoint(mouse_pos):
                    clear_markers()
                elif quit_button.collidepoint(mouse_pos):
                    show_exit_screen()
                else:
                    # Adicionar nova marcação
                    star_name = get_star_name()
                    marcacoes.append({'nome': star_name, 'posicao': mouse_pos})
            

        draw_markers()  # Desenha todas as marcações na tela
        pygame.display.flip()  # Atualiza a tela

    # Finaliza o Pygame
    pygame.quit()

# Função para exibir a constelação carregada na tela
def display_constellation():
    global marcacoes
    for marcacao in marcacoes:
        posicao = marcacao['posicao']
        nome = marcacao['nome']
        cor = random_color() 
        pygame.draw.circle(screen, cor, posicao, 20)  
        font = pygame.font.Font(None, 20)
        text_surface = font.render(nome, True, WHITE)
        screen.blit(text_surface, (posicao[0] + 15, posicao[1] - 10)) 
        
# Função para exibir a tela de saída com agradecimento e opção de sair
def show_exit_screen():
    running = True
    while running:
        screen.blit(exit_screen_bg, (0, 0))  # Fundo com imagem 'sideral.jpg'
        
        font = pygame.font.Font(None, 90)
        cor = random_color()
        text_surface = font.render("Obrigado por Jogar!!", True, cor)
        screen.blit(text_surface, ((screen_width - text_surface.get_width()) // 2, 200))

        font = pygame.font.Font(None,40 )
        text_surface = font.render("Feito por Alex Gonçalves e Leonardo Ross", True, cor)
        screen.blit(text_surface, ((screen_width - text_surface.get_width()) // 2, 300))

        # Texto "Pressione Esc para sair..." no canto inferior direito
        font = pygame.font.Font(None, 30)
        text_surface = font.render("Pressione Esc para sair...", True, WHITE)
        screen.blit(text_surface, (screen_width - text_surface.get_width() - 10, screen_height - text_surface.get_height() - 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    # Forçar a saída do Pygame ao sair da tela de saída
    pygame.quit()

# Função para exibir a tela inicial com menu
def show_start_screen():
    global in_game
    in_game = False
    running = True
    while running:
        screen.blit(start_screen_bg, (0, 0))  # Fundo com imagem 'bg.jpg'
        
        font = pygame.font.Font(None, 60)
        text_surface = font.render("Space Maker", True, WHITE)
        screen.blit(text_surface, ((screen_width - text_surface.get_width()) // 2, 100))

        # Botões centralizados na parte inferior da tela
        button_width = 200
        button_height = 50
        button_margin = 20
        play_button = pygame.Rect((screen_width - button_width) // 2, 250, button_width, button_height)
        load_button = pygame.Rect((screen_width - button_width) // 2, 320, button_width, button_height)
        quit_button = pygame.Rect((screen_width - button_width) // 2, 390, button_width, button_height)

        pygame.draw.rect(screen, WHITE, play_button, 2)
        pygame.draw.rect(screen, WHITE, load_button, 2)
        pygame.draw.rect(screen, WHITE, quit_button, 2)

        font = pygame.font.Font(None, 30)
        text_surface = font.render("Jogar", True, WHITE)
        screen.blit(text_surface, (play_button.x + 70, play_button.y + 15))

        text_surface = font.render("Carregar", True, WHITE)
        screen.blit(text_surface, (load_button.x + 50, load_button.y + 15))

        text_surface = font.render("Sair", True, WHITE)
        screen.blit(text_surface, (quit_button.x + 75, quit_button.y + 15))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_button.collidepoint(mouse_pos):
                    running = False
                    run_game()
                elif load_button.collidepoint(mouse_pos):
                    load_constellations()
                elif quit_button.collidepoint(mouse_pos):
                    running = False
                    pygame.quit()
                    return


def main():
    show_start_screen()


if __name__ == "__main__":
    main()
