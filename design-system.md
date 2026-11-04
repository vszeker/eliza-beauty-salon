# Eliza Beauty Salon — design system 1.0

Rögzítve: 2026. november 3. A kiválasztott **Csendes énidő** legutóbbi első változatának kötelező vizuális alapja a további oldalakhoz. Forrás: `koncepcio-1-csendes-enido.html`, `public/index.html`. A korábbi opcionális alap: `.webprojekt/design-system-original.md`.

Böngészhető mintatár: `design-system/index.html`. Újrahasználható CSS-változók: `design-system/tokens.css`.

## Márka és kommunikáció
Nyugodt, személyes, gondoskodó, nőies, barátságosan prémium. Magyar tegező szövegek, Eliza egyes szám első személyben beszél. Elsődleges célcsoport: 35 év feletti budapesti nők. Másodlagos: problémás bőrrel küzdő fiatalok és szüleik.
Fő CTA: **Időpontot kérek**. Másodlagos: **Megnézem a kezeléseket**. Új eredményígéretet, árat, véleményt nem találunk ki.

## Színek
| Token | Érték | Használat |
|---|---|---|
| --color-brand-primary | #8E4A5A | Rózsafa, gomb és link |
| --color-brand-secondary | #6E3644 | Sötét rózsafa, hover |
| --color-brand-accent | #C9A27E | Homokarany, dekoráció és vékony képkeret |
| --color-brand-bg | #FAF6F2 | Krém oldalháttér |
| --color-brand-surface | #F1E6DF | Púder szakasz és kártya |
| --color-brand-text | #2E2626 | Kakaó szöveg, láblécháttér |
| --color-brand-muted | #6B5F5C | Másodlagos szöveg |
| --line | #E3D6CF | Halvány elválasztó és mezőkeret |
| --color-line-strong | #D8C5BA | Elválasztó púder felületen |
| --color-white | #FFFFFF | Űrlap, véleményszakasz, gombfelirat |

Homokarany világos alapon nem szövegszín. Gombfelirat fehér. Lábléc: kakaó háttér, krém/világos púder szöveg. Számított kontrasztok a mintatárban.

## Tipográfia
Cormorant Garamond 500/600: címsorok. Jost 400/500: szöveg és UI. Fallback: Georgia, serif és system-ui, sans-serif. Magyar ékezetekkel, Google Fonts display=swap betöltéssel.

| Elem | Asztali érték | Mobil | Sormagasság |
|---|---|---|---|
| H1, 500 | clamp(40px,4.8vw,64px) | min. 40px | 1.12 |
| H2, 500 | clamp(32px,3.6vw,44px) | min. 32px | 1.12 |
| H3, 600 | 28px | 24–28px, szereptől függően | 1.12–1.2 |
| Kezelési kártyacím, 600 | 29px | 28px | 1.15 |
| Törzs, 400 | 18px | 16px | 1.65 |
| Kártyaszöveg | 16px | 16px | 1.6 |
| Gomb, 500 | 15px | 15px | 1.3 |
| Kicker | 14px | 13px | 1.65 |
| Képaláírás | 12px | 11–12px | 1.5 |
| Segédszöveg | 13–15px | 13–15px | 1.5–1.6 |

H1 betűköz −0.025em; H2 −0.02em; gomb +0.035em. Kicker: mondatkezdő nagybetű, rövid homokarany vonal előtte. Nem minden cím fölé kell kicker. Egy H1 oldalanként, utána H2 szakaszok és H3 komponenscímek.

## Elrendezés
- Maximum 1200px széles konténer: min(1200px, calc(100% - 80px)).
- 1000px alatt oldalanként 24px, 760px alatt 20px margó.
- Térközskála: 8,16,24,32,40,48,64,96,104px. Komponenseknél 12,20,28,56,80px is megjelenik.
- Normál szakasz: 104px függőleges padding, mobilon 64px.
- Két oszlop: általában 96px köz; 1000px alatt 48px; 760px alatt egy oszlop, 40px köz.
- Törzsszöveg maximum 620–680px; rövid bevezető 460–480px.
- Fejléc: sticky, 112px, mobilon 88px; horgonyokhoz felső görgetési térköz.
- Töréspontok: 1000px, 760px, 600px, 420px.

