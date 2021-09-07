# StarNavi
StarNavi is a test project with REST API on DRF.

## Installation
Use the package manager pip to install all package from requirements.txt
```bash
pip3 install -r requirements.txt
```

## Settings
Create a ".env" file as in example "env.example"

Or

Write your own local env settings in starnavi/settings.py

```python
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, 'CHANGEME!!!e8!1671ifpp362f9gbd3v@e($0_flznbb3fa2d4zg7zn@%yyk2'),
    DJANGO_ALLOWED_HOSTS=(list, []),
    DJANGO_DATABASE_URL=(str, 'postgres://USER:PASSWORD@HOST:PORT/starnavi'),
)
```

## Migrate
Apply all migrations into your DB
```bash
python manage.py migrate
```
