import arcade
import const
import solitaire

class Card(arcade.Sprite):
    def __init__(self, suit, value,numeric_value, scale =1):

        self.suit = suit
        self.value = value
        self.numeric_value = numeric_value      

        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")
    
