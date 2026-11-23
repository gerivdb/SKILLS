#!/usr/bin/env python3
# =============================================================================
# benchmark_llux.py — Mesure du débit d'inférence LLUX
#
# Mesure le nombre de tokens par seconde (tok/s) du moteur LLaMA sur ENV2.
#
# Utilisation :
#   python benchmark_llux.py --model chemin/vers/modele.gguf --prompt "texte"
#   python benchmark_llux.py --model chemin/vers/modele.gguf --prompt "texte" --tokens 50
# =============================================================================

import argparse
import time
import sys
import os

def benchmark_llux(model_path, prompt, num_tokens=50, verbose=True):
    """
    Teste le débit d'inférence d'un modèle LLaMA.
    
    Args:
        model_path: Chemin vers le fichier .gguf du modèle
        prompt: Texte de prompt pour l'inférence
        num_tokens: Nombre de tokens à générer
        verbose: Afficher les détails
    
    Returns:
        dict avec 'tokens_per_second', 'total_time', 'num_tokens'
    """
    try:
        from llama_cpp import Llama
    except ImportError:
        print("ERREUR : llama-cpp-python n'est pas installé.")
        print("Installez avec : pip install llama-cpp-python")
        return None
    
    try:
        llm = Llama(model_path=model_path, n_ctx=512, n_threads=16, verbose=False)
    except Exception as e:
        print(f"ERREUR lors du chargement du modèle : {e}")
        return None
    
    # Warm-up (1 tour pour charger le modèle en mémoire)
    if verbose:
        print("Chargement et warm-up du modèle...")
    _ = llm(prompt="Test de warm-up", max_tokens=1, echo=False)
    
    # Mesure réelle
    start = time.perf_counter()
    response = llm(prompt=prompt, max_tokens=num_tokens, echo=False)
    end = time.perf_counter()
    
    total_time = end - start
    tokens_generated = num_tokens
    tokens_per_second = tokens_generated / total_time if total_time > 0 else 0
    
    if verbose:
        print(f"\n=== RÉSULTAT BENCHMARK LLUX ===")
        print(f"Modèle : {os.path.basename(model_path)}")
        print(f"Prompt : {prompt[:50]}...")
        print(f"Tokens générés : {tokens_generated}")
        print(f"Temps total : {total_time:.3f} s")
        print(f"Débit : {tokens_per_second:.2f} tok/s")
        print(f"Temps par token : {1000/total_time:.1f} ms/token" if tokens_per_second > 0 else "N/A")
    
    return {
        "tokens_per_second": tokens_per_second,
        "total_time": total_time,
        "num_tokens": tokens_generated,
        "model_path": model_path
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark de déduction LLUX")
    parser.add_argument("--model", required=True, help="Chemin vers le fichier .gguf du modèle")
    parser.add_argument("--prompt", default="Bonjour, comment allez-vous ?", help="Texte de prompt")
    parser.add_argument("--tokens", type=int, default=50, help="Nombre de tokens à générer")
    
    args = parser.parse_args()
    
    result = benchmark_llux(args.model, args.prompt, args.tokens)
    
    if result:
        print(f"\n✓ Débit : {result['tokens_per_second']:.2f} tok/s")
    else:
        print("✗ Échec du benchmark")
        sys.exit(1)