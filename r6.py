"""a rainbow six siege operator information library"""
import random
import enum
import json

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
        """gets and returns the correct ScopeAttachment enum for the given ScopeCategory"""
        if category == Weapon.Attachment.ScopeCategory.IRON: 
            return Weapon.Attachment.IronSights
        elif category == Weapon.Attachment.ScopeCategory.NONMAGNIFIED: 
            return Weapon.Attachment.NonmagnifiedScope
        elif category == Weapon.Attachment.ScopeCategory.MAGNIFIED: 
            return Weapon.Attachment.MagnifiedScope
        elif category == Weapon.Attachment.ScopeCategory.TELESCOPIC: 
            return Weapon.Attachment.TelescopicScope
        else:
            raise TypeError(f'Value of type {type(category).__name__} for category, no valid value passed')

    @staticmethod
    def get_modifiers(data: dict, attachment_name: str):
        """gets all valid modifiers with the given attachment name"""
        modifiers = []
        for d in data.items():
            d_attach_name = d[0]
            d_data = d[1]
            #print(f'{attachment_name} ?= {d_attach_name} ({attachment_name == d_attach_name})')
            if attachment_name != d_attach_name:
                continue
            for m in d_data.items():
                modifiers.append(Weapon.Attachment.AttributeModifier(Weapon.Attachment.AttributeModifier.ModifiableWeaponAttribute[m[0]], m[1]))

        #print(f'mods for {attachment_name} has len = {len(modifiers)}')
        return modifiers


