"""AllyHeal: healing miracles and support spells also affect nearby allies (never enemies).

How it works: each spell that used to apply its SpEffect straight to the caster now spawns an
area bullet, modelled on Soothing Sunlight. The bullet gives the caster the original effect
(spEffectIDForShooter) and gives every friendly character it touches an "ally" copy of it
(spEffectId0..). The cast animation is unchanged.
"""

VERSION = '1.0.0'

ALLY_RATE = 0.75     # allies get 75% of the caster's heal
RADIUS_MAX = 3.0     # metres (Soothing Sunlight = 4.0)
SPREAD_TIME = 0.5    # seconds for the area to grow to full size

TEMPLATE_BULLET = 3100   # Soothing Sunlight area bullet (and 3101..3104 for its levels)
TEMPLATE_ALLY_SP = 1430  # Soothing Sunlight heal: its target flags define "friendly"

# magic id: (ally SpEffect base id, bullet base id, label, levels, heal)
#   levels - miracles have hidden "Level 1-4" variants at base id + 1..4
#   heal   - True: allies get ALLY_RATE of the HP restored; False: full effect
SPELLS = {
    # healing
    5000: (1440, 3400, 'Heal', 5, True),
    5020: (1450, 3410, 'Great Heal Excerpt', 5, True),
    5010: (1460, 3420, 'Great Heal', 5, True),
    5040: (1470, 3430, 'Replenishment', 5, True),
    # defensive buffs
    5600: (92000, 3440, 'Magic Barrier', 5, False),
    5610: (92010, 3450, 'Great Magic Barrier', 5, False),
    5200: (92020, 3460, 'Escape Death', 5, False),
    4310: (92030, 3470, 'Flash Sweat', 1, False),
    3610: (92040, 3480, 'Remedy', 1, False),
    3600: (92050, 3490, 'Resist Curse', 1, False),
    # stealth / utility
    3410: (92060, 3500, 'Hidden Body', 1, False),
    3510: (92070, 3510, 'Hush', 1, False),
    3540: (92080, 3520, 'Fall Control', 1, False),
    3500: (92090, 3530, 'Cast Light', 1, False),  # experimental: its animation never spawns a bullet in vanilla
    3530: (92100, 3540, 'Repair', 1, False),
}

# Remedy cures through a chain of bullets: 1300 base, then 1301 bleed, 1302 poison, 1303 toxic
REMEDY_CHAIN = {1: 'Bleed', 2: 'Poison', 3: 'Toxic'}
REMEDY_SECOND_BULLET = 2910


def apply(params):
    """params: dict param name -> (Param, Layout). Modifies Magic, SpEffectParam and Bullet in place."""
    mp, ml = params['Magic']
    sp, sl = params['SpEffectParam']
    bp, bl = params['Bullet']

    # Self must stay on: a hit on a remote player is resolved on that player's side, where they are "self"
    ally_flags = {k: sl.get(sp[TEMPLATE_ALLY_SP], k) for k in sl.slots if k.startswith('effectTarget')}
    assert ally_flags['effectTargetEnemy'] == 0 and ally_flags['effectTargetFriend'] == 1

    for magic_id, (ally_sp, bullet, label, levels, is_heal) in SPELLS.items():
        m = mp[magic_id]
        if ml.get(m, 'refCategory') == 2:      # SpEffect applied straight to the caster
            self_sp = ml.get(m, 'refId')
        else:                                   # self-only bullet (Remedy)
            self_sp = bl.get(bp[ml.get(m, 'refId')], 'spEffectIDForShooter')
        for lvl in range(levels):
            tag = '' if lvl == 0 else f' - Level {lvl}'
            own = self_sp + lvl if self_sp + lvl in sp else self_sp
            src = sp[own]
            row = sp.add(ally_sp + lvl, src, f'[AllyHeal] {label} - Ally{tag}'.encode())
            if is_heal:
                sl.set(row, 'changeHpPoint', int(round(sl.get(src, 'changeHpPoint') * ALLY_RATE)))
            for k, v in ally_flags.items():
                sl.set(row, k, v)
            b = bp.add(bullet + lvl, bp[TEMPLATE_BULLET + lvl], f'[AllyHeal] {label} - Ally{tag}'.encode())
            bl.set(b, 'spEffectIDForShooter', own)
            bl.set(b, 'spEffectId0', ally_sp + lvl)
            bl.set(b, 'hitRadiusMax', RADIUS_MAX)
            bl.set(b, 'spreadTime', SPREAD_TIME)
        ml.set(m, 'refCategory', 1)  # spawn the bullet instead of applying the effect directly
        ml.set(m, 'refId', bullet)

    # Remedy: caster keeps the original cure chain; allies get all four cures from the area bullet
    remedy_ally, remedy_bullet = SPELLS[3610][0], SPELLS[3610][1]
    b = bp[remedy_bullet]
    bl.set(b, 'HitBulletID', REMEDY_SECOND_BULLET)
    for i, what in REMEDY_CHAIN.items():
        row = sp.add(remedy_ally + i, sp[1300 + i], f'[AllyHeal] Remedy - {what} - Ally'.encode())
        for k, v in ally_flags.items():
            sl.set(row, k, v)
        bl.set(b, f'spEffectId{i}', remedy_ally + i)
