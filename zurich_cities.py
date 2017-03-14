# -*- coding: utf-8 -*-

import fuzzywuzzy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

zurich_sorted = ['50', '8002', '8004', '8810', 'Aathal', 'Aathal - Seegr\xc3\xa4ben', 'Aathal-Seegr\xc3\xa4ben', 'Adlikon', 'Adliswil', 'Aesch', 'Aesch (ZH)', 'Aeugst am Albis', 'Aeugstertal', 'Affoltern a.A.', 'Affoltern am Albis', 'Agasul', 'Aristau', 'Arni (AG)', 'Attikon', 'Au (ZH)', 'Au ZH', 'Bachenb\xc3\xbclach', 'Bachs', 'Baden', 'Baden-D\xc3\xa4ttwil', 'Baltenswil', 'Bassersdorf', 'Beinwil (Freiamt)', 'Benglen', 'Bergdietikon', 'Berikon', 'Bertschikon', 'Bertschikon bei Gossau', 'Besenb\xc3\xbcren', 'Bettwil', 'Bietenholz', 'Billikon', 'Binz', 'Birmensdorf', 'Birmensdorf (ZH)', 'Bisikon', 'Bonstetten', 'Boswil', 'Bremgarten', 'Bremgarten (AG)', 'Bremgarten AG', 'Br\xc3\xbctten', 'Br\xc3\xbcttisellen', 'Bubikon', 'Buchs', 'Buchs (ZH)', 'Buchs ZH', 'Buttwil/AG', 'B\xc3\xbclach', 'B\xc3\xbclachs', 'B\xc3\xbcnzen', 'Dielsdorf', 'Dietikon', 'Dietlikon', 'D\xc3\xa4nikon', 'D\xc3\xa4ttlikon', 'D\xc3\xa4ttwil', 'D\xc3\xbcbendorf', 'Ebertswil', 'Ebmatingen', 'Effretikon', 'Egg', 'Egg (ZH)', 'Egg bei Z\xc3\xbcrich', 'Eggenwil', 'Ehremdingen', 'Ehrendingen', 'Elsau', 'Embrach', 'Ennetbaden', 'Erlenbach', 'Erlenbach (ZH)', 'Esslingen', 'Fahrweid', 'Fehraltorf', 'Feldbach', 'Feldmeilen', 'First', 'Fislisbach', 'Forch', 'Forch (Aesch, Maur)', 'Freienstein-Teufen', 'Freienwil', 'Freudwil', 'F\xc3\xa4llanden', 'Gattikon', 'Geltwil/AG', 'Geroldswil', 'Glattbrugg', 'Glattpark', 'Glattpark (Opfikon)', 'Gockhausen', 'Gossau', 'Gossau (ZH)', 'Gossau ZH', 'Grafstal', 'Grafstal/Kempttal', 'Greifensee', 'Gr\xc3\xbcningen', 'Gr\xc3\xbct', 'Gr\xc3\xbct (Gossau ZH)', 'Gutenswil', 'Hausen am Albis', 'Hedingen', 'Hedingne', 'Hermetschwil-Staffeln', 'Herrliberg', 'Herschmettlen', 'Hinteregg', 'Hochfelden', 'Hombrechtikon', 'Horgen', 'H\xc3\xb6ri', 'Illnau', 'Islisberg', 'Jonen', 'Kemleten', 'Kemptthal', 'Kilchberg', 'Kilchberg (ZH)', 'Kilchberg ZH', 'Killwangen', 'Kindhausen', 'Kirchdorf', 'Kloster Fahr', 'Kloten', 'Kollbrunn', 'Kyburg', 'K\xc3\xbcsnacht', 'K\xc3\xbcsnacht (ZH)', 'K\xc3\xbcsnacht ZH', 'Langnau a.A.', 'Langnau am Albis', 'Lengnau', 'Lindau', 'Luckhausen', 'Lufingen', 'Madetswil', 'Maur', 'Meilen', 'Mellingen', 'Merenschwand', 'Mettmenstetten', 'Mettmenstetten ZH', 'Muri', 'Muri (AG)', 'Muri AG', 'M\xc3\xa4nnedorf', 'M\xc3\xb6nchaltorf', 'M\xc3\xbchlau', 'M\xc3\xbcswangen', 'Nassenwil', 'Neerach', 'Neftenbach', 'Neschwil', 'Nesselnbach', 'Neuenhof', 'Niderohrdorf', 'Niederglatt', 'Niederhasli', 'Niederrohrdorf', 'Niederweningen', 'Niederwil', 'Nuerendorf', 'Nuerensdorf', 'Nussbaumen', 'Nussbaumen bei Baden', 'N\xc3\xa4nikon', 'N\xc3\xbcrensdorf', 'Oberembrach', 'Oberengstgringen', 'Oberengstringen', 'Oberengstrngen', 'Oberglatt', 'Oberhasli', 'Oberlunkhofen', 'Oberrieden', 'Oberrohrdorf', 'Oberweningen', 'Oberwil b. N\xc3\xbcrensdorf', 'Oberwil-Lieli', 'Obfelden', 'Oetwil', 'Oetwil am See', 'Oetwil an der Limmat', 'Ohringen', 'Opfikon', 'Otelfingen', 'Ottenbach', 'Ottikon', 'Ottikon (Gossau ZH)', 'Pfaffhausen', 'Pfungen', 'Pf\xc3\xa4ffikon', 'Pf\xc3\xa4ffikon (ZH)', 'Pf\xc3\xa4ffikon ZH', 'Regensberg', 'Regensdorf', 'Remetschwil', 'Rieden', 'Riedikon', 'Riedikon (Uster)', 'Riedt', 'Rifferswil', 'Rikon', 'Rikon im T\xc3\xb6sstal', 'Rorbas', 'Rottenschwil', 'Rudolfstetten', 'Russikon', 'R\xc3\xa4terschen', 'R\xc3\xbclang', 'R\xc3\xbcmlang', 'R\xc3\xbcschlikon', 'Schleinikon', 'Schlieren', 'Schneisingen', 'Schongau', 'Schwerzenbach', 'Seegr\xc3\xa4ben', 'Sennhof', 'Seuzach', 'Sihlwald', 'Spreitenbach', 'Stadel', 'Stallikon', 'Steinmaur', 'St\xc3\xa4fa', 'St\xc3\xa4\xc3\xa4fa', 'Sulzbach (Uster)', 'S\xc3\xbcnikon', 'Tagelswangen', 'Thalwil', 'Theilingen', 'Uerikon', 'Uetikon am See', 'Uetliberg', 'Uitikon', 'Uitikon Waldegg', 'Uitikon-Waldegg', 'Unterengstringen', 'Unterlunkhofen', 'Urdorf', 'Uster', 'Volketswil', 'Waldegg', 'Wallisellen', 'Waltenschwil', 'Wangen', 'Wangen bei D\xc3\xbcbendorf', 'Watt', 'Weinigen', 'Weiningen', 'Weiningen (ZH)', 'Weisslingen', 'Wermatswil', 'Wettingen', 'Wettswil', 'Wettswil a. Albis', 'Wettswil am Albis', 'Wetzikon', 'Wetzikon (ZH)', 'Widen', 'Wiesendangen', 'Winkel', 'Winterberg', 'Winterberg ZH', 'Winterberg/ZH', 'Winterthur', 'Winterthur-Hegi', 'Wohlen', 'Wohlen (AG)', 'Wolfhausen', 'W\xc3\xa4denswil', 'W\xc3\xbcrenlos', 'Zollikerberg', 'Zollikon', 'Zuerich', 'Zufikon', 'Zumikon', 'Zurich', 'Zwillikon', 'Z\xc3\xbcrich', 'Z\xc3\xbcrich 50 Oerlikon', 'Z\xc3\xbcrich Gockhausen', 'Z\xc3\xbcrich-Altstetten', 'Z\xc3\xbcrich-Flughafen', 'obfelden', 'uster', 'w\xc3\xa4denswil', 'zuerich', 'z\xc3\xbcrich', '\xc3\x9cetliberg']


