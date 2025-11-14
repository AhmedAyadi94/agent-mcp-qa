# 🤖 Agent MCP QA - Assistant IA pour Ingénieurs QA

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-En%20Développement-yellow)]()

## 🎯 Vue d'Ensemble

Agent MCP QA est un **assistant intelligent automatisé** conçu pour les ingénieurs QA. Il utilise l'intelligence artificielle pour automatiser et optimiser les tâches quotidiennes de test et d'assurance qualité.

### ✨ Fonctionnalités Principales

✅ **Génération automatique de scripts de test**
- Scripts Selenium (tests UI web)
- Scripts Appium (tests mobile)
- Collections Postman (tests API)
- Utilisation de l'IA (OpenAI) pour générer du code adapté

✅ **Analyse intelligente de rapports de test**
- Support JUnit XML
- Support JSON/Newman/Postman
- Détection automatique d'anomalies
- Calcul de taux de réussite et statistiques
- Génération de résumés formatés

✅ **Reporting automatisé**
- Rapports HTML/PDF
- Statistiques visuelles
- Graphiques et tendances

✅ **Intégration CI/CD** (En développement)
- Connexion Jenkins
- Connexion GitLab CI
- Récupération automatique des builds

✅ **Gestion de tickets Jira** (En développement)
- Création automatique de bugs
- Suivi des anomalies

---

## 📦 Structure du Projet

```
agent-mcp-qa/
├── main.py                    # Point d'entrée - Interface CLI
├── requirements.txt           # Dépendances Python
├── modules/
│   ├── generator.py          # Génération de scripts de test
│   ├── analyzer.py           # Analyse de rapports de test
│   ├── reporter.py           # Génération de rapports (WIP)
│   ├── ci_cd_connector.py    # Connexion CI/CD (WIP)
│   └── jira_connector.py     # Intégration Jira (WIP)
├── data/
│   ├── examples/             # Exemples de rapports
│   └── results/              # Résultats générés
└── generated_tests/          # Scripts de test générés
```

---

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- Compte OpenAI (pour la génération de scripts)
- Git

### Étapes d'installation

```bash
# Cloner le repository
git clone https://github.com/AhmedAyadi94/agent-mcp-qa.git
cd agent-mcp-qa

# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement virtuel
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration

Créer un fichier `.env` à la racine du projet :

```bash
OPENAI_API_KEY=votre_clé_api_openai
JENKINS_URL=http://votre-jenkins.com
JENKINS_USERNAME=votre_username
JENKINS_TOKEN=votre_token
JIRA_URL=https://votre-jira.atlassian.net
JIRA_USERNAME=votre_email
JIRA_API_TOKEN=votre_token_jira
```

---

## 💻 Utilisation

### Lancer l'agent

```bash
python main.py
```

### Menu interactif

```
============================================================
    Agent MCP QA - Assistant IA pour Ingénieurs QA
============================================================

Fonctionnalités disponibles:
1. Générer un script de test (Selenium/Appium/Postman)
2. Analyser un rapport de test
3. Générer un rapport synthétique
4. Intégration CI/CD (Jenkins/GitLab)
5. Créer un ticket Jira
6. Quitter
============================================================
```

### Exemples d'utilisation

#### 1. Générer un script Selenium

```python
from modules.generator import generate_selenium_test

script = generate_selenium_test(
    "Tester le formulaire de login avec authentification Google"
)
print(script)
```

#### 2. Analyser un rapport JUnit

```python
from modules.analyzer import analyze_report

stats = analyze_report("data/results/junit-report.xml")
print(stats["summary"])
```

---

## 🛠️ Technologies Utilisées

- **Python 3.8+**
- **OpenAI API** - Génération de code avec IA
- **Selenium** - Tests UI web
- **Appium** - Tests mobile
- **Requests** - API HTTP
- **xml.etree** - Parsing XML
- **pandas** - Analyse de données
- **Streamlit** (Prévu) - Interface web

---

## 📈 Roadmap

### Version 1.0 (En cours)
- [x] Générateur de scripts Selenium
- [x] Générateur de scripts Appium  
- [x] Générateur de collections Postman
- [x] Analyseur de rapports JUnit XML
- [x] Analyseur de rapports JSON
- [x] Détection d'anomalies
- [ ] Module de reporting HTML/PDF
- [ ] Connecteur Jenkins
- [ ] Connecteur GitLab CI
- [ ] Connecteur Jira

### Version 2.0 (Futur)
- [ ] Interface web Streamlit
- [ ] Dashboard de visualisation
- [ ] Tests de performance (JMeter)
- [ ] Tests BDD (Cucumber)
- [ ] Intégration GitHub Actions
- [ ] Notifications Slack/Teams
- [ ] Support multi-langues

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👤 Auteur

**Ahmed Ayadi**
- GitHub: [@AhmedAyadi94](https://github.com/AhmedAyadi94)
- LinkedIn: [Ahmed Ayadi](https://www.linkedin.com/in/ahmed-ayadi)
- Email: ahmed.ayadi@example.com

---

## 🚀 À Propos

Ce projet a été développé dans le cadre d'une formation **POEI QA Automation Engineer** chez Cegos. Il démontre les compétences en :
- Automatisation de tests (Selenium, Appium, Postman)
- Intégration d'IA dans les processus QA
- Développement Python avancé
- Architecture logicielle modulaire
- Intégration CI/CD
- Gestion de projet DevOps

---

## ⭐ Remerciements

- OpenAI pour l'API GPT
- Communauté Selenium et Appium
- Cegos Formation
- Tous les contributeurs

---

**📌 Note**: Ce projet est en **développement actif**. Les fonctionnalités sont ajoutées régulièrement.
