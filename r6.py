"""a rainbow six siege operator information library"""
import random
import enum
import json
import random

class _util:
    @staticmethod
    def random_value_from_dict(dic: dict):
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
        for d_attach_name, d_data in data.items():
            #print(f'{attachment_name} ?= {d_attach_name} ({attachment_name == d_attach_name})')
            if attachment_name != d_attach_name:
                continue
            for m in d_data.items():
                modifiers.append(Weapon.ModifierManager.AttributeModifier(Weapon.ModifierManager.ModifiableWeaponAttribute[m[0]], m[1]))

        #print(f'mods for {attachment_name} has len = {len(modifiers)}')
        return modifiers
    
    @staticmethod
    def attachment_type_from_string(attachment: str):
        if not isinstance(attachment, str):
            raise TypeError(f'attachment must be of type str, not {type(attachment).__name__}')

        type_map = {
            'IRON': Weapon.Attachment.IronSights.IRON,
            'RED_DOT_A': Weapon.Attachment.NonmagnifiedScope.RED_DOT_A,
            'RED_DOT_B': Weapon.Attachment.NonmagnifiedScope.RED_DOT_B,
            'RED_DOT_C': Weapon.Attachment.NonmagnifiedScope.RED_DOT_C,
            'HOLO_A': Weapon.Attachment.NonmagnifiedScope.HOLO_A,
            'HOLO_B': Weapon.Attachment.NonmagnifiedScope.HOLO_B,
            'HOLO_C': Weapon.Attachment.NonmagnifiedScope.HOLO_C,
            'HOLO_D': Weapon.Attachment.NonmagnifiedScope.HOLO_D,
            'REFLEX_A': Weapon.Attachment.NonmagnifiedScope.REFLEX_A,
            'REFLEX_B': Weapon.Attachment.NonmagnifiedScope.REFLEX_B,
            'REFLEX_C': Weapon.Attachment.NonmagnifiedScope.REFLEX_C,
            'REFLEX_D': Weapon.Attachment.NonmagnifiedScope.REFLEX_D,
            'MAGNIFIED_A': Weapon.Attachment.MagnifiedScopes.MAGNIFIED_A,
            'MAGNIFIED_B': Weapon.Attachment.MagnifiedScopes.MAGNIFIED_B,
            'MAGNIFIED_C': Weapon.Attachment.MagnifiedScopes.MAGNIFIED_C,
            'TELESCOPIC_A': Weapon.Attachment.TelescopicScopes.TELESCOPIC_A,
            'TELESCOPIC_B': Weapon.Attachment.TelescopicScopes.TELESCOPIC_B,
            'TELESCOPIC_C': Weapon.Attachment.TelescopicScopes.TELESCOPIC_C,
            'COMP': Weapon.Attachment.BarrelAttachment.COMP,
            'EXT': Weapon.Attachment.BarrelAttachment.EXT,
            'FLASH': Weapon.Attachment.BarrelAttachment.FLASH,
            'MUZZLE': Weapon.Attachment.BarrelAttachment.MUZZLE,
            'SUPP': Weapon.Attachment.BarrelAttachment.SUPP,
            'NONE': Weapon.Attachment.BarrelAttachment.COMP,
            'ANGLED': Weapon.Attachment.GripAttachment.ANGLED,
            'HORI': Weapon.Attachment.GripAttachment.HORI,
            'VERT': Weapon.Attachment.GripAttachment.VERT,
            'LASER': Weapon.Attachment.UnderbarrelAttachment.LASER,
            'NONE': Weapon.Attachment.UnderbarrelAttachment.NONE
        }
        
        try: return type_map[attachment]
        except KeyError: return None
    
    @staticmethod
    def data_file_name():
        return 'operators.json'
    
    @staticmethod
    def get_attachment_category_from_type(attachment_type):
        if(not isinstance(attachment_type, Weapon.Attachment.AttachmentType)):
            raise TypeError(f'attachment_type must be of type AttachmentType, not {type(attachment_type).__name__}')
        
        type_map = {
            Weapon.Attachment.IronSights.IRON: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.NonmagnifiedScope.RED_DOT_A: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.NonmagnifiedScope.RED_DOT_B: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.NonmagnifiedScope.RED_DOT_C: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.NonmagnifiedScope.HOLO_A: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.NonmagnifiedScope.HOLO_B: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.NonmagnifiedScope.HOLO_C: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.NonmagnifiedScope.HOLO_D: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.NonmagnifiedScope.REFLEX_A: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.NonmagnifiedScope.REFLEX_B: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.NonmagnifiedScope.REFLEX_C: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.NonmagnifiedScope.REFLEX_D: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.MagnifiedScopes.MAGNIFIED_A: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.MagnifiedScopes.MAGNIFIED_B: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.MagnifiedScopes.MAGNIFIED_C: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.TelescopicScopes.TELESCOPIC_A: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.TelescopicScopes.TELESCOPIC_B: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.TelescopicScopes.TELESCOPIC_C: Weapon.Attachment.AttachmentCategory.SCOPES,
            Weapon.Attachment.BarrelAttachment.COMP: Weapon.Attachment.AttachmentCategory.BARRELS,
            Weapon.Attachment.BarrelAttachment.EXT: Weapon.Attachment.AttachmentCategory.BARRELS,
            Weapon.Attachment.BarrelAttachment.FLASH: Weapon.Attachment.AttachmentCategory.BARRELS,
            Weapon.Attachment.BarrelAttachment.MUZZLE: Weapon.Attachment.AttachmentCategory.BARRELS,
            Weapon.Attachment.BarrelAttachment.SUPP: Weapon.Attachment.AttachmentCategory.BARRELS,
            Weapon.Attachment.BarrelAttachment.NONE: Weapon.Attachment.AttachmentCategory.BARRELS,
            Weapon.Attachment.GripAttachment.ANGLED: Weapon.Attachment.AttachmentCategory.GRIPS,
            Weapon.Attachment.GripAttachment.HORI: Weapon.Attachment.AttachmentCategory.GRIPS,
            Weapon.Attachment.GripAttachment.VERT: Weapon.Attachment.AttachmentCategory.GRIPS,
            Weapon.Attachment.UnderbarrelAttachment.LASER: Weapon.Attachment.AttachmentCategory.UNDERBARRELS,
            Weapon.Attachment.UnderbarrelAttachment.NONE: Weapon.Attachment.AttachmentCategory.UNDERBARRELS,
        }

        return type_map[attachment_type]


