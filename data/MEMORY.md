# RTCF · Pétales — Mémoire projet Claude

> Charge ce fichier en début de session pour reprendre le contexte complet.
> Commande : "Lis data/MEMORY.md et reprends le contexte du projet."

---

## Le projet

**Les Glycines** (anciennement « Divine Sakura », puis RTCF · Pétales) — application web mobile de suivi de collection de fleurs pour les joueuses du club RTCF (Cozy Florist). Le nom affiché (header + `<title>`) est **Les Glycines**.

- Chaque joueuse a un profil et peut cocher les fleurs qu'elle possède
- Vue équipe avec classement, vue détail par fleur/joueuse
- Données partagées en temps réel via Supabase (toutes les joueuses voient la même collection)
- Synchronisation automatique toutes les 30 secondes

---

## Stack technique

| Élément | Détail |
|---|---|
| App | Fichier HTML statique unique (`index.html`) |
| Générateur | `data/generate_app.py` (Python, lit le xlsx et injecte les données + code) |
| Données source | `COZY FLEURIST - Pétales FR.xlsx` (feuille `Fleurs`) |
| Backend | Supabase (REST API, clé anon publique) |
| Stockage local | localStorage (clé `rtcf_v3`) |
| Profil courant | localStorage (clé `rtcf_me`) |

**Pour régénérer l'app après modif du xlsx ou du code :**
```
py data/generate_app.py
```

---

## Supabase

- **URL** : `https://qbuxhzvnbnjuibbusomn.supabase.co`
- **Clé anon** : `sb_publishable_0QYFdSbpvQQPBmlINtn2fw_Qeo4kDR4`
- **Table principale** : `rtcf_data` — id=1, colonnes : `payload` (JSON), `updated_at`
- **Table logs IT** : `rtcf_logs` — colonnes : `id`, `ts`, `event`, `player_id`, `player_name`, `ua`, `screen`, `lang`, `detail`

**Reset de la séquence ID après suppression de logs :**
```sql
-- Vider + reset à 1 (recommandé)
TRUNCATE TABLE rtcf_logs RESTART IDENTITY;

-- Reset uniquement le compteur (sans supprimer)
ALTER SEQUENCE rtcf_logs_id_seq RESTART WITH 1;
```

---

## Utilisateurs & accès

| Rôle | Identifiant | Détail |
|---|---|---|
| Admin Charline | `p1` (Rose Bouquet) | Accès onglet "Gérer" via PIN `0909` |
| Admin Court of Bloom | `CourtofBloom / Margaux` | PIN `1910` |
| Admin Sefkyy1 | `Sefkyy1` | PIN `1975` |
| Logs IT | Propriétaire du repo | Lecture via dashboard Supabase uniquement |
| Joueuses | `p0` à `p33` + `p_[timestamp]` | Profils sélectionnés sans mot de passe |

- 34 joueuses, ~362 fleurs au dernier build
- Pseudo affiché = partie après `/` dans le nom (ex: `TheaLrd / Théa` → affiche `Théa`)
- Nom en gras = partie AVANT `/` (ex: `Rose Bouquet`), label facultatif = partie APRÈS `/` (ex: `Charline`)

**Système multi-admin** (depuis 2026-06) :
- `ADMIN_PINS = {'p1':'0909'}` : admins par ID stable + leur PIN
- `ADMIN_NAME_PINS = {'CourtofBloom':'1910','Sefkyy1':'1975'}` : admins résolus par **nom** au chargement (`resolveAdminNames()` appelée après `initData()`) — robuste si l'ID change après régénération du xlsx
- `isAdmin()` → `myId in ADMIN_PINS` ; `submitPin()` valide `val === ADMIN_PINS[myId]` (PIN propre à chaque admin)

---

## Système de logs IT

Logs invisibles dans l'app, écrits dans `rtcf_logs` Supabase, lisibles uniquement via le dashboard Supabase (policy RLS : INSERT anon autorisé, SELECT anon interdit).