zurich_raw = ["Winterthur","Zürich","Volketswil","Stäfa","Fällanden","Niederweningen","Ebmatingen","Wetzikon","Au ZH","Dietlikon","Uster","Mettmenstetten ZH","Ottikon","Baden","Fehraltorf","Zuerich","Rümlang","Langnau am Albis","Pfäffikon ZH","8004","Russikon","Aathal-Seegräben","Bassersdorf","Nürensdorf","Wädenswil","Weisslingen","Seegräben","Wettingen","Riedt","Niederhasli","Greifensee","Freudwil","Ehrendingen","Gossau","Adliswil","Affoltern a.A.","Berikon","Birmensdorf (ZH)","Buchs (ZH)","Bonstetten","Bremgarten (AG)","Bülach","Dübendorf","Dietikon","Dielsdorf","Egg (ZH)","Effretikon","Forch","Fislisbach","Freienwil","Embrach","Erlenbach (ZH)","Hedingen","Hausen am Albis","Herrliberg","Grüt","Grüningen","Illnau","Hombrechtikon","Horgen","Küsnacht (ZH)","Kloten","Killwangen","Kilchberg (ZH)","Langnau a.A.","Männedorf","Muri (AG)","Nänikon","Niederrohrdorf","Niederglatt","Nussbaumen","Maur","Meilen","Mettmenstetten","Regensdorf","Rifferswil","Oberglatt","Oberrieden","Obfelden","Opfikon","Ottenbach","Pfaffhausen","Pfäffikon (ZH)","Schwerzenbach","Rüschlikon","Schlieren","Thalwil","Wallisellen","Wiesendangen","Wettswil a. Albis","Wetzikon (ZH)","Uetikon am See","Urdorf","Unterengstringen","Zollikon","Würenlos","Zumikon","Oberweningen","Grafstal","Grafstal/Kempttal","Zürich-Flughafen","Zufikon","Bremgarten","Bremgarten AG","Remetschwil","Wohlen (AG)","Wettswil","Arni (AG)","Madetswil","Gattikon","Bertschikon bei Gossau","Zurich","Lengnau","Zürich 50 Oerlikon","Neerach","Bergdietikon","Spreitenbach","Mönchaltorf","Schneisingen","Oberwil-Lieli","Binz","Baden-Dättwil","Weinigen","Oberengstringen","Widen","Besenbüren","zürich","Neuenhof","Zollikerberg","Zürich-Altstetten","Au (ZH)","Feldbach","Uerikon","Pfäffikon","Glattbrugg","Winterthur-Hegi","Gutenswil","Seuzach","Rikon","Lindau","Affoltern am Albis","Stallikon","uster","Hinteregg","Gossau (ZH)","Wolfhausen","Baltenswil","Oetwil am See","Buchs","Esslingen","Feldmeilen","Mellingen","Üetliberg","Waltenschwil","Rudolfstetten","Watt","Wohlen","zuerich","Erlenbach","Müswangen","Ennetbaden","Oberengstrngen","Oberengstgringen","Oberrohrdorf","Kilchberg","Buchs ZH","Merenschwand","Freienstein-Teufen","Rorbas","Kirchdorf","Uitikon","Hochfelden","Neftenbach","Kilchberg ZH","Zwillikon","Küsnacht","Riedikon","Aathal","Winterberg","Pfungen","Mühlau","Brüttisellen","Weiningen (ZH)","Winkel","Bachenbülach","Nussbaumen bei Baden","Wangen","Benglen","Fahrweid","Wettswil am Albis","Adlikon","Oberembrach","Islisberg","Oberlunkhofen","Glattpark (Opfikon)","Aathal - Seegräben","Niederwil","wädenswil","Tagelswangen","Kemptthal","Eggenwil","Sihlwald","Kyburg","Egg","Glattpark","Unterlunkhofen","Rieden","Ebertswil","Nassenwil","Küsnacht ZH","Aesch","Aeugst am Albis","Waldegg","Muri","Aesch (ZH)","Elsau","Bachs","Stääfa","Agasul","First","Wermatswil","Otelfingen","Luckhausen","Billikon","Kemleten","Bisikon","Oberhasli","Riedikon (Uster)","Sulzbach (Uster)","Egg bei Zürich","Höri","Brütten","Rülang","Bietenholz","Bülachs","Lufingen","Dättlikon","Gockhausen","Wangen bei Dübendorf","Ohringen","Aeugstertal","Stadel","Rikon im Tösstal","Sennhof","Dättwil","8810","Gossau ZH","Bertschikon","Neschwil","Theilingen","Kollbrunn","Grüt (Gossau ZH)","Bubikon","Ottikon (Gossau ZH)","Herschmettlen","Uitikon-Waldegg","Räterschen","50","Kindhausen","Dänikon","obfelden","Niderohrdorf","Uetliberg","Uitikon Waldegg","Winterberg/ZH","Oberwil b. Nürensdorf","Attikon","Beinwil (Freiamt)","Zürich Gockhausen","Schongau","Schleinikon","Steinmaur","Sünikon","Rottenschwil","Weiningen","Geroldswil","Muri AG","Winterberg ZH","Oetwil","Geltwil/AG","Ehremdingen","8002","Regensberg","Bünzen","Buttwil/AG","Nuerensdorf","Nuerendorf","Forch (Aesch, Maur)","Jonen","Hermetschwil-Staffeln","Nesselnbach","Birmensdorf","Kloster Fahr","Boswil","Aristau","Bettwil","Hedingne","Oetwil an der Limmat"
]

extract = process.extract("zurich", zurich_raw, limit=20)
print(extract)