## Képek és formák
| Szerep | Végleges lekerekítés |
|---|---|
| Nyitókép | 48% 48% 24px 24px; mobilon alsó 20px |
| Nagy termékkép | 24px 44% 24px 44% |
| Bemutatkozás képe | 24px 120px 24px 24px |
| Galéria 1 | 140px 140px 24px 24px |
| Galéria 2 | 24px 24px 140px 140px |
| Galéria 3 | 100px 24px 100px 24px |
| Kisokos képe | 16px 90px 16px 90px |
| Kártya | 20px |
| Panel | 16px |
| Mező | 12px |
| Gomb | 999px |

Fontos nagykép mögött eltolt púder/krém alátét és finom homokarany keret jelenhet meg. A végigfutó vonalat elvetettük, nem része a rendszernek. A nyitvatartás címe előtt nincs pötty.
Képek: meleg fény, természetes bőr, bézs/púder környezet; kezelési kártyára tényleges kezelési fotó. Egy kép egyszer szerepeljen ugyanazon az oldalon. Modellt nem nevezünk Elizának.
WebP, srcset/sizes, valós width/height, tárgyhoz igazított object-fit:cover fókusz. Eredeti fájl megmarad; a fehér vászonszélt a webes változatból levágjuk. Nincs mesterséges nagyítás. Nyitókép eager/fetchpriority=high, további képek lazy/decoding=async. Megosztási kép külön 1200×630 JPEG.

## Komponensek
### Gomb és link
Elsődleges: rózsafa háttér, fehér szöveg, 1px keret, minimum 52px magasság, 16×32px padding. Hover sötét rózsafa. Másodlagos: átlátszó háttér, rózsafa keret/szöveg, púder hover. Fókusz: 3px rózsafa körvonal 5px eltartással. Átmenet 0.2s ease-out.
Művelethez button, navigációhoz link. Kártyalink: alsó elválasztó, visszafogott nyíl.
### Fejléc és lábléc
Meglévő SVG-logók, világos fejléc finom alsó vonallal. Menü: Főoldal, Kezelések, Rólunk, Kapcsolat, időpontkérő gomb. Aktív oldal jelölve. Mobilmenü: Menü/Bezárás, aria-expanded, Escape, linkválasztás utáni bezárás. Kakaó lábléc, fehér logó, három oszlop; mobilon egymás alatt.
### Kezelési kártyák
Három egyenlő oszlop, 28px köz; 1000px alatt 20px, 760px alatt egy oszlop. Púder felület, nincs árnyék. Kép 250px magas, szűk asztali nézetben 210px, mobilon 260px. Belső tér 28px, kisebb nézetben 24px. A linkek alul egy vonalban végződnek.
### Galéria
Három kép, 0/88/32px függőleges eltolással. 1000px alatt 24px köz és 310px kép, 760px alatt 20px köz és 240px kép. 600px alatt oldalra lapozható, 76% széles képekkel és scroll-snap igazítással, 330px képmagassággal. Nincs automatikus lejátszás.
### Vélemény és folyamat
Két meglévő idézet, fehér szakaszon, mobilon egymás alatt. Nincs kitalált csillagszám vagy vendégadat. Sorszám csak a négylépéses folyamatnál.
### GYIK
Natív details/summary, plusz/mínusz jelzés, finom elválasztó, billentyűzetfókusz. Látható válaszok és FAQ JSON-LD egyezzenek.
### Űrlap
Fehér mező, 1px halvány púder keret, 12px sugár, 13×16px padding, 16px szöveg. Látható címke, nem csak placeholder. Textarea minimum 132px, függőlegesen átméretezhető. Név/e-mail/üzenet; adatkezelési hivatkozás. Státusz: role=status, aria-live=polite.
A jelenlegi formok bemutatók, adatot nem küldenek. Hibaállapot a mintatárban **javasolt** az éles bekötéshez: szöveges magyarázat, aria-invalid és aria-describedby; ne csak szín jelezzen hibát. Működő sikerállapotot csak valódi backend-visszaigazolás után mutatunk.
### Kapcsolat és nyitvatartás
Balra bevezető/nyitvatartás/elérhetőségek, jobbra űrlap. Asztali nézetben a két oszlop alja egy vonalban; nincs sticky űrlap. Mobilon természetes sorrendben egymás alatt.
Nyitvatartás: púder panel, 16px sugár, 20×24px padding, rózsafa szegély és 6–7px-rel eltolt halvány kontúr. Cím Jost 500 17px, pötty nélkül. Nap 15px, idő Jost 500 20px, hétvége 14px, feltétel 13px. Telefon és e-mail címkézett kattintható link.
### Kisokos
Púder panel, 16px sugár. Asztali nézetben balra űrlap, jobbra szöveg/kép. Padding 56×64px, oszlopköz 80px; 1000px alatt 40px; mobilon 32×24px, 420px alatt 28×20px. Mobilon előbb szöveg/kép, utána űrlap. Jelenlegi kép: a 17-es krémtextúra.

