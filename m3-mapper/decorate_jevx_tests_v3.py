#!/usr/bin/env python3
"""
Décore proprement tous les fichiers de test JEVX avec @m3_synapse.
"""

import re
from pathlib import Path

TESTS_DIR = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\JEVX\tests")
M3_MAPPER_REL = Path("..") / "SKILLS" / "m3-mapper"

# Mapping : nom_fonction -> (branch_name, synapse_name)
FUNCTION_MAPPING = {
    # B-JEVX-CORE - Moteur de décision et API
    "test_select_tests_with_empty_history_returns_all": ("CORE", "core_optimizer_select_tests_empty_history"),
    "test_select_tests_with_failures_prioritizes_failed": ("CORE", "core_optimizer_select_tests_prioritize_failed"),
    "test_optimization_report_reduction_ratio": ("CORE", "core_optimizer_report_reduction_ratio"),
    "test_test_result_coverage_valid_range": ("CORE", "core_optimizer_coverage_valid_range"),
    "test_hallucination_gold_set": ("CORE", "core_hallucination_gold_set"),
    "test_simple_replace": ("CORE", "core_ps_safe_replace_simple"),
    "test_replace_with_dollar": ("CORE", "core_ps_safe_replace_dollar"),
    "test_replace_with_quotes": ("CORE", "core_ps_safe_replace_quotes"),
    "test_no_match_warning": ("CORE", "core_ps_safe_replace_no_match"),
    "test_empty_result_corruption_detection": ("CORE", "core_ps_safe_replace_empty_result"),
    
    # B-JEVX-ADAPT - Adaptateurs Upstream
    "test_llux_adapter_import": ("ADAPT", "adapt_llux_adapter_import"),
    "test_llux_registered_in_kix": ("ADAPT", "adapt_llux_registered_in_kix"),
    "test_llux_adapter_registered_in_kix": ("ADAPT", "adapt_llux_adapter_registered_in_kix"),
    "test_llux_in_manifest": ("ADAPT", "adapt_llux_in_manifest"),
    "test_llux_adapter_request_format": ("ADAPT", "adapt_llux_adapter_request_format"),
    "test_adapter_initialization": ("ADAPT", "adapt_llux_adapter_initialization"),
    "test_format_request": ("ADAPT", "adapt_llux_format_request"),
    "test_format_chat_request": ("ADAPT", "adapt_llux_format_chat_request"),
    "test_llux_chat_completion_mocked": ("ADAPT", "adapt_llux_chat_completion_mocked"),
    
    # B-JEVX-STUDY - Veille Comparative
    "test_jevx_in_mox_crosslinks": ("STUDY", "study_mox_crosslinks"),
    "test_contracts_directory_exists": ("STUDY", "study_contracts_directory_exists"),
    "test_contracts_yaml_files": ("STUDY", "study_contracts_yaml_files"),
    "test_contract_schema": ("STUDY", "study_contracts_schema"),
    "test_resolve_jevx_from_l2": ("STUDY", "study_mox_resolve_jevx_from_l2"),
    "test_resolve_plix_from_l2": ("STUDY", "study_mox_resolve_plix_from_l2"),
    "test_resolve_unknown_repo": ("STUDY", "study_mox_resolve_unknown_repo"),
    "test_resolve_governance_hub": ("STUDY", "study_mox_resolve_governance_hub"),
    
    # B-JEVX-ROOTX - Clients ROOTX
    "test_build_causal_validator": ("ROOTX", "rootx_causal_validator_build"),
    "test_health_causal_validator": ("ROOTX", "rootx_causal_validator_health"),
    "test_build_curriculum_validator": ("ROOTX", "rootx_curriculum_validator_build"),
    "test_health_curriculum_validator": ("ROOTX", "rootx_curriculum_validator_health"),
    "test_build_meta_coherence_fixer": ("ROOTX", "rootx_meta_coherence_fixer_build"),
    "test_health_meta_coherence_fixer": ("ROOTX", "rootx_meta_coherence_fixer_health"),
    "test_build_narrative_generator": ("ROOTX", "rootx_narrative_generator_build"),
    "test_health_narrative_generator": ("ROOTX", "rootx_narrative_generator_health"),
    "test_build_rootx_client": ("ROOTX", "rootx_client_build"),
    "test_health_rootx_client": ("ROOTX", "rootx_client_health"),
    
    # B-JEVX-KIVA - Intégration KIX
    "test_kix_import": ("KIVA", "kiva_kix_import"),
    "test_kix_service_discovery": ("KIVA", "kiva_kix_service_discovery"),
    "test_kix_path_resolver": ("KIVA", "kiva_kix_path_resolver"),
    "test_service_manifest": ("KIVA", "kiva_service_manifest"),
    "test_kix_service_health": ("KIVA", "kiva_kix_service_health"),
    "test_model_selector": ("KIVA", "kiva_model_selector"),
    "test_load_manifest": ("KIVA", "kiva_service_lifecycle_manager_load_manifest"),
    "test_service_initialization": ("KIVA", "kiva_service_lifecycle_manager_service_initialization"),
    "test_check_health": ("KIVA", "kiva_service_lifecycle_manager_check_health"),
    "test_service_manifest_loads": ("KIVA", "kiva_service_lifecycle_service_manifest_loads"),
    "test_service_manifest_dependencies": ("KIVA", "kiva_service_lifecycle_service_manifest_dependencies"),
    "test_service_manifest_ports": ("KIVA", "kiva_service_lifecycle_service_manifest_ports"),
    "test_service_manifest_health_endpoints": ("KIVA", "kiva_service_lifecycle_service_manifest_health_endpoints"),
    "test_service_lifecycle_health_check": ("KIVA", "kiva_service_lifecycle_service_lifecycle_health_check"),
    "test_validation_passes": ("KIVA", "kiva_validate_jevx_structure_validation_passes"),
    "test_kilo_reports_exists": ("KIVA", "kiva_validate_jevx_structure_kilo_reports_exists"),
    "test_integration_contracts_exists": ("KIVA", "kiva_validate_jevx_structure_integration_contracts_exists"),
    "test_scope_yaml_exists": ("KIVA", "kiva_validate_jevx_structure_scope_yaml_exists"),
    "test_kiva_pipeline_exists": ("KIVA", "kiva_validate_jevx_structure_kiva_pipeline_exists"),
    "test_prd_moc_directory_exists": ("KIVA", "kiva_validate_jevx_structure_prd_moc_directory_exists"),
    "test_talex_rapport_exists": ("KIVA", "kiva_validate_jevx_structure_talex_rapport_exists"),
}

