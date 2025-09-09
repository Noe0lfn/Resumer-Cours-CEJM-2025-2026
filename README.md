# 📘 README – Pipeline CEJM (Conversion Audio → Résumé Markdown)

## 🎯 Objectif

Ce projet automatise la conversion de cours **CEJM en BTS SIO** au format audio (`.mp3`) en un **résumé pédagogique clair et structuré** au format Markdown (`.md`).

Le pipeline complet :

1. Convertit l’audio en texte avec **Whisper.cpp**.
2. Fusionne et archive les transcriptions.
3. Découpe le texte en blocs (\~25k tokens max).
4. Résume chaque bloc avec **Mixtral 8x7B** via **Ollama**.
5. Fusionne les résumés en un document unique clair et lisible.
6. Stocke le résultat final dans :

   * `resumer/` (version de travail),
   * `resumer_fini/` (archive),
   * et copie automatiquement dans ton **repository local VS Code** (`/Users/admin/Documents/VS Code/Resumer-Cours-CEJM-2025-2026`).

---

## 📂 Structure des dossiers

```
~/Desktop/Conversion audio vers texte/
├── audio/                  # Dépose ici tes fichiers .mp3 de cours
├── audio_fini/             # MP3 traités (archivés automatiquement)
├── transcription/          # TXT générés par Whisper
├── transcription_fini/     # TXT archivés après fusion
├── fusion/                 # Fusion temporaire des TXT
├── fusion_fini/            # Fusion archivées
├── decoupage-texte/        # Blocs créés (25k tokens max par fichier)
├── decoupage-texte_fini/   # Blocs archivés après résumé
├── resumer/                # Résumés globaux en Markdown
├── resumer_fini/           # Résumés globaux archivés
├── decoupe_tokens.py       # Script de découpe (utilisé en interne)
├── script_maitre.py        # 🚀 Script principal (lancer ce fichier)
└── transcription.sh        # Script Whisper (optionnel, pas nécessaire)
```

---

## ⚙️ Fonctionnement du script maître (`script_maitre.py`)

Quand tu lances le script :

1. **Transcription audio → texte**

   * Tous les `.mp3` de `audio/` sont convertis en `.txt` avec **Whisper.cpp**.
   * Les `.mp3` traités sont déplacés dans `audio_fini/`.
   * Les `.txt` sont placés dans `transcription/`.

2. **Fusion des transcriptions**

   * Tous les `.txt` sont fusionnés en un seul fichier (nommé avec la date/heure).
   * Ce fichier est stocké dans `fusion/`.
   * Les `.txt` originaux sont archivés dans `transcription_fini/`.

3. **Découpage en blocs**

   * Le fichier fusionné est découpé en blocs de **25k tokens max** (≈ 15 000 mots).
   * Les blocs sont enregistrés dans `decoupage-texte/<nom_du_fichier>/`.
   * Le fichier fusionné est ensuite déplacé vers `fusion_fini/`.

4. **Résumé avec Mixtral 8x7B (Ollama)**

   * Chaque bloc est résumé individuellement avec un **prompt CEJM**.
   * Les résumés sont fusionnés en un seul document global clair.

5. **Export du résumé global**

   * Le résumé est sauvegardé en Markdown (`.md`) dans :

     * `resumer/` (travail)
     * `resumer_fini/` (archive)
     * ton repo VS Code (`/Users/admin/Documents/VS Code/Resumer-Cours-CEJM-2025-2026/`).

6. **Archivage des blocs**

   * Le dossier de découpe est déplacé dans `decoupage-texte_fini/`.

---

## 🛠️ Installation (prérequis, une seule fois)

1. **Installer Homebrew** (si pas déjà fait) :

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Installer Whisper.cpp**

   ```bash
   git clone https://github.com/ggerganov/whisper.cpp
   cd whisper.cpp
   make
   # Télécharger modèle medium
   bash ./models/download-ggml-model.sh medium
   ```

3. **Installer Ollama + Mixtral**

   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull mixtral
   ```

4. **Installer Python et libs**

   ```bash
   brew install python@3.12
   cd ~/Desktop/"Conversion audio vers texte"
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip setuptools wheel requests tiktoken
   ```

---

## 🚀 Utilisation (après chaque redémarrage)

1. Activer l’environnement :

   ```bash
   cd ~/Desktop/"Conversion audio vers texte"
   source .venv/bin/activate
   ```

2. Déposer tes `.mp3` dans `audio/`.

3. Lancer le pipeline complet :

   ```bash
   python script_maitre.py
   ```

4. Résultat :

   * Résumé global généré au format `.md` dans `resumer/`
   * Archivé dans `resumer_fini/`
   * Copié automatiquement dans ton repo VS Code :
     `/Users/admin/Documents/VS Code/Resumer-Cours-CEJM-2025-2026`

5. Commit + Push sur GitHub depuis VS Code.

---

## 📊 Notes

* Mixtral 8x7B supporte **32k tokens max** → si un cours > 25k tokens, il est découpé automatiquement.
* La transcription Whisper peut prendre du temps selon la durée du cours.
* Le résumé final est généré en **Markdown clair** : titres, sous-parties, glossaire, résumé flash.