### IMPORT STUFF ###
import random
import time
from field_of_reeds_variables import field_of_reeds_variables
from field_of_reeds_text import field_of_reeds_text



### FUNCTIONS ###



##### GAMEPLAY FUNCTIONS ####################################################

def menu_pick():
    """Takes user input, returns user input"""
    return raw_input("What would you like to do? > ").upper()

def show_menu():
    """Show main menu, collect user's choice, return choice"""
    print """\n\nAVAILABLE ACTIONS:
    A) Live Your Life
    B) Visit the Temple
    C) Visit the Bazaar
    D) Find Work
    E) Check Deben Balance
    """
    return menu_pick()

def game_play(field_of_reeds_text, field_of_reeds_variables):
    """While loop that runs until player's character dies, continuously serves 
    main menu, prompts user for response, calls up corresponding sub-menu,
    calls functions for per-turn scorekeeping. 
    When player's character dies, exit loop"""
    while field_of_reeds_variables["mwt"] <= 100:
        menu_choice = show_menu()
        if menu_choice == "A":
            live_your_life(field_of_reeds_text, field_of_reeds_variables)
        elif menu_choice == "B":
            temple_menu(field_of_reeds_variables)
        elif menu_choice == "C":
            if ok_to_shop(field_of_reeds_variables):
                bazaar_menu(field_of_reeds_variables)
            else:
                print """\n\nSlow down, big spender! You've shopped a lot lately, come back later."""
        elif menu_choice == "D":
            labor_menu(field_of_reeds_variables)
        elif menu_choice == "E":
            deben_print(field_of_reeds_variables)
        else:
            deben_punish(field_of_reeds_variables)
        mwt_score(field_of_reeds_variables)
        random_bad(field_of_reeds_variables)
        field_of_reeds_variables["total_turns"] += 1
        print
        print field_of_reeds_text["text_dividers"]["small_divider"]



##### EVALUATE AVAILABILITY FUNCTIONS #######################################

def money_check(field_of_reeds_variables, price):
    """checks if user has enough deben to buy selected item, returns true or false"""
    if field_of_reeds_variables["deben"] >= price:
        return True
    else:
        return False
        
def ok_to_pray(field_of_reeds_variables):
    """evaluates availability of prayer action; 
    returns true if prayer is available, returns false if not available"""
    if field_of_reeds_variables["prayer_times"] < 5:
        field_of_reeds_variables["prayer_times"] += 1
        field_of_reeds_variables["prayer_compare_times"] = field_of_reeds_variables["total_turns"]
        return True
    else:
        if field_of_reeds_variables["total_turns"] - field_of_reeds_variables["prayer_compare_times"] >= 15:
            field_of_reeds_variables["prayer_times"] = 1
            return True
        else:
            return False

def ok_to_shop(field_of_reeds_variables):
    """evaluates availability of shopping action; 
    returns true if shopping is available, returns false if not available"""
    if field_of_reeds_variables["shopping_times"] < 5:
        field_of_reeds_variables["shopping_times"] += 1
        field_of_reeds_variables["shopping_compare_times"] = field_of_reeds_variables["total_turns"]
        return True
    else:
        if field_of_reeds_variables["total_turns"] - field_of_reeds_variables["shopping_compare_times"] >= 15:
            field_of_reeds_variables["shopping_times"] = 1
            return True
        else:
            return False

def ok_to_field(field_of_reeds_variables):
    """evaluates availability of field labor action; 
    returns true if field labor is available, returns false if not available"""
    if field_of_reeds_variables["field_times"] < 4:
        field_of_reeds_variables["field_times"] += 1
        field_of_reeds_variables["field_compare_times"] = field_of_reeds_variables["total_turns"]
        return True
    else:
        if field_of_reeds_variables["total_turns"] - field_of_reeds_variables["field_compare_times"] >= 10:
            field_of_reeds_variables["field_times"] = 1
            return True
        else:
            return False

