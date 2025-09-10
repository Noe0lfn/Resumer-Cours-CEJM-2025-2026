import os
import sys
import shutil
import time
import datetime
import subprocess
import json

BASE = os.path.expanduser('~/Desktop/Conversion audio vers texte')

# Dossiers (conformes à ton plan)
DIR_AUDIO            = os.path.join(BASE, 'audio')
DIR_AUDIO_DONE       = os.path.join(BASE, 'audio_fini')
DIR_TRANS            = os.path.join(BASE, 'transcription')
DIR_TRANS_DONE       = os.path.join(BASE, 'transcription_fini')
DIR_FUSION           = os.path.join(BASE, 'fusion')
DIR_FUSION_DONE      = os.path.join(BASE, 'fusion_fini')
DIR_DECOUPAGE        = os.path.join(BASE, 'decoupage-texte')
DIR_DECOUPAGE_DONE   = os.path.join(BASE, 'decoupage-texte_fini')  # pas d'accent = moins de soucis
DIR_RESUMER          = os.path.join(BASE, 'resumer')
DIR_RESUMER_DONE     = os.path.join(BASE, 'resumer_fini')

# Binaries / modèles
WHISPER_BIN   = os.path.expanduser('~/whisper.cpp/build/bin/whisper-cli')
WHISPER_MODEL = os.path.expanduser('~/whisper.cpp/models/ggml-medium.bin')

# Ollama
OLLAMA_URL   = 'http://localhost:11434/api/generate'
OLLAMA_MODEL = 'mixtral'  # Mixtral 8x7B
TEMPERATURE  = 0.2        # style scolaire
MAX_OUTPUT_TOKENS = 2048  # si jamais tu l'utilises côté LLM (ici on stream=False)

# Taille des blocs
MAX_TOKENS_PER_BLOC    = 25000  # cible ~25k tokens
FALLBACK_CHARS_PER_TOKEN = 4    # estimation si tiktoken indispo

# Prompts
PROMPT_BLOC = """Voici une partie (un bloc) d’un cours CEJM.
Résume uniquement ce bloc de façon claire et structurée (titres/sous-titres si nécessaire).
Ajoute les exemples rencontrés avec la mention "Exemple : ...".
Conclue le bloc par un mini glossaire des mots difficiles (tableau | Mot complexe | Définition simple |).
N'utilise que le texte encadré par <bloc> ... </bloc>."""

PROMPT_FINAL = """Voici les résumés de plusieurs blocs d’un même cours de Culture Économique, Juridique et Managériale (CEJM). 

Ta mission est de :
1. Fusionner tous ces résumés partiels en un seul document clair, structuré et cohérent.
2. Organiser le cours avec des titres et sous-titres logiques.
3. Intégrer tous les exemples pertinents donnés dans les résumés de blocs (écris-les avec la mention "Exemple : ...").
4. Créer un glossaire unique regroupant tous les mots et notions complexes de l’ensemble du cours 
   → présente-le sous forme de tableau :
     | Mot complexe | Définition simple |
5. Terminer par un résumé flash en 5 lignes maximum qui reprend l’essentiel à savoir pour réviser rapidement.
Utilise exclusivement le contenu entre <resumes> et </resumes>. N'ajoute aucune information qui n'y figure pas.
"""

DIR_RESUMER_BLOCS = os.path.join(BASE, 'resumer', 'blocs_intermediaires')

# Système (rôle) pour ancrer FR + style prof CEJM
SYSTEM_FR = (
    "Tu es un professeur de BTS SIO spécialisé en CEJM. "
    "Réponds UNIQUEMENT en français, de manière claire, structurée et pédagogique."
)

def ensure_dirs():
    for d in [DIR_AUDIO, DIR_AUDIO_DONE, DIR_TRANS, DIR_TRANS_DONE,
              DIR_FUSION, DIR_FUSION_DONE, DIR_DECOUPAGE, DIR_DECOUPAGE_DONE,
              DIR_RESUMER, DIR_RESUMER_DONE, DIR_RESUMER_BLOCS]:
        os.makedirs(d, exist_ok=True)


def run(cmd):
    # aide pour afficher proprement les erreurs
    print("→", " ".join(cmd))
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr)
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return res.stdout

