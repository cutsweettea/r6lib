"""a rainbow six siege operator information library"""
import argparse
import random
import sys
import enum
import json

from os import path

class _util:
    @staticmethod
    def random_value_from_dict(dic: dict) -> (str, str):
        """selects a random item from the given dictionary `dic`, and returns the key and value it selected"""
        r = random.randint(0, len(dic)-1)
        key = list(dic.keys())[r]
        val = dic[key]
        return key, val

    @staticmethod
    def random_value_from_list(ls: list):
        """selects a random value from the given list `ls`"""
        return ls[random.randint(0, len(ls)-1)]

    @staticmethod
    def get_scope_type(category):
        if(category == Weapon.Attachment.ScopeCategory.IRON): 
            return Weapon.Attachment.IronSights
        elif(category == Weapon.Attachment.ScopeCategory.NONMAGNIFIED): 
            return Weapon.Attachment.NonmagnifiedScope
        elif(category == Weapon.Attachment.ScopeCategory.MAGNIFIED): 
            return Weapon.Attachment.MagnifiedScope
        elif(category == Weapon.Attachment.ScopeCategory.TELESCOPIC): 
            return Weapon.Attachment.TelescopicScope
        else:
            raise TypeError(f'Value of type {type(category).__name__} for category, no valid value passed')

    @staticmethod
    def get_attachment_type(): pass

