#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path

REQUIRED = ("ITEM_ID", "PRODUCTNAME", "DESCRIPTION", "CATEGORYTEXT", "PRICE_VAT", "URL", "IMGURL", "DELIVERY_DATE")
ID_FIELDS = ("CODE", "ITEM_ID", "PRODUCTNO", "ITEMGROUP_ID")

def text(node, tag):
    child = node.find(tag)
    return (child.text or "").strip() if child is not None else ""

def set_text(node, tag, value):
    child = node.find(tag)
    if child is None:
        child = ET.SubElement(node, tag)
    child.text = str(value)

def detect_code(node):
    for tag in ID_FIELDS:
        value = text(node, tag)
        if value:
            return value
    return ""

def load_source(url, local_file=None):
    if local_file:
        return Path(local_file).read_bytes()
    request = urllib.request.Request(url, headers={"User-Agent": "AAArtobklady-FAVI-Feed/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()

def add_params(item, params):
    existing = {(text(p, "PARAM_NAME"), text(p, "VAL")) for p in item.findall("PARAM")}
    for name, value in params.items():
        if (name, value) in existing:
            continue
        param = ET.SubElement(item, "PARAM")
        ET.SubElement(param, "PARAM_NAME").text = name
        ET.SubElement(param, "VAL").text = value

def validate_item(item):
    missing = [tag for tag in REQUIRED if not text(item, tag)]
    if missing:
        raise ValueError(f"Produkt {detect_code(item) or '?'} postrádá povinné elementy: {', '.join(missing)}")
    if not text(item, "URL").startswith("https://"):
        raise ValueError(f"Produkt {detect_code(item)} nemá HTTPS URL")
    if not text(item, "IMGURL").startswith("https://"):
        raise ValueError(f"Produkt {detect_code(item)} nemá HTTPS IMGURL")
    try:
        if float(text(item, "PRICE_VAT").replace(",", ".")) <= 0:
            raise ValueError
    except ValueError:
        raise ValueError(f"Produkt {detect_code(item)} má neplatnou PRICE_VAT")
    try:
        delivery = int(text(item, "DELIVERY_DATE"))
        if delivery < 0:
            raise ValueError
    except ValueError:
        raise ValueError(f"Produkt {detect_code(item)} má neplatnou DELIVERY_DATE")

def build(config_path, local_source=None):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    selected = config["products"]
    source = load_source(config["source_feed_url"], local_source)
    root = ET.fromstring(source)
    source_items = root.findall(".//SHOPITEM")
    if not source_items:
        raise ValueError("Zdrojový feed neobsahuje žádné elementy SHOPITEM")

    by_code = {detect_code(item): item for item in source_items if detect_code(item)}
    missing_codes = sorted(set(selected) - set(by_code))
    if missing_codes:
        available = ", ".join(sorted(by_code)[:30])
        raise ValueError(f"Ve zdrojovém feedu nebyly nalezeny kódy: {', '.join(missing_codes)}. Dostupné kódy začínají: {available}")

    output_root = ET.Element("SHOP")
    for code, override in selected.items():
        item = deepcopy(by_code[code])
        set_text(item, "ITEM_ID", code)
        set_text(item, "PRODUCTNAME", override["product_name"])
        set_text(item, "DESCRIPTION", override["description"])
        set_text(item, "CATEGORYTEXT", override["category"])
        set_text(item, "DELIVERY_DATE", override["delivery_date"])
        add_params(item, override.get("params", {}))
        validate_item(item)
        output_root.append(item)

    ids = [text(item, "ITEM_ID") for item in output_root.findall("SHOPITEM")]
    if len(ids) != len(set(ids)):
        raise ValueError("Výstup obsahuje duplicitní ITEM_ID")

    ET.indent(output_root, space="  ")
    output_path = Path(config["output_file"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(output_root).write(output_path, encoding="utf-8", xml_declaration=True)
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Vytvoří dvouproduktový XML feed pro FAVI.cz")
    parser.add_argument("--config", default="config/products.json")
    parser.add_argument("--source-file", help="Lokální XML pouze pro testování")
    args = parser.parse_args()
    try:
        path = build(args.config, args.source_file)
        print(f"Feed vytvořen: {path}")
    except Exception as exc:
        print(f"CHYBA: {exc}", file=sys.stderr)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
