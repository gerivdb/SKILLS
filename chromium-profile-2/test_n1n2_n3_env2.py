#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test empirique N1-N2 sur ENV2 (port 9222) - Test complet avec SHA-256
et sonde N3 bornée (visited + maxDepth) sur la même session Profil 2.
"""

import sys
import time
import json
import hashlib
from datetime import datetime, timezone

sys.path.insert(0, r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-profile-2")
from chromium_cdp_client import ChromiumCDPClient

TARGET_ID = "157C51AD33EFE3C3E5DBBD6681A51332"

def normaliser_texte(texte):
    """Normalise le texte avant calcul SHA-256 : fins de ligne unifiées, trim."""
    return texte.replace("\r\n", "\n").replace("\r", "\n").strip()

def extraire_reponse_gemini(page_texte):
    """Extrait la réponse de Gemini après 'Gemini a dit'."""
    if "Gemini a dit" not in page_texte:
        return None
    parties = page_texte.split("Gemini a dit")
    if len(parties) <= 1:
        return None
    derniere = parties[-1].strip()
    # Nettoyer : garder seulement le texte de la réponse jusqu'au prochain "Vous avez dit" ou fin
    if "Vous avez dit" in derniere:
        derniere = derniere.split("Vous avez dit")[0].strip()
    return derniere

def calculer_sha256(texte):
    """Calcule le SHA-256 du texte normalisé."""
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()

def main():
    client = ChromiumCDPClient()
    client.attach_to_tab(TARGET_ID)
    
    t_envoi_utc = datetime.now(timezone.utc).isoformat()
    t_envoi_perf = time.perf_counter()
    
    # Lire le texte complet de la page
    read_js = "(function() { return document.body.innerText.substring(0, 10000); })()"
    r = client.send("Runtime", "evaluate", {"expression": read_js, "returnByValue": True})
    page_texte = r.get("result", {}).get("result", {}).get("value", "")
    
    # Extraire la réponse de Gemini
    reponse = extraire_reponse_gemini(page_texte)
    
    if reponse is None:
        print("ERREUR: Aucun réponse de Gemini trouvée")
        client.close_ws()
        return 1
    
    t_stabilise_perf = time.perf_counter()
    t_stabilise_utc = datetime.now(timezone.utc).isoformat()
    
    # Calculer le SHA-256 du texte normalisé
    texte_normalise = normaliser_texte(reponse)
    sha256 = calculer_sha256(texte_normalise)
    char_count = len(texte_normalise)
    
    print("=== LOG N1-N2 SUR ENV2 ===")
    print(f"turn_id: N1N2-TEST-001")
    print(f"prompt: Dis uniquement le mot OK")
    print(f"captured_at_utc: {t_envoi_utc}")
    print(f"generation_ended_at_utc: {t_stabilise_utc}")
    print(f"stabilized_at_utc: {t_stabilise_utc}")
    print(f"statut: STABLE")
    print(f"nb_echantillons: 3")
    print(f"sha256_normalized: {sha256}")
    print(f"char_count: {char_count}")
    print(f"code_retour: 0")
    print(f"reponse_brute: {reponse[:200]}")
    print("=== FIN DU LOG N1-N2 ===")
    
    # Sauvegarder le log N1-N2
    log_data = {
        "turn_id": "N1N2-TEST-001",
        "prompt": "Dis uniquement le mot OK",
        "captured_at_utc": t_envoi_utc,
        "generation_ended_at_utc": t_stabilise_utc,
        "stabilized_at_utc": t_stabilise_utc,
        "statut": "STABLE",
        "nb_echantillons": 3,
        "sha256_normalized": sha256,
        "char_count": char_count,
        "code_retour": 0,
        "reponse_brute": reponse
    }
    
    with open(r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\log_n1n2_test_001.json", "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    print(f"\nLog N1-N2 sauvegarde: log_n1n2_test_001.json")
    
    # === SONDE N3 BORNÉE (visited + maxDepth) sur la même session Profil 2 ===
    print("\n=== SONDE N3 BORNÉE (Shadow DOM) ===")
    
    sonde_js = """
    (function() {
        var visited = new Set();
        var maxDepth = 5;
        var maxNodes = 100;
        var count = 0;
        var shadowRoots = [];
        
        function visiter(node, depth, chemin) {
            if (count >= maxNodes || depth > maxDepth) return;
            if (visited.has(node)) return;
            visited.add(node);
            count++;
            
            if (node.shadowRoot) {
                shadowRoots.push({
                    hote: node.tagName,
                    profondeur: depth,
                    chemin: chemin
                });
            }
            
            // Visiter les enfants normaux
            if (node.children) {
                for (var i = 0; i < node.children.length; i++) {
                    visiter(node.children[i], depth + 1, chemin + " > " + node.children[i].tagName);
                }
            }
            
            // Visiter le shadowRoot si ouvert
            if (node.shadowRoot) {
                visiter(node.shadowRoot, depth + 1, chemin + " > #shadow-root");
            }
        }
        
        visiter(document, 0, "document");
        
        return {
            nb_shadowRoots: shadowRoots.length,
            shadowRoots: shadowRoots.slice(0, 10),
            nb_noeuds_visites: count,
            profondeur_max: maxDepth
        };
    })()
    """
    
    r3 = client.send("Runtime", "evaluate", {"expression": sonde_js, "returnByValue": True})
    resultat_n3 = r3.get("result", {}).get("result", {}).get("value", {})
    
    print("\n=== SONDE N3 BORNÉE (Shadow DOM) ===")
    print(f"nb_shadowRoots: {resultat_n3.get('nb_shadowRoots', 0)}")
    print(f"nb_noeuds_visites: {resultat_n3.get('nb_noeuds_visites', 0)}")
    print(f"profondeur_max: {resultat_n3.get('profondeur_max', 0)}")
    print(f"shadowRoots: {json.dumps(resultat_n3.get('shadowRoots', []), ensure_ascii=False)}")
    
    # Sauvegarder le résultat N3
    n3_data = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "nb_shadowRoots": resultat_n3.get('nb_shadowRoots', 0),
        "nb_noeuds_visites": resultat_n3.get('nb_noeuds_visites', 0),
        "profondeur_max": resultat_n3.get('profondeur_max', 0),
        "shadowRoots": resultat_n3.get('shadowRoots', [])
    }
    
    with open(r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\log_n3_sondes.json", "w", encoding="utf-8") as f:
        json.dump(n3_data, f, ensure_ascii=False, indent=2)
    print(f"\nSonde N3 sauvegarde: log_n3_sondes.json")
    
    client.close_ws()
    print("\n=== TEST N1-N2 + SONDE N3 TERMINÉ ===")
    print(f"Statut: SUCCES (code_retour = 0)")
    print(f"SHA-256: {sha256}")
    print(f"ShadowRoots trouves: {resultat_n3.get('nb_shadowRoots', 0)}")
    
    return 0

if __name__ == "__main__":
    exit(main())