class Weapon:
    class WeaponType(enum.Enum):
        AR = "Assault rifle"
        SMG = "Submachine gun"
        LMG = "Light machine gun"
        SHOTGUN = "Shotgun"
        SLUG = "Slug"
        RIFLE = "Precision rifle"
        MP = "Machine pistol"
        HG = "Handgun"
        HC = "Hand cannon"
        SHIELD = "Shield"

    class Attachment:
        class AttachmentCategory(enum.Enum): 
            SCOPES = "Scope"
            BARRELS = "Barrel"
            GRIPS = "Grip"
            UNDERBARRELS = "Underbarrel"

        class AttachmentType: pass

        class ScopeAttachment(AttachmentType): pass

        class ScopeCategory(enum.Enum):
            IRON = "Iron"
            NONMAGNIFIED = "Nonmagnified"
            MAGNIFIED = "Magnified"
            TELESCOPIC = "Telescopic"

        class IronSights(ScopeAttachment, enum.Enum):
            IRON = "Iron sights"

        class NonmagnifiedScope(ScopeAttachment, enum.Enum):
            RED_DOT_A = "Red dot A"
            RED_DOT_B = "Red dot B"
            RED_DOT_C = "Red dot C"
            HOLO_A = "Holo A"
            HOLO_B = "Holo B"
            HOLO_C = "Holo C"
            HOLO_D = "Holo D"
            REFLEX_A = "Reflex A"
            REFLEX_B = "Reflex B"
            REFLEX_C = "Reflex C"
            REFLEX_D = "Reflex D"

        class MagnifiedScopes(ScopeAttachment, enum.Enum):
            MAGNIFIED_A = "Magnified A"
            MAGNIFIED_B = "Magnified B"
            MAGNIFIED_C = "Magnified C"

        class TelescopicScopes(ScopeAttachment, enum.Enum):
            TELESCOPIC_A = "Telescopic A"
            TELESCOPIC_B = "Telescopic B"
            TELESCOPIC_C = "Telescopic C"

        class BarrelAttachment(AttachmentType, enum.Enum):
            FLASH = "Flash hider"
            COMP = "Compensator"
            MUZZLE = "Muzzle break"
            SUPP = "Suppressor"
            EXT = "Extended barrel"
            NONE = "None"

        class GripAttachment(AttachmentType, enum.Enum):
            VERT = "Vertical grip"
            ANGLED = "Angled"
            HORI = "Horizontal"

        class UnderbarrelAttachment(AttachmentType, enum.Enum):
            LASER = "Laser sight"
            NONE = "None"

        class AttachmentModifier():
            class ModifiableWeaponAttribute(enum.Enum):
                DAMAGE = ("Damage", int)
                ADS = ("Ads time", float)
                RELOAD_SPEED = ("Reload speed", float)
                RSM = ("Run speed modifier", float)

            def __init__(self, modified_attribute: ModifiableWeaponAttribute, modifier: float | int):
                if(not isinstance(modified_attribute, self.ModifiableWeaponAttribute)):
                    raise TypeError(f'modified_attribute must be of type ModifiableWeaponAttribute, not {type(modified_attribute).__name__}')

                if(not isinstance(modifier, modified_attribute.value[1])):
                    raise TypeError(f'modifier must be of type {type(modified_attribute.value[1]).__name__} for attribute {modifier.name}, not {type(modifier).__name__}')

                self.modified_attribute = modified_attribute
                self.modifier = modifier

            def __repr__(self):
                return f"AttachmentModifier<modified_attribute={self.modified_attribute}, modifier={self.modifier}>"

        def __init__(self, attachment_category: AttachmentCategory, attachment_type: AttachmentType, *, modifiers: list[AttachmentModifier] = []):
            if(not isinstance(attachment_category, self.AttachmentCategory)):
                raise TypeError(f'attachment_category must be of type AttachmentCategory, not {type(attachment_category).__name__}')

            if(not isinstance(attachment_type, self.AttachmentType)):
                raise TypeError(f'attachment_type must be of type AttachmentType, not {type(attachment_type).__name__}') 

            for m in range(len(modifiers)):
                mod = modifiers[m]
                if(not isinstance(mod, self.AttachmentModifier)): raise TypeError(f'modifier {mod} at index {m} must be of type AttachmentModifier, not {type(mod).__name__}')

            self.attachment_category = attachment_category
            self.attachment_type = attachment_type
            self.modifiers = modifiers

        def __repr__(self):
            return f'Attachment<attachment_category={self.attachment_category}, attachment_type={self.attachment_type}, modifiers={self.modifiers}>'

        def add_modifier(self, modifier: AttachmentModifier):
            if(not isinstance(modifier, self.AttachmentModifier)): 
                raise TypeError(f'modifier ({modifier}) must be of type AttachmentModifier, not {type(modifier).__name__}')

            self.modifiers.append(modifier)

    class Destruction(enum.Enum):
        LOW = "Low"
        MED = "Medium"
        HIGH = "High"
        FULL = "Full"

    def __init__(self, weapon_type: WeaponType, damage: int, fire_rate: int, mag: int, max_mag: int, ads: float, reload_speed: float, rsm: float, destruction: Destruction, attachments: list[Attachment]):
        if(not isinstance(weapon_type, self.WeaponType)):
            raise TypeError(f'weapon_type ({weapon_type}) must be of type WeaponType, not {type(weapon_type).__name__}')
        if(not isinstance(damage, int)):
            raise TypeError(f'damage ({damage}) must be of type int, not {type(damage).__name__}')
        if(not isinstance(fire_rate, int)):
            raise TypeError(f'fire_rate ({fire_rate}) must be of type int, not {type(fire_rate).__name__}')
        if(not isinstance(mag, int)):
            raise TypeError(f'mag ({msg}) must be of type int, not {type(mag).__name__}')
        if(not isinstance(max_mag, int)):
            raise TypeError(f'max_mag ({max_mag}) must be of type int, not {type(max_mag).__name__}')
        if(not isinstance(ads, float)):
            if(isinstance(ads, int)): ads = float(ads)
            else: raise TypeError(f'ads ({ads}) must be of type float, not {type(ads).__name__}')
        if(not isinstance(reload_speed, float)):
            if(isinstance(reload_speed, int)): reload_speed = float(reload_speed)
            else: raise TypeError(f'reload_speed ({reload_speed}) must be of type float, not {type(reload_speed).__name__}')
        if(not isinstance(rsm, float)):
            if(isinstance(rsm, int)): rsm = float(rsm)
            else: raise TypeError(f'rsm ({rsm}) must be of type float, not {type(rsm).__name__}')
        if(not isinstance(destruction, self.Destruction)):
            raise TypeError(f'destruction must be Destruction, not {type(destruction).__name__}')

        if(isinstance(attachments, dict)):
            for c, d in attachments.items():
                if(not isinstance(d, list) and not isinstance(d, dict)):
                    raise TypeError(f'weapon list ({d}) must be of type list or dict, not {type(d).__name__}')

                if(isinstance(d, list)):
                    for a in range(len(d)):
                        attachment = d[a]
                        if(not isinstance(attachment, self.Attachment.AttachmentType)):
                            raise TypeError(f'attachment {attachment} at index {a} must be of type Attachment, not {type(attachment).__name__}')
                else:
                    for scope_category, scope_list in d.items():
                        if(not isinstance(scope_category, Weapon.Attachment.ScopeCategory)):
                            raise TypeError(f'scope_category ({scope_category}) must be of type ScopeCategory, not {type(scope_category).__name__}')
        else:
            raise TypeError(f'attachments must be of type list, not {type(attachments).__name__}')

        self.weapon_type = weapon_type
        self.damage = damage
        self.fire_rate = fire_rate
        self.mag = mag
        self.max_mag = max_mag
        self.ads = ads
        self.reload_speed = reload_speed
        self.rsm = rsm
        self.destruction = destruction
        self.attachments = attachments
        
    def __repr__(self): 
        return f'Weapon<weapon_type={self.weapon_type}, damage={self.damage}, fire_rate={self.fire_rate}, mag={self.mag}, max_mag={self.max_mag}, ads={self.ads}, reload_speed={self.reload_speed}, rsm={self.rsm}, destruction={self.destruction}, attachments={self.attachments}>'

