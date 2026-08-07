"""Tests for pre_impl_inventory."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pre_impl_inventory import AssetScanner, SPIDX, InventoryEngine


def test_asset_scanner():
    scanner = AssetScanner()
    assets = scanner.scan()
    assert len(assets) > 0, "Expected at least one asset"
    kinds = {a.kind for a in assets}
    assert "skill" in kinds, "Expected skills"
    print(f"PASS: test_asset_scanner ({len(assets)} assets)")


def test_spidx_partition():
    scanner = AssetScanner()
    assets = scanner.scan()[:10]
    spidx = SPIDX(assets)
    partition = spidx.partition()
    assert "S" in partition and "K" in partition and "R" in partition
    total = len(partition["S"]) + len(partition["K"]) + len(partition["R"])
    assert total == len(assets)
    print(f"PASS: test_spidx_partition (S={len(partition['S'])}, K={len(partition['K'])}, R={len(partition['R'])})")


def test_inventory_engine():
    target = Path("D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode/act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/architecture/PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md")
    if not target.exists():
        print("SKIP: test_inventory_engine - target not found")
        return
    engine = InventoryEngine(target)
    result = engine.run(target)
    assert result.valid
    assert len(result.assets) > 0
    assert len(result.outputs) == 5
    for name, path in result.outputs.items():
        assert path.exists(), f"Output {name} missing: {path}"
    print(f"PASS: test_inventory_engine ({len(result.assets)} assets, {len(result.outputs)} outputs)")


if __name__ == "__main__":
    test_asset_scanner()
    test_spidx_partition()
    test_inventory_engine()
    print("\n=== ALL TESTS PASSED ===")
