import arcade
import const
import cardsetup
import random

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Solitaire"

class Solitaire(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)

        arcade.set_background_color(arcade.color.AERO_BLUE)

        self.card_list = None
        self.held_cards = None
        self.held_cards_original_position = None
        self.pile_mat_list = None

    def setup(self):
        self.held_cards = []
        self.held_cards_original_position = []


        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        pile = arcade.SpriteSolidColor(const.MAT_WIDTH, const.MAT_HEIGHT, arcade.csscolor.BROWN)
        pile.position = const.START_X, const.BOTTOM_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(const.MAT_WIDTH, const.MAT_HEIGHT, arcade.csscolor.BROWN)
        pile.position = const.START_X + const.X_SPACING, const.BOTTOM_Y
        self.pile_mat_list.append(pile)

        for i in range(7):
            pile = arcade.SpriteSolidColor(const.MAT_WIDTH, const.MAT_HEIGHT, arcade.csscolor.BROWN)
            pile.position = const.START_X + i * const.X_SPACING, const.MIDDLE_Y
            self.pile_mat_list.append(pile)

        for i in range(4):
            pile = arcade.SpriteSolidColor(const.MAT_WIDTH, const.MAT_HEIGHT, arcade.csscolor.BROWN)
            pile.position = const.START_X + i * const.X_SPACING, const.TOP_Y
            self.pile_mat_list.append(pile)


        self.card_list = arcade.SpriteList()

        for card_suit in const.CARD_SUITS:
            for card_value in const.CARD_VALUES:
                card = cardsetup.Card(card_suit, card_value, const.CARD_SCALE)
                card.position = const.START_X, const.BOTTOM_Y
                self.card_list.append(card)
        
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)
         
        

    def on_draw(self):
        self.clear()
        self.pile_mat_list.draw()
        self.card_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        if len(cards) > 0:
            primary_card = cards[-1]

            self.held_cards = [primary_card]
            self.held_cards_original_position = [self.held_cards[0].position]
            self.pull_to_top(self.held_cards[0])
        

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):

        if len(self.held_cards) == 0:
            return

        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        if arcade.check_for_collision(self.held_cards[0], pile):
            for i, dropped_card in enumerate(self.held_cards):
                dropped_card.position = pile.center_x, pile.center_y
            reset_position = False
        
        if reset_position:
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]

        self.held_cards = []
        

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy
        

    def pull_to_top(self, card: arcade.Sprite):
        self.card_list.remove(card)
        self.card_list.append(card)


def main():
    window = Solitaire()
    window.setup()
    arcade.run()

if __name__== "__main__":
    main()




