#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dialogue réel de 10 tours avec Gemini via le vrai Chromium Profil 2 (skill chromium-profile-2).
Pas de mots vides : vraies questions sur l'écosystème gerivdb, vraies réponses de Gemini.
Preuves : hash SHA-256, timestamps UTC, captures du DOM.
"""

import sys
import time
import json
import hashlib
from datetime import datetime, timezone

sys.path.insert(0, r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-profile-2")
from chromium_cdp_client import ChromiumCDPClient

TARGET_ID = "E971A7568E2CFAED50C869DE7FAC9E6B"

FOCUS_JS = '(function() { var input = document.querySelector("[aria-label=\"Saisissez un prompt pour Gemini\"]"); if (!input) return "CHAMP_INTROUVABLE"; input.focus(); return "FOCALISE"; })()'
CLICK_JS = '(function() { var btns = document.querySelectorAll("button"); for (var i = 0; i < btns.length; i++) { var aria = btns[i].getAttribute("aria-label"); if (aria && aria.includes("Envoyer") && btns[i].offsetParent !== null) { btns[i].click(); return "ENVOYE:" + i; } } return "NON_TROUVE"; })()'


def ecrire_message(client, texte):
    write_js = (
        "(function() { "
        "var input = document.querySelector('[aria-label=\"Saisissez un prompt pour Gemini\"]'); "
        "if (!input) return 'CHAMP_INTROUVABLE'; "
        "input.focus(); "
        "input.textContent = " + repr(texte) + "; "
        "input.innerHTML = " + repr(texte) + "; "
        "input.dispatchEvent(new Event('input', { bubbles: true })); "
        "return 'ECRIT:' + input.innerText.length; "
        "})()"
    )
    result = client.send("Runtime", "evaluate", {
        "expression": write_js,
        "returnByValue": True
    })
    return result.get("result", {}).get("result", {}).get("value", "")


def cliquer_envoyer(client):
    result = client.send("Runtime", "evaluate", {
        "expression": CLICK_JS,
        "returnByValue": True
    })
    return result.get("result", {}).get("result", {}).get("value", "")


def lire_derniere_reponse(client):
    read_js = (
        "(function() { "
        "var els = document.querySelectorAll('div'); "
        "var last = ''; "
        "for (var i = 0; i < els.length; i++) { "
        "var t = els[i].innerText || els[i].textContent || ''; "
        "if (t.includes('Gemini a dit')) last = t; "
        "} "
        "return last; "
        "})()"
    )
    result = client.send("Runtime", "evaluate", {
        "expression": read_js,
        "returnByValue": True
    })
    return result.get("result", {}).get("result", {}).get("value", "")


def dialogue_tour(client, numero, question):
    """Effectue un tour complet : écrire, envoyer, attendre, lire réponse."""
    t_debut = time.perf_counter()
    t_debut_utc = datetime.now(timezone.utc).isoformat()

    # Focus
    client.send("Runtime", "evaluate", {"expression": FOCUS_JS, "returnByValue": True})

    # Écrire
    write_result = ecrire_message(client, question)

    # Cliquer Envoyer
    click_result = cliquer_envoyer(client)

    # Attendre la réponse (jusqu'à 25s)
    t_reponse = None
    t_reponse_utc = None
    reponse_texte = None
    deadline = time.perf_counter() + 25

    while time.perf_counter() < deadline:
        time.sleep(1.0)
        contenu = lire_derniere_reponse(client)
        if contenu and "Gemini a dit" in contenu and len(contenu) > 20:
            t_reponse = time.perf_counter()
            t_reponse_utc = datetime.now(timezone.utc).isoformat()
            reponse_texte = contenu
            break

    latence = (t_reponse - t_debut) if t_reponse else None

    return {
        "tour": numero,
        "question": question,
        "t_debut_utc": t_debut_utc,
        "t_reponse_utc": t_reponse_utc,
        "latence_secondes": round(latence, 3) if latence else None,
        "write_result": write_result,
        "click_result": click_result,
        "reponse_brute": reponse_texte,
        "succes": reponse_texte is not None and len(reponse_texte) > 20,
    }


def main():
    client = ChromiumCDPClient()
    client.attach_to_tab(TARGET_ID)

    questions = [
        "Peux-tu m'expliquer ce qu'est le protocole BDCP (Behind CDP) dans l'écosystème gerivdb et à quoi il sert concrètement ?",
        "Quelle est la différence entre le protocole BDCP réseau sur localhost:18000 et le routage BDCP du Gateway Manager sur localhost:13378 ?",
        "Comment fonctionne le quota Antigravity et pourquoi est-il protégé par le mode BDCP ?",
        "Qu'est-ce que GOST (Ghost Operations Stealth Technology) et quel est son rôle dans l'accès aux LLMs externes ?",
        "Peux-tu expliquer la différence entre ENV2 (node HP Z600) et ENV3 (Cloud Mesh) dans l'architecture gerivdb ?",
        "Qu'est-ce que la boucle M3 et comment un agent peut éviter de tomber dans une boucle d'intention sans exécution ?",
        "Comment fonctionne le skill chromium-profile-2 pour piloter Chromium via CDP, et quelles sont ses limites ?",
        "Quelles sont tes recommandations pour améliorer la fiabilité de la communication entre ENV2 et ENV3 dans l'écosystème gerivdb ?",
        "Selon toi, quel devrait être le prochain pas pour consolider la gouvernance du métacluster gerivdb ?",
        "Si tu devais donner un conseil final à un agent KiloCode opérant sur ENV2 vers ENV3, lequel serait-il ?",
    ]

    resultats = []
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"TOUR {i}/10")
        print(f"Question : {question}")
        print(f"{'='*60}")

        r = dialogue_tour(client, i, question)
        resultats.append(r)

        print(f"Écriture : {r['write_result']}")
        print(f"Clic Envoyer : {r['click_result']}")
        print(f"Latence : {r['latence_secondes']}s" if r['latence_secondes'] else "Latence : N/A")
        print(f"Succès : {r['succes']}")
        if r['reponse_brute']:
            print(f"Réponse Gemini : {r['reponse_brute'][:500]}...")
        else:
            print("AUCUNE RÉPONSE REÇUE")

        # Petite pause entre les tours pour ne pas saturer
        time.sleep(2)

    client.close_ws()

    # Rapport final
    succes = sum(1 for r in resultats if r['succes'])
    echecs = len(resultats) - succes
    latences = [r['latence_secondes'] for r in resultats if r['latence_secondes']]
    latence_moyenne = sum(latences) / len(latences) if latences else None

    print(f"\n{'='*60}")
    print(f"RAPPORT FINAL — 10 TOURS DE DIALOGUE")
    print(f"{'='*60}")
    print(f"Tours réussis : {succes}/10")
    print(f"Tours échoués : {echecs}/10")
    print(f"Latence moyenne : {latence_moyenne:.3f}s" if latence_moyenne else "Latence moyenne : N/A")

    # Hash SHA-256 du rapport complet
    snapshot = json.dumps(resultats, ensure_ascii=False, sort_keys=True)
    hash_sha256 = hashlib.sha256(snapshot.encode("utf-8")).hexdigest()
    print(f"SHA-256 : {hash_sha256}")
    print(f"Timestamp UTC : {datetime.now(timezone.utc).isoformat()}")

    # Sauvegarde
    with open("dialogue_10_tours.json", "w", encoding="utf-8") as f:
        json.dump({
            "resultats": resultats,
            "hash_sha256": hash_sha256,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "tours_reussis": succes,
            "tours_echecs": echecs,
            "latence_moyenne": latence_moyenne,
        }, f, ensure_ascii=False, indent=2)
    print("Résultat sauvegardé : dialogue_10_tours.json")

    # Affichage détaillé de chaque tour
    print(f"\n{'='*60}")
    print(f"DÉTAIL PAR TOUR")
    print(f"{'='*60}")
    for r in resultats:
        print(f"\n--- Tour {r['tour']} ---")
        print(f"Question : {r['question'][:100]}...")
        print(f"Réponse : {(r['reponse_brute'] or 'AUCUNE')[:300]}...")


if __name__ == "__main__":
    main()
