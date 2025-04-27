# Plant Disease Detection Microservice

### Group
- Aoudia Fahem  
- Chachoua Mohamed  
- Doriane NIKIEMA  
- Doria NIKIEMA

---

## Présentation du projet

Ce projet est une extension supplémentaire du projet présenté avec M. Bruel.  
Nous avons souhaité approfondir nos connaissances en mettant en place une architecture Microservices en utilisant Docker, tout en intégrant :
- un système d'authentification avec OTP (One-Time Password),
- une application de chatbot pour enrichir l'expérience utilisateur.

---

## Composants du projet

- **api_gateway** : Passerelle d'entrée qui gère toutes les requêtes externes.
- **auth_service** : Microservice qui gère l'authentification OTP.
- **prediction_service** : Microservice qui prédit la maladie d'une plante à partir d'une image.
- **frontend** : Application web développée avec React.js pour l'interface utilisateur.

---

## Utilisation

1. L'utilisateur envoie une image de plante via l'interface.
2. Le service de prédiction renvoie le nom de la maladie détectée ainsi que le taux de confiance associé.
3. Vous pouvez tester l'application en utilisant les images du dossier `image_test/`.

---

## Remarques importantes

- Assurez-vous que le modèle d'intelligence artificielle `plant_disease_model.h5` est bien téléchargé.

---

## Lancer le projet

```bash
docker-compose up --build