class Portable:
    def export(self, **options):
        pass

    def import_from(self, data, **options):
        pass

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
        class AttachmentLoadout:
            def __init__(self, **attachments):
                self._attachments = {}
                for c, d in attachments.items():
                    category = Weapon.Attachment.AttachmentCategory[c]
                    if not isinstance(d, list) and not isinstance(d, dict):
                        raise TypeError(f'attachment list ({d}) must be of type list or dict, not {type(d).__name__}')

                    if isinstance(d, list):
                        for a in range(len(d)):
                            attachment = d[a]
                            if not isinstance(attachment, Weapon.Attachment):
                                raise TypeError(f'attachment {attachment} at index {a} must be of type Attachment, not {type(attachment).__name__}')
                    else:
                        for scope_category, _ in d.items():
                            if not isinstance(scope_category, Weapon.Attachment.ScopeCategory):
                                raise TypeError(f'scope_category ({scope_category}) must be of type ScopeCategory, not {type(scope_category).__name__}')
                            
                    category = Weapon.Attachment.AttachmentCategory[c]
                    self._attachments.update({category: d})
                    setattr(self, category.name.lower(), d)

            def _get_attachments_by_category(self, category) -> list:
                if not isinstance(category, Weapon.Attachment.AttachmentCategory):
                    raise TypeError(f'category must be of type AttachmentCategory, not {type(category).__name__}')
                
                for c, a in self._attachments.items():
                    if(c == category):
                        return a
                return None

            def get_scopes(self) -> list:
                return self._get_attachments_by_category(Weapon.Attachment.AttachmentCategory.SCOPES)
            
            def get_barrels(self) -> list:
                return self._get_attachments_by_category(Weapon.Attachment.AttachmentCategory.BARRELS)
            
            def get_grips(self) -> list:
                return self._get_attachments_by_category(Weapon.Attachment.AttachmentCategory.GRIPS)
            
            def get_underbarrels(self) -> list:
                return self._get_attachments_by_category(Weapon.Attachment.AttachmentCategory.UNDERBARRELS)

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

        def _random_attachments(self, attachments: AttachmentLoadout, *, categorize_scopes: bool = False):
            if not isinstance(attachments, self.AttachmentLoadout):
                raise TypeError(f'attachments must be of type AttachmentLoadout, not {type(attachments).__name__}')

            random_attachments = {}
            for c, d in attachments._attachments.items():
                if isinstance(d, dict):
                    if categorize_scopes:
                        scope_category_data = d[list(d.keys())[random.randint(0,len(d.keys())-1)]]
                        random_scope = scope_category_data[random.randint(0,len(scope_category_data)-1)]
                    else:
                        all_scopes = []
                        for d in d.values():
                            all_scopes = all_scopes + d
                        random_scope = all_scopes[random.randint(0,len(all_scopes)-1)]
                    random_attachments.update({c: random_scope})
                elif isinstance(d, list):
                    attach = d[random.randint(0,len(d)-1)]
                    random_attachments.update({c: attach})
                else:
                    raise TypeError(f'attachment data in each attachment category should be of type list of dict, not {type(d).__name__}')
            return random_attachments

        def randomize(self):
            random_primary = self.primaries[random.randint(0, len(self.primaries)-1)]
            random_attachments_primary = self._random_attachments(random_primary.attachments)
            primary = Finished._Weapon(random_primary.weapon_category, random_primary.weapon_type, random_primary._weapon_data, random_primary.damage, random_primary.fire_rate, random_primary.mag, random_primary.max_mag, random_primary.ads, random_primary.reload_speed, random_primary.rsm, random_primary.destruction, Finished._Weapon._Loadout._AttachmentLoadout(**{k.name: v for k, v in random_attachments_primary.items()}), random_primary.modifiers)

            random_secondary = self.secondaries[random.randint(0, len(self.secondaries)-1)]
            random_attachments_secondary = self._random_attachments(random_secondary.attachments)
            secondary = Finished._Weapon(random_secondary.weapon_category, random_secondary.weapon_type, random_secondary._weapon_data, random_secondary.damage, random_secondary.fire_rate, random_secondary.mag, random_secondary.max_mag, random_secondary.ads, random_secondary.reload_speed, random_secondary.rsm, random_secondary.destruction, Finished._Weapon._Loadout._AttachmentLoadout(**{k.name: v for k, v in random_attachments_secondary.items()}), random_secondary.modifiers)

            return Finished._Weapon._Loadout(primary, secondary)
        
        def __repr__(self):
            return f'Loadout<primaries={self.primaries}, secondaries={self.secondaries}>'

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
            def get_category(self):
                return _util.get_attachment_category_from_type(self)

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

        def __init__(self, attachment_type: AttachmentType, *, modifiers: list = []):
            """constructor for Attachment class"""
            if not isinstance(attachment_type, self.AttachmentType):
                raise TypeError(f'attachment_type must be of type AttachmentType, not {type(attachment_type).__name__}') 

            #print(f' mod len: {len(modifiers)}')
            for m in range(len(modifiers)):
                mod = modifiers[m]
                if not isinstance(mod, self.AttributeModifier): raise TypeError(f'modifier {mod} at index {m} must be of type AttributeModifier, not {type(mod).__name__}')

            self.attachment_type = attachment_type
            self.modifiers = modifiers

        def __repr__(self):
            """representation of Attachment class"""
            return f'Attachment<attachment_type={self.attachment_type}, modifiers={self.modifiers}>'

        def add_modifier(self, modifier):
            """adds a modifier to the attachment"""
            if not isinstance(modifier, Weapon.ModifierManager.AttributeModifier): 
                raise TypeError(f'modifier ({modifier}) must be of type AttributeModifier, not {type(modifier).__name__}')

            #print(f' % attr mod: {modifier}')
            self.modifiers.append(modifier)

        def remove_modifier(self, *modifiers):
            for m in range(len(modifiers)):
                mod = modifiers[m]
                if not isinstance(mod, Weapon.ModifierManager.AttributeModifier):
                    raise TypeError(f'modifier at index {m} must be of type AttributeModifier, not {type(m).__name__}')

                self.modifiers.remove(mod)

    class ModifierManager():
        class ModifiableWeaponAttribute(enum.Enum):
            """enum of modifiable weapon attributes, with corresponding labels and types"""
            DAMAGE = ("Damage", int)
            ADS = ("Ads time", float)
            RELOAD = ("Reload speed", float)
            RSM = ("Run speed modifier", float)
            
        class AttributeModifier():
            """class for attribute modifiers"""
            def __init__(self, modified_attribute, modifier: any):
                """constructor for AttributeModifier class"""
                if not isinstance(modified_attribute, Weapon.ModifierManager.ModifiableWeaponAttribute):
                    raise TypeError(f'modified_attribute must be of type ModifiableWeaponAttribute, not {type(modified_attribute).__name__}')

                expected_type = modified_attribute.value[1]
                if not isinstance(modifier, expected_type):
                    raise TypeError(f'modifier must be of type {expected_type.__name__} for attribute {modified_attribute}, not {type(modifier).__name__}')

                self.modified_attribute = modified_attribute
                self.modifier = modifier

            def __repr__(self):
                """representation of AttributeModifier class"""
                return f"AttributeModifier<modified_attribute={self.modified_attribute}, modifier={self.modifier}>"

        def __init__(self, **modifiers): 
            if len(modifiers) == 0: 
                print('skipped b/c empty')
                return
            
            self._modifiers = {}
            for _, mods in modifiers.items():
                if not isinstance(mods, dict):
                    raise TypeError(f'modifiers for each attachment category must be of type dict, not {type(mods).__name__}')

                for a, m in mods.items():
                    attach_type = _util.attachment_type_from_string(a)
                    if not isinstance(m, dict):
                        raise TypeError(f'modifiers for each attachment type must be of type dict, not {type(mods).__name__}')
                    
                    modifier_list = []
                    for v, mod in m.items():
                        modded_value = self.ModifiableWeaponAttribute[v]
                        modifier_list.append(self.AttributeModifier(modded_value, mod))
                    self._modifiers.update({attach_type: modifier_list})

        def has_modifier(self, attachment_type) -> bool:
            if not isinstance(attachment_type, Weapon.Attachment.AttachmentType):
                raise TypeError(f'attachment_type must be of type AttachmentType, not {attachment_type}')
            
            for t, _ in self._modifiers.items():
                if(t == attachment_type):
                    return True
            return False

        def get_modifier(self, attachment_type) -> list | None:
            if not isinstance(attachment_type, Weapon.Attachment.AttachmentType):
                raise TypeError(f'attachment_type must be of type AttachmentType, not {attachment_type}')
            
            for t, m in self._modifiers.items():
                if(t == attachment_type):
                    return m
            return None


    def __init__(self, weapon_category: WeaponCategory, weapon_type: WeaponType, weapon_data: dict, damage: int, fire_rate: int, mag: int, max_mag: int, ads: float, reload_speed: float, rsm: float, destruction: Destruction, attachments: dict, modifiers: ModifierManager):
        """constructor for Weapon class"""
        if not isinstance(weapon_category, self.WeaponCategory):
            raise TypeError(f'weapon_category ({weapon_category}) must be of type WeaponCategory, not {type(weapon_category).__name__}')
        if not isinstance(weapon_type, self.WeaponType):
            raise TypeError(f'weapon_type ({weapon_type}) must be of type WeaponType, not {type(weapon_type).__name__}')
        if not isinstance(weapon_data, dict):
            raise TypeError(f'weapon_data ({weapon_data}) must be of type dict, not {type(weapon_data).__name__}')
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
        if not isinstance(attachments, self.Loadout.AttachmentLoadout):
            raise TypeError(f'attachments must be of type AttachmentLoadout, not {type(attachments).__name__}')
        if not isinstance(modifiers, self.ModifierManager):
            raise TypeError(f'modifiers must be of type ModifierManager, not {type(modifiers).__name__}')

        self.weapon_category = weapon_category
        self.weapon_type = weapon_type
        self._weapon_data = weapon_data
        self.damage = damage
        self.fire_rate = fire_rate
        self.mag = mag
        self.max_mag = max_mag
        self.ads = ads
        self.reload_speed = reload_speed
        self.rsm = rsm
        self.destruction = destruction
        self.attachments = attachments
        self.modifiers = modifiers

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

    def __init__(self, operator_type: OperatorType, operator_data: dict, roles: list[Role], difficulty: int, speed: int, health: int, ability: Ability, gadgets: list[OperatorGadget], weapons: Weapon.Loadout):
        """constructor for Operator class"""
        if not isinstance(operator_type, Operator.OperatorType):
            raise TypeError(f'operator_type must be of type OperatorType, not {type(operator_type).__name__}')

        if not isinstance(operator_data, dict):
            raise TypeError(f'operator_data must be of type dict, not {type(operator_data)}')

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
        self._operator_data = operator_data
        self.roles = roles
        self.difficulty = difficulty
        self.speed = speed
        self.health = health
        self.ability = ability
        self.gadgets = gadgets
        self.weapons = weapons

    def randomize(self):
        return Finished._Operator(self.operator_type, self._operator_data, self.roles, self.difficulty, self.speed, self.health, self.ability, self.gadgets, self.weapons.randomize())

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
            total_weapon_data = all_weapon_data[slot_index]
            for name, data in total_weapon_data.items():
                #print(f' # {name}')
                attachments_data = data['ATTACHMENTS']
                attachment_map = {}

                modifier_manager = Weapon.ModifierManager()
                mod_in_data = 'modifiers' in data
                if(mod_in_data):
                    modifier_manager = Weapon.ModifierManager(**data['modifiers'])

                for attachment_category, attachments in attachments_data.items():
                    attachment_category_class = Weapon.Attachment.AttachmentCategory[attachment_category]
                    if attachment_category_class == Weapon.Attachment.AttachmentCategory.SCOPES: 
                        scopes = {}
                        for scope_category, scope_list in attachments.items():
                            category = Weapon.Attachment.ScopeCategory[scope_category]
                            scope_type = _util.get_scope_type(category)
                            
                            final_scopes = []
                            for s in scope_list:
                                #print(f's {scope_type[s]}: {s}')
                                # do not remove the modifiers=[] because all mods will be passed into constructor if not?????
                                attach = Weapon.Attachment(scope_type[s], modifiers=[])
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
                        
                        attachment_map.update({attachment_category_class: scopes})
                        #print(f'scopes: {scopes}')
                    elif attachment_category_class == Weapon.Attachment.AttachmentCategory.BARRELS:
                        barrels = []
                        for b in attachments:
                            #print(f'attachment_category={attachment_category}, type(b)={type(b).__name__}, b={b}')
                            attach = Weapon.Attachment(Weapon.Attachment.BarrelAttachment[b], modifiers=[])
                            if mod_in_data:
                                modifier_data = data['modifiers']

                                if attachment_category in modifier_data:
                                    modifiers = modifier_data[attachment_category]
                                    for m in _util.get_modifiers(modifiers, b):
                                        #print(f'adding {m} to {b}')
                                        attach.add_modifier(m)
                            barrels.append(attach)
                        attachment_map.update({attachment_category_class: barrels})
                        #print(f'barrels: {barrels}')
                    elif attachment_category_class == Weapon.Attachment.AttachmentCategory.GRIPS:
                        grips = []
                        for g in attachments:
                            #print(f'attachment_category={attachment_category}, type(g)={type(g).__name__}, b={g}')

                            attach = Weapon.Attachment(Weapon.Attachment.GripAttachment[g], modifiers=[])
                            if mod_in_data:
                                modifier_data = data['modifiers']

                                if attachment_category in modifier_data:
                                    modifiers = modifier_data[attachment_category]
                                    for m in _util.get_modifiers(modifiers, g):
                                        #print(f'adding {m} to {g}')
                                        attach.add_modifier(m)
                            grips.append(attach)
                        attachment_map.update({attachment_category_class: grips})
                        #print(f'grips: {grips}')
                    elif attachment_category_class == Weapon.Attachment.AttachmentCategory.UNDERBARRELS:
                        grips = []
                        for u in attachments:
                            #print(f'attachment_category={attachment_category}, type(g)={type(u).__name__}, b={u}')

                            attach = Weapon.Attachment(Weapon.Attachment.UnderbarrelAttachment[u], modifiers=[])
                            if mod_in_data:
                                modifier_data = data['modifiers']

                                if attachment_category in modifier_data:
                                    modifiers = modifier_data[attachment_category]
                                    for m in _util.get_modifiers(modifiers, u):
                                        #print(f'adding {m} to {u}')
                                        attach.add_modifier(m)
                            grips.append(attach)
                        attachment_map.update({attachment_category_class: grips})
                        #print(f'grips: {grips}')
                    else: 
                        raise ValueError(f'attachment_category has an invalid value of {attachment_category}')

                new_weapon = Weapon(
                    Weapon.WeaponCategory[data['TYPE']],
                    Weapon.WeaponType[name],
                    data,
                    data['DAMAGE'],
                    data['FIRE_RATE'],
                    data['MAG'],
                    data['MAX'],
                    data['ADS'],
                    data['RELOAD'],
                    data['RSM'],
                    Weapon.Destruction[data['DEST']],
                    Weapon.Loadout.AttachmentLoadout(**{k.name: v for k, v in attachment_map.items()}),
                    modifier_manager
                )
                
                if slot_index == 0: 
                    primaries.append(new_weapon)
                elif slot_index == 1: 
                    secondaries.append(new_weapon)
                else:
                    raise ValueError(f'slot_index is != 0, 1 ({slot_index})')
        
        weapons = Weapon.Loadout(primaries, secondaries)

        return Operator(
            operator_type, d, roles, d['difficulty'], d['speed'], d['health'], ability, gadgets, weapons
        )

    @staticmethod
    def get(operator_type: OperatorType):
        """static method for getting an Operator object using an OperatorType or corresponding string representation"""
        if not isinstance(operator_type, Operator.OperatorType):
            raise TypeError(f'operator_type must be of type str or OperatorType, not {type(operator_type).__name__}')

        with open(_util.data_file_name(), 'r') as f:
            categorized_operators = json.loads(f.read())
            for c in categorized_operators:
                for n, d in categorized_operators[c].items():
                    if n != operator_type.name: continue

                    return Operator.load(operator_type, c, d)