IMPORT_SYS = "import sys"
IMPORT_PATH = "from pathlib import Path"
IMPORT_M3_PATH = 'sys.path.insert(0, str(Path(__file__).parent.parent / "L4-TOOLS" / "SKILLS" / "m3-mapper"))'
IMPORT_M3 = "from m3_mapper import m3_synapse"

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    
    # 1. Ajouter 'import sys' en tout début (après shebang/docstring si présent)
    if not re.search(r'^import sys\s*$', content, re.MULTILINE):
        lines = content.split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if i == 0 and stripped.startswith('#!'):
                insert_idx = i + 1
            elif i == 0 and stripped.startswith('"""'):
                # Docstring en début de fichier, insérer après
                insert_idx = i + 1
                # Trouver la fin du docstring
                for j in range(i + 1, len(lines)):
                    if '"""' in lines[j]:
                        insert_idx = j + 1
                        break
                break
            elif stripped.startswith('import ') or line.startswith('from '):
                insert_idx = i
                break
            elif stripped and not stripped.startswith('#'):
                insert_idx = i
                break
        lines.insert(insert_idx, IMPORT_SYS)
        content = '\n'.join(lines)
    
    # 2. Ajouter 'from pathlib import Path' si Path est utilisé mais pas importé
    if 'Path(' in content and not re.search(r'^from pathlib import', content, re.MULTILINE):
        lines = content.split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                insert_idx = i + 1
        lines.insert(insert_idx, IMPORT_PATH)
        content = '\n'.join(lines)
    
    # 3. Ajouter sys.path.insert pour m3-mapper
    if 'm3-mapper' not in content:
        lines = content.split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                insert_idx = i + 1
        lines.insert(insert_idx, IMPORT_M3_PATH)
        content = '\n'.join(lines)
    
    # 4. Ajouter 'from m3_mapper import m3_synapse'
    if 'from m3_mapper import m3_synapse' not in content:
        lines = content.split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                insert_idx = i + 1
        lines.insert(insert_idx, IMPORT_M3)
        content = '\n'.join(lines)
    
    # 5. Ajouter le décorateur @m3_synapse sur chaque fonction de test
    test_functions = re.findall(r'^(\s*)def (test_\w+)\b', content, re.MULTILINE)
    
    for indent, func_name in test_functions:
        if func_name in FUNCTION_MAPPING:
            branch_name, synapse_name = FUNCTION_MAPPING[func_name]
            # Vérifier si déjà décoré
            already_decorated = re.compile(
                r'@m3_synapse\(branch_name="[^"]+", synapse_name="' + re.escape(func_name) + r'", tree_id="T-JEVX"\)\n\s*def ' + re.escape(func_name) + r'\b',
                re.MULTILINE
            )
            if already_decorated.search(content):
                continue
            
            pattern = re.compile(
                r'(\n)(\s*)def ' + re.escape(func_name) + r'\b',
                re.MULTILINE
            )
            decorator = f'@m3_synapse(branch_name="{branch_name}", synapse_name="{synapse_name}", tree_id="T-JEVX")\n'
            
            def replacer(match):
                return match.group(1) + match.group(2) + decorator + match.group(2) + 'def ' + func_name
            
            content = pattern.sub(replacer, content, count=1)
    
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [OK] {filepath.name}")
        return True
    else:
        print(f"  [SKIP] {filepath.name}")
        return False

def main():
    test_files = sorted(TESTS_DIR.glob("test_*.py"))
    print(f"Trouvé {len(test_files)} fichiers de test\n")
    
    decorated = 0
    for tf in test_files:
        print(f"  {tf.name}", end="")
        if process_file(tf):
            decorated += 1
            print(" - décoré")
        else:
            print(" - inchangé")
    
    print(f"\n{decorated}/{len(test_files)} fichiers modifiés")

if __name__ == "__main__":
    main()