# Webre optimalizált képek

Az eredeti képek az `images/` mappában változatlanul megmaradtak.

Minden forrásképhez három WebP-verzió készült:
- `név.webp`: nagy változat, legfeljebb 1600 × 1600 pixeles befoglaló méretben, eredeti képaránnyal. Az új 1080 × 1350 pixeles PNG-k mérete ebben a változatban megmaradt.
- `név-800w.webp`: 800 pixel széles változat.
- `név-480w.webp`: 480 pixel széles változat.

Nincs nagyítás és nincs képkivágás. A képekbe épített fehér margók is megmaradtak; az oldalon való elhelyezéskor szükség esetén külön vágott változat készíthető. WebP-minőség: 84, optimalizálási fokozat: 6. A tájolást a konvertálás figyelembe veszi, a beágyazott színprofilt sRGB-re alakítja, ha van ilyen. Személyes metaadatokat a kimenetek nem tartalmaznak.

Összesen 23 forrásból 69 WebP készült. A nagy változatok együtt 1 056 656 bájtot tesznek ki az eredeti 14 329 951 bájt helyett (92,6% csökkenés). A háromféle méret együtt 1 828 234 bájt.

Az oldalak képhivatkozásai nem módosultak. A harmadik koncepció változatlan.

Részletes méret- és fájllista: `.webprojekt/image-optimization.json` a projekt gyökeréhez viszonyítva.
