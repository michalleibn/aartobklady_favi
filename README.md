# AAArtobklady – vlastní feed pro FAVI.cz

Repozitář každý den stáhne zdrojový Shoptet feed, ponechá pouze produkty s kódy **71** a **205**, doplní české názvy, popisy, kategorii a parametry a publikuje výsledný `feed.xml` přes GitHub Pages.

## První nastavení na GitHubu

1. Vytvořte veřejný repozitář, například `favi-feed`.
2. Nahrajte do něj celý obsah této složky a commitněte jej do větve `main`.
3. Otevřete **Settings → Pages** a jako **Source** zvolte **GitHub Actions**.
4. Otevřete záložku **Actions**, vyberte workflow **Vytvořit a publikovat FAVI feed** a spusťte **Run workflow**.
5. Po úspěšném běhu bude feed na adrese:
   `https://UZIVATEL.github.io/NAZEV-REPOZITARE/feed.xml`

## Automatická aktualizace

Workflow běží:

- při změně zdrojových nebo konfiguračních souborů na větvi `main`,
- ručně přes `workflow_dispatch`,
- denně ve 03:17 UTC.

Cena, URL, hlavní obrázek a další původní údaje se přebírají z živého Shoptet feedu. Český název, popis, kategorie, doba dodání a doplňkové parametry se nastavují v `config/products.json`.

## Lokální ověření

```bash
python -m unittest discover -s tests -v
python src/generate_feed.py
python src/validate_feed.py public/feed.xml
```

## Důležité

- `DELIVERY_DATE` je nastaveno na `35`, protože e-shop uvádí dodání přibližně 4–5 týdnů; FAVI hodnoty 31 a více zobrazuje jako zboží na objednávku.
- Před aktivací kampaně zkontrolujte vygenerované názvy, ceny, URL a obrázky přímo v `feed.xml`.
- Případnou cenu dopravy lze nastavit v administraci FAVI; nemusí být nutně součástí feedu.
