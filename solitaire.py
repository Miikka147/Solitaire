import arcade
import const
import cardsetup
import random
import arcade.gui


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Solitaire"


class GameView(arcade.View):

    def __init__(self):
        super().__init__()
 
        self.background = None

        self.card_list = None
        self.held_cards = None
        self.held_cards_original_position = None
        self.pile_mat_list = None
        self.piles = None
        self.primary_card = None
        self.total_time = 0.0
        self.moves = 0
        self.timer_text = arcade.Text(
            text="00:00:00",
            start_x=SCREEN_WIDTH // 2,
            start_y=SCREEN_HEIGHT - SCREEN_HEIGHT + 20,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )
        self.moves_text = arcade.Text(
            text="MOVES: 0",
            start_x=SCREEN_WIDTH // 2 + SCREEN_WIDTH // 5,
            start_y=SCREEN_HEIGHT - SCREEN_HEIGHT + 20,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )
        

    def setup(self):
        self.held_cards = []
        self.held_cards_original_position = []
        self.total_time = 0.0
        self.moves = 0
        self.background = arcade.load_texture(const.BACKGROUND_IMAGE)


        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        pile = arcade.SpriteSolidColor(const.MAT_WIDTH, const.MAT_HEIGHT, arcade.csscolor.DARK_GREEN)
        pile.position = const.START_X, const.TOP_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(const.MAT_WIDTH, const.MAT_HEIGHT, arcade.csscolor.DARK_GREEN)
        pile.position = const.START_X + const.X_SPACING, const.TOP_Y
        self.pile_mat_list.append(pile)


        for i in range(7):
            pile = arcade.SpriteSolidColor(const.MAT_WIDTH, const.MAT_HEIGHT, arcade.csscolor.RED)
            pile.position = const.START_X + i * const.X_SPACING, const.MIDDLE_Y
            #pile.position = const.START_X + i * const.X_SPACING, SCREEN_HEIGHT/2 - const.X_SPACING
            self.pile_mat_list.append(pile)
            

        for i in range(4):
            pile = arcade.SpriteSolidColor(const.MAT_WIDTH, const.MAT_HEIGHT, arcade.csscolor.DARK_GREEN)
            pile.position = SCREEN_WIDTH - const.START_X - i*const.X_SPACING , const.TOP_Y
            
            self.pile_mat_list.append(pile)


        self.card_list = arcade.SpriteList()

        
        for card_suit in const.CARD_SUITS:
            i=0
            for card_value in const.CARD_VALUES:
                card_numeric = const.CARD_NUMERIC_VALUES[i]
                card = cardsetup.Card(card_suit, card_value,card_numeric, const.CARD_SCALE)
                card.position = const.START_X, const.TOP_Y
                self.card_list.append(card)
                i=i+1
        
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        self.piles = [[] for _ in range(const.PILE_COUNT)]
        for card in self.card_list:
            self.piles[const.BOTTOM_FACE_DOWN_PILE].append(card)

        for pile_no in range(const.PLAY_PILE_1, const.PLAY_PILE_7 + 1):
            for j in range(pile_no - const.PLAY_PILE_1 + 1):
                card = self.piles[const.BOTTOM_FACE_DOWN_PILE].pop()
                self.piles[pile_no].append(card)
                card.position = self.pile_mat_list[pile_no].position[0] , \
                                SCREEN_HEIGHT - const.MAT_HEIGHT - const.X_SPACING - const.CARD_VERTICAL_OFFSET * j 
                self.pull_to_top(card)

        for i in range(const.PLAY_PILE_1, const.PLAY_PILE_7 + 1):
            self.piles[i][-1].face_up()
         
    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0,0,
                                          SCREEN_WIDTH, SCREEN_HEIGHT,self.background)
        self.pile_mat_list.draw()
        self.card_list.draw()
        self.timer_text.draw()
        self.moves_text.draw()
        


    def on_update(self, delta_time):
        if self.moves > 0:
            self.total_time += delta_time
            minutes = int(self.total_time) // 60
            seconds = int(self.total_time) % 60
            self.timer_text.text = f"{minutes:02d}:{seconds:02d}"
            self.moves_text.text = "MOVES: "+str(self.moves)

    
        

    def on_mouse_press(self, x, y, button, key_modifiers):
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        if len(cards) > 0:
            primary_card = cards[-1]
            assert isinstance(primary_card, cardsetup.Card)

            pile_index = self.get_pile_for_card(primary_card)

            if pile_index == const.BOTTOM_FACE_DOWN_PILE:
                for i in range(const.CARDS_TO_FLIP):
                    if len(self.piles[const.BOTTOM_FACE_DOWN_PILE]) == 0:
                        break
                    card = self.piles[const.BOTTOM_FACE_DOWN_PILE][-1]
                    card.face_up()
                    card.position = self.pile_mat_list[const.BOTTOM_FACE_UP_PILE].position
                    self.piles[const.BOTTOM_FACE_DOWN_PILE].remove(card)
                    self.piles[const.BOTTOM_FACE_UP_PILE].append(card)
                    self.pull_to_top(card)
                    self.moves +=1
                    print(self.moves)
            
            elif primary_card.is_face_down and self.piles[pile_index].index(primary_card) == len(self.piles[pile_index])-1:
                primary_card.face_up()
            
            else:
                self.held_cards = [primary_card]
                self.held_cards_original_position = [self.held_cards[0].position]
                self.pull_to_top(self.held_cards[0])

                card_index = self.piles[pile_index].index(primary_card)
                for i in range(card_index + 1, len(self.piles[pile_index])):
                    card = self.piles[pile_index][i]
                    self.held_cards.append(card)
                    self.held_cards_original_position.append(card.position)
                    self.pull_to_top(card)
        else:
            mats = arcade.get_sprites_at_point((x, y), self.pile_mat_list)

            if len(mats) > 0:
                mat = mats[0]
                mat_index = self.pile_mat_list.index(mat)

                if mat_index == const.BOTTOM_FACE_DOWN_PILE and len(self.piles[const.BOTTOM_FACE_DOWN_PILE]) == 0:
                    temp_list = self.piles[const.BOTTOM_FACE_UP_PILE].copy()
                    for card in reversed(temp_list):
                        card.face_down()
                        self.piles[const.BOTTOM_FACE_UP_PILE].remove(card)
                        self.piles[const.BOTTOM_FACE_DOWN_PILE].append(card)
                        card.position = self.pile_mat_list[const.BOTTOM_FACE_DOWN_PILE].position

        

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
        
        #print(check_color)

    
        #if (len(self.piles[self.pile_mat_list.index(pile)])) > 0:
            #print(self.piles[self.pile_mat_list.index(pile)][len(self.piles[self.pile_mat_list.index(pile)])-1].numeric_value)
        print(self.held_cards[0].numeric_value)

        if (len(self.piles[self.pile_mat_list.index(pile)])) < 1:
            if(int(self.held_cards[0].numeric_value) == 13):
                return(True)
            else:
                return(False)
        elif  int(self.held_cards[0].numeric_value) + 1 == int(self.piles[self.pile_mat_list.index(pile)][len(self.piles[self.pile_mat_list.index(pile)])-1].numeric_value) and check_color == "black" and (self.piles[self.pile_mat_list.index(pile)][len(self.piles[self.pile_mat_list.index(pile)])-1].suit == "Diamonds" or self.piles[self.pile_mat_list.index(pile)][len(self.piles[self.pile_mat_list.index(pile)])-1].suit == "Hearts"):
            return(True)
        elif int(self.held_cards[0].numeric_value) + 1 == int(self.piles[self.pile_mat_list.index(pile)][len(self.piles[self.pile_mat_list.index(pile)])-1].numeric_value) and check_color == "red" and (self.piles[self.pile_mat_list.index(pile)][len(self.piles[self.pile_mat_list.index(pile)])-1].suit == "Spades" or self.piles[self.pile_mat_list.index(pile)][len(self.piles[self.pile_mat_list.index(pile)])-1].suit == "Clubs"):
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
                    #print("pinossa on " + str(len(self.piles[pile_index])))
                    top_card = self.piles[pile_index][-1]
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = top_card.center_x, \
                                                top_card.center_y - const.CARD_VERTICAL_OFFSET * (1*(i+1))
                    #print(dropped_card.position)
                 

                else:
                    #print("pino on tyhjä")
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = pile.center_x, \
                                                SCREEN_HEIGHT - const.MAT_HEIGHT - const.X_SPACING - const.CARD_VERTICAL_OFFSET * i
                                                 
                        print(dropped_card.position)

                for card in self.held_cards:
                    self.move_card_to_new_pile(card,pile_index)

               
                reset_position = False          # if successful


            elif const.TOP_PILE_1 <= pile_index <= const.TOP_PILE_4 and len(self.held_cards) == 1 and self.check_top_move_rules(pile) == True:
                self.held_cards[0].position = pile.position
                for card in self.held_cards:
                    self.move_card_to_new_pile(card, pile_index)
                    
                    
                
                reset_position = False          # if successful
        
        if reset_position:
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]
        else:
            self.moves +=1
            print(self.moves)

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

   
        
