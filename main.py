# attachments:
#   - scopes
#       - iron sights: IRON
#           - iron sights: IRON
#       - non magnifying: NM
#           - holo a/b/c/d: HOLO_A/B/C/D
#           - red dot a/b/c: RED_DOT_A/B/C
#           - reflex a/b/c/d: REFLEX_A/B/C/D
#       - magnified: MAG
#           - magnified a/b/c: MAGNIFIED_A/B/C
#       - telescopic: TES
#           - telescopic a/b: TELESCOPIC_A/B
#   - barrels: barrels
#       - flash hider: FLASH
#       - compensator: COMP
#       - muzzle break: MUZZLE
#       - suppressor: SUPP
#       - extended barrel: EXT
#       - none: NONE
#   - grips: grips
#       - vertical grip: VERT
#       - angled grip: ANGLED
#       - horizontal grip: HORI
#   - under barrel: underbarrels
#       - laser: LASER
#       - none: NONE
#   - gadgets: gadgets
#       - attackers: attack
#           - breach charge: BREACH
#           - claymore: CLAY
#           - impact emp grenade: EMP
#           - frag grenade: FRAG
#           - hard breach: HARD_BREACH
#           - smoke grenade: SMOKE
#           - flash grenade: FLASH
#       - defenders: defend
#           - barbed wire: BARB
#           - bulletproof camera: BP
#           - deployable shield: DEP
#           - observation blocker: OBV
#           - impact grenade: IMP
#           - c4: C4
#           - proximity alarm: PROX
# types:
#   - operator types:
#       - intel: INTEL
#       - anti-gadget: AG
#       - support: SUP
#       - front line: FL
#       - map control: MP
#       - breach: BREACH
#       - trapper: TRAP
#       - anti-entry: AE
#       - crowd control: CC
#   - weapon types:
#       - assault rifle: AR
#       - submachine gun: SMG
#       - light machine gun: LMG
#       - shotgun: SHOTGUN
#       - slug shotgun: SLUG
#       - precision rifle: RIFLE
#       - machine pistol: MP
#       - handgun: HG
#       - hand cannon: HC
#       - shield: SHIELD
# operators:
#   - sentry: SENTRY
#       - ability=! UNIQUE !
#   - smoke: SMOKE
#       - ability=remote gas grenade: GAS
# attributes:
#   - weapon attributes: 
#       - damage: DAMAGE
#       - ads time: ADS
#       - fire rate: FIRE_RATE
#       - magazine: MAG
#       - max capacitY: MAX
#       - reload speed: RELOAD
#       - run speed modifier: RSM
#       - destruction: DEST
#           - Low: LOW
#           - Medium: MED
#           - High: HIGH
#           - Full: FULL
#   - operator attributes:
#       - difficulty: difficulty
#       - speed: speed
#       - health: health
# notes:
#   - fire rate = 0 means single shot
# special options:
#   - categorize scopes when randomizing``

import argparse
import os.path as path
import json
import random

# operator stuff
argp = argparse.ArgumentParser(
    description="random operator and loadout generator for R6",
    epilog="rainbowww six siegeee"
)

argp.add_argument("-o", "--operators", help="File with operators and their data", default="operators.json", dest="ops")
argp.add_argument("-t", "--operator-type", help="Type of operator", default="operators.json", choices=["attacker", "defender"], dest="optype", required=True)

args = argp.parse_args()

def random_value_from_dict(dic: dict) -> (str, str):
    r = random.randint(0, len(dic)-1)
    key = list(dic.keys())[r]
    val = dic[key]
    return key, val

def random_value_from_list(ls: list) -> any:
    return ls[random.randint(0, len(ls)-1)]

def get_valid_modifiers(attachment: str, modifier_list: list):
    final_modifiers = {}
    for mod in modifier_list:
        modifier_data = modifier_list[mod]
        if(mod == attachment):
            print(f'! modify from {mod}')
            for v in modifier_data.items():
                key, val = v[0], v[1]
                print(f'modifying: {key}, {val}')
                final_modifiers.update({key: val})

    return final_modifiers

