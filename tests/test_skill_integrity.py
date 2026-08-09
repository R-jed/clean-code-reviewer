import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "clean-code-reviewer"
VALIDATOR_PATH = SKILL_DIR / "scripts" / "validate_skill.py"

spec = importlib.util.spec_from_file_location("validate_skill", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def write_skill(parent, directory_name="sample-skill", frontmatter=None):
    skill_dir = Path(parent) / directory_name
    skill_dir.mkdir()
    data = frontmatter or {
        "name": directory_name,
        "description": "A valid test skill used for validator regression tests.",
    }
    body = yaml.safe_dump(data, sort_keys=False)
    (skill_dir / "SKILL.md").write_text(f"---\n{body}---\n\n# Test\n", encoding="utf-8")
    return skill_dir


def extract_rule_numbers(path, prefix):
    text = path.read_text(encoding="utf-8")
    pattern = rf"^\|\s*{prefix}-(\d+)\s*\|"
    return [int(value) for value in re.findall(pattern, text, flags=re.MULTILINE)]


class ValidatorTests(unittest.TestCase):
    def test_repository_skill_is_valid(self):
        valid, message = validator.validate_skill(SKILL_DIR)
        self.assertTrue(valid, message)

    def test_empty_name_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = write_skill(tmp, frontmatter={"name": "", "description": "Valid description"})
            valid, _ = validator.validate_skill(skill)
            self.assertFalse(valid)

    def test_whitespace_description_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = write_skill(tmp, frontmatter={"name": "sample-skill", "description": "   "})
            valid, _ = validator.validate_skill(skill)
            self.assertFalse(valid)

    def test_top_level_version_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = write_skill(
                tmp,
                frontmatter={
                    "name": "sample-skill",
                    "description": "Valid description",
                    "version": "1.0.0",
                },
            )
            valid, message = validator.validate_skill(skill)
            self.assertFalse(valid)
            self.assertIn("Unexpected key", message)

    def test_compatibility_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = write_skill(
                tmp,
                frontmatter={
                    "name": "sample-skill",
                    "description": "Valid description",
                    "compatibility": "Requires Python 3.11+",
                },
            )
            valid, message = validator.validate_skill(skill)
            self.assertTrue(valid, message)

    def test_metadata_requires_string_keys_and_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = write_skill(
                tmp,
                frontmatter={
                    "name": "sample-skill",
                    "description": "Valid description",
                    "metadata": {"version": 1.0},
                },
            )
            valid, _ = validator.validate_skill(skill)
            self.assertFalse(valid)

    def test_allowed_tools_requires_string(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = write_skill(
                tmp,
                frontmatter={
                    "name": "sample-skill",
                    "description": "Valid description",
                    "allowed-tools": ["Read"],
                },
            )
            valid, _ = validator.validate_skill(skill)
            self.assertFalse(valid)

    def test_name_must_match_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = write_skill(
                tmp,
                directory_name="directory-name",
                frontmatter={"name": "different-name", "description": "Valid description"},
            )
            valid, message = validator.validate_skill(skill)
            self.assertFalse(valid)
            self.assertIn("must match skill name", message)


class RepositoryIntegrityTests(unittest.TestCase):
    def test_frontmatter_uses_spec_fields(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        self.assertIsNotNone(match)
        metadata = yaml.safe_load(match.group(1))
        self.assertNotIn("version", metadata)
        self.assertEqual(metadata["metadata"]["version"], "1.4.0")
        self.assertEqual(metadata["license"], "MIT")

    def test_rule_inventory_is_exact(self):
        refs = SKILL_DIR / "references"
        cc = extract_rule_numbers(refs / "clean-code.md", "CC")
        pp = extract_rule_numbers(refs / "pragmatic-programmer.md", "PP")
        ca = extract_rule_numbers(refs / "clean-architecture.md", "CA")

        expected_cc = set(range(1, 64)) | set(range(78, 203))
        self.assertEqual(set(cc), expected_cc)
        self.assertEqual(len(cc), 188)
        self.assertEqual(len(cc), len(set(cc)))

        self.assertEqual(set(pp), set(range(1, 101)))
        self.assertEqual(len(pp), 100)
        self.assertEqual(len(pp), len(set(pp)))

        self.assertEqual(set(ca), set(range(1, 49)))
        self.assertEqual(len(ca), 48)
        self.assertEqual(len(ca), len(set(ca)))

        self.assertEqual(len(cc) + len(pp) + len(ca), 336)

    def test_rule_inventory_documentation_matches_sources(self):
        text = (SKILL_DIR / "docs" / "rule-sources.md").read_text(encoding="utf-8")
        self.assertIn("350 source-numbered rules", text)
        self.assertIn("336 active review rules", text)
        self.assertIn("| **CC-##** | Clean Code | 202 | 188 |", text)
        self.assertIn("| **Total** | | **350** | **336** |", text)

    def test_dry_threshold_example_matches_l3_policy(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("L3: max 3 → report on 4th occurrence", text)
        self.assertIn("Duplicate validation knowledge (4th occurrence)", text)
        self.assertNotIn("Duplicate validation logic (3rd occurrence)", text)

    def test_features_verdict_matches_skill_verdict(self):
        text = (SKILL_DIR / "docs" / "features.md").read_text(encoding="utf-8")
        self.assertIn("≥3 Critical or fundamental design problem", text)
        self.assertIn("Any Critical or >2 Important", text)
        self.assertIn("0 Critical and ≤2 Important", text)

    def test_known_rule_mappings_are_correct(self):
        glossary = (SKILL_DIR / "references" / "principles-glossary.md").read_text(encoding="utf-8")
        spectrum = (SKILL_DIR / "references" / "principles-spectrum.md").read_text(encoding="utf-8")
        lookup = (SKILL_DIR / "references" / "quick-lookup.md").read_text(encoding="utf-8")

        self.assertIn("CC-127", glossary)
        self.assertIn("Plugin Architecture** | Details as plugins to core | CA-47", glossary)
        self.assertIn("Humble Object** | Isolate hard-to-test code | CA-32, CA-46", glossary)
        self.assertIn("| CC-127 | Contains No Duplication |", spectrum)
        self.assertIn("PP-15, CC-37, CC-127, CC-155", lookup)

    def test_positioning_has_sixteen_terminal_combinations(self):
        text = (SKILL_DIR / "references" / "positioning.md").read_text(encoding="utf-8")
        self.assertIn("| Valid terminal combinations | 16 |", text)


if __name__ == "__main__":
    unittest.main()