def transcribe_all_mp3():
    mp3s = [f for f in os.listdir(DIR_AUDIO) if f.lower().endswith('.mp3')]
    if not mp3s:
        print("ℹ️ Aucun .mp3 à traiter dans audio/")
        return []
    out_txt_files = []
    for f in mp3s:
        src = os.path.join(DIR_AUDIO, f)
        print(f"🎤 Transcription : {src}")
        run([WHISPER_BIN, "-m", WHISPER_MODEL, "-f", src, "-l", "fr", "-otxt"])
        produced = src + ".txt"
        if not os.path.isfile(produced):
            # selon versions, whisper peut écrire à côté : on tente plan B: même nom dans cwd
            alt = os.path.basename(src) + ".txt"
            if os.path.isfile(alt):
                produced = alt
        if not os.path.isfile(produced):
            raise FileNotFoundError(f"Sortie TXT introuvable pour {src}")
        dest_txt = os.path.join(DIR_TRANS, os.path.basename(produced))
        shutil.move(produced, dest_txt)
        out_txt_files.append(dest_txt)
        # ranger le mp3
        shutil.move(src, os.path.join(DIR_AUDIO_DONE, os.path.basename(src)))
    return out_txt_files

def fuse_transcriptions_to_single_file():
    # Fusionner tous les .txt présents dans DIR_TRANS en un seul fichier horodaté
    txts = [os.path.join(DIR_TRANS, f) for f in os.listdir(DIR_TRANS) if f.endswith('.txt')]
    if not txts:
        print("ℹ️ Aucun .txt à fusionner dans transcription/")
        return None
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fused_name = f"{timestamp}_CEJM_fusion.txt"
    fused_path = os.path.join(DIR_FUSION, fused_name)
    with open(fused_path, "w", encoding="utf-8") as out:
        for i, p in enumerate(sorted(txts)):
            with open(p, "r", encoding="utf-8") as inp:
                txt = inp.read().strip()
            out.write(txt)
            if i < len(txts) - 1:
                out.write("\n\n---\n\n")  # séparateur doux
    # déplacer tous les txt de transcription vers transcription_fini
    for p in txts:
        shutil.move(p, os.path.join(DIR_TRANS_DONE, os.path.basename(p)))
    return fused_path

def try_import_tiktoken():
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return enc
    except Exception:
        return None

def split_to_blocks(fused_path):
    # créer un sous-dossier dans decoupage-texte du nom du fichier sans extension
    base = os.path.splitext(os.path.basename(fused_path))[0]
    out_dir = os.path.join(DIR_DECOUPAGE, base)
    os.makedirs(out_dir, exist_ok=True)

    with open(fused_path, "r", encoding="utf-8") as f:
        text = f.read()

    enc = try_import_tiktoken()
    blocks_paths = []

    if enc:
        tokens = enc.encode(text)
        total = len(tokens)
        print(f"🔎 Découpage par tokens (tiktoken) — total ≈ {total} tokens")
        start = 0
        idx = 0
        while start < total:
            end = min(start + MAX_TOKENS_PER_BLOC, total)
            block_tokens = tokens[start:end]
            block_text = enc.decode(block_tokens)
            idx += 1
            outp = os.path.join(out_dir, f"bloc_{idx}.txt")
            with open(outp, "w", encoding="utf-8") as g:
                g.write(block_text)
            blocks_paths.append(outp)
            start = end
    else:
        print("⚠️ tiktoken indisponible — fallback caractères approximatifs")
        block_size = MAX_TOKENS_PER_BLOC * FALLBACK_CHARS_PER_TOKEN
        n = len(text)
        start = 0
        idx = 0
        while start < n:
            end = min(start + block_size, n)
            idx += 1
            outp = os.path.join(out_dir, f"bloc_{idx}.txt")
            with open(outp, "w", encoding="utf-8") as g:
                g.write(text[start:end])
            blocks_paths.append(outp)
            start = end

    # ranger le fused dans fusion_fini
    shutil.move(fused_path, os.path.join(DIR_FUSION_DONE, os.path.basename(fused_path)))
    return out_dir, blocks_paths

def ollama_generate(prompt, text, *, system=None, num_ctx=32768, temperature=0.2):
    """
    Appel Ollama /api/generate avec:
    - system: rôle (prof CEJM, FR only)
    - prompt: consigne
    - text: contenu du bloc / des résumés, encadré par balises par l'appelant
    """
    import requests
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"{prompt}\n\n{text}",
        "stream": False,  # on récupère la réponse quand c'est fini
        "options": {
            "num_ctx": num_ctx,
            "temperature": temperature
        }
    }
    if system:
        payload["system"] = system
    r = requests.post(OLLAMA_URL, json=payload, timeout=900)
    r.raise_for_status()
    data = r.json()
    return data.get("response", "")

