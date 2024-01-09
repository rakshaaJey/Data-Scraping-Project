# Imports
import urllib3
from bs4 import BeautifulSoup
import constants
import time

class Case:
    def __init__(self, name, price, num_mil_spec_grade = 0, num_restricted = 0, num_classified = 0, num_covert = 0, 
                    weapon_list = []):
        """
        @param name represents the name of the case
        @param price represents the price of the case
        @param num_mil_spec_grade represents the number of weapons in the case that have a rarity of mil spec grade
        @param num_restricted represents the number of weapons in the case that have a rarity of restricted
        @param num_classified represents the number of weapons in the case that have a rarity of classified
        @param num_covert represents the number of weapons in the case that have a rarity of covert
        @param weapon_list represents a list of weapons you can get in the case
        """

        self.num_mil_spec_grade = num_mil_spec_grade
        self.num_restricted = num_restricted
        self.num_classified = num_classified
        self.num_covert = num_covert
        self.name = name
        self.price = price
        self.weapon_list = weapon_list

    def __str__(self):
        return f"{self.name} - " + '${:,.2f}'.format(self.price)
    
    def get_name(self):
        """ get_name() retuns the name of the case
        """
        return self.name
    
    def get_price(self):
        """ get_price() returns the price of the case
        """
        return self.price   
    
    def get_num_mil_spec_grade(self):
        """ get_num_mil_spec_grade() returns the number of mil spec grade weapons you can get from the case
        """
        return self.num_mil_spec_grade  

    def get_num_restricted(self):
        """ get_num_restricted() returns the number of restricted weapons you can get from the case
        """
        return self.num_restricted 

    def get_num_classified(self):
        """ get_num_classified() returns the number of classified weapons you can get from the case
        """
        return self.num_classified 
    
    def get_num_covert(self):
        """ get_num_covert() returns the number of covert weapons you can get from the case
        """
        return self.num_covert
    
    def get_weapon_list(self):
        """ get_weapon_list() returns the list of weapons that you can get from the case
        """
        return self.weapon_list   
    
    def set_name(self, new_name):
        """ set_name(new_name) sets the name of the weapon case to new_name

        @param new_name is the new name of the case
        """
        self.name = new_name
    
    def set_price(self, new_price):
        """ set_price(new_price) sets the price of the case to new_price

        @param new_price is the new price of the case
        """
        self.price = new_price

    def set_weapon_list(self, new_weapon_list):
        """ set_weapon_list() sets the list of weapons to new_weapon_list

        @param new_weapon_list is the new list of weapons for the case
        """
        self.weapon_list = new_weapon_list   
    

class Weapon:

    WEARS = (constants.BATTLE_SCARRED, constants.WELL_WORN, constants.FIELD_TESTED, 
                constants.MIN_WEAR, constants.FAC_NEW)
    STATTRAK = (True, False)
    RARITIES = (None, constants.MIL_SPEC_GRADE, constants.RESTRICTED, constants.CLASSIFIED,
                    constants.COVERT, constants.EXCEEDINGLY_RARE)

    def __init__(self, name, is_stat_trak, wear, price, rarity = None):
        """
        @param name represents the name of the skin
        @param is_stat_trak represents whether or not the skin is stat_track or not
        @param wear represents the wear of the skin
        @param price represents the price of the skin
        @param rarity represents the rarity of the skin
        """

        if wear not in self.WEARS:
            raise ValueError ("%s is not a valid wear." % wear)
        if is_stat_trak != True and is_stat_trak != False:
            raise TypeError ("is_stat_trak takes in Boolean values")
        if rarity not in self.RARITIES:
            raise ValueError ("%s is not a valid rarity." % rarity)

        self.name = name
        self.is_stat_trak = is_stat_trak
        self.wear = wear
        self.price = price
        self.rarity = rarity

    def __str__(self):
        if(self.is_stat_trak):
            return f"StatTrak™ {self.name} ({self.wear}) - " + '${:,.2f}'.format(self.price)
        else: 
            return f"{self.name} ({self.wear}) - " + '${:,.2f}'.format(self.price)
    
    def __repr__(self):
        return str(self)
        
    def get_name(self):
        """ get_name() retuns the name of the skin
        """
        return self.name
    
    def get_is_stat_trak(self):
        """ get_is_stat_trak() returns whether or not the skin is stattrak
        """
        return self.is_stat_trak
    
    def get_wear(self):
        """ get_wear() returns the wear of the skin
        """
        return self.wear
    
    def get_price(self):
        """ get_price() returns the price of the skin
        """
        return self.price   
    
    def get_rarity(self):
        """ get_rarity() returns the rarity of the skin
        """
        return self.rarity
    
    def set_name(self, new_name):
        """ set_name(new_name) sets the name of the weapon skin to new_name

        @param new_name is the new name of the skin
        """
        self.name = new_name
    
    def set_is_stat_trak(self, new_is_stat_trak):
        """set_is_stat_trak(new_is_stat_trak) sets whether or not the skin is stattrack to 
        new_is_stat_trak

        @param new_is_stat_trak is the new determinant if the weapon is stattrak or not
        """
        self.is_stat_trak = new_is_stat_trak

    def set_wear(self, new_wear):
        """ set_wear(new_wear) sets the wear of the weapon skin to new_wear

        @param new_wear is the new wear of the skin
        """
        self.wear = new_wear
    
    def set_price(self, new_price):
        """ set_price(new_price) sets the price of the weapon skin to new_price

        @param new_price is the new price of the skin
        """
        self.price = new_price
        
    def set_rarity(self, new_rarity):
        """ set_rarity(new_rarity) sets the rarity of the weapon skin to new_rarity

        @param new_rarity is the new rarity of the skin
        """
        self.rarity = new_rarity
    
