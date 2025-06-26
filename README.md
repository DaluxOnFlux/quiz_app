## 📸 Aperçu



https://github.com/user-attachments/assets/8e59f416-2457-49a6-9711-345e3017fb38



# 🎯 Projet Quiz App – Vue 3 + Flask

Une application web complète permettant à un joueur de passer un quiz avec score final, et à un administrateur d'ajouter, modifier ou supprimer des questions via une interface sécurisée.

---

## 📦 Technologies

- 🎨 **Frontend** : Vue 3 + Vite
- 🧠 **Backend** : Flask + SQLite
- 📡 **API** : RESTful avec authentification par token

---

## 🚀 Installation

### 1. Clone le projet

```bash
git clone https://github.com/IchRak-1999/quiz_app
cd quiz-app
```

### 2. Lancer le backend (API Flask)

```bash
cd quiz-api
pip install -r requirements.txt
```

> ⚠️ Par défaut, l'API tourne sur `http://127.0.0.1:5000`

### 3. Lancer le frontend (Vue)

```bash
cd quiz-ui
npm install
npm run dev
```

> 🔗 Frontend disponible sur `http://localhost:3000`

---

## ⚙️ Configuration

### `.env.development` dans `quiz-ui`

```env
VITE_API_URL=http://127.0.0.1:5000
```

---

## 👤 Fonctionnalités Joueur

- Saisie du nom de joueur
- Lancement du quiz
- Affichage des questions avec 4 propositions
- Affichage du score final

---

## 🔐 Fonctionnalités Admin

- Connexion via mot de passe (`iloveflask`)
- Liste des questions existantes
- Création / édition / suppression de questions
- Upload d’image en base64
- Sélection des bonnes réponses
- Interface simple et responsive

---

## 🔏 Authentification

- Le token d'admin est stocké en `localStorage`
- Requis pour les appels POST / PUT / DELETE

---

## 🧪 Rebuild de la BDD

Pour réinitialiser la base de données SQLite :

```bash
curl -X POST http://127.0.0.1:5000/rebuild-db
```

![schema bdd](https://github.com/user-attachments/assets/f71dea77-80d6-45ef-a990-f33641acf190)


---

## 👨‍🏫 Projet réalisé par

- Dalil HIANE
- Alassane TRAORE
- Ichrak SMIRANI

---
