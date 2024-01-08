import constants 
import item

'''
MAG-7 | Insomnia (Mil-Spec Grade)
MP9 | Featherweight (Mil-Spec Grade)
SCAR-20 | Fragments (Mil-Spec Grade)
P250 | Re.built (Mil-Spec Grade)
MP5-SD | Liquidation (Mil-Spec Grade)
SG 553 | Cyberforce (Mil-Spec Grade)
Tec-9 | Rebel (Mil-Spec Grade)
M4A1-S | Emphorosaur-S (Restricted)
Glock-18 | Umbral Rabbit (Restricted)
MAC-10 | Sakkaku (Restricted)
R8 Revolver | Banana Cannon (Restricted)
P90 | Neoqueen (Restricted)
AWP | Duality (Classified)
UMP-45 | Wild Child (Classified)
P2000 | Wicked Sick (Classified)
M4A4 | Temukau (Covert)
AK-47 | Head Shot (Covert)
'''

# main line
def get_expected_returns_on_case(case_name):
    case_file = open("CS-GO Probabilities\Cases\\"+ case_name +".txt", "r")
    case_data = case_file.read()
    case_file.close()

    num_of_items = case_data.count('\n') 
    num_mil_spec_grade = case_data.count(constants.MIL_SPEC_GRADE)
    num_restricted = case_data.count(constants.RESTRICTED)
    num_classified = case_data.count(constants.CLASSIFIED)
    num_covert = case_data.count(constants.COVERT)

    print(item.get_weapon_case(case_name))
    '''case_lines = open("CS-GO Probabilities\Cases\\"+ case_name +".txt", "r").readlines()
    for line in case_lines:
        if line.find(constants.MIL_SPEC_GRADE) != -1:
            my_item = item.get_weapon_data(line.replace(' (' + constants.MIL_SPEC_GRADE + ')',''), 
                                                constants.MIL_SPEC_GRADE)
        elif line.find(constants.RESTRICTED) != -1:
            my_item = item.get_weapon_data(line.replace(' (' + constants.RESTRICTED + ')',''), 
                                                constants.RESTRICTED)
        elif line.find(constants.CLASSIFIED) != -1:
            my_item = item.get_weapon_data(line.replace(' (' + constants.CLASSIFIED + ')',''), 
                                                constants.CLASSIFIED)
        else:
            my_item = item.get_weapon_data(line.replace(' (' + constants.COVERT + ')',''), 
                                                constants.COVERT)
        print(my_item)
    case_file.close()'''

get_expected_returns_on_case("Revolution Case")