def ok_to_corvee(field_of_reeds_variables):
    """evaluates availability of corvee labor action; 
    returns true if corvee labor is available, returns false if not available"""
    if field_of_reeds_variables["corvee_times"] < 2:
        field_of_reeds_variables["corvee_times"] += 1
        field_of_reeds_variables["corvee_compare_times"] = field_of_reeds_variables["total_turns"]
        return True
    else:
        if field_of_reeds_variables["total_turns"] - field_of_reeds_variables["corvee_compare_times"] >= 15:
            field_of_reeds_variables["corvee_times"] = 1
            return True
        else:
            return False



##### SCOREKEEPING FUNCTIONS ################################################

def deben_print(field_of_reeds_variables):
    """Print's the user's current deben balance"""
    print "\n\nYour current deben balance is {}.".format(field_of_reeds_variables["deben"])

def deben_score(field_of_reeds_variables, field_of_reeds_text, scenario_number, user_choice):
    """Looks up deben value corresponding to a scenario choice, 
    adds correct # of deben to DEBEN score, updates DEBEN score in dictionary"""
    field_of_reeds_variables["deben"] += field_of_reeds_text["life_scenarios"][scenario_number]["deben_" + user_choice]

def deben_punish(field_of_reeds_variables):
    """If player is disobedient to the gods (gives invalid answers), 
    player is punished by having DEBEN score reduced & MAAT_BAD score incremented"""
    print "\nThat is not a valid choice. Thoth sees your disobedience to the gods. \nYou forfeit 25 deben."
    field_of_reeds_variables["deben"] += -25
    field_of_reeds_variables["maat_bad"] += 10

def update_score(field_of_reeds_variables, score_name, amount):
    """Takes in name of score to update, adds new value (can be negative 
    if score is being penalized), updates value in dictionary"""
    field_of_reeds_variables[score_name] += amount

def mwt_score(field_of_reeds_variables):
    """randomly generate a number 2-8, add generated number to MWT score, 
    updates MWT score in dictionary"""
    rand_num = random.randint(2,8)
    field_of_reeds_variables["mwt"] += rand_num

def determine_maat_value(field_of_reeds_variables, field_of_reeds_text, scenario_number, user_choice):
    """Checks whether user's choice is good, neutral, or bad; 
    calls appropriate score updating function"""
    if field_of_reeds_text["life_scenarios"][scenario_number]["maat_" + user_choice] == "good":
        update_score(field_of_reeds_variables, "maat_good", 10)
    elif field_of_reeds_text["life_scenarios"][scenario_number]["maat_" + user_choice] == "meh":
        update_score(field_of_reeds_variables, "maat_meh", 10)
    else:
        update_score(field_of_reeds_variables, "maat_bad", 20)
        
def judge_scores(field_of_reeds_variables, deben, maat_good, maat_meh, maat_bad):
    """Evaluates player score, determines if player wins or loses"""
    if maat_good > deben:
        if maat_good > maat_bad:
            pure_win_print(field_of_reeds_text)
        else:
            if (maat_good + deben/200) >= maat_bad:
                conditional_win_print(field_of_reeds_text)
            else:
                lose_print(field_of_reeds_text)
    else:
        if (maat_good + deben/200) > (maat_bad + maat_meh):
            conditional_win_print(field_of_reeds_text)
        else:
            lose_print(field_of_reeds_text)

def random_bad(field_of_reeds_variables):
    """Rolls a random number; if divisible by 4, increments MAAT_BAD score by 5"""
    rand_num = random.randint(1, 100)
    if rand_num % 4 == 0:
        update_score(field_of_reeds_variables, "maat_bad", 5)
    else:
        pass



##### TEMPLE FUNCTIONS ######################################################

def deity_picker(field_of_reeds_variables):
    """randomly selects a deity from a pool of deities. returns deity."""
    deity_num = random.randint(0,len(field_of_reeds_variables["deities"]) - 1)
    return field_of_reeds_variables["deities"][deity_num]

             