def extract_data_from_html(data_string: str) -> str:
    """ extract_data_from_html(data_string) takes in a string containing either the prices of the 
    weapon skins or the names of the weapon skins and returns an array of strings containing just the 
    skin names or the skin prices

    @param data_string an html string that contains data that we want (price or skin name) but 
    is muddied with tags
    """
    inside_tag = True
    current_data = ''
    data_list = []
    for x in data_string: 
        if x == "<":
            inside_tag = True
        elif x == ">":
            inside_tag = False
        elif inside_tag == False and x != '[' and x != ']' and x != ',':
            current_data = current_data + x
        elif x == ",":
            if len(data_list) != 0:
                current_data = current_data[1:]
            data_list.append(current_data)
            current_data = ''
    if(current_data != ''):
        data_list.append(current_data[1:])
    return data_list

def name_to_url(weapon_name: str) -> str:
    """name_to_url(weapon_name) takes a weapon name and converts it into a format such that 
    when put into a url it will search the steam market place for the prices of the skin
    on a weapon model

    @param weapon_name is the name of the weapon
    """
    new_name = ''
    for x in weapon_name:
        if x == ' ':
            new_name = new_name + '+'
        elif x == '|':
            new_name = new_name + '%7C'
        elif x == '&':
            new_name = new_name + '%26'
        else: 
            new_name = new_name + x
    return new_name

def to_weapon(skin_name: str, price: str) -> Weapon:
    # Checks if the skin is StatTrack
    if constants.STATTRACK in skin_name:
        is_stattrack = True
    else: 
        is_stattrack = False
    
    # Determines weapon quality 
    if constants.BATTLE_SCARRED in skin_name:
        ware = constants.BATTLE_SCARRED
    elif constants.WELL_WORN in skin_name: 
        ware = constants.WELL_WORN
    elif constants.FIELD_TESTED in skin_name:
        ware = constants.FIELD_TESTED
    elif constants.MIN_WEAR in skin_name:
        ware = constants.MIN_WEAR
    else:
        ware = constants.FAC_NEW
    
    # Determines weapon price
    price = price.replace(' USD', '').replace('$', '')

    # Determines weapon name
    skin_name = skin_name.replace('StatTrak™ ','').replace(' (' + ware + ')', '')
    
    return Weapon(skin_name, is_stattrack, ware, float(price))

def get_weapon_data(skin: str, rarity: str) -> list:
    """ get_weapon_data(skin, rarity) compiles a list of the skins of different rarities, wares and prices of a 
    selected skin line

    @param skin is the name of the skin
    @param rarity is the rarity of the skin
    """

    # Gets the link to the steam page containing the listing for the weapon skins
    time.sleep(constants.WAIT_TIME)
    resp = urllib3.request("GET", "https://steamcommunity.com/market/search?appid=730&q="+ name_to_url(skin))

    soup = BeautifulSoup(resp.data, 'html.parser')
    soup.prettify()

    # Retrieves the parts of the HTML source code that contain the data for the skin names and prices
    price_data = soup.find_all("span", attrs={"data-currency": "1"})
    name_data = soup.find_all("span", attrs={"class": "market_listing_item_name"})
    
    price = str(price_data)
    name = str(name_data)

    price_list = extract_data_from_html(price)
    name_list = extract_data_from_html(name)

    x = 0
    weapon_list = []
    while x < len(price_list):
        weapon_list.append(to_weapon(name_list[x], price_list[x]))
        to_weapon(name_list[x], price_list[x])
        weapon_list[x].set_rarity(rarity)
        x = x + 1
        
        if not weapon_list:
            get_weapon_data(skin, rarity)
            break

    return weapon_list

