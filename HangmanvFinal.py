#Hangman game engine
import random
import pygame
import os
import sys
pygame.init()

nom_fichier = "wordlist.txt"

def obtenir_mot(nom_fichier):
    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()
        mots = [mot.strip() for mot in lignes]
        mot_aleatoire = random.choice(mots)
        return mot_aleatoire
    
def shake_interface(surface, shake_intensity, duration):
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration:
        offset_x = random.randint(-shake_intensity, shake_intensity)
        offset_y = random.randint(-shake_intensity, shake_intensity)
        surface.blit(pygame.Surface.copy(surface), (offset_x, offset_y))
        pygame.display.flip()
    
mot_pendu = obtenir_mot(nom_fichier)
x=mot_pendu
y = ""
z = ""
for i in x :
    y += "_ "
 
for i in x:
    z += i + " "
current_life = 7
shake_duration = 700
shake_intensity = 500

largeur, hauteur = 800, 600

fenetre = pygame.display.set_mode((largeur,hauteur))
blanc = (255, 255, 255)

police = pygame.font.Font("Tele.ttf", 18)
saisie = ""
saisie_rect = pygame.Rect(300,450,200,40)
saisie_active = False
victoire = False
defaite = False
Used_letters = []
cursor_visible = True
cursor_timer = 0
game_over = False
ecran_accueil = True
attente_entree = True


restart_button_rect = pygame.Rect(300, 500, 200, 50)
restart_button_text = "Restart Game"

frames = [f"F{i}.gif" for i in range(0, 13)]

images = [pygame.transform.scale(pygame.image.load(os.path.join("FramesReper", frame)), (largeur, hauteur)) for frame in frames]

indice_frame = 0

horloge = pygame.time.Clock()

while ecran_accueil:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                ecran_accueil = False  # Lorsque l'utilisateur appuie sur Entrée, passez à la partie du jeu

    # Dessinez l'écran d'accueil
    fenetre.fill((0, 0, 0))  # Fond noir
    titre_texte = police.render("HANGMAN", True, blanc)
    instructions_texte = police.render("Enter to start...But are you sur to play this game ?", True, blanc)
    fenetre.blit(titre_texte, (largeur // 2 - titre_texte.get_width() // 2, 200))
    fenetre.blit(instructions_texte, (largeur // 2 - instructions_texte.get_width() // 2, 300))
    
    pygame.display.flip()
    



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if saisie_rect.collidepoint(event.pos):
                    saisie_active = True
                else:
                    saisie_active = False
       
            if event.type == pygame.KEYDOWN and saisie_active:
                if event.key == pygame.K_RETURN:
                    lettre = saisie.lower()

                    if lettre == x:
                            victoire = True

                    if lettre in z:
                        for i in range(len(z)):
                            if z[i] == lettre:
                                y = y[:i] + lettre + y[i + 1:] 
                        
                        if y == z:
                            victoire = True
                        
                    else:
                        if lettre.isalpha() and len(lettre)==1:
                            Used_letters.append(lettre)
                            if current_life > 0:
                                current_life -= 1
                                shake_interface(fenetre, shake_intensity, shake_duration)
                        if current_life == 0:
                            defaite = True
                            
                            
                        
                    saisie = ""
                elif event.key == pygame.K_BACKSPACE:
                    saisie = saisie[:-1]
                else:
                    saisie = saisie + event.unicode
                

    if game_over and event.type == pygame.MOUSEBUTTONDOWN:
        if restart_button_rect.collidepoint(event.pos):
            # Reset game variables
            mot_pendu = obtenir_mot(nom_fichier)
            x=mot_pendu
            y = ""
            z = ""
            life = 10
            for i in x :
                y += "_ "
 
            for i in x:
                z += i + " "
            life = 7
            current_life = 7
            saisie = ""
            Used_letters = []
            cursor_visible = True
            cursor_timer = 0
            game_over = False
            victoire = False
            defaite = False
                

    hangman_images = []
    for i in range(7, -1, -1):
        image = pygame.image.load(f'H{i}.png')
        hangman_images.append(image)
    
    


    fenetre.fill((0,0,0))

    fenetre.blit(images[indice_frame], (0, 0))

    indice_frame = (indice_frame + 1) % len(images)

    if 0<= current_life <= 7:
        hangman_image = hangman_images[current_life]
        fenetre.blit(hangman_image, (500, 350))


    texte_mot = police.render(f"Word: {y}", True, (255, 255, 255))
    fenetre.blit(texte_mot, (100, 100))

    texte_vies = police.render(f"Remaining lives: {current_life}", True, (255, 255, 255))
    fenetre.blit(texte_vies, (100, 150))
    Texte_Used_letters = police.render(f"Used letters: {Used_letters}", True, (255, 255, 255))
    fenetre.blit(Texte_Used_letters, (100, 250))

    pygame.draw.rect(fenetre, (255, 255, 255), saisie_rect, 2)
    texte_saisie = police.render(saisie, True, (255, 255, 255))
    fenetre.blit(texte_saisie, (saisie_rect.x + 5, saisie_rect.y + 5))
    saisie_rect.w = max(200, texte_saisie.get_width() + 10)

    if victoire:
        texte_victoire = police.render(f"Good job you find the word !", True, (255, 255, 255))
        fenetre.blit(texte_victoire, (100, 350))

    if defaite:
        texte_defaite = police.render(f"You no longer have any life !The word was '{x}'", True, (255, 255, 255))
        fenetre.blit(texte_defaite, (50, 350))



    if saisie_active:
        cursor_timer += 1
        if cursor_timer >= 30:
            cursor_timer = 0
            cursor_visible = not cursor_visible

    if cursor_visible and saisie_active:
        cursor_x = saisie_rect.x + texte_saisie.get_width() + 5
        pygame.draw.line(fenetre, (255, 255, 255), (cursor_x, saisie_rect.y + 5), (cursor_x, saisie_rect.y + saisie_rect.height - 5))

    if game_over:
        pygame.draw.rect(fenetre, (255, 255, 255), restart_button_rect)
        text_surface = police.render(restart_button_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=restart_button_rect.center)
        fenetre.blit(text_surface, text_rect)

    
    
    pygame.display.flip()

    horloge.tick(10)



    if victoire or defaite:
        game_over = True

pygame.quit()
