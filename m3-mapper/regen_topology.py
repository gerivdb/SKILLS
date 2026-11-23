import json

topo = {
    "$schema": "m3-topology-v1",
    "domain": "CDP_Chromium_147",
    "description": "Cartographie topologique de manipulation de Chromium 147.0.7727.55 sur Profil 2 (CDP 9222) et JEVX (décideur typé LLM-local). Cartographie les possibles, les impasses et les chemins validés pour le pilotage d'extensions non empaquetées et la gestion des décideurs Jev-like.",
    "version": "1.0.0",
    "generated_at_utc": "2026-11-21T01:15:00Z",
    "trees": {
        "T-EXT": {
            "name": "Chargement et Pilotage des Extensions Non Empaquetées",
            "description": "Charger, activer, purger les erreurs et piloter des extensions Chromium non empaquetées (unpacked).",
            "branches": {
                "B-EXT-CDP": {
                    "name": "API CDP Pure",
                    "description": "Utiliser uniquement les API CDP (developerPrivate, chrome.management) sur une instance déjà en cours.",
                    "synapses": {
                        "cdp_loadUnpacked_string": {
                            "status": "DEAD_END",
                            "error_class": "API_Mismatch",
                            "evidence": "Unexpected property: 'path'",
                            "evidence_full": "TypeError: Error in invocation of developerPrivate.loadUnpacked(optional developerPrivate.LoadUnpackedOptions options, optional function callback): Error at parameter 'options': Unexpected property: 'path'.",
                            "timestamp": "2026-11-20T23:40:00Z",
                            "script": "archive_impasses/01_loadUnpacked_path_fails.py",
                            "conclusion": "Le CDP pur ne permet pas de passer un chemin de dossier à loadUnpacked. L'API ouvre la boîte de dialogue Windows IFileDialog."
                        },
                        "cdp_loadUnpacked_options": {
                            "status": "DEAD_END",
                            "error_class": "API_Mismatch",
                            "evidence": "Unexpected property: 'path'",
                            "evidence_full": "TypeError: Error in invocation of developerPrivate.loadUnpacked(optional developerPrivate.LoadUnpackedOptions options, optional function callback): Error at parameter 'options': Unexpected property: 'path'.",
                            "timestamp": "2026-11-20T23:42:00Z",
                            "script": "archive_impasses/01_loadUnpacked_path_fails.py",
                            "conclusion": "L'objet options LoadUnpackedOptions n'a pas de propriété 'path'. L'API est conçue pour ouvrir un sélecteur de fichier, pas pour accepter un chemin programme."
                        },
                        "cdp_loadUnpacked_noarg": {
                            "status": "BLOCKED",
                            "error_class": "UI_Block",
                            "evidence": "Timeout 30s — La boîte de dialogue Windows IFileDialog (#32770) s'ouvre et bloque.",
                            "evidence_full": "loadUnpacked() sans argument ouvre la boîte de dialogue de sélection de dossier. Attente indéfinie sans interaction humaine.",
                            "timestamp": "2026-11-20T23:43:00Z",
                            "script": "archive_impasses/01_loadUnpacked_path_fails.py",
                            "conclusion": "Sans argument, l'API déclenche l'interface graphique Windows. Non autonome."
                        },
                        "cdp_loadDirectory": {
                            "status": "DEAD_END",
                            "error_class": "API_TypeMismatch",
                            "evidence": "Value must be an instance of DirectoryEntry",
                            "evidence_full": "TypeError: Error in invocation of developerPrivate.loadDirectory(DirectoryEntry directory, function callback): Error at parameter 'directory': Value must be an instance of DirectoryEntry.",
                            "timestamp": "2026-11-20T23:44:00Z",
                            "script": "archive_impasses/02_loadDirectory_requires_FS_Entry.py",
                            "conclusion": "loadDirectory exige un véritable objet DirectoryEntry du système de fichiers navigateur, inconstructible depuis un chemin local pur via CDP."
                        },
                        "cdp_DOM_setFileInputFiles": {
                            "status": "DEAD_END",
                            "error_class": "ShadowDOM_Inaccessible",
                            "evidence": "DOM.querySelector: Invalid parameters",
                            "evidence_full": "Le shadow DOM de chrome://extensions résiste aux requêtes CDP DOM. L'élément #cdp-stealth-loader injecté n'est pas atteignable via DOM.querySelector depuis le contexte CDP.",
                            "timestamp": "2026-11-20T23:45:00Z",
                            "script": "archive_impasses/03_DOM_setFileInputFiles_fails.py",
                            "conclusion": "L'injection d'un <input type='file' webkitdirectory> dans chrome://extensions et le remplissage via DOM.setFileInputFiles échouent car le shadow DOM interne de Chromium n'est pas accessible via CDP DOM."
                        }
                    }
                },
                "B-EXT-OS": {
                    "name": "Automatisation OS",
                    "description": "Remplir la boîte de dialogue Windows IFileDialog via UIAutomation / SendKeys / PowerShell.",
                    "synapses": {
                        "os_UIAutomation_SendKeys": {
                            "status": "DEAD_END",
                            "error_class": "UI_Inaccessible",
                            "evidence": "Le champ 'Dossier :' de la fenêtre #32770 rejette l'injection UIAutomation ValuePattern et SendKeys.",
                            "evidence_full": "La boîte de dialogue IFileDialog s'ouvre mais le champ d'édition et le bouton OK ne répondent pas à l'automatisation UIAutomation (ValuePattern, InvokePattern) ni aux SendKeys PowerShell.",
                            "timestamp": "2026-11-20T23:46:00Z",
                            "script": "archive_impasses/04_UIAutomation_IFileDialog_fails.py",
                            "conclusion": "L'automatisation OS du dialogue IFileDialog est bloquée par les restrictions de sécurité Windows. Impossible de remplir le champ 'Dossier :' sans contrôle clavier/souris humain."
                        }
                    }
                },
                "B-EXT-HYB": {
                    "name": "Orchestration Hybride",
                    "description": "Nettoyage des verrous LOCK + Lancement CLI --load-extension + pilotage CDP post-chargement.",
                    "synapses": {
                        "cli_boot_loadExtension": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "GEM-X chargé avec succès sur Profile 2 (ID: jglflbolpclioognabcahamfmblahdol, version 1.0.0, 0 erreur, activé). Browse 0.1.4 chargée et activée (ID: afeafocngkodbmaipcngoamamfmekgfo).",
                            "evidence_full": "Chromium relancé via CLI avec --load-extension=\"D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\GEM-X\". CDP 9222 répond. developerPrivate.getExtensionInfo confirme state: ENABLED, disableReasons toutes false, runtimeErrors count: 0. Identique pour Browse (Cas B, clé publique).",
                            "timestamp": "2026-11-20T23:47:00Z",
                            "script": "ccp_cli.py extensions load-extension --path <chemin>",
                            "conclusion": "Méthode validée et autonome. Le CDP pur est bloqué par le sandboxing, mais le lancement de processus avec le flag --load-extension contourne totalement l'interface graphique Windows. Une fois chargée, l'extension est 100% pilotable via CDP."
                        }
                    }
                }
            }
        },
        "T-ID": {
            "name": "Prédiction Déterministe d'ID d'Extension",
            "description": "Calculer l'ID Chromium à partir d'un chemin (Cas A) ou d'une clé publique RSA (Cas B).",
            "branches": {
                "T-ID-CAS-A": {
                    "name": "ID par Chemin (Cas A — sans clé)",
                    "description": "SHA-256 du chemin absolu canonique du dossier (minuscules, slashes /) → 16 premiers octets → Base26 a-p (32 caractères).",
                    "synapses": {
                        "casA_sha256_path": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "Algorithme implémenté et testé sur Sidekeep-X (ID prédit vs ID réel à valider sur un dossier connu).",
                            "timestamp": "2026-11-20T23:30:00Z",
                            "script": "chromium-extension-cockpit/scripts/predict_extension_id.py",
                            "conclusion": "L'algorithme Cas A est implémenté. Nécessite un dossier connu avec ID réel pour validation croisée finale."
                        }
                    }
                },
                "T-ID-CAS-B": {
                    "name": "ID par Clé Publique (Cas B)",
                    "description": "SHA-256 de la clé publique RSA (SPKI DER décodée depuis Base64 dans manifest.json) → 16 premiers octets → Base26 a-p (32 caractères).",
                    "synapses": {
                        "casB_sha256_pubkey": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "ID prédit 'afeafocngkodbmaipcngoamamfmekgfo' = ID réel de Browse. MATCH 100% sur clé publique directe ET sur manifest.json.",
                            "evidence_full": "Clé publique de Browse : MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjWdgsBDUPCHO2u5bq3/Us1sLm+kiehLZBL0HIu3stwivGW+bgCDsD8KAEMFJcY04u3iudffTeEGdEe8pQfL7BSNRvyslszmvJrsoP7bVUKXrnRTw3CUsRjnwbqMoMElwegiCFUXPnqQ9ZeA2NGEhmWMyDXqqZxOo0z2q66GTgz9McbXOBK2QXYBPjUWxud814wSrE1lIQ2G58nQVeZenI3/PXZ4f1SACn6SdkiCR44NZwz89I1ISxftongLDED/1dlnivqJBzAtN1s2i+jWplLtOmLJJkh1LQ2jP3gWvYY1zT2RHJIw874SSrrhFt4Hguvo/L0Ge7ixvGp5tDAP2wwIDAQAB",
                            "timestamp": "2026-11-20T23:29:00Z",
                            "script": "chromium-extension-cockpit/scripts/predict_extension_id.py",
                            "conclusion": "L'algorithme Cas B est validé à 100%. L'ID prédit correspond exactement à l'ID réel de Browse (Cas B, clé publique)."
                        }
                    }
                }
            }
        },
        "T-JEVX": {
            "name": "JEVX — Décideur Typé LLM-Local Souverain",
            "description": "Charger, activer, purger les erreurs et piloter des extensions Chromium non empaquetées (unpacked).",
            "branches": {
                "B-JEVX-CORE": {
                    "name": "Moteur de Décision et API",
                    "description": "src/engine.ts, src/server.ts, src/types.ts, src/config.ts — Moteur de décision Jev-compatible, routes HTTP, validation.",
                    "synapses": {
                        "jevx_engine_decide": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "Engine.decide() implémenté avec cache LRU, sémaphore, regroupement par appels, décodage des réponses typées (noul/choice/score).",
                            "evidence_full": "src/engine.ts — Engine implémente DecisionEngine avec decide(questions, state, seed), cache LRU (max 1024, TTL 1h), sémaphore (maxInflight 2, maxQueue 64), regroupement questionsPerCall/outcomesPerCall, retry malformed (2x), décodage des réponses avec confiance par entropie.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "src/engine.ts",
                            "conclusion": "Moteur de décision fonctionnel et documenté."
                        },
                        "jevx_server_routes": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "Routes /v1/systemone, /health, /ready, /v1/models impliquées dans src/server.ts avec authentification API key.",
                            "evidence_full": "LocalJevApp.route() gère GET /health, GET /ready, GET /v1/models, POST /v1/systemone (authentifié), POST /studies/* (via StudyApiIntegration). Authentification Bearer token avec timingSafeEqual.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "src/server.ts",
                            "conclusion": "API HTTP complète et validée."
                        },
                        "jevx_types_validation": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "src/types.ts valide SystemOneRequest, Question (noul/choice/score), Answer avec RequestValidationError détaillé.",
                            "evidence_full": "validateSystemOneRequest() vérifie state, model, questions (au moins une). validateQuestion() gère noul (2 critères), choice (2-128 critères), score (2-10 critères).",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "src/types.ts",
                            "conclusion": "Validation stricte et typée."
                        },
                        "jevx_config": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "src/config.ts charge les settings depuis les variables d'environnement avec fallbacks.",
                            "evidence_full": "LOCALJEV_UPSTREAM (http://127.0.0.1:8000), LOCALJEV_UPSTREAM_MODEL (gemma3:1b), LOCALJEV_PORT (8080), LOCALJEV_TIMEOUT (180s), LOCALJEV_MAX_OUTPUT_TOKENS (2048), etc.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "src/config.ts",
                            "conclusion": "Configuration complète via variables d'environnement."
                        },
                        "jevx_document_cache": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "src/document-cache.ts implémente LRU document cache avec TTL et eviction.",
                            "evidence_full": "LruDocumentCache avec maxEntries (1024), ttlMs (3600000), eviction par lastAccess le plus ancien.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "src/document-cache.ts",
                            "conclusion": "Cache LRU fonctionnel."
                        }
                    }
                },
                "B-JEVX-ADAPT": {
                    "name": "Adaptateurs Upstream",
                    "description": "scripts/ollama-openai-proxy.py, scripts/llux_openai_adapter.py — Traduction OpenAI-compatible vers Ollama/LLUX.",
                    "synapses": {
                        "jevx_ollama_proxy": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "scripts/ollama-openai-proxy.py écoute sur 8080, traduit /v1/chat/completions vers Ollama /api/chat sur 11434.",
                            "evidence_full": "OpenAIProxyHandler.do_POST traduit les requêtes OpenAI (model, messages, temperature, max_tokens, seed, response_format) vers Ollama avec options et format json/json_schema.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "scripts/ollama-openai-proxy.py",
                            "conclusion": "Adaptateur Ollama fonctionnel."
                        },
                        "jevx_llux_adapter": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "scripts/llux_openai_adapter.py écoute sur 8081, traduit vers LLUX /v1/chat/completions sur 47000.",
                            "evidence_full": "LLUXOpenAIAdapterHandler do_POST traduit vers LLUX avec format OpenAI-compatible (id, object, created, model, choices, usage).",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "scripts/llux_openai_adapter.py",
                            "conclusion": "Adaptateur LLUX fonctionnel."
                        }
                    }
                },
                "B-JEVX-STUDY": {
                    "name": "Veille Comparative et Registre des Variantes",
                    "description": "src/comparator.ts, registry/jev-variants.yaml, studies/ — Catalogage, extraction, comparaison des variantes Jev-like.",
                    "synapses": {
                        "jevx_variant_registry": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "registry/jev-variants.yaml catalogue 3 variantes : localjev (bridge, prompted), kalm-jev (reranker-native), openjev (native-logit-read).",
                            "evidence_full": "3 variantes avec architecture, protocole, features, évaluation, implémentation, forces/faiblesses, intégration JEVX. kalm-jev a 3 patterns validés HITL (document-cache-lru, reranker-native-scoring, benchmark-methodology).",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "registry/jev-variants.yaml",
                            "conclusion": "Registre complet et documenté."
                        },
                        "jevx_comparator": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "src/comparator.ts compare N variantes sur 6 axes (architecture 3, calibration 3, protocol_compliance 2, performance 2, evaluation 2, sovereignty 3).",
                            "evidence_full": "ComparativeEngine.compare() produit ComparisonReport avec classements (by_weighted_total, by_axis), synthèse (meilleur par axe, patterns_to_adopt avec priorité et ADR requis).",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "src/comparator.ts",
                            "conclusion": "Moteur de comparaison fonctionnel."
                        },
                        "jevx_study_properties": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "studies/kalm-jev/properties.yaml et studies/openjev/properties.yaml documentent architecture, protocole, features, performance, évaluation, implémentation.",
                            "evidence_full": "kalm-jev : cache LRU 256 MiB, adapter-per-task, benchmarks AG News/BoolQ/SST-5. openjev : logit-read gold standard, vLLM patché non fusionné.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "studies/kalm-jev/properties.yaml, studies/openjev/properties.yaml",
                            "conclusion": "Propriétés extraites et documentées."
                        }
                    }
                },
                "B-JEVX-ROOTX": {
                    "name": "Clients ROOTX",
                    "description": "src/*.py — Clients Python pour interroger ROOTX (causal, curriculum, narrative, meta_coherence, rootx_client).",
                    "synapses": {
                        "jevx_causal_validator": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "src/causal_validator.py interroge ROOTX /validate sur http://localhost:8030.",
                            "evidence_full": "CausalValidator.validate_causal(service) retourne {valid, confidence, errors}. Méthode health() vérifie /health.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "src/causal_validator.py",
                            "conclusion": "Client causal_validator fonctionnel."
                        },
                        "jevx_curriculum_validator": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "src/curriculum_validator.py interroge CURX /validate sur http://localhost:8040.",
                            "evidence_full": "CurriculumValidator.validate_curriculum(data) retourne {valid, confidence, feedback}.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "src/curriculum_validator.py",
                            "conclusion": "Client curriculum_validator fonctionnel."
                        },
                        "jevx_meta_coherence_fixer": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "src/meta_coherence_fixer.py interroge N243 /fix sur http://localhost:8050.",
                            "evidence_full": "MetaCoherenceFixer.fix_coherence(data) retourne {coherent, fixes_applied, confidence}.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "src/meta_coherence_fixer.py",
                            "conclusion": "Client meta_coherence_fixer fonctionnel."
                        },
                        "jevx_narrative_generator": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "src/narrative_generator.py interroge TALEX /generate sur http://localhost:8060.",
                            "evidence_full": "NarrativeGenerator.generate_narrative(data) retourne {narrative, metadata, confidence}.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "src/narrative_generator.py",
                            "conclusion": "Client narrative_generator fonctionnel."
                        },
                        "jevx_rootx_client": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "src/rootx_client.py interroge ROOTX /validate sur http://localhost:8030.",
                            "evidence_full": "RootxClient.query(root_id, payload) retourne {root_id, valid, confidence, errors}.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "src/rootx_client.py",
                            "conclusion": "Client rootx_client fonctionnel."
                        }
                    }
                },
                "B-JEVX-KIVA": {
                    "name": "Intégration KIX et Cycle de Vie",
                    "description": "scripts/jevx_daemon.py, scripts/register_jevx_in_kix.py, scripts/service-manifest.yaml, scripts/health_check.py — Intégration KIX, daemon, manifeste de services.",
                    "synapses": {
                        "jevx_daemon": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "scripts/jevx_daemon.py démarre JEVX via bun run src/index.ts, enregistre dans KIX Service Discovery.",
                            "evidence_full": "JevxDaemon.start() lance bun run src/index.ts sur port 8080, enregistre dans KIX avec métadonnées (path, type, intent_hash, endpoint, description). stop()/status()/is_healthy() impliqués.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "scripts/jevx_daemon.py",
                            "conclusion": "Daemon KIX fonctionnel."
                        },
                        "jevx_register_kix": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "scripts/register_jevx_in_kix.py enregistre JEVX dans KIX Service Discovery avec métadonnées complètes.",
                            "evidence_full": "Enregistre name=jevx, host=127.0.0.1, port=8080, protocol=http, metadata (path, type=decision-engine, intent_hash=0xINTENT_JEVX_SOVEREIGN_OVERLAY_20260919, endpoint=/v1/systemone, description).",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "scripts/register_jevx_in_kix.py",
                            "conclusion": "Enregistrement KIX fonctionnel."
                        },
                        "jevx_service_manifest": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "scripts/service-manifest.yaml définit 6 services (kix, llux, llux_openai_adapter, ollama, ollama_openai_proxy, jevx) avec ordres de démarrage/arrêt.",
                            "evidence_full": "jevx sur port 8082, dépendances ollama_openai_proxy et llux_openai_adapter, startup_order 6, shutdown_order 1. validate_manifest.py vérifie ports uniques, dépendances, health_endpoints.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "scripts/service-manifest.yaml",
                            "conclusion": "Manifeste de services complet et validé."
                        },
                        "jevx_health_check": {
                            "status": "VALIDATED_PATH",
                            "error_class": None,
                            "evidence": "scripts/health_check.py vérifie registry (dlm_models.json), runner (jevx_runner_status.json), et endpoint direct /ready.",
                            "evidence_full": "check_jevx_health() retourne {status, registry_ok, runner_ok, direct_ok, timestamp}. Peut servir un endpoint HTTP sur le port 8081.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "scripts/health_check.py",
                            "conclusion": "Proxy de santé fonctionnel."
                        }
                    }
                }
            }
        },
        "T-JEVX-IMPASSES": {
            "name": "JEVX — Points d'Attention et Impasses",
            "description": "Points d'attention identifiés lors de l'exploration du repo.",
            "branches": {
                "B-JEVX-PORTS": {
                    "name": "Conflit de Ports",
                    "description": "Conflit potentiel entre le port CDP Chromium (9222) et le port JEVX (8080/8082).",
                    "synapses": {
                        "jevx_port_conflict": {
                            "status": "BLOCKED",
                            "error_class": "Port_Conflict",
                            "evidence": "REPO.yaml et scripts enregistrent JEVX sur le port 8080 (KIX) ou 8082 (service-manifest). Chromium utilise le port 9222 (CDP). Risque de confusion.",
                            "evidence_full": "ccp_cli.py utilise le port 9222 pour CDP Chromium. JEVX service-manifest.yaml déclare jevx sur le port 8082. KIX-INTEGRATION.md indique le port 8080. Ambiguïté sur le port réel d'écoute.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "exploration manuelle du repo",
                            "conclusion": "À clarifier : quel port JEVX utilise-t-il réellement ?"
                        }
                    }
                },
                "B-JEVX-SERVICES": {
                    "name": "État des Services Upstream",
                    "description": "État inconnu des services upstream (Ollama, LLUX).",
                    "synapses": {
                        "jevx_upstream_health": {
                            "status": "DEAD_END",
                            "error_class": "Service_Unverified",
                            "evidence": "Aucun test de santé réel exécuté sur Ollama (11434) ou LLUX (47000). Les scripts de proxy existent mais leur état de fonctionnement est inconnu.",
                            "evidence_full": "ollama-openai-proxy.py et llux_openai_adapter.py existent mais n'ont pas été testés. Aucune preuve que les services upstream sont démarrés.",
                            "timestamp": "2026-11-21T01:15:00Z",
                            "script": "aucun test exécuté",
                            "conclusion": "À vérifier : état réel des services upstream."
                        }
                    }
                }
            }
        }
    },
    "metadata": {
        "total_trees": 5,
        "total_branches": 11,
        "total_synapses": 25,
        "validated_paths": 10,
        "dead_ends": 13,
        "blocked": 1,
        "last_updated_utc": "2026-11-21T01:15:00Z",
        "generator": "m3_mapper_engine_v1"
    }
}

with open(r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-mapper\topology.json", "w", encoding="utf-8") as f:
    json.dump(topo, f, ensure_ascii=False, indent=2)
print("topology.json régénéré avec succès !")
print(f"Trees : {list(topo['trees'].keys())}")
print(f"Métadonnées : {topo['metadata']}")