## Mozgás és hozzáférhetőség
Rövid ease-out interakciók, finom egyszeri hero-belépés. Nincs folyamatos animáció, parallax vagy futó vonal. prefers-reduced-motion esetén animáció és sima görgetés kikapcsol.
Billentyűzettel minden funkció elérhető, fókusz mindig látszik. Dekoráció aria-hidden; tartalmi kép leíró altot kap. Modális ablak bezárható és visszaadja a fókuszt. Kontrasztellenőrzés minden új színpárosításhoz.

## Aloldalak szabályai
| Oldal | Szerkezet |
|---|---|
| Kezelések | Rövidebb hero, kezelési kategóriák, forrás szerinti csomagok/árak, garancia, időpontkérés |
| Rólunk | Történet, szakmai háttér, értékek, kezelési/hangulatfotó; saját portré csak ha rendelkezésre áll |
| Kapcsolat | Egyetlen kontaktűrlap, elérhetőségek, nyitvatartás, GYIK; nincs megismételt alsó űrlap |
| Adatkezelés | Maximum 680px szövegoszlop, jóváhagyott szöveg, díszgaléria nélkül |
Minden oldalon egységes fejléc, lábléc, tipográfia, CTA és formanyelv; nem kell minden főoldali komponenst megismételni.

## Fejlesztési átadás
A tokens.css újrahasználható alap, nem teljes komponenskönyvtár. A mintatár a kiválasztott oldal tényleges CSS-ét/komponensrészleteit használja. A főoldal történeti CSS-felülírásai helyett az új oldalakhoz a fenti végső értékeket alkalmazzuk. A közös CSS-re bontás külön fejlesztési lépés, vizuális regresszióellenőrzéssel.
A design system elkészítése nem módosítja a főoldalt. Minden későbbi oldalmódosítás a forrásban és a public megfelelőjén is átvezetendő. A dokumentáció/mintatár munkaanyag: nem kerül a public mappába.

## Többoldalas megvalósítás
Az új belépési pont az index.html, a további oldalak: kezelesek.html, rolunk.html, kapcsolat.html, adatkezeles.html. A közös megjelenés az assets/site.css, az interakciók az assets/site.js fájlba kerültek; a public mappa ezeket és az oldalakat tartalmazza. A korábbi koncepciófájlok archív minták.

Aloldali szakaszkezdés: nincs Főoldal / … morzsamenü. A rövid kategóriafelirat marad, a hero felső térköze 48px, mobilon 24px. A Mesotica kártya és részletképe a 27-es meleg tónusú kezelési fotó.
