# Teljesítmény-optimalizálás — 2026. november 4.

Kapott jelentés: https://pagespeed.web.dev/analysis/https-app-netlify-com-edge-access/83bggkyrq5?form_factor=mobile

A jelentés elérhető szövegében mobil Performance 30, FCP 13,0 s, LCP 19,8 s, TBT 1330 ms és 5506 KiB összes adat szerepel. A jelentés URL-je a Netlify edge-access beléptető oldalára utal, nem az Eliza tartalmi oldalára. Az Eliza főoldalának független HTTP-lekérése 401-et adott. A Netlify beléptető oldalának nagy JavaScript-terhelése nem rendelhető a saját, néhány KB-os site.js fájlhoz; ezt a jelentést nem használjuk az Eliza előtte/utána összehasonlítására.

## Elvégzett módosítások
- Cormorant Garamond és Jost: saját tárhelyről betöltött, változó WOFF2. Csak latin és latin-ext; 4 fájl, összesen 115 056 bájt. A fontlicencek mellékelve.
- Megszűnt a Google Fonts CSS és a két külső fontdomain-kapcsolat. A helyi mobiloldalon mért külső kérések száma: 0.
- A két alap latin font előtöltése, font-display:swap; a magyar ékezetes részhalmazok a CSS unicode-range alapján töltődnek.
- A fontos nyitókép reszponzív preload jelölést kapott, az img srcset/sizes beállításával egyezően.
- A főoldali szöveg és nyitókép kezdeti belépő animációja megszűnt, azonnal láthatóak.
- CSS kommentek/felesleges whitespace eltávolítva; azonosítót kapó CSS/JS-fájlnevek tartalmi hash alapján. A verziózott assetek hosszú immutable cache-t, a képek rövid újraellenőrzési ablakot kapnak a public/_headers fájlban.
- Az adatkezelési technikai leírás már a helyi betűbetöltést tükrözi.

## Ellenőrzés
- Öt oldal × három képernyőméret: 15 ellenőrzés, 0 hiba.
- Magyar betűkészlet, 4 betöltött font-face, működő nyitókép-preload, 0 külső kérés: `.webprojekt/qa/performance-resources.json`.
- Nem állítunk új Lighthouse-pontszámot vagy mérés nélküli LCP-gyorsulást.
- Érdemi új PageSpeed-méréshez a https://elizaweboldal.netlify.app/ URL-t a mérőszolgáltatásnak hozzáférhetővé kell tenni. A hozzáférésvédelmet nem módosítottuk.

Hivatalos háttér: https://web.dev/articles/font-best-practices és https://web.dev/articles/optimize-lcp