**Événements loggés :**
| Event | Déclencheur |
|---|---|
| `page_load` | Ouverture du site |
| `sync_ok` | Connexion Supabase réussie au chargement |
| `sync_error` | Échec de sauvegarde |
| `sync_offline` | Pas de réseau au démarrage |
| `sync_update` | Mise à jour distante détectée et appliquée |
| `profile_select` | Joueuse choisit son profil |
| `profile_clear` | Clic sur "Changer de profil" |

---

## Système de sauvegarde automatique

GitHub Actions — tourne entièrement sur GitHub, indépendant du poste local.

- **Fichier** : `.github/workflows/backup.yml` (doit rester à la racine — contrainte GitHub)
- **Sauvegardes stockées** : `data/backups/weekly/` et `data/backups/monthly/`
- **Fréquence** : chaque dimanche à 7h00 UTC → `data/backups/weekly/YYYY-MM-DD.json`
- **Consolidation mensuelle** : 1er dimanche du mois → copie en `data/backups/monthly/YYYY-MM.json` + supprime les anciens hebdos
- **Déclenchement manuel** : GitHub → Actions → "Sauvegarde Divine Sakura" → Run workflow
- **Suivi** : `github.com/Cozy-Florist/RTCF/actions`

---

## Repository Git

- **Remote** : `https://github.com/Cozy-Florist/RTCF.git`
- **Branche principale** : `main`
- **Token actif** : `ghp_` classic PAT (scopes : `repo` + `workflow`) — fourni en session, ne pas stocker ici
- **Ancien nom** : `Cozy-Fleurist` → renommé `Cozy-Florist` (GitHub redirige l'ancien URL)

**Structure du repo :**
```
RTCF/
├── index.html                    ← app web (généré, ne pas éditer à la main)
├── rtcf_fleurs.html              ← version standalone (pour l'exe)
├── RTCF_Petales.exe              ← launcher Windows
├── COZY FLEURIST - Pétales FR.xlsx
├── .github/
│   └── workflows/
│       └── backup.yml            ← workflow GitHub Actions (backup auto)
└── data/
    ├── MEMORY.md                 ← ce fichier
    ├── generate_app.py           ← générateur HTML (source de vérité du code)
    ├── rtcf_launcher.py          ← launcher Python (embarque rtcf_fleurs.html)
    └── backups/
        ├── weekly/               ← sauvegardes hebdomadaires (JSON)
        └── monthly/              ← sauvegardes mensuelles (JSON)
```

---

## Décisions techniques prises

- **Logs IT dans `data/` non auto-chargés** : intentionnel, le propriétaire contrôle quand Claude charge ce contexte pour éviter les mélanges entre instances
- **Clé Supabase dans le JS** : assumé (app publique, clé anon, RLS protège la lecture des logs)
- **PINs admin hardcodés** : Charline `0909`, Court of Bloom `1910`, Sefkyy1 `1975` (un PIN par admin)
- **Auto-suppression de profil interdite** : une joueuse ne peut pas supprimer son propre profil (bouton remplacé par « (toi) » dans Gérer + garde JS dans `askDelPlayerById` qui bloque si `id===myId`)
- **Warning RLS Supabase** sur `rtcf_logs` (INSERT always true) : ignoré volontairement, comportement attendu
- **`index.html` jamais édité à la main** : toujours regénéré via `py data/generate_app.py`
- **`.github/workflows/` à la racine** : contrainte GitHub Actions, impossible de déplacer dans `data/`
- **Backups dans `data/backups/`** : cohérent avec le reste des fichiers de gestion

---

## Fonctionnalités app (implémentées)

- Système de rareté : N / R / SR / SSR / UR avec badges colorés
- Système de points : 9 / 14 / 21 / 23 / 25 / 28 / 30 pts
- Toggle fleurs uniquement depuis l'onglet "Fleurs" (pas depuis les profils)
- Profil : nom en gras (non modifiable) + label facultatif modifiable
- Multi-admin : Charline (p1, 0909), Court of Bloom (1910), Sefkyy1 (1975) — accès onglet "Gérer", édition des fleurs
- Auto-suppression de son propre profil désactivée
- FAB "Ajouter au catalogue" uniquement sur l'onglet Fleurs
- Barres de progression alignées (largeur fixe sur le bouton toggle)
