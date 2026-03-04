# API Choice

- Étudiant : Nicolas

- API choisie : Agify

- URL base : https://api.agify.io

- Documentation officielle :
  https://agify.io/

- Auth : None (pas de clé API requise)

- Endpoints testés :
  - GET /?name=michael

- Hypothèses de contrat (champs attendus, types, codes) :
  - Code 200 attendu
  - Champ "name" présent (string)
  - Champ "age" présent (integer)
  - Champ "count" présent (integer)

- Limites / rate limiting connu :
  - API publique avec limitation de requêtes possible (429)

- Risques (instabilité, downtime, CORS, etc.) :
  - Rate limit si trop de requêtes
  - Indisponibilité temporaire possible
