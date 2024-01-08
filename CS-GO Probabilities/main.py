import constants 
import item

# main line
def get_expected_returns_on_case(case_name):
    case_data = open("CS-GO Probabilities\Cases\\"+ case_name +".txt", "r").read()

    num_mil_spec_grade = case_data.count(constants.MIL_SPEC_GRADE)
    num_restricted = case_data.count(constants.RESTRICTED)
    num_classified = case_data.count(constants.CLASSIFIED)
    num_covert = case_data.count(constants.COVERT)

    my_case = item.get_weapon_case(case_name)
    case_lines = open("CS-GO Probabilities\Cases\\"+ case_name +".txt", "r").readlines()
    for line in case_lines:
        if line.find(constants.MIL_SPEC_GRADE) != -1:
            my_item_list = item.get_weapon_data(line.replace(' (' + constants.MIL_SPEC_GRADE + ')',''), 
                                                constants.MIL_SPEC_GRADE)
        elif line.find(constants.RESTRICTED) != -1:
            my_item_list = item.get_weapon_data(line.replace(' (' + constants.RESTRICTED + ')',''), 
                                                constants.RESTRICTED)
        elif line.find(constants.CLASSIFIED) != -1:
            my_item_list = item.get_weapon_data(line.replace(' (' + constants.CLASSIFIED + ')',''), 
                                                constants.CLASSIFIED)
        else:
            my_item_list = item.get_weapon_data(line.replace(' (' + constants.COVERT + ')',''), 
                                                constants.COVERT)
        my_case.set_weapon_list = my_case.get_weapon_list + my_item_list

    expected_value = 0
    for x in my_case.set_weapon_list:
        probability = 1
        current_weapon = my_case.weapon_list[x]
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
            probability = probability * (constants.MIN_WEAR_PROBABILITY / num_mil_spec_grade)
        elif current_weapon.get_rarity() == constants.RESTRICTED:
            probability = probability * (constants.RESTRICTED_PROBABILITY / num_restricted)
        elif current_weapon.get_rarity() == constants.CLASSIFIED:
            probability = probability * (constants.CLASSIFIFIED_PROBABILITY / num_classified)
        else:
            probability = probability * (constants.COVERT_PROBABILITY / num_covert)
        
        if current_weapon.get_is_stat_trak():
            probability = probability * constants.STAT_TRAK_PROABILITY
        else: 
            probability = probability * (1 - constants.STAT_TRAK_PROABILITY)
        
        expected_value = expected_value + (probability * current_weapon.get_price())
    
    return expected_value
