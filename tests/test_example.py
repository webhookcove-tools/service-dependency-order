"""Pinned deterministic example; no inference or network access."""
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('tool',ROOT/'main.py');tool=importlib.util.module_from_spec(spec);spec.loader.exec_module(tool)
class ExampleTest(unittest.TestCase):
    def test_documented_example(self):
        self.assertEqual(tool.analyze(json.loads((ROOT/'examples/input.json').read_text())),json.loads((ROOT/'examples/expected.json').read_text()))
if __name__=='__main__':unittest.main()
