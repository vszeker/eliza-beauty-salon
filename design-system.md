# Eliza Beauty Salon – design system

> **Opcionális alap.** Ha saját arculattal (színekkel, betűkkel, logóval) szeretnél dolgozni, nyugodtan válts. Ilyenkor a saját döntéseidet írd le egy ugyanilyen szerkezetű fájlba, és azt add oda az AI-nak.

Ezt a fájlt add oda az AI-nak a projekt elején (tedd a projektmappába, és hivatkozz rá a briefben). Minden szín, betű és stílus innen jöjjön; ha az AI mást használ, kérd meg, hogy igazodjon ehhez a fájlhoz.

## Hangulat

Nőies, elegáns, nyugodt, prémium, de barátságos. Olyan, mint egy csendes, világos szalon természetes anyagokkal: sok levegő, puha krém- és púdertónusok, finom rózsafa kiemelés.

**Ne legyen:** csillogó, rózsaszín-giccses, túldíszített, harsány. Ne legyen benne neon, erős színátmenet, sötét mód vagy „tech startup” hatás.

## Színek

| Szerep | Név | Hex | Mire |
|---|---|---|---|
| Elsődleges | Rózsafa | `#8E4A5A` | Gombok, linkek, kiemelt címsorok, ikonok |
| Elsődleges sötét | Sötét rózsafa | `#6E3644` | Gomb hover, aktív állapot |
| Akcentus | Homokarany | `#C9A27E` | Csak díszítés: vékony vonalak, kis ikonok, számok sötét háttéren. **Világos háttéren szövegre nem jó.** |
| Háttér | Krém | `#FAF6F2` | Az oldal alap háttere |
| Felület | Púder | `#F1E6DF` | Váltakozó szakasz-háttér, kártyák |
| Szöveg | Sötét kakaó | `#2E2626` | Törzsszöveg, címsorok |
| Másodlagos szöveg | Szürkésbarna | `#6B5F5C` | Leírások, kisebb szövegek, űrlap-címkék |
| Vonal | Halvány púder | `#E3D6CF` | Elválasztók, űrlapmezők kerete |
| Sötét szakasz | Sötét kakaó | `#2E2626` | Lábléc, egy-egy kiemelt CTA-sáv, krém (`#FAF6F2`) szöveggel |

Ellenőrzött kontrasztok (WCAG AA, normál szövegre min. 4,5): szöveg krémen 13,7; másodlagos szöveg krémen 5,7, púderen 5,0; fehér a rózsafán 6,4; rózsafa krémen 6,0; homokarany sötét kakaón 6,3.

## Betűtípusok

Mindkettő ingyenes, a Google Fontsról tölthető be, és van benne magyar ékezet (ő, ű).

- **Címsor:** Cormorant Garamond, 500 és 600 vastagság. Elegáns, vékony talpas betű.
- **Törzsszöveg:** Jost, 400 és 500 vastagság. Letisztult, geometrikus talpatlan betű.
- **Gombok, kis feliratok (kicker):** Jost 500, nagybetűvel, 0,08em ritkítással.

### Méretskála (desktop / mobil)

| Elem | Betű | Desktop | Mobil | Sormagasság |
|---|---|---|---|---|
| H1 | Cormorant Garamond 500 | 64px | 40px | 1,1 |
| H2 | Cormorant Garamond 500 | 44px | 32px | 1,15 |
| H3 | Cormorant Garamond 600 | 28px | 24px | 1,2 |
| Kicker | Jost 500, nagybetű | 14px | 13px | 1,4 |
| Törzs | Jost 400 | 18px | 16px | 1,65 |
| Kis szöveg | Jost 400 | 15px | 14px | 1,5 |
| Gomb | Jost 500, nagybetű | 15px | 15px | 1 |

## Térközök és elrendezés

- Alapegység **8px**: minden térköz ennek többszöröse (8, 16, 24, 32, 48, 64, 96, 128).
- Szakaszok függőleges térköze: desktopon 96–128px, mobilon 64px.
- Tartalom maximális szélessége: 1200px; folyó szöveg max. 680px széles.
- Oldalsó margó mobilon: 20px.

## Komponensek

- **Elsődleges gomb:** rózsafa háttér, fehér szöveg, 16px × 32px belső térköz, 999px lekerekítés (kapszula). Hoverre sötét rózsafa.
- **Másodlagos gomb:** átlátszó háttér, 1px rózsafa keret, rózsafa szöveg, ugyanaz a forma.
- **Kártya:** púder vagy fehér háttér, 16px lekerekítés, nincs vagy csak nagyon halvány árnyék.
- **Képek:** 16px lekerekítés; meleg, természetes fényű fotók, sok bőrtónussal, krém és bézs környezettel.
- **Űrlapmező:** fehér háttér, 1px halvány púder keret, 12px lekerekítés, fókuszra rózsafa keret.
- **Ikonok:** vékony vonalas ikonkészlet (például Lucide vagy Phosphor Light), rózsafa vagy homokarany színben.

## Logó

Szöveges logó: „Eliza” Cormorant Garamonddal, alatta „BEAUTY SALON” Jost betűvel, ritkítva. A `logo/` mappában: `logo.svg` / `logo.png` (világos háttérre), `logo-feher.svg` / `logo-feher.png` (sötét háttérre), valamint `favicon.svg` / `favicon.png` (egy „E” betű).
