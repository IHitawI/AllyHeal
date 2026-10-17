# Nexus Mods — заполнение страницы

**Игра:** Dark Souls Remastered
**Название:** AllyHeal — Group Heals and Buffs
**Версия:** 1.0.0
**Категория:** Gameplay Effects and Changes (или Magic — Spells, если есть)

**Краткое описание (Brief overview, до 350 символов):**
> Heal, Great Heal, Replenishment and 11 support spells now also affect allies within 3 m, like in DS2/DS3/Elden Ring. Allies get 75% of your heal; enemies and PvP opponents are never affected. For co-op with Mod Engine 2 / Seamless Co-op.

**Описание:** `description_en.bbcode` (основное), `description_ru.bbcode` можно добавить
ниже под спойлер `[spoiler]...[/spoiler]` или отдельной страницей.
Репозиторий: https://github.com/IHitawI/AllyHeal

**Теги:** Gameplay, Co-op, Multiplayer, Magic, Miracles, Healing, Balance

**Requirements (Nexus):** Mod Engine 2 — внешняя ссылка https://github.com/soulsmods/ModEngine2/releases
(опционально: Seamless Co-op — ссылка на его страницу Nexus).

**Файл:** `dist/AllyHeal-1.0.0.zip`, категория Main. Описание файла:
> AllyHeal 1.0.0. Extract the AllyHeal folder into your Mod Engine 2 folder and add it to config_darksoulsremastered.toml (see INSTALL.txt).

**Permissions (рекомендация):** разрешить использование в других модах с указанием автора
(это и так следует из MIT-лицензии кода); загрузку на другие сайты — по запросу.

**Картинки:** `nexus/images/allyheal_header_1920x480.png` (шапка страницы) и
`nexus/images/allyheal_main_1280x720.png` (главная картинка / превью). Сделаны из скриншота игры
скриптом `tools/make_nexus_art.py` (`python tools/make_nexus_art.py <скриншот 1920x1080> nexus/images`);
интерфейс и ники игроков обрезаны. Если форма Nexus попросит другой размер — поменять размеры в скрипте.

**Скриншоты:** нужны из игры — например, каст Лечения рядом с союзником и его полоска HP,
иконка баффа (Волшебный барьер) у союзника.