class Weapon:
    class WeaponCategory(enum.Enum):
        """class for weapon categories"""
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

    class WeaponType(enum.Enum):
        """class for weapon types"""
        COMMANDO_9 = "Commando 9"
        M870 = "M870"
        TCSG12 = "TCSG12"
        C75_AUTO = "C75 Auto"
        SUPER_SHORTY = "Super Shorty"
        M590A1 = "M590A1"
        FMG_9 = "Fmg-9"
        SMG_11 = "Smg 11"
        P226_MK_25 = "P226 Mk 25"

    class Destruction(enum.Enum):
        """enum for destruction levels"""
        LOW = "Low"
        MED = "Medium"
        HIGH = "High"
        FULL = "Full"

    class Loadout:
        """used for storing primaries and secondaries"""
        def __init__(self, primaries: list, secondaries: list):
            for p in range(len(primaries)):
                primary = primaries[p]
                if not isinstance(primary, Weapon): raise TypeError(f'Primary at index {p} must be of type Weapon, not {type(primary).__name__}')

            for p in range(len(secondaries)):
                secondary = secondaries[p]
                if not isinstance(secondary, Weapon): raise TypeError(f'Secondary at index {p} must be of type Weapon, not {type(primary).__name__}')

            self.primaries = primaries
            self.secondaries = secondaries

    class Attachment:
        """contains all classes and methods related to attachment creation and management"""
        class AttachmentCategory(enum.Enum): 
            """enum for attachment categories, with corresponding labels"""
            SCOPES = "Scope"
            BARRELS = "Barrel"
            GRIPS = "Grip"
            UNDERBARRELS = "Underbarrel"

        class AttachmentType: 
            """base class for each attachment type"""
            pass

        class ScopeAttachment(AttachmentType): 
            """base class for each scope attachment type"""
            pass

        class ScopeCategory(enum.Enum):
            """enum for scope categories, with corresponding labels"""
            IRON = "Iron"
            NONMAGNIFIED = "Nonmagnified"
            MAGNIFIED = "Magnified"
            TELESCOPIC = "Telescopic"

        class IronSights(ScopeAttachment, enum.Enum):
            """child enum of ScopeAttachment for scopes categorized as iron sights, with corresponding labels"""
            IRON = "Iron sights"

        class NonmagnifiedScope(ScopeAttachment, enum.Enum):
            """child enum of ScopeAttachment for scopes categorized as nonmagnified, with corresponding labels"""
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
            """child enum of ScopeAttachment for scopes categorized as magnified, with corresponding labels"""
            MAGNIFIED_A = "Magnified A"
            MAGNIFIED_B = "Magnified B"
            MAGNIFIED_C = "Magnified C"

        class TelescopicScopes(ScopeAttachment, enum.Enum):
            """child enum of ScopeAttachment for scopes categorized as telescopic, with corresponding labels"""
            TELESCOPIC_A = "Telescopic A"
            TELESCOPIC_B = "Telescopic B"
            TELESCOPIC_C = "Telescopic C"

        class BarrelAttachment(AttachmentType, enum.Enum):
            """child enum of AttachmentType for barrel attachments, with corresponding labels"""
            FLASH = "Flash hider"
            COMP = "Compensator"
            MUZZLE = "Muzzle break"
            SUPP = "Suppressor"
            EXT = "Extended barrel"
            NONE = "None"

        class GripAttachment(AttachmentType, enum.Enum):
            """child enum of AttachmentType for grip attachments, with corresponding labels"""
            VERT = "Vertical grip"
            ANGLED = "Angled"
            HORI = "Horizontal"

        class UnderbarrelAttachment(AttachmentType, enum.Enum):
            """child enum of AttachmentType for underbarrel attachments, with corresponding labels"""
            LASER = "Laser sight"
            NONE = "None"

        class AttributeModifier():
            """class for attribute modifiers"""
            class ModifiableWeaponAttribute(enum.Enum):
                """enum of modifiable weapon attributes, with corresponding labels and types"""
                DAMAGE = ("Damage", int)
                ADS = ("Ads time", float)
                RELOAD_SPEED = ("Reload speed", float)
                RSM = ("Run speed modifier", float)

            def __init__(self, modified_attribute: ModifiableWeaponAttribute, modifier: any):
                """constructor for AttributeModifier class"""
                if not isinstance(modified_attribute, self.ModifiableWeaponAttribute):
                    raise TypeError(f'modified_attribute must be of type ModifiableWeaponAttribute, not {type(modified_attribute).__name__}')

                expected_type = modified_attribute.value[1]
                if not isinstance(modifier, expected_type):
                    raise TypeError(f'modifier must be of type {expected_type.__name__} for attribute {modified_attribute}, not {type(modifier).__name__}')

                self.modified_attribute = modified_attribute
                self.modifier = modifier

            def __repr__(self):
                """representation of AttributeModifier class"""
                return f"AttributeModifier<modified_attribute={self.modified_attribute}, modifier={self.modifier}>"

        def __init__(self, attachment_category: AttachmentCategory, attachment_type: AttachmentType, *, modifiers: list[AttributeModifier] = []):
            """constructor for Attachment class"""

            #print(f' ^ attach creation attachment_category={attachment_category} attachment_type={attachment_type} modifiers={modifiers}')
            if not isinstance(attachment_category, self.AttachmentCategory):
                raise TypeError(f'attachment_category must be of type AttachmentCategory, not {type(attachment_category).__name__}')

            if not isinstance(attachment_type, self.AttachmentType):
                raise TypeError(f'attachment_type must be of type AttachmentType, not {type(attachment_type).__name__}') 

            #print(f' mod len: {len(modifiers)}')
            for m in range(len(modifiers)):
                mod = modifiers[m]
                if not isinstance(mod, self.AttributeModifier): raise TypeError(f'modifier {mod} at index {m} must be of type AttributeModifier, not {type(mod).__name__}')

            self.attachment_category = attachment_category
            self.attachment_type = attachment_type
            self.modifiers = modifiers

        def __repr__(self):
            """representation of Attachment class"""
            return f'Attachment<attachment_category={self.attachment_category}, attachment_type={self.attachment_type}, modifiers={self.modifiers}>'

        def add_modifier(self, modifier: AttributeModifier):
            """adds a modifier to the attachment"""
            if not isinstance(modifier, self.AttributeModifier): 
                raise TypeError(f'modifier ({modifier}) must be of type AttributeModifier, not {type(modifier).__name__}')

            #print(f' % attr mod: {modifier}')
            self.modifiers.append(modifier)

    def __init__(self, weapon_category: WeaponCategory, weapon_type: WeaponType, damage: int, fire_rate: int, mag: int, max_mag: int, ads: float, reload_speed: float, rsm: float, destruction: Destruction, attachments: list[Attachment]):
        """constructor for Weapon class"""
        if not isinstance(weapon_category, self.WeaponCategory):
            raise TypeError(f'weapon_category ({weapon_category}) must be of type WeaponCategory, not {type(weapon_category).__name__}')
        if not isinstance(weapon_type, self.WeaponType):
            raise TypeError(f'weapon_type ({weapon_type}) must be of type WeaponType, not {type(weapon_type).__name__}')
        if not isinstance(damage, int):
            raise TypeError(f'damage ({damage}) must be of type int, not {type(damage).__name__}')
        if not isinstance(fire_rate, int):
            raise TypeError(f'fire_rate ({fire_rate}) must be of type int, not {type(fire_rate).__name__}')
        if not isinstance(mag, int):
            raise TypeError(f'mag ({msg}) must be of type int, not {type(mag).__name__}')
        if not isinstance(max_mag, int):
            raise TypeError(f'max_mag ({max_mag}) must be of type int, not {type(max_mag).__name__}')
        if not isinstance(ads, float):
            if isinstance(ads, int): ads = float(ads)
            else: raise TypeError(f'ads ({ads}) must be of type float, not {type(ads).__name__}')
        if not isinstance(reload_speed, float):
            if isinstance(reload_speed, int): reload_speed = float(reload_speed)
            else: raise TypeError(f'reload_speed ({reload_speed}) must be of type float, not {type(reload_speed).__name__}')
        if not isinstance(rsm, float):
            if isinstance(rsm, int): rsm = float(rsm)
            else: raise TypeError(f'rsm ({rsm}) must be of type float, not {type(rsm).__name__}')
        if not isinstance(destruction, self.Destruction):
            raise TypeError(f'destruction must be Destruction, not {type(destruction).__name__}')

        if isinstance(attachments, dict):
            for c, d in attachments.items():
                if not isinstance(d, list) and not isinstance(d, dict):
                    raise TypeError(f'weapon list ({d}) must be of type list or dict, not {type(d).__name__}')

                if isinstance(d, list):
                    for a in range(len(d)):
                        attachment = d[a]
                        if not isinstance(attachment, self.Attachment):
                            raise TypeError(f'attachment {attachment} at index {a} must be of type Attachment, not {type(attachment).__name__}')
                else:
                    for scope_category, scope_list in d.items():
                        if not isinstance(scope_category, Weapon.Attachment.ScopeCategory):
                            raise TypeError(f'scope_category ({scope_category}) must be of type ScopeCategory, not {type(scope_category).__name__}')
        else:
            raise TypeError(f'attachments must be of type list, not {type(attachments).__name__}')

        self.weapon_category = weapon_category
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
        """representation for Weapon class"""
        return f'Weapon<weapon_category={self.weapon_category}, weapon_type={self.weapon_type}, damage={self.damage}, fire_rate={self.fire_rate}, mag={self.mag}, max_mag={self.max_mag}, ads={self.ads}, reload_speed={self.reload_speed}, rsm={self.rsm}, destruction={self.destruction}, attachments={self.attachments}>'