def set_random_attachments(weapon_object: dict, weapon_data: dict, available_attachments: dict):
    finished_attachments = {}
    for a in available_attachments.items():
        attachment_group = a[0]
        attachments_list = a[1]
        if(isinstance(attachments_list, dict)): 
            _, attachment_group_data = random_value_from_dict(attachments_list)
            attachment = random_value_from_list(attachment_group_data)
            print(f'attachment dict for {attachment_group}: {attachment}')
        elif(isinstance(attachments_list, list)): 
            attachment = random_value_from_list(attachments_list)
            print(f'attachment array for {attachment_group}: {attachment}')
        else:
            print(f'unknown attachment container type \'{type(attachments_list).__name__}\'')
            exit(1)

        finished_attachments.update({attachment_group[:-1]: attachment})
        if('modifiers' in weapon_data):
            modifiers = weapon_data['modifiers']
            for m in modifiers.keys():
                if(attachment_group != m): continue
                modifier_list = modifiers[m]
                valid_modifiers = get_valid_modifiers(attachment, modifier_list)
                for mod in valid_modifiers:
                    if('modifiers' in weapon_object): weapon_object.update({'modifiers': {}})
                    weapon_object.update({'modifiers': {mod: (valid_modifiers[mod], m, attachment)}})

    weapon_object.update({'attachments': finished_attachments})

def generate_finished_operator(operators: dict) -> dict:
    finished_op = {}
    op_name, op_data = random_value_from_dict(operators)
    print(f'selected operator {op_name}')

    finished_op.update({"name": op_name})
    finished_op.update({"difficulty": op_data["difficulty"]})
    finished_op.update({"speed": op_data["speed"]})
    finished_op.update({"health": op_data["health"]})

    weapons = op_data["weapons"]
    primaries = weapons["primaries"]
    secondaries = weapons["secondaries"]

    print(f'operator has {len(primaries)} primaries and {len(secondaries)} secondaries')
    primary_name, primary_data = random_value_from_dict(primaries)
    secondary_name, secondary_data = random_value_from_dict(secondaries)

    print(f'selected primary \'{primary_name}\' and secondary \'{secondary_name}\'')
    finished_primary_data, finished_secondary_data = {}, {}
    required_weapon_values = ['TYPE', 'DAMAGE', 'FIRE_RATE', 'MAG', 'MAX', 'ADS', 'RELOAD', 'RSM', 'DEST']
    for val in required_weapon_values:
        if(val in primary_data): finished_primary_data.update({val: primary_data[val]})
        if(val in secondary_data): finished_secondary_data.update({val: secondary_data[val]})

    print(f'pre-mod primary stats: {finished_primary_data}\npre-mod secondary stats: {finished_secondary_data}')

    if("attachments" in primary_data):
        attachments = primary_data["attachments"]
        finished_primary_attachments = set_random_attachments(finished_primary_data, primary_data, attachments)
        print(f'finished primary attachments: {finished_primary_attachments}')

    if("attachments" in secondary_data):
        attachments = secondary_data["attachments"]
        finished_secondary_attachments = set_random_attachments(finished_secondary_data, secondary_data, attachments)
        print(f'finished secondary attachments: {finished_secondary_attachments}')

    print(f'post-mod primary stats: {finished_primary_data}\npost-mod secondary stats: {finished_secondary_data}')

    finished_weapons = {}
    finished_weapons.update({'primary': finished_primary_data})
    finished_weapons.update({'secondary': finished_secondary_data})
    finished_op.update({'weapons': finished_weapons})

    return finished_op

def main():
    if(not path.exists(args.ops)):
        print(f"file '{args.ops}' doesn't exist")
        exit(1)

    with open(args.ops, 'r') as f:
        try: data = json.loads(f.read())
        except Exception as ex:
            print(f'error thrown: {type(ex).__name__}, {ex.args[0]}')
            exit(1)

    attackers = data["attack"]
    defenders = data["defend"]
    
    print(f'found {len(attackers)} attackers and {len(defenders)} defenders')
    if(args.optype == "attacker"):
        pass
    elif(args.optype == "defender"):
        op = generate_finished_operator(defenders)
        print(f'op: {json.dumps(op, indent=4)}')
    else: 
        print('no operator type found')
        exit(1)


if(__name__ == "__main__"):
    main()

