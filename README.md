# EMSP (Django)

## Prérequis

- Python 3.x
- Dépendances: `pip install -r requirements.txt`

## Lancer en local

PowerShell :

```powershell
python manage.py migrate
python manage.py runserver
```

Puis ouvrir `http://127.0.0.1:8000/`.

## Variables d'environnement

Le projet lit quelques variables (optionnel en local, recommandé en prod) :

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (`1`/`0`)
- `DJANGO_ALLOWED_HOSTS` (séparés par des virgules)
- `DJANGO_CSRF_TRUSTED_ORIGINS` (séparés par des virgules)

Voir `.env.example` pour un exemple.

## Commandes utiles

```powershell
python manage.py check
python manage.py test
python manage.py collectstatic
```
