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
| Admin Selkyy1 | `Selkyy1` | PIN `1975` |
| Logs IT | Propriétaire du repo | Lecture via dashboard Supabase uniquement |
| Joueuses | `p0` à `p33` + `p_[timestamp]` | Profils sélectionnés sans mot de passe |

- 34 joueuses, ~362 fleurs au dernier build
- Pseudo affiché = partie après `/` dans le nom (ex: `TheaLrd / Théa` → affiche `Théa`)
- Nom en gras = partie AVANT `/` (ex: `Rose Bouquet`), label facultatif = partie APRÈS `/` (ex: `Charline`)

**Système multi-admin** (depuis 2026-06) :
- `ADMIN_PINS = {'p1':'0909'}` : admins par ID stable + leur PIN
- `ADMIN_NAME_PINS = {'CourtofBloom':'1910','Selkyy1':'1975'}` : admins résolus par **nom** au chargement (`resolveAdminNames()` appelée après `initData()`) — robuste si l'ID change après régénération du xlsx
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
- **Sauvegardes stockées** : `data/backups/daily/` et `data/backups/monthly/`
- **Fréquence** : chaque jour à 7h00 UTC → `data/backups/daily/YYYY-MM-DD.json` (depuis 2026-08 ; avant : hebdo dominical dans `weekly/`)
- **Consolidation mensuelle** : le 1er du mois (`DAY = 01`) → copie en `data/backups/monthly/YYYY-MM.json` + supprime les anciens quotidiens
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
        ├── daily/                ← sauvegardes quotidiennes (JSON)
        └── monthly/              ← sauvegardes mensuelles (JSON)
```

---

## Décisions techniques prises

- **Logs IT dans `data/` non auto-chargés** : intentionnel, le propriétaire contrôle quand Claude charge ce contexte pour éviter les mélanges entre instances
- **Clé Supabase dans le JS** : assumé (app publique, clé anon, RLS protège la lecture des logs)
- **PINs admin hardcodés** : Charline `0909`, Court of Bloom `1910`, Selkyy1 `1975` (un PIN par admin)
- **Auto-suppression de profil interdite** : une joueuse ne peut pas supprimer son propre profil (bouton remplacé par « (toi) » dans Gérer + garde JS dans `askDelPlayerById` qui bloque si `id===myId`)
- **Changement de profil → `refreshAll()` obligatoire** : `setMe()` et `clearMe()` doivent appeler `refreshAll()` (pas seulement `renderProfil()`). Sinon les marqueurs `(toi)` de l'onglet Gérer et `(moi)` de l'onglet Équipe restent figés sur l'ancien profil (bug corrigé en 2026-06). Règle générale : dès que `myId` change, re-rendre TOUTES les vues.
- **`openPinSheet(cb)` accepte un callback** : si fourni, exécuté après déverrouillage PIN au lieu de `goTab('gerer')`. Permet de déclencher une action admin (ex : édition du bloc-notes) depuis n'importe quel onglet. Sans argument → comportement historique (ouvre l'onglet Gérer)
- **Écriture concurrente sûre (2026-07)** : abandon du modèle « dernier qui écrit gagne » (qui réécrivait tout le document JSON et écrasait les modifs des autres). Remplacé par de l'**optimistic concurrency**. `save()` n'existe plus → tout passe par `commit(op)`.
  - chaque mutation = une **opération idempotente** `applyOp(doc,op)`, types : `addPlayer / removePlayer / renamePlayer / addFlower / editFlower / removeFlower / setOwn / setLabel / setNotes / replaceAll`. **`setOwn` est absolu (`val:true/false`)**, jamais un toggle — indispensable pour un rejeu sûr. `replaceAll` (import/reset) préserve `doc.notes`.
  - `commit(op)` : applique en local (UI instantanée) → empile dans `opQueue` → `drain()`.
  - `drain()` : relit le doc frais (`supaFetch`), rejoue les ops en attente, écrit via **compare-and-swap** `supaSaveCAS(doc,base)` = `PATCH …&updated_at=eq.<base>&select=updated_at` avec `Prefer: return=representation` ; **0 ligne renvoyée = conflit** → refait (fetch+rejeu, jusqu'à 8 fois). Puis réconcilie `D` avec le serveur.
  - `checkSync` : si `opQueue` non vide → `drain()` au lieu d'écraser `D`.
  - Corrige : profils supprimés qui réapparaissaient (résurrection Ayra) + collections écrasées quand tout le monde édite avant la compét (Megane/Feyra).
- **Anti-doublons de fleurs (2026-07)** : `addFlower` et `pickerCreate` réutilisent une fleur existante si `norm(nom)` correspond déjà (insensible casse/accents) au lieu d'en recréer une. Doublons passés nettoyés par fusion (garde la fiche la mieux renseignée + union des propriétaires). Cause du bug Karine : variantes de casse (« Purple clematis » vs « Purple Clematis »).
- **Warning RLS Supabase** sur `rtcf_logs` (INSERT always true) : ignoré volontairement, comportement attendu
- **`index.html` jamais édité à la main** : toujours regénéré via `py data/generate_app.py`
- **`.github/workflows/` à la racine** : contrainte GitHub Actions, impossible de déplacer dans `data/`
- **Backups dans `data/backups/`** : cohérent avec le reste des fichiers de gestion
- **Backups QUOTIDIENS (depuis 2026-08)** : `backup.yml` cron `0 7 * * *` (avant : hebdo dominical). Consolidation mensuelle le **1er du mois** (`DAY = 01`) → archive dans `monthly/` + purge les quotidiens du mois écoulé. Perte max en cas d'incident = 1 jour.
- **Incident du 2026-08-02 (perte de données)** : un appareil tournant **encore avec l'ancien code** (onglet ouvert depuis avant le correctif concurrence du 21/07) s'est réveillé et a **écrasé toute la base** avec sa copie périmée (« dernier qui écrit gagne »). Joueuses supprimées (Camsouille, Orianne, Aélie38, Fugazi…) + coches effacées. **« lalou » définitivement perdue** (créée puis supprimée entre le 26/07 et l'incident → jamais capturée par une sauvegarde). Récupération : **fusion name-keyed** `backup 19/07 ∪ état live` (union stricte, n'enlève rien ; joueuses/fleurs matchées par `norm(pseudo)`, ownership unionnée) → +967 coches, +4 joueuses, +6 fleurs restaurées. Scripts dans le scratchpad (`recover_merge.py`/`apply_merge.py`). Snapshot restauré sauvegardé dans `backups/daily/2026-08-02.json`.
- **Préventions anti-récidive (2026-08)** — 3 couches :
  1. **Version-gate client** : `const BUILD` dans le code (actuellement `3`). À chaque `checkSync` et au chargement, `checkBuild()` compare `BUILD` à `D._minBuild`. Pour **forcer le rechargement de tous les onglets périmés** après un déploiement critique : bumper `BUILD` dans le code ET écrire `payload._minBuild = <nouveau BUILD>` en base (une écriture REST). Les onglets avec `BUILD < _minBuild` se rechargent seuls. (Ne protège que les onglets qui ont DÉJÀ ce code ; les onglets pré-2026-08 ne se rechargent pas tout seuls → il faut leur demander de fermer/rouvrir.) Le build est **affiché** en petit (`vN`, blanc translucide) en haut à droite du header (`#hdr-build`, texte = `'v'+BUILD`) — utile au support pour repérer un appareil sur ancien code.
  2. **Garde-fou base de données** : trigger PostgreSQL `trg_guard_rtcf_data` (SQL dans `data/sql/guard_rtcf_data.sql`, à exécuter dans Supabase). Rejette toute écriture supprimant >3 joueuses ou >300 coches d'un coup, **quel que soit le code du client**. Désactivable temporairement pour un gros nettoyage légitime.
  3. **Backups quotidiens** (voir ci-dessus).

