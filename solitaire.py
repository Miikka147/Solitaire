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
        self.piles = None
        self.primary_card = None

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
            i=0
            for card_value in const.CARD_VALUES:
                card_numeric = const.CARD_NUMERIC_VALUES[i]
                card = cardsetup.Card(card_suit, card_value,card_numeric, const.CARD_SCALE)
                card.position = const.START_X, const.BOTTOM_Y
                self.card_list.append(card)
                i=i+1
        
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        self.piles = [[] for _ in range(const.PILE_COUNT)]
        for card in self.card_list:
            self.piles[const.BOTTOM_FACE_DOWN_PILE].append(card)
         
        

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

    def check_top_move_rules(self,pile):
        #print(self.held_cards[0].suit)
        #print(self.held_cards[0].value)
        #print(self.__dict__)
        #print(self.pile_mat_list.index(pile))
        #print(len(self.piles[9]))
          #print(self.piles[self.pile_mat_list.index(pile)][0].suit)
               # print(self.held_cards[0].suit)
        check_value = self.held_cards[0].value

        if(self.held_cards[0].value) == "A":
            check_value = 1
        elif(self.held_cards[0].value) == "J":
            check_value = 11
        elif(self.held_cards[0].value) == "Q":
            check_value = 12
        elif(self.held_cards[0].value) == "K":
            check_value = 13

        if (len(self.piles[self.pile_mat_list.index(pile)])) < 1:  # if top pile is empty
            if int(check_value) == (len(self.piles[self.pile_mat_list.index(pile)])+1): # check the card is an ace
                return(True)
        elif int(check_value) == (len(self.piles[self.pile_mat_list.index(pile)])+1) and self.piles[self.pile_mat_list.index(pile)][0].suit == self.held_cards[0].suit: # check card suit is same as the lowest card on the pile & card number is 1 higher than top card on pile
            print(len(self.piles[self.pile_mat_list.index(pile)])+1)
            return(True)
        else:
             return(False)

    def check_bot_move_rules(self,pile):
        check_color = ""

        if(self.held_cards[0].suit) == "Diamonds" or (self.held_cards[0].suit) == "Hearts":
            check_color = "red"
        else:
            check_color = "black"

    
        if (len(self.piles[self.pile_mat_list.index(pile)])) > 0:
            print(self.piles[self.pile_mat_list.index(pile)][len(self.piles[self.pile_mat_list.index(pile)])-1].numeric_value)

        if (len(self.piles[self.pile_mat_list.index(pile)])) < 1:
            return(True)
        elif  int(self.held_cards[0].numeric_value) + 1 == int(self.piles[self.pile_mat_list.index(pile)][len(self.piles[self.pile_mat_list.index(pile)])-1].numeric_value) and (check_color == "black" and self.piles[self.pile_mat_list.index(pile)][len(self.piles[self.pile_mat_list.index(pile)])-1].suit == "Diamonds" or self.piles[self.pile_mat_list.index(pile)][len(self.piles[self.pile_mat_list.index(pile)])-1].suit == "Hearts"):
            return(True)
        elif int(self.held_cards[0].numeric_value) + 1 == int(self.piles[self.pile_mat_list.index(pile)][len(self.piles[self.pile_mat_list.index(pile)])-1].numeric_value) and (check_color == "red" and self.piles[self.pile_mat_list.index(pile)][len(self.piles[self.pile_mat_list.index(pile)])-1].suit == "Spades" or self.piles[self.pile_mat_list.index(pile)][len(self.piles[self.pile_mat_list.index(pile)])-1].suit == "Clubs"):
            return(True)
        else:
            return(False)
  
        

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):

        if len(self.held_cards) == 0:
            return

        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        if arcade.check_for_collision(self.held_cards[0], pile):

            pile_index = self.pile_mat_list.index(pile)

            if pile_index == self.get_pile_for_card(self.held_cards[0]):
                pass

            elif const.PLAY_PILE_1 <= pile_index <= const.PLAY_PILE_7 and self.check_bot_move_rules(pile) == True:
                if len(self.piles[pile_index]) > 0:
                    top_card = self.piles[pile_index][-1]
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = top_card.center_x, \
                                                top_card.center_y - const.CARD_VERTICAL_OFFSET * 1
                else:
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = pile.center_x, \
                                                pile.center_y - const.CARD_VERTICAL_OFFSET * 1
                for card in self.held_cards:
                    self.move_card_to_new_pile(card,pile_index)

               
                reset_position = False          # if successful


            elif const.TOP_PILE_1 <= pile_index <= const.TOP_PILE_4 and len(self.held_cards) == 1 and self.check_top_move_rules(pile) == True:
                self.held_cards[0].position = pile.position
                for card in self.held_cards:
                    self.move_card_to_new_pile(card, pile_index)
                    
                    

                reset_position = False          # if successful

            for i, dropped_card in enumerate(self.held_cards):          #center cards on bottom row
                dropped_card.position = pile.center_x, pile.center_y

        

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
    
    def get_pile_for_card(self,card):
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

    def remove_card_from_pile(self,card):
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break
    
    def move_card_to_new_pile(self,card, pile_index):
        self.remove_card_from_pile(card)
        self.piles[pile_index].append(card)



def main():
    window = Solitaire()
    window.setup()
    arcade.run()

if __name__== "__main__":
    main()




