import pygame
from pygame.locals import *
from pygame.sprite import Sprite

from enum import Enum

class CardSuit(Enum):
    DIAMONDS = 1
    SPADES = 2
    HEARTS = 3
    CLUBS = 4

class CardAssets():
    @staticmethod
    def load_assets(card_back, scale):
        CardAssets.scale = scale
        CardAssets.assets = []
        for i in range(0, 4):
            CardAssets.assets.append([])
            for j in range(0, 13):
                CardAssets.assets[i].append(CardAssets.scale_surface(CardAssets.load_card_asset(i + 1, j + 1)))
        CardAssets.back_asset = CardAssets.scale_surface(pygame.image.load("assets/cards/cardBack_" + card_back + ".png").convert_alpha())
        CardAssets.pile_asset = CardAssets.scale_surface(pygame.image.load("assets/cards/panel.png").convert_alpha())
        CardAssets.card_width = CardAssets.back_asset.get_width()
        CardAssets.card_height = CardAssets.back_asset.get_height()

    @staticmethod
    def load_card_asset(suit, value):
        new_suit = ""
        if suit == CardSuit.DIAMONDS.value:
            new_suit = "Diamonds"
        elif suit == CardSuit.SPADES.value:
            new_suit = "Spades"
        elif suit == CardSuit.HEARTS.value:
            new_suit = "Hearts"
        elif suit == CardSuit.CLUBS.value:
            new_suit = "Clubs"
    
        return pygame.image.load("assets/cards/card" + new_suit + str(value) + ".png").convert_alpha()

    @staticmethod
    def scale_surface(surface):
        return pygame.transform.smoothscale(surface, 
            (int(surface.get_width() * CardAssets.scale), 
             int(surface.get_height() * CardAssets.scale)))

    @staticmethod
    def get_card_asset(suit, value, visible):
        if not visible:
            return CardAssets.back_asset
        else:
            print(suit.value)
            print(value)
            return CardAssets.assets[suit.value - 1][value - 1]

class Card(Sprite):

    @staticmethod
    def is_valid_tableau_append(tableau_cards, new_card):
        if not tableau_cards:
            if new_card.value == 13:
                return True
        elif (abs(tableau_cards[-1].suit.value - new_card.suit.value) % 2 != 0 and
               tableau_cards[-1].value - 1 == new_card.value):
             return True
            
        return False

    def __init__(self, suit, value, visible, pos = (0, 0)):
        Sprite.__init__(self)
        self.suit = suit
        self.value = value
        self.visible = visible
        self.image = CardAssets.get_card_asset(self.suit, self.value, self.visible)
        self.rect = Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())
        self.moving = False
        self.last = pos
    
    def unhide(self):
        self.visible = True
        self.update_image()

    def hide(self):
        self.visible = False
        self.update_image()

    def update_image(self):
        self.image = CardAssets.get_card_asset(self.suit, self.value, self.visible)

    def move(self, pos):
        # if self.moving:
        self.rect.x += pos[0]
        self.rect.y += pos[1]
            # self.last = new_mouse_pos
