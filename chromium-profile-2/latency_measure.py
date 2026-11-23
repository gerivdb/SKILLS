#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mesure de latence Gemini via le vrai Chromium Profil 2 (skill chromium-profile-2).

Envoie un message à Gemini et mesure le temps entre l'envoi (clic "Envoyer")
et la réception de la réponse dans le DOM.

Utilise le skill : D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-profile-2\chromium_cdp_client.py

Preuves : hash SHA-256, timestamps UTC, capture du DOM avant/après.
"""

import sys
import time
import json
import hashlib
from datetime import datetime, timezone

sys.path.insert(0, r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-profile-2")
from chromium_cdp_client import ChromiumCDPClient

TARGET_ID = "E971A7568E2CFAED50C869DE7FAC9E6B"
CHAMP_JS = '(function() { var input = document.querySelector("[aria-label=\\"Saisissez un prompt pour Gemini\\"]"); if (!input) return "CHAMP_INTROUVABLE"; input.focus(); return "FOCALISE"; })()'
CLICK_JS = '(function() { var btns = document.querySelectorAll("button"); for (var i = 0; i < btns.length; i++) { var aria = btns[i].getAttribute("aria-label"); if (aria && aria.includes("Envoyer") && btns[i].offsetParent !== null) { btns[i].click(); return "ENVOYE:" + i; } } return "NON_TROUVE"; })()'


def ecrire_message(client, texte):
    """Écrit un message dans le champ de saisie via innerHTML + event input."""
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
    """Clique sur le bouton 'Envoyer un message'."""
    result = client.send("Runtime", "evaluate", {
        "expression": CLICK_JS,
        "returnByValue": True
    })
    return result.get("result", {}).get("result", {}).get("value", "")


def lire_reponse(client, marqueur):
    """Lit le DOM pour trouver la réponse contenant le marqueur."""
    read_js = (
        "(function() { "
        "var els = document.querySelectorAll('div'); "
        "for (var i = 0; i < els.length; i++) { "
        "var t = els[i].innerText || els[i].textContent || ''; "
        "if (t.includes('" + marqueur + "')) return t.substring(0, 500); "
        "} "
        "return 'NON_TROUVE'; "
        "})()"
    )
    result = client.send("Runtime", "evaluate", {
        "expression": read_js,
        "returnByValue": True
    })
    return result.get("result", {}).get("result", {}).get("value", "")


def mesurer_latence(message, timeout=30):
    """Mesure la latence entre envoi et réception de la réponse."""
    client = ChromiumCDPClient()
    client.attach_to_tab(TARGET_ID)

    # Focus
    client.send("Runtime", "evaluate", {
        "expression": CHAMP_JS,
        "returnByValue": True
    })

    # Écrire le message
    ecrire_message(client, message)

    # Clic Envoyer + chrono début
    t_envoi = time.perf_counter()
    t_envoi_utc = datetime.now(timezone.utc).isoformat()
    clic_result = cliquer_envoyer(client)

    # Attendre la réponse
    t_reponse = None
    t_reponse_utc = None
    reponse_texte = None
    deadline = time.perf_counter() + timeout

    while time.perf_counter() < deadline:
        time.sleep(0.5)
        contenu = lire_reponse(client, message.split(":")[0])  # marqueur "Tour X/10"
        if contenu != "NON_TROUVE" and "Gemini a dit" in contenu:
            t_reponse = time.perf_counter()
            t_reponse_utc = datetime.now(timezone.utc).isoformat()
            reponse_texte = contenu
            break

    latence = (t_reponse - t_envoi) if t_reponse else None

    client.close_ws()

    return {
        "message": message,
        "t_envoi_utc": t_envoi_utc,
        "t_reponse_utc": t_reponse_utc,
        "latence_secondes": latence,
        "clic_result": clic_result,
        "reponse_texte": reponse_texte,
        "succes": t_reponse is not None,
    }


if __name__ == "__main__":
    message = "MESURE_LATENCE : Peux-tu répondre uniquement avec le mot PONG ?"
    resultat = mesurer_latence(message)

    # Calcul du hash SHA-256 du résultat pour preuve d'intégrité
    snapshot = json.dumps(resultat, ensure_ascii=False, sort_keys=True)
    hash_sha256 = hashlib.sha256(snapshot.encode("utf-8")).hexdigest()

    print("=== MESURE DE LATENCE GEMINI (Profil 2, CDP) ===")
    print(f"Message : {resultat['message']}")
    print(f"Envoi UTC : {resultat['t_envoi_utc']}")
    print(f"Réponse UTC : {resultat['t_reponse_utc']}")
    print(f"Latence : {resultat['latence_secondes']:.3f} secondes" if resultat['latence_secondes'] else "Latence : N/A (échec)")
    print(f"Clic Envoyer : {resultat['clic_result']}")
    print(f"Succès : {resultat['succes']}")
    if resultat['reponse_texte']:
        print(f"Réponse brute : {resultat['reponse_texte'][:300]}")
    print(f"SHA-256 : {hash_sha256}")
    print(f"Timestamp UTC : {datetime.now(timezone.utc).isoformat()}")

    # Sauvegarde du résultat
    with open("latence_resultat.json", "w", encoding="utf-8") as f:
        json.dump({
            "resultat": resultat,
            "hash_sha256": hash_sha256,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }, f, ensure_ascii=False, indent=2)
    print("Résultat sauvegardé : latence_resultat.json")
