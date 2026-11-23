#!/usr/bin/env python3
"""
Exécute tous les tests JEVX avec le décorateur @m3_synapse appliqué dynamiquement.
Version robuste : capture toutes les exceptions, continue malgré les erreurs.
"""

import importlib
import sys
import traceback
from pathlib import Path
from datetime import datetime, timezone

from m3_mapper import m3_synapse, load_topology, save_topology

TESTS_DIR = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\JEVX\tests")
M3_MAPPER_DIR = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-mapper")

sys.path.insert(0, str(M3_MAPPER_DIR))
sys.path.insert(0, str(TESTS_DIR.parent))

FUNCTION_MAPPING = {
    # B-JEVX-CORE
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
    # B-JEVX-ADAPT
    "test_llux_adapter_import": ("ADAPT", "adapt_llux_adapter_import"),
    "test_llux_registered_in_kix": ("ADAPT", "adapt_llux_registered_in_kix"),
    "test_llux_adapter_registered_in_kix": ("ADAPT", "adapt_llux_adapter_registered_in_kix"),
    "test_llux_in_manifest": ("ADAPT", "adapt_llux_in_manifest"),
    "test_llux_adapter_request_format": ("ADAPT", "adapt_llux_adapter_request_format"),
    "test_adapter_initialization": ("ADAPT", "adapt_llux_adapter_initialization"),
    "test_format_request": ("ADAPT", "adapt_llux_format_request"),
    "test_format_chat_request": ("ADAPT", "adapt_llux_format_chat_request"),
    "test_llux_chat_completion_mocked": ("ADAPT", "adapt_llux_chat_completion_mocked"),
    # B-JEVX-STUDY
    "test_jevx_in_mox_crosslinks": ("STUDY", "study_mox_crosslinks"),
    "test_contracts_directory_exists": ("STUDY", "study_contracts_directory_exists"),
    "test_contracts_yaml_files": ("STUDY", "study_contracts_yaml_files"),
    "test_contract_schema": ("STUDY", "study_contracts_schema"),
    "test_resolve_jevx_from_l2": ("STUDY", "study_mox_resolve_jevx_from_l2"),
    "test_resolve_plix_from_l2": ("STUDY", "study_mox_resolve_plix_from_l2"),
    "test_resolve_unknown_repo": ("STUDY", "study_mox_resolve_unknown_repo"),
    "test_resolve_governance_hub": ("STUDY", "study_mox_resolve_governance_hub"),
    # B-JEVX-ROOTX
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
    # B-JEVX-KIVA
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

def run_test_function(func, branch_name, synapse_name):
    decorated = m3_synapse(branch_name=branch_name, synapse_name=synapse_name, tree_id="T-JEVX")(func)
    try:
        result = decorated()
        return {"status": "PASSED", "result": str(result)[:200] if result else None}
    except BaseException as e:
        return {"status": "FAILED", "error": str(e), "traceback": traceback.format_exc()}

def main():
    test_files = sorted(TESTS_DIR.glob("test_*.py"))
    print(f"Trouvé {len(test_files)} fichiers de test\n")
    
    total_tests = 0
    passed = 0
    failed = 0
    errors = 0
    
    for test_file in test_files:
        print(f"\n=== {test_file.name} ===")
        
        try:
            module_name = test_file.stem
            spec = importlib.util.spec_from_file_location(module_name, test_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except BaseException as e:
            print(f"  ERREUR d'import du module: {type(e).__name__}: {e}")
            errors += 1
            continue
        
        for name in dir(module):
            if not name.startswith("test_"):
                continue
            func = getattr(module, name)
            if not callable(func):
                continue
            
            total_tests += 1
            branch_name, synapse_name = FUNCTION_MAPPING.get(name, ("UNKNOWN", name))
            
            print(f"  {name}...", end=" ")
            
            try:
                result = run_test_function(func, branch_name, synapse_name)
                if result["status"] == "PASSED":
                    passed += 1
                    print("PASSED")
                else:
                    failed += 1
                    print(f"FAILED: {result.get('error', '')[:80]}")
            except BaseException as e:
                failed += 1
                print(f"ERROR: {e}")
    
    print(f"\n{'='*60}")
    print(f"Total: {total_tests} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors (import): {errors}")

if __name__ == "__main__":
    main()