# Compétences d'Ingénierie de Contexte DSGS - Guide de Démarrage Rapide (French)

## Aperçu du Projet

DSGS (Dynamic Specification Growth System) Context Engineering Skills est un ensemble professionnel d'outils de développement assisté par IA spécialement conçu pour les plateformes CLI d'IA, fournissant des analyses de contexte, des optimisations et des modèles cognitifs avec flux de travail de sécurité IA.

## Améliorations Majeures

### 1. Architecture de Compétences Unifiée
- **Implémentation Consolidée** : Modes standard et amélioré fusionnés en une seule implémentation
- **Basculage de Mode** : Utiliser le paramètre `mode` pour contrôler le niveau fonctionnel ('standard' ou 'enhanced')
- **Interface Unique** : Interface simplifiée évitant les fonctionnalités dupliquées

### 2. Structure de Répertoire Plate
- **Une Compétence Par Répertoire** : Chaque compétence dans son propre répertoire, sans imbrication inutile
- **Organisation Simplifiée** : Emplacement intuitif des compétences, maintenance plus facile
- **Moins de Confusion** : Limites claires des compétences, pas de chevauchement fonctionnel

### 3. Flux de Travail de Sécurité de l'IA
- **Espace de Travail Temporaire** : Contenu généré par IA d'abord stocké dans zone temporaire
- **Gestion Automatique** : Alerte automatique quand nombre de fichiers dépasse 20
- **Mécanisme de Confirmation** : Contenu doit être vérifié avant inclusion dans projet principal
- **Nettoyage Automatique** : Nettoyage automatique de l'espace de travail temporaire après tâche terminée

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/AgentPsy/dsgs-context-engineering.git
cd dsgs-context-engineering

# Installer
pip install -e .
```

## Utilisation

### Commandes CLI
```
/speckit.dsgs.context-analysis "Analyser la qualité de ce document des exigences" mode=enhanced
/speckit.dsgs.cognitive-template "Comment améliorer les performances" template=verification
/speckit.dsgs.context-optimization "Optimiser cette exigence" optimization_goals=clarity,relevance
/speckit.dsgs.architect "Concevoir l'architecture du système de commerce électronique"
/speckit.dsgs.git-skill operation=status
/speckit.dsgs.temp-workspace operation=create-workspace
```

### API Python
```python
from clean_skills.context_analysis import execute as context_analysis_execute

# Mode Standard
result = context_analysis_execute({
    'context': 'Concevoir la fonction de connexion utilisateur',
    'mode': 'standard'
})

# Mode Amélioré
result = context_analysis_execute({
    'context': 'Concevoir la fonction sécurisée de connexion utilisateur',
    'mode': 'enhanced'
})
```

## Bonnes Pratiques de Sécurité IA

1. **Avant Génération IA** : Toujours créer d'abord espace de travail temporaire
2. **Valider Contenu** : Utiliser mécanisme de confirmation pour vérifier contenu généré par IA
3. **Nettoyage Régulier** : Surveiller nombre de fichiers temporaires
4. **Nettoyer Espace** : Nettoyer zone temporaire après complétion tâche

---
*Auteur : pTree Dr. Zhang*  
*Organisation : Laboratoire de Personnalité IA 2025*  
*Contact : 3061176@qq.com*  
*Site Web : https://AgentPsy.com*