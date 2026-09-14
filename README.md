AAArtobklady – vlastní feed pro FAVI.cz
Repozitář každý den stáhne zdrojový Shoptet feed, ponechá pouze produkty s kódy 71, 205, 689 a 206, doplní české názvy, popisy, kategorii a parametry a publikuje výsledný `feed.xml` přes GitHub Pages.
První nastavení na GitHubu
Vytvořte veřejný repozitář, například `favi-feed`.
Nahrajte do něj celý obsah této složky a commitněte jej do větve `main`.
Otevřete Settings → Pages a jako Source zvolte GitHub Actions.
Otevřete záložku Actions, vyberte workflow Vytvořit a publikovat FAVI feed a spusťte Run workflow.
Po úspěšném běhu bude feed na adrese:
`https://UZIVATEL.github.io/NAZEV-REPOZITARE/feed.xml`
Automatická aktualizace
Workflow běží:
při změně zdrojových nebo konfiguračních souborů na větvi `main`,
ručně přes `workflow_dispatch`,
denně ve 03:17 UTC.
Cena, URL, hlavní obrázek a další původní údaje se přebírají z živého Shoptet feedu. Český název, popis, kategorie, doba dodání a doplňkové parametry se nastavují v `config/products.json`.
Lokální ověření
```bash
python -m unittest discover -s tests -v
python src/generate_feed.py
python src/validate_feed.py public/feed.xml
```
Důležité
`DELIVERY_DATE` je nastaveno na `35`, protože e-shop uvádí dodání přibližně 4–5 týdnů; FAVI hodnoty 31 a více zobrazuje jako zboží na objednávku.
Před aktivací kampaně zkontrolujte vygenerované názvy, ceny, URL a obrázky přímo v `feed.xml`.
Případnou cenu dopravy lze nastavit v administraci FAVI; nemusí být nutně součástí feedu.
Přidání produktů 689 a 206
Původní konfigurace produktů 71 a 205 zůstává beze změn, včetně kategorií.
Nové produkty mají `CATEGORYTEXT` nastavený na `Stavba a rekonstrukce > Obklady`.
V XML se oddělovač zapisuje jako `&gt;`; po načtení XML jde o tentýž znak `>`.
Názvy nových produktů obsahují „keramické obklady“, protože FAVI při zařazování
zohledňuje také název produktu. Konečné zařazení je nutné ověřit po importu na FAVI.
Specifikace: https://help.favionline.com/en/meanings-and-requirements-for-individual-elements
Cílová kategorie: https://favi.cz/produkty/kategorie/obklady
Rozměry a dodání 4–5 týdnů byly ověřeny na produktových stránkách.
Živý Shoptet feed obsahuje 206, ale při kontrole neobsahoval produkt 689
(ani jeho URL). Nejdříve povolte jeho export do Shoptet FAVI feedu a ověřte,
že https://www.aaartobklady.cz/favi.xml obsahuje `<CODE>689</CODE>`.
Jinak generátor záměrně skončí chybou; nepublikuje neúplný výběr.
`public/feed.xml` zůstává původní ukázkou. GitHub Actions po doplnění 689
do zdrojového feedu stáhne aktuální ceny, URL a obrázky a vygeneruje čtyři produkty.
Lokální regresní test se syntetickými daty prošel; živá generace je blokována chybějícím 689.
Nahraďte `config/products.json`, `src/generate_feed.py`, `tests/test_generator.py`,
`tests/fixtures/source.xml` a `README.md`. Workflow ani validátor změnu nepotřebují.
Po commitu do `main` ověřte úspěšný běh Actions a čtyři položky v publikovaném feedu.
