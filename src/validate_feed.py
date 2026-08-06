#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REQUIRED = ("ITEM_ID", "PRODUCTNAME", "DESCRIPTION", "CATEGORYTEXT", "PRICE_VAT", "URL", "IMGURL", "DELIVERY_DATE")
path = Path(sys.argv[1] if len(sys.argv) > 1 else "public/feed.xml")
root = ET.parse(path).getroot()
items = root.findall("SHOPITEM")
assert root.tag == "SHOP", "Kořen musí být SHOP"
assert len(items) == 2, f"Očekávány 2 produkty, nalezeno {len(items)}"
ids = []
for item in items:
    for tag in REQUIRED:
        assert item.find(tag) is not None and (item.findtext(tag) or "").strip(), f"Chybí {tag}"
    ids.append(item.findtext("ITEM_ID").strip())
assert set(ids) == {"71", "205"}, f"Neočekávané ITEM_ID: {ids}"
assert len(ids) == len(set(ids)), "Duplicitní ITEM_ID"
print(f"OK: {path} obsahuje produkty 71 a 205 a všechny povinné elementy.")