class Operator:
    class OperatorType(enum.Enum):
        SENTRY = "Sentry"
        SMOKE = "Smoke"

    class Role(enum.Enum):
        INTEL = "Intel"
        AG = "Anti gadget"
        SUPP  = "Support"
        FL = "Front line"
        MP = "Map control"
        BREACH = "Breach"
        TRAP = "Trapper"
        AE = "Anti entry"
        CC = "Crowd control"

    class OperatorGadget: pass

    class AttackerGadget(OperatorGadget, enum.Enum):
        SOFT = "Breaching charge"
        CLAY = "Claymore"
        EMP = "Impact emp grenade"
        FRAG = "Frag grenade"
        HARD = "Hard breach"
        SMOKE = "Smoke grenade"
        FLASH = "Flash grenade"

    class DefenderGadget(OperatorGadget, enum.Enum):
        BARB = "Barbed wire"
        BP = "Bulletproof camera"
        DEP = "Deployable shield"
        OBV = "Observation blocker"
        IMP = "Impact grenade"
        CF = "C4"
        PROX = "Proximity alarm"

    class Ability: pass

    class AttackerAbility(Ability, enum.Enum): pass

    class DefenderAbility(Ability, enum.Enum): 
        SPECIAL = "Special"
        GAS = "Gas Grenade"

    def __init__(self, operator_type: OperatorType, roles: list[Role], difficulty: int, speed: int, health: int, ability: Ability, gadgets: list[OperatorGadget], weapons: dict):
        if(not isinstance(operator_type, Operator.OperatorType)):
            raise TypeError(f'operator_type must be of type OperatorType, not {type(operator_type).__name__}')

        if(not isinstance(roles, list)):
            raise TypeError(f'operator_type must be of type list, not {type(operator_type).__name__}')
        else:
            for r in range(len(roles)):
                role = roles[r]
                if(not isinstance(role, Operator.Role)):
                    raise TypeError(f'role at index {r} must be of type Role, not {type(role).__name__}')

        if(not isinstance(difficulty, int)):
            raise ValueError(f'difficulty must be of type int, not {type(difficulty).__name__}')
        if(not isinstance(speed, int)):
            raise ValueError(f'speed must be of type int, not {type(speed).__name__}')
        if(not isinstance(health, int)):
            raise ValueError(f'health must be of type int, not {type(health).__name__}')
        if(not isinstance(ability, Operator.Ability)):
            raise ValueError(f'ability must be of type Ability, not {type(ability).__name__}')

        if(not isinstance(gadgets, list)):
            raise TypeError(f'gadgets must be of type list, not {type(gadgets).__name__}')
        else:
            for g in range(len(gadgets)):
                gadget = gadgets[g]
                if(not isinstance(gadget, Operator.OperatorGadget)):
                    raise TypeError(f'gadget at index {g} must be of type OperatorGadget, not {type(gadget).__name__}')

        if(not isinstance(weapons, dict)):
            raise TypeError(f'weapons must be of type dict, not {type(weapons).__name__}')
        else:
            required_weapon_categories = ['primaries', 'secondaries']
            for c in required_weapon_categories:
                if c not in weapons:
                    raise ValueError(f'weapons dict doesn\'t contain required key {c}')

                weapon_list = weapons[c]
                if not isinstance(weapon_list, list):
                    raise TypeError(f'category {c}\'s value must be of type list, not {type(c).__name__}')

                for w in range(len(weapon_list)):
                    weapon = weapon_list[w]
                    if(not isinstance(weapon, Weapon)):
                        raise TypeError(f'weapon {weapon} at index {w} in {c} must be of type Weapon, not {type(weapon).__name__}')
                    

        self.operator_type = operator_type
        self.roles = roles
        self.difficulty = difficulty
        self.speed = speed
        self.health = health
        self.ability = ability
        self.gadgets = gadgets
        self.weapons = weapons

    def __repr__(self):
        return f'Operator<operator_type={self.operator_type}, roles={self.roles}, difficulty={self.difficulty}, speed={self.speed}, health={self.health}, ability={self.ability}, gadgets={self.gadgets}, weapons={self.weapons}>'

    def get_valid_modifiers(self, attachment: str, modifier_list: list):
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

    def _set_random_attachments(self, weapon_object: dict, weapon_data: dict, available_attachments: dict, *, categorize_scopes: bool = True):
        """directly sets random attachments for the `weapon_object`, using the given `weapon_data` and `available_attachments`. this function also adds modifiers to a dictionary item called 'modifiers'"""
        finished_attachments = {}
        for a in available_attachments.items():
            attachment_group = a[0]
            attachments_list = a[1]

            if isinstance(attachments_list, dict):
                # scopes
                if categorize_scopes:
                    _, attachment_group_data = _util.random_value_from_dict(attachments_list)
                    attachment = _util.random_value_from_list(attachment_group_data)
                    print(f'attachment dict for {attachment_group}: {attachment}')
                else:
                    attachments_full_list = []
                    for a in attachments_list.items():
                        attachments_full_list = attachments_full_list + a[1]
                    attachment = _util.random_value_from_list(attachments_full_list)
            elif isinstance(attachments_list, list):
                # everything but scopes
                attachment = _util.random_value_from_list(attachments_list)
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

    def generate_finished_operator(self, operators: dict, *, categorize_scopes: bool = True) -> dict:
        """this generates a random finished operator from the `operators` dictionary"""
        finished_op = {}
        op_name, op_data = _util.random_value_from_dict(operators)
        print(f'selected operator {op_name}')

        finished_op.update({"name": op_name})
        finished_op.update({"difficulty": op_data["difficulty"]})
        finished_op.update({"speed": op_data["speed"]})
        finished_op.update({"health": op_data["health"]})

        weapons = op_data["weapons"]
        primaries = weapons["primaries"]
        secondaries = weapons["secondaries"]

        print(f'operator has {len(primaries)} primaries and {len(secondaries)} secondaries')
        primary_name, primary_data = _util.random_value_from_dict(primaries)
        secondary_name, secondary_data = _util.random_value_from_dict(secondaries)

        print(f'selected primary \'{primary_name}\' and secondary \'{secondary_name}\'')
        finished_primary_data, finished_secondary_data = {}, {}
        required_weapon_values = [
            'TYPE', 'DAMAGE', 'FIRE_RATE', 'MAG', 'MAX', 'ADS', 'RELOAD_SPEED', 'RSM', 'DEST'
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
            finished_primary_attachments = _set_random_attachments(
                finished_primary_data, primary_data, attachments,
                categorize_scopes=categorize_scopes
            )
            print(f'finished primary attachments: {finished_primary_attachments}')

        if "attachments" in secondary_data:
            attachments = secondary_data["attachments"]
            finished_secondary_attachments = _set_random_attachments(
                finished_secondary_data, secondary_data, attachments,
                categorize_scopes=categorize_scopes
            )
            print(f'finished secondary attachments: {finished_secondary_attachments}')

        print(f'post-mod primary stats: {finished_primary_data}')
        print(f'post-mod secondary stats: {finished_secondary_data}')

        finished_weapons = {}
        finished_weapons.update({'primary': finished_primary_data})
        finished_weapons.update({'secondary': finished_secondary_data})
        finished_op.update({'weapons': finished_weapons})

        return finished_op

    @staticmethod
    def get(operator_type: str | OperatorType):
        if(isinstance(operator_type, str)):
            try: operator_type = OperatorType[operator_type]
            except KeyError:
                print(f'key error for key "{operator_type}" on OperatorType enum')
                return
        elif(type(operator_type) is Operator.OperatorType):
            pass
        else:
            raise TypeError(f'operator_type must be of type str or OperatorType, not {type(operator_type).__name__}')

        with open('operators.json', 'r') as f:
            categorized_operators = json.loads(f.read())
            all_operators = {}
            for c in categorized_operators:
                for n, d in categorized_operators[c].items():
                    if(n != operator_type.name): continue

                    roles = [Operator.Role[t] for t in d['type']]
                    ability = Operator.AttackerAbility[d['ability']] if c == "attacker" else Operator.DefenderAbility[d['ability']]
                    gadgets = [
                        (Operator.AttackerGadget[g] if c == "attacker" else Operator.DefenderGadget[g]) for g in d['gadgets']
                    ]

                    primaries = []
                    secondaries = []

                    primary_data = d['weapons']['primaries']
                    secondary_data = d['weapons']['secondaries']

                    for name, data in primary_data.items():
                        attachments_data = data['attachments']
                        attachment_list = {}
                        for attachment_category, attachments in attachments_data.items():
                            if(attachment_category == "scopes"): 
                                scopes = {}
                                for scope_category, scope_list in attachments.items():
                                    category = Weapon.Attachment.ScopeCategory[scope_category]
                                    scope_type = _util.get_scope_type(category)
                                    
                                    final_scopes = []
                                    mod_in_data = 'modifiers' in data
                                    for s in scope_list:
                                        attach = Weapon.Attachment(Weapon.Attachment.AttachmentCategory.SCOPES, scope_type[s])
                                        
                                        if(mod_in_data):
                                            modifiers = data['modifiers']
                                            for mc, md in modifiers.items():
                                                for mi, mv in md.items():
                                                    # TODO: make ts work rahhh
                                                    if(mi != s):
                                                        print('continue')
                                                        continue

                                                    print(f'EXECUTING: {mi}')
                                                    mv_items = list(mv.items())[0]
                                                    attr = Weapon.Attachment.AttachmentModifier.ModifiableWeaponAttribute[mv_items[0]]
                                                    #attach.add_modifier(Weapon.Attachment.AttachmentModifier(attr, mv_items[1]))

                                        print(attach)

                                    scopes.update({category: final_scopes})
                                
                                attachment_list.update({attachment_category: scopes})
                            elif(attachment_category == "barrels"):
                                attachment_list.update({attachment_category: [Weapon.Attachment.BarrelAttachment[b] for b in attachments]})
                            elif(attachment_category == "grips"):
                                attachment_list.update({attachment_category: [Weapon.Attachment.GripAttachment[g] for g in attachments]})
                            elif(attachment_category == "underbarrels"):
                                attachment_list.update({attachment_category: [Weapon.Attachment.UnderbarrelAttachment[u] for u in attachments]})
                            else: 
                                raise ValueError(f'attachment_category has an invalid value of {attachment_category}')

                        
                        new_weapon = Weapon(
                            Weapon.WeaponType[data['TYPE']], data['DAMAGE'], data['FIRE_RATE'], data['MAG'], data['MAX'], data['ADS'], data['RELOAD'], data['RSM'], Weapon.Destruction[data['DEST']], attachment_list
                        )
                        print(new_weapon)
                    
                    weapons = {
                        'primaries': primaries,
                        'secondaries': secondaries
                    }

                    return Operator(
                        operator_type, roles, d['difficulty'], d['speed'], d['health'], ability, gadgets, weapons
                    )


def random_operator():
    Operator.get()
