#Hangman game engine
import random
import pygame
from pygame.transform import scale
from pygame import PixelArray
pygame.init()

nom_fichier = "wordlist.txt"

def obtenir_mot(nom_fichier):
    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()
        mots = [mot.strip() for mot in lignes]
        mot_aleatoire = random.choice(mots)
        return mot_aleatoire
    
mot_pendu = obtenir_mot(nom_fichier)
x=mot_pendu
y = ""
z = ""
life = 10
for i in x :
    y += "_ "
 
for i in x:
    z += i + " "
life = 10


fenetre = pygame.display.set_mode((800,600))
blanc = (255, 255, 255)

police = pygame.font.Font(None, 36)
saisie = ""
saisie_rect = pygame.Rect(250,450,200,50)
saisie_active = False
victoire = False
defaite = False
Used_letters = []

lettres_images = {}
for lettre in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    image = pygame.image.load(f"{lettre}.png")
    image = scale(image, (40, 40))  # Redimensionne l'image à la taille 40x40
    lettres_images[lettre] = image

mouse_position = (0,0)


def traiter_lettre(lettre, y):
        global victoire, defaite, saisie, life
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
                    life = life-1
                    
                if life <= 0:
                    defaite = True
            
            saisie = ""
            return y

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if saisie_rect.collidepoint(event.pos):
                saisie_active = not saisie_active
            else:
                saisie_active = False
            
            mouse_position = pygame.mouse.get_pos()


            for lettre in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                lettre_image = lettres_images[lettre]
                lettre_rect = lettre_image.get_rect()
                lettre_rect.topleft = (position_x_letters, position_y_letters)
                fenetre.blit(lettre_image, lettre_rect)

                if lettre_rect.collidepoint(mouse_position):
                    lettre_clic = lettre.lower()

                    if lettre_rect.collidepoint(mouse_position) and event.type == pygame.MOUSEBUTTONDOWN:
                        lettre_clic = lettre.lower()
                        y= traiter_lettre(lettre_clic, y)

       
        if event.type == pygame.KEYDOWN and saisie_active:
            if event.key == pygame.K_RETURN:
                lettre = saisie.lower()
                y = traiter_lettre(lettre, y)

            elif event.key == pygame.K_BACKSPACE:
                saisie = saisie[:-1]
            else:
                saisie = saisie + event.unicode
    

                

    fenetre.fill((0,0,0))

    position_y_letters = 400
    position_x_letters = 100

    for lettre in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        lettre_image = lettres_images[lettre]
        lettre_rect = lettre_image.get_rect()
        lettre_rect.topleft = (position_x_letters, position_y_letters)
        fenetre.blit(lettre_image, lettre_rect)

        if lettre_rect.collidepoint(mouse_position):
            if event.type == pygame.MOUSEBUTTONDOWN:
                lettre_clic = lettre.lower()

                if lettre_clic in x:
                    for i in range(len(x)):
                        if x[i] == lettre_clic:
                            y = y[:i] + lettre_clic + y[i + 1:]


        position_x_letters += 40

    texte_mot = police.render(f"Mot : {y}", True, (255, 255, 255))
    fenetre.blit(texte_mot, (100, 100))

    texte_vies = police.render(f"Vies restantes: {life}", True, (255, 255, 255))
    fenetre.blit(texte_vies, (100, 150))
    Texte_Used_letters = police.render(f"Lettres utilisées: {Used_letters}", True, (255, 255, 255))
    fenetre.blit(Texte_Used_letters, (100, 250))

    

    pygame.draw.rect(fenetre, (255, 255, 255), saisie_rect, 2)
    texte_saisie = police.render(saisie, True, (255, 255, 255))
    fenetre.blit(texte_saisie, (saisie_rect.x + 5, saisie_rect.y + 5))
    saisie_rect.w = max(200, texte_saisie.get_width() + 10)

    if victoire:
        texte_victoire = police.render(f"Good job you find the word ! You still have {life} lives !", True, (255, 255, 255))
        fenetre.blit(texte_victoire, (100, 350))

    if defaite:
        texte_defaite = police.render(f"You lose, you no longer have any life ! The word was {x}", True, (255, 255, 255))
        fenetre.blit(texte_defaite, (50, 350))

    
    
    pygame.display.flip()

    if victoire or defaite:
        pygame.time.delay(5000)
        pygame.quit()
        break
