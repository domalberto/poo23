import pygame
from pygame.locals import *
from pygame.sprite import Group

import os

from random import shuffle

from enum import Enum
from solitaire.card import Card, CardSuit, CardAssets
from solitaire.cardpile import *

# TODO: use these game states
class GameState(Enum):
    MENU = 1
    GAME = 2
    GAME_OVER = 3

class Solitaire:
    game_state = GameState.GAME
    should_quit = False

    def __init__(self, spacing, tableau_spacing):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Solitaire")
        
        CardAssets.load_assets("green1", 0.7)
        card_width = CardAssets.card_width
        card_height = CardAssets.card_height

        width = 8 * spacing + 7 * int(card_width)
        height = 2 * spacing + int(card_height) + 600
        self.screen = pygame.display.set_mode((width, height))
        
        self.dragged_cards_pile = None
        self.dragged_cards = []

        background_path = os.path.join("C:/Users/pfagu/OneDrive/Documentos/solitaire-py-master/assets/cards", "background.png")
        self.background = pygame.image.load(background_path)
        self.background = pygame.transform.scale(self.background, self.screen.get_size())

        cards = []
        for suit in CardSuit:
            for value in range(1, 14):
                cards.append((Card(suit, value, False)))
        shuffle(cards)
 
        # Stock pile
        self.stock = StockPile(Rect(spacing, spacing, card_width, card_height), CardAssets.pile_asset)
        
        # Waste pile
        self.waste = WastePile(Rect(2 * spacing + card_width, spacing, card_width, card_height), (card_width + spacing ) / 4)
        
        # Foundation piles
        self.foundations = []
        for i in range (0, 4):
            foundation_rect = Rect(4 * spacing + 3 * card_width + (spacing + card_width) * i, spacing, card_width, card_height)
            self.foundations.append(FoundationPile(foundation_rect, CardAssets.pile_asset))

        # Tableau piles
        self.tableaus = []
        index = 0
        for i in range(0, 7):
            tableau_rect = Rect(spacing + (spacing + card_width) * i, 2 * spacing + card_height, card_width, card_height)
            self.tableaus.append(TableauPile(tableau_rect, CardAssets.pile_asset, tableau_spacing))
            for j in range (0, i + 1):
                self.tableaus[i].add_card(cards[index])
                index += 1

        # Add cards to stock
        for i in range(28, 52):
            self.stock.add_card(cards[i])

    def update(self):
        # print(self.dragged_cards)
        for event in pygame.event.get():
            if event.type == QUIT:
                self.should_quit = True
            elif event.type == MOUSEBUTTONDOWN:
                if not self.dragged_cards:
                    if self.stock.collidepoint(event.pos):
                        if not self.stock.is_empty():
                            cards_from_stock = self.stock.get_cards()
                            for card in cards_from_stock: 
                                card.unhide()
                                self.waste.add_card(card)
                        else:
                            cards_from_waste = self.waste.get_cards()
                            for card in cards_from_waste:
                                card.hide()
                                self.stock.add_card(card)
                    draggable_piles = self.tableaus + self.foundations + [self.waste]
                    for pile in draggable_piles:
                        if pile.collidepoint(event.pos):
                            self.dragged_cards = pile.start_drag(event.pos)
                            if self.dragged_cards:
                                self.dragged_cards_pile = pile
                            break
            elif event.type == MOUSEMOTION:
                mouse_rel = pygame.mouse.get_rel()
                for sprite in self.dragged_cards:
                    sprite.move(mouse_rel)
                
            elif event.type == MOUSEBUTTONUP:
                if self.dragged_cards:
                    for tableau in self.tableaus:
                        if tableau.collidepoint(event.pos):
                            if tableau.drop(self.dragged_cards):
                                self.dragged_cards = []
                            break
                    if len(self.dragged_cards) == 1:
                        for foundation in self.foundations:
                            if foundation.collidepoint(event.pos):
                                if foundation.drop(self.dragged_cards[0]):
                                    self.dragged_cards = []
                                break
                    for card in self.dragged_cards:
                        self.dragged_cards_pile.add_card(card)
                    self.dragged_cards = []
                    self.dragged_cards_pile.end_drag()
                    self.dragged_cards_pile = None
                    
        self.stock.update()
        for tableau in self.tableaus:
            tableau.update()

    def render(self):
        self.screen.blit(self.background, (0, 0))

        self.stock.draw(self.screen)
        self.waste.draw(self.screen)

        for foundation in self.foundations:
            foundation.draw(self.screen)

        for tableau in self.tableaus:
            tableau.draw(self.screen)

        for card_sprite in self.dragged_cards:
            self.screen.blit(card_sprite.image, card_sprite.rect)
        
        pygame.display.flip()

    def run(self):
        while not self.should_quit:
            self.update()
            self.render() 