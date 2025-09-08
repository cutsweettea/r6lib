"""mo"""
import argparse
import json
import random
import sys

from os import path

def random_value_from_dict(dic: dict) -> (str, str):
    """selects a random item from the given dictionary `dic`, and returns the key and value it selected"""
    r = random.randint(0, len(dic)-1)
    key = list(dic.keys())[r]
    val = dic[key]
    return key, val

def random_value_from_list(ls: list):
    """selects a random value from the given list `ls`"""
    return ls[random.randint(0, len(ls)-1)]

def get_valid_modifiers(attachment: str, modifier_list: list):
    """gets any valid modifiers for the given `attachment` from the `modifier_list`"""
    final_modifiers = {}
    for mod in modifier_list:
        modifier_data = modifier_list[mod]
        if mod == attachment:
            print(f'! modify from {mod}')
            for v in modifier_data.items():
                key, val = v[0], v[1]
                print(f'modifying: {key}, {val}')
                final_modifiers.update({key: val})

    return final_modifiers

def set_random_attachments(weapon_object: dict, weapon_data: dict, available_attachments: dict):
    """directly sets random attachments for the `weapon_object`, using the given `weapon_data` and `available_attachments`. this function also adds modifiers to a dictionary item called 'modifiers'"""
    finished_attachments = {}
    for a in available_attachments.items():
        attachment_group = a[0]
        attachments_list = a[1]

        if isinstance(attachments_list, dict):
            # scopes
            if args.categorize_scopes:
                _, attachment_group_data = random_value_from_dict(attachments_list)
                attachment = random_value_from_list(attachment_group_data)
                print(f'attachment dict for {attachment_group}: {attachment}')
            else:
                attachments_full_list = []
                for a in attachments_list.items():
                    attachments_full_list = attachments_full_list + a[1]
                attachment = random_value_from_list(attachments_full_list)
        elif isinstance(attachments_list, list):
            # everything but scopes
            attachment = random_value_from_list(attachments_list)
            print(f'attachment array for {attachment_group}: {attachment}')
        else:
            print(f'unknown attachment container type \'{type(attachments_list).__name__}\'')
            sys.exit(1)

        finished_attachments.update({attachment_group[:-1]: attachment})
        if 'modifiers' in weapon_data:
            modifiers = weapon_data['modifiers']
            for m in modifiers.keys():
                if attachment_group != m:
                    continue

                modifier_list = modifiers[m]
                valid_modifiers = get_valid_modifiers(attachment, modifier_list)
                for mod in valid_modifiers:
                    if 'modifiers' not in weapon_object:
                        weapon_object.update({'modifiers': []})

                    weapon_modifiers = weapon_object['modifiers']
                    weapon_modifiers.append({
                        'modifier': mod,
                        'value': valid_modifiers[mod],
                        'source_category': m,
                        'source_attachment': attachment
                    })

    weapon_object.update({'attachments': finished_attachments})

def generate_finished_operator(operators: dict) -> dict:
    """this generates a random finished operator from the `operators` dictionary"""
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
    required_weapon_values = [
        'TYPE', 'DAMAGE', 'FIRE_RATE', 'MAG', 'MAX', 'ADS', 'RELOAD', 'RSM', 'DEST'
    ]
    for val in required_weapon_values:
        if val in primary_data:
            finished_primary_data.update({val: primary_data[val]})
        if val in secondary_data:
            finished_secondary_data.update({val: secondary_data[val]})

    print(f'pre-mod primary stats: {finished_primary_data}')
    print(f'pre-mod secondary stats: {finished_secondary_data}')

    if "attachments" in primary_data:
        attachments = primary_data["attachments"]
        finished_primary_attachments = set_random_attachments(
            finished_primary_data, primary_data, attachments
        )
        print(f'finished primary attachments: {finished_primary_attachments}')

    if "attachments" in secondary_data:
        attachments = secondary_data["attachments"]
        finished_secondary_attachments = set_random_attachments(
            finished_secondary_data, secondary_data, attachments
        )
        print(f'finished secondary attachments: {finished_secondary_attachments}')

    print(f'post-mod primary stats: {finished_primary_data}')
    print(f'post-mod secondary stats: {finished_secondary_data}')

    finished_weapons = {}
    finished_weapons.update({'primary': finished_primary_data})
    finished_weapons.update({'secondary': finished_secondary_data})
    finished_op.update({'weapons': finished_weapons})

    return finished_op

def main():
    if not path.exists(args.ops):
        print(f"file '{args.ops}' doesn't exist")
        sys.exit(1)

    with open(args.ops, 'r') as f:
        try: data = json.loads(f.read())
        except Exception as ex:
            print(f'error thrown: {type(ex).__name__}, {ex.args[0]}')
            sys.exit(1)

    attackers = data["attack"]
    defenders = data["defend"]

    print(f'found {len(attackers)} attackers and {len(defenders)} defenders')
    if args.optype == "attacker":
        pass
    elif args.optype == "defender":
        op = generate_finished_operator(defenders)
        print(f'op: {json.dumps(op, indent=4)}')
    else:
        print('no operator type found')
        sys.exit(1)


if __name__ == "__main__":
    # argument stuff
    argp = argparse.ArgumentParser(
        description="random operator and loadout generator for R6",
        epilog="rainbowww six siegeee"
    )

    operator_group = argp.add_argument_group(
        "operator arguments", 
        "arguments related to operator selection and its data"
    )

    operator_group.add_argument(
        "-o", "--operators",
        help="File with operators and their data",
        default="operators.json",
        dest="ops"
    )
    operator_group.add_argument(
        "-t", "--operator-type",
        help="Type of operator",
        default="operators.json",
        choices=["attacker", "defender"],
        dest="optype",
        required=True
    )


    randomization_group = argp.add_argument_group(
        "randomization group",
        "arguments related to selecting a random operator"
    )

    randomization_group.add_argument(
        "-cs", "--categorize-scopes",
        help="Categorize different scopes by magnification type, and select a group of scopes randomly before selecting a single scope",
        action="store_false",
        dest="categorize_scopes"
    )

    # parse args and gooo
    args = argp.parse_args()
    main()
