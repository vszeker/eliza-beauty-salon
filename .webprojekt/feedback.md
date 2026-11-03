# Következő módosítások alapja

- A felhasználó az első és második irány között választ, inkább az első felé húz.
- Legfrissebb döntés: mostantól kizárólag az első koncepción szabad módosítani. A második és harmadik változatot meg kell őrizni.
- Több kép szükséges; a stockfotókat később saját fotók váltják.
- Az első koncepcióban változatosabb képlekerekítések és a képek mögött végigvezetett grafikai elem a kért irány.
- A feltöltött saját képanyag bekerült mindkét mintaoldalra: az első hét, a második hat különböző fotót használ. A PNG-k fehér vászonszéleit a külön webes változatokból levágtuk; az eredetik változatlanok. Az oldalak az `images/website/` WebP-fájljait használják, reszponzív `srcset` és `sizes` attribútumokkal. A pontos forrás- és kivágáslista: `.webprojekt/website-images.json`.

## Elkészült finomítás
- Legfrissebb elsőoldali módosítás: új nyitókép (`mask-care.webp`), új kezelési kép a bemutatkozás mellett (`facial-care.webp`), a végigfutó vonal eltávolítva. A galéria három függőlegesen elcsúsztatott képet tartalmaz, mobilon vízszintesen lapozható. A kapcsolat résznél külön kiemelt nyitvatartási panel és címkézett cím/telefon/e-mail blokk készült.
- Első irány: íves felső képszél, aszimmetrikus lekerekítések, eltolt púder/krém alátétek és finom homokarany vonal. További kezelési és hangulatfotók a szolgáltatásoknál, a bemutatkozás mellett, a folyamat utáni képpárban és a Kisokosnál.
- Második irány: széles fotó a folyamat alatt, képpár a bemutatkozás után, hangulatfotó a Kisokosnál.
- A harmadik HTML és a választóoldal nem módosult.

## Képcsere saját fotókra
A HTML-fájlokban az `images/` mappára hivatkozó `src` értékek cserélhetők. A képaláírásokat és az alternatív szövegeket is a saját fotóhoz kell igazítani.
- `treatment.jpg`: a nyitóblokk kezelési képe; az elsőn álló, a másodikon fekvő kivágás.
- `facial-care.jpg`: kezelési részletek, álló és fekvő képkivágással.
- `spa-interior.jpg`: hangulati részletek a bemutatkozásnál, képpárban vagy feliratkozásnál.
- `skincare.jpg`: bőrápolási termékhangulat.
Az eredeti fájlnevek felülírásával végzett képcsere a harmadik irányt is érintené; a harmadik érintetlensége érdekében a saját fotók új fájlnevet kapjanak, és csak az első/második HTML-ben módosuljon a hivatkozás.