def get_weapon_case(case_name: str, num_mil_spec_grade: int, num_restricted: int, num_classified: int, 
                        num_covert: int) -> Case:
    """ get_weapon_case(case_name, num_mil_spec_grade, num_restricted, num_classified, num_covert) returns the
    all the data related to the case using data from the steam web page

    @param case_name represents the name of the case 
    @param num_mil_spec_grade represents the number of mil spec grade items there are in the case
    @param num_restricted represents the number of weapons in the case that have a rarity of restricted
    @param num_classified represents the number of weapons in the case that have a rarity of classified
    @param num_covert represents the number of weapons in the case that have a rarity of covert
    """
    resp = urllib3.request("GET", "https://steamcommunity.com/market/search?appid=730&q="+ name_to_url(case_name))

    soup = BeautifulSoup(resp.data, 'html.parser')
    soup.prettify()
    
    price_data = soup.find_all("span", attrs={"data-currency": "1"})

    price = str(price_data)
    price = extract_data_from_html(price)
    price = str(price).replace(' USD', '').replace('[','').replace(']','').replace('\'','')

    try:
        return Case(case_name, float(price), num_mil_spec_grade, num_restricted, num_classified, num_covert)

    except:
        time.sleep(constants.WAIT_TIME)
        get_weapon_case(case_name)

def get_case(case_name: str) -> Case:
    """ get_case(case_name) returns all data related to the case including weapon data using data from the 
    steam web page

    @param case_name is the name of the case
    """
    case_data = open("CS-GO Probabilities\Cases\\"+ case_name +".txt", "r").read()

    num_mil_spec_grade = case_data.count(constants.MIL_SPEC_GRADE)
    num_restricted = case_data.count(constants.RESTRICTED)
    num_classified = case_data.count(constants.CLASSIFIED)
    num_covert = case_data.count(constants.COVERT)

    my_case = get_weapon_case(case_name, num_mil_spec_grade, num_restricted, num_classified, num_covert)
    
    case_lines = open("CS-GO Probabilities\Cases\\"+ case_name +".txt", "r").readlines()

    for line in case_lines:
        if line.find(constants.MIL_SPEC_GRADE) != -1:
            my_item_list = get_weapon_data(line.replace(' (' + constants.MIL_SPEC_GRADE + ')',''), 
                                                constants.MIL_SPEC_GRADE)
        elif line.find(constants.RESTRICTED) != -1:
            my_item_list = get_weapon_data(line.replace(' (' + constants.RESTRICTED + ')',''), 
                                                constants.RESTRICTED)
        elif line.find(constants.CLASSIFIED) != -1:
            my_item_list = get_weapon_data(line.replace(' (' + constants.CLASSIFIED + ')',''), 
                                                constants.CLASSIFIED)
        else:
            my_item_list = get_weapon_data(line.replace(' (' + constants.COVERT + ')',''), 
                                                constants.COVERT)

        my_case.set_weapon_list(my_case.get_weapon_list() + my_item_list) 
    return my_case 

def get_case_expected_value(case: Case) -> int:
    """ def get_case_expected_value(case) returns the expected value of the return you would recive if you were
    to open the case

    @param Case represents the case in which you want to find the expected value of
    """
    expected_value = 0
    for current_weapon in case.get_weapon_list():
        probability = 1
        if current_weapon.get_ware() == constants.BATTLE_SCARRED:
            probability = probability * constants.BATTLE_SCARRED_PROBABILITY
        elif current_weapon.get_ware() == constants.WELL_WORN:
            probability = probability * constants.WELL_WORN_PROBABILITY
        elif current_weapon.get_ware() == constants.FIELD_TESTED:
            probability = probability * constants.FIELD_TESTED_PROBABILITY
        elif current_weapon.get_ware() == constants.MIN_WEAR:
            probability = probability * constants.MIN_WEAR_PROBABILITY
        else:
            probability = probability * constants.FAC_NEW_PROBABILITY
        
        if current_weapon.get_rarity() == constants.MIL_SPEC_GRADE:
            probability = probability * (constants.MIN_WEAR_PROBABILITY / case.get_num_mil_spec_grade())
        elif current_weapon.get_rarity() == constants.RESTRICTED:
            probability = probability * (constants.RESTRICTED_PROBABILITY / case.get_num_restricted())
        elif current_weapon.get_rarity() == constants.CLASSIFIED:
            probability = probability * (constants.CLASSIFIFIED_PROBABILITY / case.get_num_classified())
        else:
            probability = probability * (constants.COVERT_PROBABILITY / case.get_num_covert())
        
        if current_weapon.get_is_stat_trak():
            probability = probability * constants.STAT_TRAK_PROABILITY
        else: 
            probability = probability * (1 - constants.STAT_TRAK_PROABILITY)
        
        expected_value = expected_value + (probability * current_weapon.get_price())
    
    return expected_value