def offering_options(field_of_reeds_variables, set_price):
    """provides random options of items to offer at the temple"""
    
    offerings_set = set_price + "_offerings"                        
    return random.choice(field_of_reeds_variables[offerings_set].keys())


def make_offering():
    """presents options of offerings to buy"""
    cheap = offering_options(field_of_reeds_variables, "cheap")
    cheap_price = field_of_reeds_variables["cheap_offerings"][cheap]
    fancy = offering_options(field_of_reeds_variables, "fancy")
    fancy_price = field_of_reeds_variables["fancy_offerings"][fancy]
    
    print """\n\nOFFERINGS AVAILABLE TODAY:
    A. {} [{} deben]
    B. {} [{} deben]
    C. None of these.\n\n""".format(cheap, cheap_price, fancy, fancy_price)
    
    menu_choice = menu_pick()
    
    if menu_choice == "A":
        print "\n\nCongratulations, you have chosen to pay homage to the gods by offering {}. Your gift has been accepted by the temple, and {} deben have been subtracted from your balance.".format(cheap, cheap_price)
        update_score(field_of_reeds_variables, "deben", cheap_price * -1)
        update_score(field_of_reeds_variables, "mwt", -2)
        update_score(field_of_reeds_variables, "maat_good", 1)
    elif menu_choice == "B":
        print "\n\nCongratulations, you have chosen to pay homage to the gods by offering {}. Your gift has been accepted by the temple, and {} deben have been subtracted from your balance.".format(fancy, fancy_price)
        update_score(field_of_reeds_variables, "deben", fancy_price * -1)
        update_score(field_of_reeds_variables, "mwt", -5)
        update_score(field_of_reeds_variables, "maat_good", 2)
    elif menu_choice == "C":
        pass
    else:
        deben_punish(field_of_reeds_variables)
 
def temple_menu(field_of_reeds_variables):
    """Shows text of visiting temple, displays menu of options"""
    deity = deity_picker(field_of_reeds_variables)
    print "\n\nYou walk down to the shore, down the lane shaded by palm trees, to the imposing Temple of {}.".format(deity)
    print """\nAVAILABLE ACTIONS:
    A. Pray
    B. Make an offering
    C. Go Back
    """
    menu_choice = menu_pick()
                            
    if menu_choice == "A":
        if ok_to_pray(field_of_reeds_variables) == True:
            print "\n\nYou approach the Chapel of the Hearing Ear at the side of the temple of {} and say a quick prayer. The gods see and appreciate your piety.".format(deity)
            field_of_reeds_variables["maat_good"] += 1
        else:
            print "\n\nYou have prayed enough for now. A pious life is not lived only at the temple! Come back later."
    elif menu_choice == "B":
        if field_of_reeds_variables["deben"] >= 200:
            make_offering()
        else:
            print "\n\nSorry, you don't have enough deben to make an offering today. Try again later."
    elif menu_choice == "C":
        pass
    else:
        deben_punish(field_of_reeds_variables)



##### BAZAAR FUNCTIONS ######################################################

def shopping_options(field_of_reeds_variables, category):
    """randomly selects an option of item to buy from a pool of items 
    corresponding with the requested category. Returns item."""
    return random.choice(field_of_reeds_variables["shopping"][category].keys())

def shopping_prompt(field_of_reeds_variables, shopping_pick, price):
    """takes arguments of previously selected shopping item & price; 
    prompts user to buy. Takes user input on choice to make purchase; 
    checks if user can afford the purchase, and if so will recalculate deben balance"""
    print """\nThe item for sale today is {}. [{} deben]\n
    OPTIONS: 
    A. Buy it.
    B. Don't buy it.\n\n""".format(shopping_pick, price)
    menu_choice = menu_pick()
    
    if menu_choice == "A":
        affordable = money_check(field_of_reeds_variables, price)
        if affordable == True:
            field_of_reeds_variables["deben"] = field_of_reeds_variables["deben"] - price
            print "\nYou have successfully purchased {}.".format(shopping_pick)
            update_score(field_of_reeds_variables, "maat_meh", 5)
        else:
            print "\nYou don't have enough deben to buy that now. Come back later."
    elif menu_choice == "B":
        pass
    else:
        deben_punish(field_of_reeds_variables)