class Error:
    class AttachmentNotAvailableError(Exception): pass

class Finished:
    class _Weapon(Portable):
        class _Loadout(Portable):
            class _AttachmentLoadout(Portable):
                def __init__(self, **attachments):
                    self._attachments = {}
                    for c, a in attachments.items():
                        if not isinstance(a, Weapon.Attachment):
                            raise TypeError(f'attachment must be of type Attachment, not {type(a).__name__}')
                                
                        category = Weapon.Attachment.AttachmentCategory[c]
                        self._attachments.update({category: a})
                        setattr(self, category.name.lower(), a)

                def export(self):
                    return {c.name[:-1]:a.attachment_type.name for c, a in self._attachments.items()}

                def _get_attachment_by_category(self, category) -> Weapon.Attachment:
                    if not isinstance(category, Weapon.Attachment.AttachmentCategory):
                        raise TypeError(f'category must be of type AttachmentCategory, not {type(category).__name__}')
                    
                    for c, a in self._attachments.items():
                        if(c == category):
                            return a
                    return None

                def get_scope(self) -> Weapon.Attachment:
                    return self._get_attachment_by_category(Weapon.Attachment.AttachmentCategory.SCOPES)
                
                def get_barrel(self) -> Weapon.Attachment:
                    return self._get_attachment_by_category(Weapon.Attachment.AttachmentCategory.BARRELS)
                
                def get_grip(self) -> Weapon.Attachment:
                    return self._get_attachment_by_category(Weapon.Attachment.AttachmentCategory.GRIPS)
                
                def get_underbarrel(self) -> Weapon.Attachment:
                    return self._get_attachment_by_category(Weapon.Attachment.AttachmentCategory.UNDERBARRELS)
                
            def __init__(self, primary, secondary):
                """constructor for _Loadout class"""
                if not isinstance(primary, Finished._Weapon):
                    raise TypeError(f'primary must be of type _Weapon, not {type(primary).__name__}')

                if not isinstance(secondary, Finished._Weapon):
                    raise TypeError(f'secondary must be of type _Weapon, not {type(secondary).__name__}')

                self.primary = primary
                self.secondary = secondary

            def export(self):
                return {
                    'primary': self.primary.export(),
                    'secondary': self.secondary.export()
                }

            def __repr__(self):
                return f'_Loadout<primary={self.primary}, secondary={self.secondary}>'

        def __init__(self, weapon_category: Weapon.WeaponCategory, weapon_type: Weapon.WeaponType, weapon_data: dict, damage: int, fire_rate: int, mag: int, max_mag: int, ads: float, reload_speed: float, rsm: float, destruction: Weapon.Destruction, attachments, modifiers: Weapon.ModifierManager):
            if not isinstance(weapon_category, Weapon.WeaponCategory):
                raise TypeError(f'weapon_category ({weapon_category}) must be of type WeaponCategory, not {type(weapon_category).__name__}')
            if not isinstance(weapon_type, Weapon.WeaponType):
                raise TypeError(f'weapon_type ({weapon_type}) must be of type WeaponType, not {type(weapon_type).__name__}')
            if not isinstance(weapon_data, dict):
                raise TypeError(f'weapon_data ({weapon_data}) must be of type dict, not {type(weapon_data).__name__}')
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
            if not isinstance(destruction, Weapon.Destruction):
                raise TypeError(f'destruction must be Destruction, not {type(destruction).__name__}')
            if not isinstance(attachments, Finished._Weapon._Loadout._AttachmentLoadout):
                raise TypeError(f'attachments must be of type _AttachmentLoadout, not {type(attachments).__name__}')
            if not isinstance(modifiers, Weapon.ModifierManager):
                raise TypeError(f'modifiers must be of type ModifierManager, not {type(modifiers).__name__}')

            self.weapon_category = weapon_category
            self.weapon_type = weapon_type
            self._weapon_data = weapon_data
            self._base_damage = damage
            self.fire_rate = fire_rate
            self.mag = mag
            self.max_mag = max_mag
            self._base_ads = ads
            self._base_reload_speed = reload_speed
            self._base_rsm = rsm
            self.destruction = destruction
            self.attachments = attachments
            self.modifiers = modifiers

        def export(self):
            return {
                self.weapon_type.name: {
                    'TYPE': self.weapon_category.name,
                    'DAMAGE': self._base_damage,
                    'FIRE_RATE': self.fire_rate,
                    'MAG': self.mag,
                    'MAX': self.max_mag,
                    'ADS': self._base_ads,
                    'RELOAD': self._base_reload_speed,
                    'RSM': self._base_rsm,
                    'DEST': self.destruction.name,
                    'ATTACHMENTS': self.attachments.export(),
                    'MODIFIERS': self.get_all_modifiers()
                }
            }

        def __repr__(self):
            return f'_Weapon<weapon_category={self.weapon_category}, weapon_type={self.weapon_type}, _base_damage={self._base_damage}, fire_rate={self.fire_rate}, mag={self.mag}, max_mag={self.max_mag}, _base_ads={self._base_ads}, _base_reload_speed={self._base_reload_speed}, _base_rsm={self._base_rsm}, destruction={self.destruction}, attachments={self.attachments}>'

        def equip(self, attachment_type):
            if not isinstance(attachment_type, Weapon.Attachment.AttachmentType):
                raise TypeError(f'attachment_type must be of type AttachmentType, not {type(attachment_type).__name__}')

            category = _util.get_attachment_category_from_type(attachment_type)
            for c, a in self.attachments._attachments.items():
                attach = Weapon.Attachment(attachment_type, modifiers=[])
                if c != category: continue

                if(attachment_type == a.attachment_type): 
                    return
                
                if 'modifiers' in self._weapon_data:
                    mods = self._weapon_data['modifiers'][category.name]
                    for m in _util.get_modifiers(mods, attachment_type.name):
                        attach.add_modifier(m)

                self.attachments._attachments[c] = attach
                break
            else:
                raise Error.AttachmentNotAvailableError(f"Attachment category {category.name} isn\'t available on weapon {self.weapon_type.name}")
            
        def has_attachment(self, attachment_type):
            if not isinstance(attachment_type, Weapon.Attachment.AttachmentType):
                raise TypeError(f'attachment_type must be of type AttachmentType, not {type(attachment_type).__name__}')
            
            for _, d in self.attachments._attachments.items():
                if attachment_type != d.attachment_type:
                    continue
                return True
            return False
        
        def allows_attachment(self, attachment_type):
            if not isinstance(attachment_type, Weapon.Attachment.AttachmentType):
                raise TypeError(f'attachment_type must be of type AttachmentType, not {type(attachment_type).__name__}')
            
            category = attachment_type.get_category()
            for c, _ in self.attachments._attachments.items():
                if c != category: 
                    continue
                return True
            return False
        
        def allows_attachment_category(self, attachment_category):
            if not isinstance(attachment_category, Weapon.Attachment.AttachmentCategory):
                raise TypeError(f'attachment_category must be of type AttachmentCategory, not {type(attachment_category).__name__}')
            
            for c, _ in self.attachments._attachments.items():
                if c != attachment_category: 
                    continue
                return True
            return False

        def get_all_attachments(self) -> list[Weapon.Attachment]:
            return [a for _, a in self.attachments._attachments.items()]

        def get_all_modifiers(self) -> list[Weapon.ModifierManager.AttributeModifier]:
            mods = []
            for a in self.get_all_attachments():
                mods = mods + a.modifiers
            return mods
        
        def get_attachment(self, attachment_category: Weapon.Attachment.AttachmentCategory) -> Weapon.Attachment | None:
            for c, a in self.attachments._attachments.items():
                if c == attachment_category:
                    return a
            return None
        
        def get_scope(self) -> Weapon.Attachment.ScopeAttachment | None:
            return self.get_attachment(Weapon.Attachment.AttachmentCategory.SCOPES)
        
        def get_barrel(self) -> Weapon.Attachment.ScopeAttachment | None:
            return self.get_attachment(Weapon.Attachment.AttachmentCategory.BARRELS)

        def get_grip(self) -> Weapon.Attachment.ScopeAttachment | None:
            return self.get_attachment(Weapon.Attachment.AttachmentCategory.GRIPS)

        def get_underbarrel(self) -> Weapon.Attachment.ScopeAttachment | None:
            return self.get_attachment(Weapon.Attachment.AttachmentCategory.UNDERBARRELS)
        
        def _get_modified_value(self, base_val: int | float, attr):
            if not isinstance(base_val, int) and not isinstance(base_val, float):
                raise TypeError(f'base_val must be of type int or float, not {type(base_val).__name__}')

            if not isinstance(attr, Weapon.ModifierManager.ModifiableWeaponAttribute):
                raise TypeError(f'attr must be of type ModifiableWeaponAttribute, not {type(attr).__name__}')

            for _, d in self.attachments._attachments.items():
                if len(d.modifiers) == 0:
                    continue

                for m in d.modifiers:
                    if m.modified_attribute != attr: continue
                    base_val = round(base_val + m.modifier, 3)
            return base_val

        @property
        def damage(self):
            """gets weapon damage with attachment modifiers"""
            return self._get_modified_value(self._base_damage, Weapon.ModifierManager.ModifiableWeaponAttribute.DAMAGE)

        @property
        def ads(self):
            return self._get_modified_value(self._base_ads, Weapon.ModifierManager.ModifiableWeaponAttribute.ADS)

        @property
        def reload_speed(self):
            return self._get_modified_value(self._base_reload_speed, Weapon.ModifierManager.ModifiableWeaponAttribute.RELOAD)

        @property
        def rsm(self):
            return self._get_modified_value(self._base_rsm, Weapon.ModifierManager.ModifiableWeaponAttribute.RSM)
        
        @property
        def name(self):
            return self.weapon_type.value

    class _Operator(Portable):
        def __init__(self, operator_type: Operator.OperatorType, operator_data: dict, roles: list[Operator.Role], difficulty: int, speed: int, health: int, ability: Operator.Ability, gadgets: list[Operator.OperatorGadget], weapons):
            """constructor for _Operator class"""
            if not isinstance(operator_type, Operator.OperatorType):
                raise TypeError(f'operator_type must be of type OperatorType, not {type(operator_type).__name__}')
            
            if not isinstance(operator_data, dict):
                raise TypeError(f'operator_data must be of type dict, not {type(operator_data)}')

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

            if not isinstance(weapons, Finished._Weapon._Loadout):
                raise TypeError(f'weapons must be of type Loadout, not {type(weapons).__name__}')

            self.operator_type = operator_type
            self._operator_data = operator_data
            self.roles = roles
            self.difficulty = difficulty
            self.speed = speed
            self.health = health
            self.ability = ability
            self.gadgets = gadgets
            self.weapons = weapons

        def export(self):
            return {
                self.operator_type.name: {
                    'type': [r.name for r in self.roles],
                    'difficulty': self.difficulty,
                    'speed': self.speed,
                    'health': self.health,
                    'ability': self.ability,
                    'gadgets': [g.name for g in self.gadgets],
                    'weapons': self.weapons.export(),
                }
            }

        def __repr__(self):
            return f'_Operator<operator_type={self.operator_type}, roles={self.roles}, difficulty={self.difficulty}, speed={self.speed}, health={self.health}, ability={self.ability}, gadgets={self.gadgets}, weapons={self.weapons}>'

        def get_primary(self):
            return self.weapons.primary

        def get_secondary(self):
            return self.weapons.secondary