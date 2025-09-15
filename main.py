import argparse
import r6
import sys
import json
import random

from os import path

def main(args):
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

    if args.optype == "attacker":
        pass
    elif args.optype == "defender":
        random_operator = r6._util.random_kvp_from_dict(defenders)[0]
        operator = r6.Operator.get(random_operator)
        print(f'selected operator: {operator}')
        print(f'operator: {json.dumps(operator, indent=4)}')
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
    main(args)
