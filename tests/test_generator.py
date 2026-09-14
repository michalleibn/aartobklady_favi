import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from src.generate_feed import build

class GeneratorTest(unittest.TestCase):
    def test_filters_and_overrides(self):
        root = Path(__file__).resolve().parents[1]
        config = json.loads((root / "config/products.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            config["output_file"] = str(Path(tmp) / "feed.xml")
            cfg = Path(tmp) / "config.json"
            cfg.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
            output = build(cfg, root / "tests/fixtures/source.xml")
            items = ET.parse(output).getroot().findall("SHOPITEM")
            self.assertEqual([i.findtext("ITEM_ID") for i in items], ["71", "205", "689", "206"])
            old_category = "Dům a zahrada > Bydlení a doplňky > Obklady a dlažby > Dekorativní obklady"
            self.assertEqual([i.findtext("CATEGORYTEXT") for i in items],
                             [old_category, old_category, "Stavba a rekonstrukce > Obklady", "Stavba a rekonstrukce > Obklady"])
            for item in items:
                self.assertEqual(len(item.findall("CATEGORYTEXT")), 1)
            for item in items[2:]:
                self.assertIn("keramické obklady", item.findtext("PRODUCTNAME"))
                self.assertEqual(item.findtext("PRICE_VAT"), "3000")
            self.assertIn("Rosa Sulfurea", items[0].findtext("DESCRIPTION"))
            self.assertEqual(items[1].findtext("DELIVERY_DATE"), "35")

if __name__ == "__main__":
    unittest.main()
