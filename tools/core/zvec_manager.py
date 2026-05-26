from pathlib import Path
import json

class ZVecManager:
    """Minimal local shim for ZVecManager used by index_skills.py

    Stores small in-memory index and writes a zvec_index.json file in data_dir.
    Methods implemented: __init__(data_dir), add_text(id, text, metadata), get_stats()
    """
    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = Path('data') / 'zvec'
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.index = []

    def add_text(self, doc_id, text, metadata=None):
        entry = {
            'id': doc_id,
            'text': text,
            'metadata': metadata or {}
        }
        self.index.append(entry)
        # persist incremental index to file
        out = {
            'size': len(self.index),
            'entries': self.index
        }
        with open(self.data_dir / 'zvec_index.json', 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

    def get_stats(self):
        return {'size': len(self.index)}
