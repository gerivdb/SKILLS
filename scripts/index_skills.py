#!/usr/bin/env python3
"""
Index all skills from perplexity/*.md into zvec index.
Usage: python scripts/index_skills.py
"""
import json
import re
import sys
from pathlib import Path

# Allow importing project's ZVecManager if present
sys.path.insert(0, str(Path.cwd()))
try:
    from tools.core.zvec_manager import ZVecManager
except Exception:
    class ZVecManager:
        def __init__(self, data_dir=None):
            if data_dir is None:
                data_dir = Path.cwd() / 'data' / 'zvec'
            self.data_dir = Path(data_dir)
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.index = []
        def add_text(self, doc_id, text, metadata=None):
            entry = {'id': doc_id, 'text': text, 'metadata': metadata or {}}
            self.index.append(entry)
            out = {'size': len(self.index), 'entries': self.index}
            with open(self.data_dir / 'zvec_index.json', 'w', encoding='utf-8') as f:
                json.dump(out, f, ensure_ascii=False, indent=2)
        def get_stats(self):
            return {'size': len(self.index)}


def parse_frontmatter(md_text):
    """Return dict with keys found in frontmatter: name, description"""
    fm = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", md_text, re.S)
    if not m:
        return fm
    body = m.group(1)
    # look for name
    name_m = re.search(r"^\s*name:\s*(?:\"|\')?(.*?)(?:\"|\')?\s*$", body, re.M)
    if name_m:
        fm['name'] = name_m.group(1).strip()
    # description: handle block scalar '|' or inline
    desc_block = re.search(r"^\s*description:\s*\|\s*\n((?:\s+.*\n)+)", body, re.M)
    if desc_block:
        lines = desc_block.group(1).splitlines()
        # strip leading indentation
        stripped = [re.sub(r"^\s+", "", ln) for ln in lines]
        fm['description'] = '\n'.join([ln.rstrip() for ln in stripped]).strip()
    else:
        desc_inline = re.search(r"^\s*description:\s*(?:\"|\')?(.*?)(?:\"|\')?\s*$", body, re.M)
        if desc_inline:
            fm['description'] = desc_inline.group(1).strip()
    return fm


def extract_title_and_body(md_text):
    # find first H1
    m = re.search(r"^#\s+(.*)", md_text, re.M)
    title = m.group(1).strip() if m else ''
    # find first paragraph after title or after frontmatter
    # remove frontmatter if present
    md_no_fm = re.sub(r"^---\s*\n.*?\n---\s*\n", "", md_text, flags=re.S)
    # split into paragraphs
    paras = re.split(r"\n\s*\n", md_no_fm)
    first_para = ''
    for p in paras:
        p_strip = p.strip()
        if p_strip:
            # ignore a single heading paragraph
            if re.match(r"^#", p_strip):
                continue
            first_para = p_strip
            break
    return title, first_para


def index_all_perplexity():
    skills_dir = Path.cwd() / 'perplexity'
    out_dir = Path.cwd() / 'data' / 'zvec'
    mgr = ZVecManager(data_dir=out_dir)

    md_files = sorted(skills_dir.glob('*.md'))
    indexed = 0

    for md in md_files:
        try:
            text = md.read_text(encoding='utf-8')
        except Exception:
            text = md.read_text(encoding='latin-1')

        fm = parse_frontmatter(text)
        name = fm.get('name') or md.stem
        description = fm.get('description','').strip()

        # if description empty, try to extract from body
        if not description:
            title, para = extract_title_and_body(text)
            if para:
                description = para
            elif title:
                description = title

        # prepare content to index
        content = f"{name} {description}"
        metadata = {
            'name': name,
            'source_file': str(md.relative_to(Path.cwd())),
        }
        mgr.add_text(name, content, metadata)
        indexed += 1
        print(f"Indexed skill: {name}")

    print(f"\nTotal skills indexed: {indexed}")
    stats = mgr.get_stats()
    print(f"Vector index size: {stats['size']}")


if __name__ == '__main__':
    index_all_perplexity()