---

## Fonctionnalités app (implémentées)

- Système de rareté : N / R / SR / SSR / UR avec badges colorés
- Système de points : 9 / 14 / 21 / 23 / 25 / 28 / 30 pts
- Onglet Fleurs : 2 rangées de chips de filtre combinables — rareté (N/R/SR/SSR/UR, état `fleursF`) et points (chips générées dynamiquement depuis les valeurs présentes, état `fleursP`). Fonctions `buildFleursChips`/`buildFleursPChips` + `setFleursF`/`setFleursP`
- Toggle fleurs uniquement depuis l'onglet "Fleurs" (pas depuis les profils)
- Profil : nom en gras (non modifiable) + label facultatif modifiable
- Multi-admin : Charline (p1, 0909), Court of Bloom (1910), Selkyy1 (1975) — accès onglet "Gérer", édition des fleurs
- Auto-suppression de son propre profil désactivée
- FAB "Ajouter au catalogue" uniquement sur l'onglet Fleurs
- Barres de progression alignées (largeur fixe sur le bouton toggle)
- **Bloc-notes** (depuis 2026-07) : encart en haut de l'onglet Équipe, visible par toutes, modifiable uniquement par les admins. Stocké dans `D.notes` (string), synchronisé via Supabase. Fonctions `notesCardHTML`/`openNotesView`/`openNotesEdit`/`saveNotes`. La carte affiche un aperçu limité à 4 lignes (`.note-body.clamp`) ; **un appui ouvre le texte complet en lecture** via `openNotesView()` (accessible à **toutes**, pas seulement aux admins). Le bouton « Modifier » n'apparaît que si `isAdmin()` (carte + vue) ; l'édition exige le PIN (via `openPinSheet(callback)`)
- **Renommage des joueuses** (depuis 2026-07) : bouton « Renommer » dans l'onglet Gérer (pour toutes, y compris soi-même). Fonctions `renamePlayer`/`openRenamePlayer`/`submitRename`. Met à jour `name` + `short` en respectant le format `Pseudo / Prénom`