class Operator:
    class OperatorType:
        """parent class for operator types"""
        pass

    class AttackOperatorType(OperatorType, enum.Enum):
        """child of OperatorType class for attacker operator types, with corresponding labels"""
        pass

    class DefendOperatorType(OperatorType, enum.Enum):
        """child of OperatorType class for defender operator types, with corresponding labels"""
        SENTRY = "Sentry"
        SMOKE = "Smoke"

    class Role(enum.Enum):
        """enum for operator roles"""
        INTEL = "Intel"
        AG = "Anti gadget"
        SUPP  = "Support"
        FL = "Front line"
        MP = "Map control"
        BREACH = "Breach"
        TRAP = "Trapper"
        AE = "Anti entry"
        CC = "Crowd control"

    class OperatorGadget: 
        """parent class for operators gadgets"""
        pass

    class AttackerGadget(OperatorGadget, enum.Enum):
        """child enum of OperatorGadget for attacker gadgets, with corresponding labels"""
        SOFT = "Breaching charge"
        CLAY = "Claymore"
        EMP = "Impact emp grenade"
        FRAG = "Frag grenade"
        HARD = "Hard breach"
        SMOKE = "Smoke grenade"
        FLASH = "Flash grenade"

    class DefenderGadget(OperatorGadget, enum.Enum):
        """child enum of OperatorGadget for defender gadgets, with corresponding labels"""
        BARB = "Barbed wire"
        BP = "Bulletproof camera"
        DEP = "Deployable shield"
        OBV = "Observation blocker"
        IMP = "Impact grenade"
        CF = "C4"
        PROX = "Proximity alarm"

    class Ability: 
        """parent class for operator abilities"""
        pass

    class AttackerAbility(Ability, enum.Enum): 
        """child enum of Ability for attacher gadgets, with corresponding labels"""
        pass

    class DefenderAbility(Ability, enum.Enum): 
        """child enum of Ability for defender gadgets, with corresponding labels"""
        SPECIAL = "Special"
        GAS = "Gas Grenade"

    def __init__(self, operator_type: OperatorType, roles: list[Role], difficulty: int, speed: int, health: int, ability: Ability, gadgets: list[OperatorGadget], weapons: Weapon.Loadout):
        """constructor for Operator class"""
        if not isinstance(operator_type, Operator.OperatorType):
            raise TypeError(f'operator_type must be of type OperatorType, not {type(operator_type).__name__}')

        if not isinstance(roles, list):
            raise TypeError(f'operator_type must be of type list, not {type(operator_type).__name__}')
        else:
            for r in range(len(roles)):
                role = roles[r]
                if not isinstance(role, Operator.Role):
                    raise TypeError(f'role at index {r} must be of type Role, not {type(role).__name__}')

        if not isinstance(difficulty, int):
            raise ValueError(f'difficulty must be of type int, not {type(difficulty).__name__}')
        if not isinstance(speed, int):
            raise ValueError(f'speed must be of type int, not {type(speed).__name__}')
        if not isinstance(health, int):
            raise ValueError(f'health must be of type int, not {type(health).__name__}')
        if not isinstance(ability, Operator.Ability):
            raise ValueError(f'ability must be of type Ability, not {type(ability).__name__}')

        if not isinstance(gadgets, list):
            raise TypeError(f'gadgets must be of type list, not {type(gadgets).__name__}')
        else:
            for g in range(len(gadgets)):
                gadget = gadgets[g]
                if not isinstance(gadget, Operator.OperatorGadget):
                    raise TypeError(f'gadget at index {g} must be of type OperatorGadget, not {type(gadget).__name__}')

        if not isinstance(weapons, Weapon.Loadout):
            raise TypeError(f'weapons must be of type Loadout, not {type(weapons).__name__}')

        self.operator_type = operator_type
        self.roles = roles
        self.difficulty = difficulty
        self.speed = speed
        self.health = health
        self.ability = ability
        self.gadgets = gadgets
        self.weapons = weapons

    def __repr__(self):
        """representation for Operator class"""
        return f'Operator<operator_type={self.operator_type}, roles={self.roles}, difficulty={self.difficulty}, speed={self.speed}, health={self.health}, ability={self.ability}, gadgets={self.gadgets}, weapons={self.weapons}>'

    @staticmethod
    def load(operator_type, c, d):
        """static method for loading getting an Operator class with the operator type, operator category (attack / defend) and operator"""
        roles = [Operator.Role[t] for t in d['type']]
        ability = Operator.AttackerAbility[d['ability']] if c == "attacker" else Operator.DefenderAbility[d['ability']]
        gadgets = [
            (Operator.AttackerGadget[g] if c == "attacker" else Operator.DefenderGadget[g]) for g in d['gadgets']
        ]

        primaries = []
        secondaries = []

        primary_data = d['weapons']['primaries']
        secondary_data = d['weapons']['secondaries']
        all_weapon_data = [primary_data, secondary_data]

        for slot_index in range(len(all_weapon_data)):
            for name, data in primary_data.items():
                #print(f' # {name}')
                attachments_data = data['attachments']
                attachment_list = {}
                mod_in_data = 'modifiers' in data
                for attachment_category, attachments in attachments_data.items():
                    if attachment_category == "scopes": 
                        scopes = {}
                        for scope_category, scope_list in attachments.items():
                            category = Weapon.Attachment.ScopeCategory[scope_category]
                            scope_type = _util.get_scope_type(category)
                            
                            final_scopes = []
                            for s in scope_list:
                                #print(f's {scope_type[s]}: {s}')
                                # do not remove the modifiers=[] because all mods will be passed into constructor if not?????
                                attach = Weapon.Attachment(Weapon.Attachment.AttachmentCategory.SCOPES, scope_type[s], modifiers=[])
                                #print(f'attach-pre: {scope_category}, {s}: {attach}')
                                
                                if mod_in_data:
                                    modifier_data = data['modifiers']

                                    if attachment_category in modifier_data:
                                        modifiers = modifier_data[attachment_category]
                                        for m in _util.get_modifiers(modifiers, scope_category):
                                            attach.add_modifier(m)

                                #print(f'attach-post: {scope_category}, {s}: {attach}\n')
                                final_scopes.append(attach)

                            scopes.update({category: final_scopes})
                        
                        attachment_list.update({attachment_category: scopes})
                        #print(f'scopes: {scopes}')
                    elif attachment_category == "barrels":
                        category = Weapon.Attachment.AttachmentCategory[attachment_category.upper()]
                        barrels = []
                        for b in attachments:
                            #print(f'attachment_category={attachment_category}, type(b)={type(b).__name__}, b={b}')
                            attach = Weapon.Attachment(category, Weapon.Attachment.BarrelAttachment[b], modifiers=[])
                            if mod_in_data:
                                modifier_data = data['modifiers']

                                if attachment_category in modifier_data:
                                    modifiers = modifier_data[attachment_category]
                                    for m in _util.get_modifiers(modifiers, b):
                                        #print(f'adding {m} to {b}')
                                        attach.add_modifier(m)
                            barrels.append(attach)
                        attachment_list.update({attachment_category: barrels})
                        #print(f'barrels: {barrels}')
                    elif attachment_category == "grips":
                        category = Weapon.Attachment.AttachmentCategory[attachment_category.upper()]
                        grips = []
                        for g in attachments:
                            #print(f'attachment_category={attachment_category}, type(g)={type(g).__name__}, b={g}')

                            attach = Weapon.Attachment(category, Weapon.Attachment.GripAttachment[g], modifiers=[])
                            if mod_in_data:
                                modifier_data = data['modifiers']

                                if attachment_category in modifier_data:
                                    modifiers = modifier_data[attachment_category]
                                    for m in _util.get_modifiers(modifiers, g):
                                        #print(f'adding {m} to {g}')
                                        attach.add_modifier(m)
                            grips.append(attach)
                        attachment_list.update({attachment_category: grips})
                        #print(f'grips: {grips}')
                    elif attachment_category == "underbarrels":
                        category = Weapon.Attachment.AttachmentCategory[attachment_category.upper()]
                        grips = []
                        for u in attachments:
                            #print(f'attachment_category={attachment_category}, type(g)={type(u).__name__}, b={u}')

                            attach = Weapon.Attachment(category, Weapon.Attachment.UnderbarrelAttachment[u], modifiers=[])
                            if mod_in_data:
                                modifier_data = data['modifiers']

                                if attachment_category in modifier_data:
                                    modifiers = modifier_data[attachment_category]
                                    for m in _util.get_modifiers(modifiers, u):
                                        #print(f'adding {m} to {u}')
                                        attach.add_modifier(m)
                            grips.append(attach)
                        attachment_list.update({attachment_category: grips})
                        #print(f'grips: {grips}')
                    else: 
                        raise ValueError(f'attachment_category has an invalid value of {attachment_category}')

                new_weapon = Weapon(
                    Weapon.WeaponCategory[data['TYPE']], Weapon.WeaponType[name], data['DAMAGE'], data['FIRE_RATE'], data['MAG'], data['MAX'], data['ADS'], data['RELOAD'], data['RSM'], Weapon.Destruction[data['DEST']], attachment_list
                )
                
                if slot_index == 0: 
                    primaries.append(new_weapon)
                elif slot_index == 1: 
                    secondaries.append(new_weapon)
                else:
                    raise ValueError(f'slot_index is != 0, 1 ({slot_index})')
        
        weapons = Weapon.Loadout(primaries, secondaries)

        return Operator(
            operator_type, roles, d['difficulty'], d['speed'], d['health'], ability, gadgets, weapons
        )
        

    @staticmethod
    def get(operator_type: OperatorType):
        """static method for getting an Operator object using an OperatorType or corresponding string representation"""
        if not isinstance(operator_type, Operator.OperatorType):
            raise TypeError(f'operator_type must be of type str or OperatorType, not {type(operator_type).__name__}')

        with open('operators.json', 'r') as f:
            categorized_operators = json.loads(f.read())
            for c in categorized_operators:
                for n, d in categorized_operators[c].items():
                    if n != operator_type.name: continue

                    return Operator.load(operator_type, c, d)


def random_operator():
    """work in progress, not to random operators yet"""
    Operator.get()