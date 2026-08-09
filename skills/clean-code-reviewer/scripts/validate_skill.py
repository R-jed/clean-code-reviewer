#!/usr/bin/env python3
"""
Skill Validator - validates a skill folder against the Agent Skills frontmatter spec.

Usage:
    python scripts/validate_skill.py <path/to/skill-folder>
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


ALLOWED_PROPERTIES = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500


def validate_skill(skill_path):
    """Validate one Agent Skill directory."""
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", content, re.DOTALL)
    if not match:
        return False, "Invalid or missing YAML frontmatter"

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return False, f"Invalid YAML in frontmatter: {exc}"

    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a YAML dictionary"

    unexpected_keys = set(frontmatter) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    name = frontmatter["name"]
    if not isinstance(name, str) or not name.strip():
        return False, "Name must be a non-empty string"
    name = name.strip()
    if len(name) > MAX_NAME_LENGTH:
        return False, f"Name is too long ({len(name)} characters). Maximum is {MAX_NAME_LENGTH} characters."
    if not NAME_PATTERN.fullmatch(name):
        return False, f"Name '{name}' must contain only lowercase letters, digits, and hyphens"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
    if skill_path.name != name:
        return False, f"Directory name '{skill_path.name}' must match skill name '{name}'"

    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"
    description = frontmatter["description"]
    if not isinstance(description, str) or not description.strip():
        return False, "Description must be a non-empty string"
    if len(description) > MAX_DESCRIPTION_LENGTH:
        return False, (
            f"Description is too long ({len(description)} characters). "
            f"Maximum is {MAX_DESCRIPTION_LENGTH} characters."
        )

    if "license" in frontmatter:
        license_value = frontmatter["license"]
        if not isinstance(license_value, str) or not license_value.strip():
            return False, "License must be a non-empty string"

    if "compatibility" in frontmatter:
        compatibility = frontmatter["compatibility"]
        if not isinstance(compatibility, str) or not compatibility.strip():
            return False, "Compatibility must be a non-empty string"
        if len(compatibility) > MAX_COMPATIBILITY_LENGTH:
            return False, (
                f"Compatibility is too long ({len(compatibility)} characters). "
                f"Maximum is {MAX_COMPATIBILITY_LENGTH} characters."
            )

    if "metadata" in frontmatter:
        metadata = frontmatter["metadata"]
        if not isinstance(metadata, dict):
            return False, "Metadata must be a mapping"
        for key, value in metadata.items():
            if not isinstance(key, str) or not isinstance(value, str):
                return False, "Metadata keys and values must be strings"

    if "allowed-tools" in frontmatter:
        allowed_tools = frontmatter["allowed-tools"]
        if not isinstance(allowed_tools, str) or not allowed_tools.strip():
            return False, "Allowed-tools must be a non-empty string"

    return True, "Skill is valid!"


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_skill.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(f"{'✅' if valid else '❌'} {message}")
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
