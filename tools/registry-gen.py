#!/usr/bin/env python3
"""
SKILLS Registry Generator
=========================

Generates REGISTRY.yaml from all SKILL.md files found in the repository.

Usage:
    python tools/registry-gen.py [--output REGISTRY.yaml]
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


def extract_frontmatter(content: str) -> dict[str, Any] | None:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return None
    
    # Find the end of frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    
    frontmatter_text = parts[1]
    
    try:
        return yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return None


def get_skill_files(root_dir: Path) -> list[Path]:
    """Find all SKILL.md files in the repository."""
    skill_files = []
    
    for path in root_dir.rglob("SKILL.md"):
        # Skip .git and other hidden directories
        if ".git" in path.parts:
            continue
        skill_files.append(path)
    
    return sorted(skill_files)


def determine_source(path: Path) -> str:
    """Determine the source type (native/external) from path."""
    parts = path.parts
    
    if "native" in parts:
        return "native"
    elif "external" in parts or "ext" in parts:
        return "external"
    else:
        return "unknown"


def determine_type(path: Path) -> str:
    """Determine the skill type from path."""
    parts = path.parts
    
    if "foundational" in parts:
        return "foundational"
    elif "domain" in parts:
        return "domain"
    else:
        return "external"


def generate_registry(skill_files: list[Path], root_dir: Path) -> dict[str, Any]:
    """Generate the registry dictionary from skill files."""
    skills = []
    
    for skill_file in skill_files:
        try:
            content = skill_file.read_text(encoding="utf-8")
            frontmatter = extract_frontmatter(content)
            
            if not frontmatter:
                print(f"Warning: No valid frontmatter in {skill_file}", file=sys.stderr)
                continue
            
            # Build skill entry
            relative_path = skill_file.relative_to(root_dir)
            
            skill_entry = {
                "name": frontmatter.get("name", ""),
                "description": frontmatter.get("description", ""),
                "type": determine_type(skill_file),
                "triggers": frontmatter.get("triggers", []),
                "domain": frontmatter.get("domain", ""),
                "version": frontmatter.get("version", "1.0.0"),
                "author": frontmatter.get("author", "gerivdb"),
                "license": frontmatter.get("license", "MIT"),
                "status": frontmatter.get("status", "active"),
                "created": frontmatter.get("created", datetime.now().strftime("%Y-%m-%d")),
                "updated": frontmatter.get("updated", datetime.now().strftime("%Y-%m-%d")),
                "phi_weight": frontmatter.get("phi_weight", 0.001),
                "path": str(relative_path),
                "source": determine_source(skill_file),
                "assimilation_status": "N/A" if determine_source(skill_file) == "native" else "pending"
            }
            
            # Add dependencies if present
            if "deps" in frontmatter:
                skill_entry["consumes_from"] = frontmatter["deps"]
            
            skills.append(skill_entry)
            
        except Exception as e:
            print(f"Error processing {skill_file}: {e}", file=sys.stderr)
    
    # Calculate total φ-CPS contribution
    phi_contribution = sum(s.get("phi_weight", 0.001) for s in skills)
    
    registry = {
        "registry": {
            "version": "1.0.0",
            "ecosystem": "ecosystem-1",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "total_skills": len(skills)
        },
        "skills": skills,
        "metadata": {
            "phi_cps_contribution": round(phi_contribution, 3),
            "governance_level": "L2",
            "citizen": "skills-registry",
            "lifecycle": "GENESIS"
        }
    }
    
    return registry


def main():
    parser = argparse.ArgumentParser(
        description="Generate REGISTRY.yaml from SKILL.md files"
    )
    parser.add_argument(
        "--output", "-o",
        default="REGISTRY.yaml",
        help="Output file path (default: REGISTRY.yaml)"
    )
    parser.add_argument(
        "--root", "-r",
        default=".",
        help="Root directory to scan (default: .)"
    )
    
    args = parser.parse_args()
    
    root_dir = Path(args.root).resolve()
    output_file = Path(args.output)
    
    if not root_dir.exists():
        print(f"Error: Directory {root_dir} does not exist", file=sys.stderr)
        sys.exit(1)
    
    print(f"Scanning {root_dir} for SKILL.md files...")
    skill_files = get_skill_files(root_dir)
    
    if not skill_files:
        print("No SKILL.md files found", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found {len(skill_files)} skill files")
    
    registry = generate_registry(skill_files, root_dir)
    
    # Write output
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# SKILLS Registry — Index Canonical\n")
        f.write(f"# Generated: {datetime.now().isoformat()}\n")
        f.write("# Version: 1.0.0\n")
        f.write("# IntentHash: 0xA3F2E891_SKILLS_REGISTRY_INIT_20260317\n")
        f.write("\n")
        
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False)
    
    print(f"Registry generated: {output_file}")
    print(f"Total skills: {registry['registry']['total_skills']}")
    print(f"φ-CPS contribution: {registry['metadata']['phi_cps_contribution']}")


if __name__ == "__main__":
    main()
