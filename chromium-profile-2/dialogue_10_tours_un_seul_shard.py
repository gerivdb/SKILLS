#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dialogue de 10 tours sur UN SEUL shard Gemini (vrai Profil 2, port 9222).
Même conversation continue, une question après l'autre, avec réponse de Gemini entre chaque.
"""

import sys
import time
import json
import hashlib
from datetime import datetime, timezone

sys.path.insert(0, r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-profile-2")
from chromium_cdp_client import ChromiumCDPClient

TARGET_ID = None  # sera défini à l'ouverture de l'onglet

QUESTIONS = [
    "Bonjour Gemini. Je suis un agent KiloCode sur l'écosystème gerivdb (ENV2, HP Z600). Peux-tu m'expliquer ce qu'est le protocole BDCP (Behind CDP) et à quoi il sert pour protéger le quota Antigravity ?",
    "Quelle est la différence entre le protocole BDCP réseau sur localhost:18000 et le routage BDCP du Gateway Manager sur localhost:13378 ?",
    "Comment fonctionne le quota Antigravity et pourquoi est-il protégé par le mode BDCP ? Que se passe-t-il si on bascule en mode FREE sans ordre explicite ?",
    "Qu'est-ce que GOST (Ghost Operations Stealth Technology) et quel est son rôle dans l'accès aux LLMs externes depuis ENV2 ?",
    "Quelle est la différence entre ENV2 (node HP Z600 physique) et ENV3 (Cloud Mesh) dans l'architecture gerivdb ?",
    "Qu'est-ce que la boucle M3 et comment un agent peut éviter de tomber dans une boucle d'intention sans exécution d'outil ?",
    "Comment fonctionne le skill chromium-profile-2 pour piloter Chromium via CDP, et quelles sont ses limites ?",
    "Quelles sont tes recommandations pour améliorer la fiabilité de la communication entre ENV2 et ENV3 dans l'écosystème gerivdb ?",
    "Selon toi, quel devrait être le prochain pas pour consolider la gouvernance du métacluster gerivdb ?",
    "Si tu devais donner un conseil final à un agent KiloCode opérant sur ENV2 vers ENV3, lequel serait-il ?",
]


def ecrire_message(client, texte):
    write_js = (
        "(function() { "
        "var input = document.querySelector('[aria-label=\"Saisissez un prompt pour Gemini\"]'); "
        "if (!input) { var all = document.querySelectorAll(\"div[contenteditable='true']\"); if (all.length > 0) { input = all[0]; } else { return 'CHAMP_INTROUVABLE'; } } "
        "input.focus(); "
        "var range = document.createRange(); "
        "range.selectNodeContents(input); "
        "range.deleteContents(); "
        "var node = document.createTextNode(" + repr(texte) + "); "
        "range.insertNode(node); "
        "input.dispatchEvent(new InputEvent('input', { inputType: 'insertText', data: " + repr(texte) + ", bubbles: true })); "
        "return 'ECRIT:' + input.innerText.length; "
        "})()"
    )
    result = client.send("Runtime", "evaluate", {"expression": write_js, "returnByValue": True})
    return result.get("result", {}).get("result", {}).get("value", "")


def envoyer_entree(client):
    key_js = (
        "(function() { "
        "var input = document.querySelector('[aria-label=\"Saisissez un prompt pour Gemini\"]'); "
        "if (!input) { var all = document.querySelectorAll(\"div[contenteditable='true']\"); if (all.length > 0) { input = all[0]; } else { return 'CHAMP_INTROUVABLE'; } } "
        "input.focus(); "
        "var down = new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', bubbles: true, cancelable: true }); "
        "var up = new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', bubbles: true, cancelable: true }); "
        "input.dispatchEvent(down); "
        "input.dispatchEvent(up); "
        "return 'ENTREE_SIMULEE'; "
        "})()"
    )
    result = client.send("Runtime", "evaluate", {"expression": key_js, "returnByValue": True})
    return result.get("result", {}).get("result", {}).get("value", "")


def lire_page_complete(client):
    read_js = "(function() { return document.body.innerText.substring(0, 8000); })()"
    result = client.send("Runtime", "evaluate", {"expression": read_js, "returnByValue": True})
    return result.get("result", {}).get("result", {}).get("value", "")


def extraire_derniere_reponse(texte_page):
    """Extrait la dernière réponse de Gemini à partir du texte complet de la page."""
    if not texte_page or "Gemini a dit" not in texte_page:
        return None
    # Trouver toutes les occurrences de "Gemini a dit" et prendre la dernière
    parties = texte_page.split("Gemini a dit")
    if len(parties) <= 1:
        return None
    derniere = parties[-1]
    return derniere.strip()[:1500]


def main():
    client = ChromiumCDPClient()

    # Ouvrir un seul onglet pour toute la conversation
    print("=== Ouverture d'un seul onglet Gemini sur le vrai Profil 2 ===")
    new_tab = client.open_tab("https://gemini.google.com/app")
    target_id = new_tab["targetId"]
    print(f"Nouvel onglet : {target_id}")

    time.sleep(5)

    # Naviguer vers Gemini dans cet onglet
    client.attach_to_tab(target_id)
    nav = client.send("Page", "navigate", {"url": "https://gemini.google.com/app"})
    print(f"Navigation : {nav.get('result', {}).get('frameId', 'OK')}")

    time.sleep(5)
    r = client.send("Runtime", "evaluate", {"expression": "document.title", "returnByValue": True})
    print(f"Titre : {r.get('result', {}).get('result', {}).get('value', '')}")

    resultats = []

    for i, question in enumerate(QUESTIONS, 1):
        print(f"\n{'='*60}")
        print(f"TOUR {i}/10 (même shard)")
        print(f"Question : {question[:80]}...")
        print(f"{'='*60}")

        t_debut = time.perf_counter()

        # Écrire la question
        ecriture = ecrire_message(client, question)
        print(f"Écriture : {ecriture}")

        # Envoyer
        entree = envoyer_entree(client)
        print(f"Envoi : {entree}")

        # Attendre la réponse (jusqu'à 25s)
        t_reponse = None
        reponse_texte = None
        deadline = time.perf_counter() + 25

        while time.perf_counter() < deadline:
            time.sleep(2.0)
            page_texte = lire_page_complete(client)
            reponse_texte = extraire_derniere_reponse(page_texte)
            if reponse_texte and len(reponse_texte) > 20:
                t_reponse = time.perf_counter()
                break

        latence = (t_reponse - t_debut) if t_reponse else None
        succes = reponse_texte is not None and len(reponse_texte) > 20

        print(f"Latence : {round(latence, 3)}s" if latence else "Latence : N/A")
        print(f"Succès : {succes}")
        if reponse_texte:
            print(f"Réponse Gemini : {reponse_texte[:400]}...")
        else:
            print("AUCUNE RÉPONSE REÇUE")

        resultats.append({
            "tour": i,
            "question": question,
            "t_debut_utc": datetime.now(timezone.utc).isoformat(),
            "t_reponse_utc": datetime.now(timezone.utc).isoformat() if t_reponse else None,
            "latence_secondes": round(latence, 3) if latence else None,
            "succes": succes,
            "reponse_brute": reponse_texte,
        })

        # Petite pause entre les tours sur le même shard
        time.sleep(2)

    client.close_ws()

    # Rapport final
    succes = sum(1 for r in resultats if r['succes'])
    echecs = len(resultats) - succes
    latences = [r['latence_secondes'] for r in resultats if r['latence_secondes']]
    latence_moyenne = sum(latences) / len(latences) if latences else None

    print(f"\n{'='*60}")
    print(f"RAPPORT FINAL — 10 TOURS SUR UN SEUL SHARD")
    print(f"{'='*60}")
    print(f"Tours réussis : {succes}/10")
    print(f"Tours échoués : {echecs}/10")
    print(f"Latence moyenne : {round(latence_moyenne, 3)}s" if latence_moyenne else "Latence moyenne : N/A")

    snapshot = json.dumps(resultats, ensure_ascii=False, sort_keys=True)
    hash_sha256 = hashlib.sha256(snapshot.encode("utf-8")).hexdigest()
    print(f"SHA-256 : {hash_sha256}")
    print(f"Timestamp UTC : {datetime.now(timezone.utc).isoformat()}")

    # Sauvegarde
    with open("dialogue_10_tours_un_seul_shard.json", "w", encoding="utf-8") as f:
        json.dump({
            "resultats": resultats,
            "hash_sha256": hash_sha256,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "tours_reussis": succes,
            "tours_echecs": echecs,
            "latence_moyenne": latence_moyenne,
            "methode": "un_seul_shard_conversation_continue",
        }, f, ensure_ascii=False, indent=2)
    print("Résultat sauvegardé : dialogue_10_tours_un_seul_shard.json")

    # Détail par tour
    print(f"\n{'='*60}")
    print(f"DÉTAIL PAR TOUR")
    print(f"{'='*60}")
    for r in resultats:
        print(f"\n--- Tour {r['tour']} ---")
        print(f"Question : {r['question'][:100]}...")
        print(f"Réponse : {(r['reponse_brute'] or 'AUCUNE')[:300]}...")


if __name__ == "__main__":
    main()
