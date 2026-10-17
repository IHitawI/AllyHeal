<p align="center"><img src="docs/images/banner.png" alt="AllyHeal — group heals and support spells for Dark Souls Remastered co-op"></p>

# AllyHeal — Dark Souls Remastered

[![Release](https://img.shields.io/github/v/release/IHitawI/AllyHeal)](https://github.com/IHitawI/AllyHeal/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Healing miracles and support spells also affect allies standing next to you, the way they do in
Dark Souls II, III and Elden Ring. Enemies and PvP opponents are never affected.

[Русская версия ниже](#allyheal--русский)

## What it does

**Healing** — allies within 3 m receive 75% of what you heal yourself:

| Spell | You | Allies |
|---|---|---|
| Heal | 300 | 225 |
| Great Heal | 800 | 600 |
| Great Heal Excerpt | 800 | 600 |
| Replenishment | 10 HP/s, 60 s | 8 HP/s, 60 s |

The hidden spell levels (Level 1–4) scale the same way. Soothing Sunlight and Bountiful Sunlight
are unchanged, so they stay the stronger group heals (100%, 4 m).

**Support spells** — full effect on allies within 3 m:
Magic Barrier, Great Magic Barrier, Escape Death, Flash Sweat, Remedy, Resist Curse,
Hidden Body, Hush, Fall Control, Cast Light, Repair.

Cast animations, costs and requirements are unchanged.

## Download

Get **AllyHeal-1.0.0.zip** from the [latest release](https://github.com/IHitawI/AllyHeal/releases/latest).

## Install

See [docs/INSTALL.txt](docs/INSTALL.txt). In short: Mod Engine 2, copy the `AllyHeal` folder into it,
add `{enabled = true, name = "AllyHeal", path = "AllyHeal"},` to the `mods` list in
`config_darksoulsremastered.toml`.

- **Co-op:** every player needs the mod (hits on a player are resolved on that player's game).
- **Conflicts:** any other mod that ships `GameParam.parambnd.dcx`.
- **Online:** do not use on the official servers; play offline or with Seamless Co-op.

## Building from source

The repository contains no game files. The build reads the parameters from your own installation:

```
python build.py
python build.py --game "D:\Games\DARK SOULS REMASTERED" --report
```

Python 3.10+, no packages. Output: `dist/AllyHeal/` and `dist/AllyHeal-<version>.zip`.
The game folder must be unmodified (the build refuses an already-patched GameParam).

| File | What |
|---|---|
| `src/allyheal.py` | the mod: which spells, numbers, IDs |
| `src/soulsformats.py` | readers/writers for DCX, BND3, PARAMDEF, PARAM, FMG (written from scratch, byte-exact round-trip) |
| `build.py` | loads the game files, applies the mod, writes the mod folder and zip |
| `tools/make_banner.py` | builds the README banner from an in-game screenshot (HUD and names cropped) |

### How it works

In vanilla, Heal and the other self spells apply a SpEffect directly to the caster
(`Magic.refCategory = 2`). AllyHeal points them at a new area bullet instead (`refCategory = 1`),
cloned from Soothing Sunlight:

- `spEffectIDForShooter` = the original effect, so the caster gets exactly what they got before;
- `spEffectId0` = an ally copy of that effect with Soothing Sunlight's target flags
  (friends yes, enemies no) and, for heals, 75% of the HP.

New IDs: SpEffect 1440–1474 and 92000–92104, Bullet 3400–3544. Remedy keeps its vanilla cure chain
for the caster and gives allies all four cures from the area bullet.

## Known issues

- Cast Light is experimental: its animation never spawns a bullet in vanilla.
- An ally may not see the heal visual on themselves, the HP is still restored.
- Replenishment on an ally replaces a stronger Bountiful Sunlight regen (same effect category).

## License

Code: [MIT](LICENSE). Dark Souls and its data belong to FromSoftware / Bandai Namco;
this repository contains none of it.

---

## AllyHeal — русский

Чудеса лечения и вспомогательные заклинания действуют и на союзников рядом с тобой,
как в Dark Souls II, III и Elden Ring. На врагов и соперников в PvP не действуют.

**Лечение:** союзники в радиусе 3 м получают 75% от твоего хила.

| Заклинание | Тебе | Союзникам |
|---|---|---|
| Лечение | 300 | 225 |
| Мощное лечение | 800 | 600 |
| Слова мощного лечения | 800 | 600 |
| Восстановление | 10 HP/сек, 60 сек | 8 HP/сек, 60 сек |

Скрытые уровни заклинаний (Level 1–4) считаются так же. Успокаивающий Свет и Изобильный Свет не изменены.

**Поддержка:** полный эффект на союзников в радиусе 3 м:
Волшебный барьер, Большой волшебный барьер, Уход от смерти, Сырая плоть, Исцеление,
Сопротивление проклятию, Незаметность, Бесшумность, Осторожное падение, Заклинание Света, Починка.

**Скачать:** архив **AllyHeal-1.0.0.zip** в [последнем релизе](https://github.com/IHitawI/AllyHeal/releases/latest).

**Установка:** [docs/INSTALL_RU.txt](docs/INSTALL_RU.txt). Мод нужен всем игрокам в коопе.
Конфликтует с модами, у которых есть свой `GameParam.parambnd.dcx`.
Не заходите с модами на официальные серверы.

**Сборка из исходников:** `python build.py` (Python 3.10+). Файлы игры берутся из твоей установки,
в репозитории их нет.