class MenuView(arcade.View): 
    def __init__(self): 
        super().__init__()
        self.menu_background = arcade.load_texture(const.MENU_BACKGROUND_IMAGE)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
       
        centering_widget = arcade.gui.UIAnchorLayout(
        anchor_x="center_x",
        anchor_y="top"
        )

        v_box = arcade.gui.UIBoxLayout(
        vertical=True,
        padding=(350, 100, 100, 100),
        align_items="center",
        size_hint=(1.0, None),
        height=SCREEN_HEIGHT-300
        )
        
        menu_title = arcade.gui.UILabel(text="SOLITAIRE",
                                              width=450,
                                              height=130,
                                              font_size=50,
                                              align="center",
                                              font_name="Kenney Future"
                                              )

        

        start_button = arcade.gui.UIFlatButton(
            text="START",
            width=200,
            height=60
        )
        settings_button = arcade.gui.UIFlatButton(
            text="SETTINGS",
            width=200,
            height=60
        )
        quit_button = arcade.gui.UIFlatButton(
            text="QUIT",
            width=200,
            height=50
        )
        
        v_box.add(menu_title.with_padding(bottom=10))
        v_box.add(start_button.with_padding(bottom=10))
        v_box.add(settings_button.with_padding(bottom=10))
        v_box.add(quit_button)

        centering_widget.add(v_box)

        self.manager.add(centering_widget)
        

        @start_button.event("on_click")
        def on_click_start_button(event):
            self.clear()
            self.manager.clear()
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        @settings_button.event("on_click")
        def on_click_start_button(event):
            self.scene = SCENE_SETTINGS

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            arcade.close_window()
            

    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.menu_background)
        self.manager.draw()
        



def main():
    window = arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
    start_view = MenuView()
    window.show_view(start_view)
    arcade.run()

if __name__== "__main__":
    main()




