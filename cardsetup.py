import arcade
import const
import solitaire

class Card(arcade.Sprite):
    def __init__(self, suit, value,numeric_value, scale =1):

        self.suit = suit
        self.value = value
        self.numeric_value = numeric_value      

        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"
        self.is_face_up = False

        super().__init__(const.FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")

    def face_down(self):
        self.texture = arcade.load_texture(const.FACE_DOWN_IMAGE)
        self.is_face_up = False
        
    def face_up(self):
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    @property
    def is_face_down(self):
        return not self.is_face_up

    