def bazaar_menu(field_of_reeds_variables):
    """Shows text of visiting bazaar, displays menu of options & 
    executes actions based on user choice"""
    print "\n\nWelcome to the bazaar! In the bustling town of Men-Nefer, merchants have something new to offer every day!"
    print """\nAVAILABLE ACTIONS:
    A. Buy Some Food
    B. Buy Something to Wear
    C. Buy Something Fancy
    D. Go Back
    """
    menu_choice = menu_pick()
    
    if menu_choice == "A":
        shopping_pick = shopping_options(field_of_reeds_variables, "food")
        price = field_of_reeds_variables["shopping"]["food"][shopping_pick]
        shopping_prompt(field_of_reeds_variables, shopping_pick, price)
    elif menu_choice == "B":
        shopping_pick = shopping_options(field_of_reeds_variables, "clothes")
        price = field_of_reeds_variables["shopping"]["clothes"][shopping_pick]
        shopping_prompt(field_of_reeds_variables, shopping_pick, price)    
    elif menu_choice == "C":
        shopping_pick = shopping_options(field_of_reeds_variables, "luxury")
        price = field_of_reeds_variables["shopping"]["luxury"][shopping_pick]
        shopping_prompt(field_of_reeds_variables, shopping_pick, price)    
    elif menu_choice == "D":
        pass
    else:
        deben_punish(field_of_reeds_variables)



##### WORK/LABOR FUNCTIONS ##################################################

def labor_menu(field_of_reeds_variables):
    """Shows text of looking for work, displays menu of options & 
    executes actions based on user choice"""
    print "\n\nYou ask around to see what work opportunities are available."
    print """\nAVAILABLE ACTIONS:
    A. Work in the Fields
    B. Do Corvee Labor (Pay your Taxes with Work Hours)
    C. Go Back
    """
    menu_choice = menu_pick()
    
    if menu_choice == "A":
        if ok_to_field(field_of_reeds_variables) == True:
            print "\n\nThe land of KMT is bountiful and the farmers always need a little extra help with their harvest. You earn 50 deben."
            field_of_reeds_variables["deben"] += 50
        else:
            print "\n\nThe annual flood has begun, and the farmers don't require any help just now. Check again later."
    elif menu_choice == "B":
        if ok_to_corvee(field_of_reeds_variables) == True:
            print "\n\nEvery year Pharaoh demands a set number of days of labor from every able-bodied worker to help Him construct His great works.\nYou are sent to help build His Mansion of Millions of Years. You earn 100 deben."
            field_of_reeds_variables["deben"] += 100
        else:
            print "\n\nYou have already devoted enough time to Pharaoh's great works. Come back later."
    elif menu_choice == "C":
        pass
    else:
        deben_punish(field_of_reeds_variables)



##### SCENARIO FUNCTIONS ####################################################

def live_your_life(field_of_reeds_text, field_of_reeds_variables):
    """Serves player a random scenario, prompts them to make a choice of what to do. 
    Serves the corresponding outcome & updates all scores"""
    print field_of_reeds_text["text_dividers"]["small_divider"]
    scenario_number = "scenario" + str(random.randint(1, len(field_of_reeds_text["life_scenarios"])))
    print field_of_reeds_text["life_scenarios"][scenario_number]["text"]
    print """\nWhat would you like to do?
    A. {}
    B. {}
    C. {}""".format(
    field_of_reeds_text["life_scenarios"][scenario_number]["short_text_A"],
    field_of_reeds_text["life_scenarios"][scenario_number]["short_text_B"],
    field_of_reeds_text["life_scenarios"][scenario_number]["short_text_C"]
    )
    user_choice = raw_input("\n> ").upper()
    time.sleep(1)
        
    if user_choice not in "ABC" or len(user_choice) > 1:
        deben_punish(field_of_reeds_variables)

    else:
        if user_choice == "A":
            print "\n" + field_of_reeds_text["life_scenarios"][scenario_number]["text_A"]
        elif user_choice == "B":
            print "\n" + field_of_reeds_text["life_scenarios"][scenario_number]["text_B"]
        elif user_choice == "C":
            print "\n" + field_of_reeds_text["life_scenarios"][scenario_number]["text_C"]
                
        deben_score(field_of_reeds_variables, field_of_reeds_text, scenario_number, user_choice)
        determine_maat_value(field_of_reeds_variables, field_of_reeds_text, scenario_number, user_choice)

    raw_input("\n\nPRESS ENTER TO CONTINUE >>> ")



