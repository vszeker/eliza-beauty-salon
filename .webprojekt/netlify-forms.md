# Netlify Forms — kapcsolati űrlapok

Dokumentáció: https://docs.netlify.com/manage/forms/setup/ és https://docs.netlify.com/manage/forms/spam-filters/

- A felhasználó megerősítette, hogy a form detection aktív.
- Statikus POST űrlapok: `idopontkeres-index`, `idopontkeres-kezelesek`, `idopontkeres-rolunk`, `idopontkeres-kapcsolat`.
- Minden formban `data-netlify="true"`, egyező rejtett `form-name`, valamint `bot-field` honeypot.
- Név, e-mail, üzenet mezők; `name="email"` a Netlify válaszcím funkciójához.
- JavaScript: URL-encoded POST `/` végpontra, válaszkód ellenőrzés, dupla küldés elleni védelem, siker/hiba státusz. Hiba esetén az adatokat megtartja.
- JavaScript nélkül natív POST `/koszonjuk.html` sikeroldalra. A sikeroldal noindex, nincs a sitemapben.
- A hírlevél és Kisokos továbbra is bemutató, nincs feliratkozás.
- A kapcsolati adatkezelési leírás a Netlify Forms használatát követi; a tényleges adatkezelő, megőrzési idő és további végleges adatok még pontosítandók.
- Értesítési e-mail nincs a HTML-be beégetve. A Netlify Forms / Submission notifications alatt állítható be: https://docs.netlify.com/manage/forms/notifications/
- Az integrációs teszt helyi szerveren szimulál sikeres, HTTP-hibás és hálózati hibás választ; nem küld valós levelet vagy személyes adatot.
