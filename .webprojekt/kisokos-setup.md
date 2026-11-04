# Egyszeri Arcápolási Kisokos – élesítés

A feladó és a válaszcím: szeviki1020@gmail.com. A címzett nem kerül Brevo marketinglistára; csak a tranzakciós e-mail API-t hívjuk.

1. A Brevóban hitelesítsd a feladót, és ellenőrizd a tranzakciós küldés engedélyezését. Gmail feladónál a Brevo módosíthatja a technikai feladói domaint.
2. Hozz létre Brevo API-kulcsot. A kulcsot ne tedd fájlba, Gitbe vagy chatbe.
3. Netlify → Project configuration → Environment variables: BREVO_API_KEY, Secret, Functions hatókör, Production környezet.
4. Brevo → Transactional → Settings: a naplók és e-mail-előnézetek megőrzését állítsd 30 napra. A szolgáltató alapbeállítása nem 30 nap. A Netlify beküldések törlése továbbra is kézi.
5. Új deploy szükséges. A Functions listán a kisokos eseményfüggvénynek kell megjelennie.
6. Kérj teszt-PDF-et a saját címedre. Ellenőrizd a Netlify Forms beérkezést, a Functions naplót, a Brevo Transactional naplót és a tényleges levél megérkezését, a PDF linkjét is. A levél sikeres szolgáltatói átvétele még nem bizonyít kézbesítést.

Az eseményt a Netlify platform hitelesíti. A frontend sikerüzenete csak a kérés beérkezését jelenti; a küldési hibák a Functions/Brevo naplóban látszanak. Elutasított/spam Netlify-beküldés nem indít e-mailt. A feladó napi kerete és a Netlify használati korlátai érvényesek.

A letöltési PDF nyilvános statikus fájl, nem jelszóval védett tartalom. A link továbbküldhető. A kitalált adatkezelői mintanév nem helyettesíti a tényleges adatkezelő azonosítását.

Dokumentáció:
- https://docs.netlify.com/build/functions/trigger-on-events/
- https://developers.brevo.com/docs/send-a-transactional-email
- https://help.brevo.com/hc/en-us/articles/360021533839-Manage-your-transactional-logs-and-email-previews