def summarize_blocks(blocks_paths, out_basename):
    """
    Résume chaque bloc avec Mixtral et sauvegarde aussi chaque résumé
    dans resumer/blocs_intermediaires/<out_basename>/
    """
    summaries = []

    # dossier spécifique pour ce cours
    bloc_dir = os.path.join(DIR_RESUMER_BLOCS, out_basename)
    os.makedirs(bloc_dir, exist_ok=True)

    for idx, p in enumerate(blocks_paths, start=1):
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        wrapped = f"<bloc>\n{content}\n</bloc>"
        print(f"🧠 Résumé bloc {idx}/{len(blocks_paths)} …")

        summary = ollama_generate(
            PROMPT_BLOC,
            wrapped,
            system=SYSTEM_FR,
            num_ctx=32768,
            temperature=TEMPERATURE
        )
        summaries.append(summary)

        # Sauvegarder le résumé intermédiaire
        bloc_file = os.path.join(bloc_dir, f"resume_bloc_{idx}.md")
        with open(bloc_file, "w", encoding="utf-8") as g:
            g.write(summary)

    return summaries

def final_fusion_markdown(summaries, out_basename):
    """
    Fusion finale:
    - N'utilise PAS le premier résumé (exclusion demandée): summaries[1:]
    - Encadre les résumés dans <resumes> ... </resumes> pour contraindre le modèle
    """
    print("🧠 Fusion finale des résumés de blocs …")

    if len(summaries) <= 1:
        usable = summaries[:]  # s'il n'y en a qu'un, on prend tout de même
    else:
        usable = summaries[1:]  # ⬅️ exclusion du premier

    big_text = "\n\n---\n\n".join(usable)
    wrapped = f"<resumes>\n{big_text}\n</resumes>"

    final_md = ollama_generate(
        PROMPT_FINAL,
        wrapped,
        system=SYSTEM_FR,
        num_ctx=32768,
        temperature=TEMPERATURE
    )

    md_name = f"resumer_{out_basename}.md"
    md_path = os.path.join(DIR_RESUMER, md_name)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(final_md)

    # Copier dans resumer_fini/
    shutil.copy(md_path, os.path.join(DIR_RESUMER_DONE, os.path.basename(md_path)))

    # Copier dans ton repo VS Code local (si présent)
    repo_dir = "/Users/admin/Documents/VS Code/Resumer-Cours-CEJM-2025-2026"
    if os.path.isdir(repo_dir):
        shutil.copy(md_path, os.path.join(repo_dir, os.path.basename(md_path)))
        print(f"✅ Copié aussi dans le repo VS Code : {repo_dir}")
    else:
        print(f"⚠️ Repo VS Code introuvable : {repo_dir}")

    return md_path

def main():
    ensure_dirs()

    # 1) Transcrire tous les MP3
    transcribed = transcribe_all_mp3()

    # 2) Fusionner tous les TXT présents dans transcription/
    fused_path = fuse_transcriptions_to_single_file()
    if not fused_path:
        print("ℹ️ Rien à fusionner — fin.")
        return

    # 3) Découper en blocs (25k tokens cibles)
    out_dir, blocks = split_to_blocks(fused_path)
    if not blocks:
        print("❌ Aucun bloc créé — fin.")
        return

    # 4) Résumer les blocs (Mixtral via Ollama)
    out_basename = os.path.basename(out_dir)  # même nom que le dossier de blocs
    summaries = summarize_blocks(blocks, out_basename)


    # 5) Fusion finale en .md dans resumer/ (+ copie vers resumer_fini/ et repo VS Code)
    out_basename = os.path.basename(out_dir)  # même nom que le dossier de blocs
    md_path = final_fusion_markdown(summaries, out_basename)
    print(f"✅ Résumé global (Markdown) : {md_path}")

    # 6) Ranger le dossier de découpage dans decoupage-texte_fini/
    shutil.move(out_dir, os.path.join(DIR_DECOUPAGE_DONE, os.path.basename(out_dir)))
    print("✅ Dossier de découpe archivé.")

    print("\n🎉 Pipeline terminé.")

if __name__ == "__main__":
    # vérifs rapides
    for needed in [WHISPER_BIN, WHISPER_MODEL]:
        if not os.path.exists(needed):
            print(f"❌ Manquant : {needed}")
            sys.exit(1)
    main()