##### GAMETEXT FUNCTIONS ####################################################

def get_player_name():
    """Asks for player's name, returns name"""
    print "What is your name?"
    return raw_input("> ")

def sleepdots_x(num_times):
    """Invokes time.sleep and prints 3 dots, repeats the number of times in parameter. 
    Assists with timing of dramatic scenes."""
    for i in range(num_times):
        time.sleep(1)
        print "..."

def pure_win_print(field_of_reeds_text):
    """Prints text of 100% pure win scenario! good job!"""
    print insert_dotformat("end_text","pure_win_text")
    
def conditional_win_print(field_of_reeds_text):
    """Prints text of conditional win, in which player must pay all deben to the gods. 
    Ok I guess."""
    print insert_dotformat("end_text","conditional_win_text")

def lose_print(field_of_reeds_text):
    """Prints text of LOSE scenario. 
    Too bad, so sad, should have lived a more virtuous life!"""
    print insert_dotformat("end_text","conditional_win_text")
        
def judgement_day(field_of_reeds_text):
    """After game_play loop ends and player's character dies, prints judgement scenario. 
    Calls function to evaluate scores."""
    
    print field_of_reeds_text["text_dividers"]["big_divider"]
    print field_of_reeds_text["end_text"]["death_scene"]
    raw_input("PRESS ENTER TO CONTINUE >>> ")
    print "\n\n"
    sleepdots_x(3)
    print field_of_reeds_text["text_dividers"]["big_divider"]
    print insert_dotformat("end_text","judgement_scene_1")
    raw_input("PRESS ENTER TO CONTINUE >>> ")
    
    print insert_dotformat("end_text","judgement_scene_2")
    print field_of_reeds_text["end_text"]["anubis"]
    print
    raw_input("PRESS ENTER TO CONTINUE >>> ")
    print "\n\n"
    sleepdots_x(3)
    time.sleep(1)
    print "\n\n"
    
    judge_scores(field_of_reeds_variables, field_of_reeds_variables["deben"], field_of_reeds_variables["maat_good"], field_of_reeds_variables["maat_meh"], field_of_reeds_variables["maat_bad"])

def intro_text(field_of_reeds_text):
    """print intro text & credits"""
    print field_of_reeds_text["start_text"]["intro_ascii"]
    print field_of_reeds_text["start_text"]["intro_credits"]
    raw_input("PRESS ENTER TO BEGIN >>> ")
    print "\n\n"
    sleepdots_x(3)
    time.sleep(1)
    print
    field_of_reeds_variables["player_name"] = get_player_name().title()
    print
    sleepdots_x(3)
    print field_of_reeds_text["text_dividers"]["big_divider"]
    print insert_dotformat("start_text","intro_user_backstory")
    raw_input("PRESS ENTER TO CONTINUE >>> ")
    print 

def insert_dotformat(key_name1, key_name2):
    """Allows .format to be used on text from one dictionary using 
    variables from another dictionary"""
    
    return field_of_reeds_text[key_name1][key_name2].format(
        player_name = field_of_reeds_variables["player_name"],
        deben = str(field_of_reeds_variables["deben"])
        )




### GAME PLAY STARTS HERE ###

intro_text(field_of_reeds_text)
game_play(field_of_reeds_text, field_of_reeds_variables)
judgement_day(field_of_reeds_text)