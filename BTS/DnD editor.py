import pygame
from pygame.locals import *
import tkinter as tk
from tkinter import filedialog
import os
import cv2
import numpy as np

BLUE = (25, 25, 255)
BRIGHT_BLUE = (135, 206, 250)  # Cor brilhante para o efeito de clareamento

class DraggableObject:
    def __init__(self, image, position):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.offset = (0, 0)
        self.dragging = False
        self.selected = False
        self.filtered_image = None
    
    def update(self):
        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.topleft = (mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1])
    
    def draw(self, surface):
        if self.filtered_image:
            surface.blit(self.filtered_image, self.rect)
        else:
            surface.blit(self.image, self.rect)
        
        if self.selected:
            pygame.draw.rect(surface, BLUE, self.rect, 2)
    
    def apply_grayscale_filter(self):
        if self.image:
            image_array = pygame.surfarray.array3d(self.image)
            gray_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            gray_surface = pygame.surfarray.make_surface(gray_image)
            self.filtered_image = gray_surface
    
    def apply_blur_filter(self):
        if self.image:
            image_array = pygame.surfarray.array3d(self.image)
            blurred_image = cv2.blur(image_array, (5, 5))
            blurred_surface = pygame.surfarray.make_surface(blurred_image)
            self.filtered_image = blurred_surface
    
    def apply_brightness_filter(self):
        if self.image:
            image_array = pygame.surfarray.array3d(self.image)
            hsv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)
            brightness_adjusted_image = cv2.add(hsv_image[:, :, 2], 20)
            hsv_image[:, :, 2] = np.clip(brightness_adjusted_image, 0, 255)
            adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
            adjusted_surface = pygame.surfarray.make_surface(adjusted_image)
            self.filtered_image = adjusted_surface
    
    def apply_invert_filter(self):
        if self.image:
            inverted_image = 255 - pygame.surfarray.array3d(self.image)
            inverted_surface = pygame.surfarray.make_surface(inverted_image)
            self.filtered_image = inverted_surface

class Button:
    def __init__(self, text, position):
        self.font = pygame.font.Font(None, 24)
        self.text = text
        self.surface = self.font.render(self.text, True, BLUE)
        self.rect = self.surface.get_rect(topleft=position)
    
    def draw(self, surface):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # Botão selecionado - Aplica o efeito de clareamento
            pygame.draw.rect(surface, BRIGHT_BLUE, self.rect)
        surface.blit(self.surface, self.rect)

def open_image_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpeg")])
    return file_path

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("DnD editor")
icn = pygame.image.load("toreador.png")
pygame.display.set_icon(icn)

objects = []
buttons = [
    Button("Adicionar", (10, 10)),
    Button("Remover", (10, 50)),
    Button("Editar", (10, 90)),
    Button("Preto e Branco", (10, 130)),
    Button("Blur", (10, 170)),
    Button("Brilho", (10, 210)),
    Button("Inverter", (10, 250)),
    Button("Download", (10, 290)),
]

selected_object = None
filtered_buttons_visible = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in buttons:
                        if button.rect.collidepoint(event.pos) and button.text == "Adicionar":
                            image_path = open_image_dialog()
                            if image_path:
                                _, extension = os.path.splitext(image_path)
                                if extension.lower() in ['.png', '.jpeg']:
                                    new_image = pygame.image.load(image_path)
                                    new_object = DraggableObject(new_image, (100, 100))
                                    objects.append(new_object)
                                    selected_object = new_object
                                    filtered_buttons_visible = False
                        elif button.rect.collidepoint(event.pos) and button.text == "Remover":
                            if selected_object:
                                objects.remove(selected_object)
                                selected_object = None
                                filtered_buttons_visible = False
                        elif button.rect.collidepoint(event.pos) and button.text == "Editar":
                            filtered_buttons_visible = not filtered_buttons_visible
                            selected_object = None
                            
                        elif button.rect.collidepoint(event.pos) and selected_object:
                            if button.text == "Preto e Branco":
                                selected_object.apply_grayscale_filter()
                            elif button.text == "Blur":
                                selected_object.apply_blur_filter()
                            elif button.text == "Brilho":
                                selected_object.apply_brightness_filter()
                            elif button.text == "Inverter":
                                selected_object.apply_invert_filter()
                            elif button.text == "Download":
                                screen.fill((255, 255, 255))
                                for obj in objects:
                                    obj.update()
                                    obj.draw(screen)
                                
                                root = tk.Tk()
                                root.withdraw()
                                file_path = filedialog.asksaveasfilename(defaultextension=".png")
                                if file_path:
                                    pygame.image.save(screen, file_path)
                                root.destroy()
                else:
                    for obj in reversed(objects):
                        if obj.rect.collidepoint(event.pos):
                            obj.dragging = True
                            obj.selected = True
                            mouse_x, mouse_y = event.pos
                            obj.offset = (mouse_x - obj.rect.x, mouse_y - obj.rect.y)
                            selected_object = obj
                            break
                        else:
                            obj.selected = False
                            obj.dragging = False
                        
                    
        
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                for obj in objects:
                    obj.dragging = False
    
    screen.fill((255, 255, 255))
    
    for obj in objects:
        obj.update()
        obj.draw(screen)
    
    # Desenha a barra de menu
    pygame.draw.rect(screen, (250, 250, 210), (0, 0, 150, 350))
    pygame.draw.rect(screen, (220, 177, 25), (0, 0, 150, 350), 4)
    
    for button in buttons:
        if not (button.text == "Preto e Branco" or button.text == "Blur" or button.text == "Brilho" or button.text == "Inverter"):
            button.draw(screen)
        elif filtered_buttons_visible:
            button.draw(screen)
    
    pygame.display.update()
