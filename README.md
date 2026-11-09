# Road Collision Severity Predictor

A Django application and machine learning project that estimates UK road collision severity as fatal, serious, or slight. The predictor uses road, vehicle, time, and weather features.

## Local setup

The trained models are stored in Git LFS. Install Git LFS before cloning, or run `git lfs pull` after cloning so the model files are downloaded instead of their pointer files.

On Windows PowerShell:

```powershell
git lfs install
git clone <repository-url>
cd Road-Collision-Severity-Predictor
git lfs pull
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DJANGO_DEBUG = "True"
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. The local development key is only used when debug mode is explicitly enabled.

The notebook expects the UK road casualty CSV files in the ignored `data/` directory. Download the collision, vehicle, and casualty datasets separately before running the notebook. Those datasets and the local SQLite database are intentionally not included in Git.

## Production configuration

Keep `DJANGO_DEBUG=False` (the default), set a unique `DJANGO_SECRET_KEY`, and set `DJANGO_ALLOWED_HOSTS` to the deployed hostnames. Production settings enable secure session and CSRF cookies and redirect HTTP requests to HTTPS. Deploy behind HTTPS and configure the host and proxy settings for the chosen platform. After confirming HTTPS is enforced for the whole domain, set `DJANGO_SECURE_HSTS_SECONDS` to enable HSTS. If the application sends email, configure `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and either `EMAIL_USE_TLS` or `EMAIL_USE_SSL` in the deployment environment.

Do not commit `.env` files, local databases, datasets, or credentials. Git ignores those files. Model pickle files are tracked with Git LFS; only load model files from a trusted source because Python pickle files can execute code when loaded.

## Assets and licenses

The site includes media and template assets. Confirm that you have permission to redistribute each image, video, and third-party template asset before publishing the repository. The original template attribution and license notes are in `car/Readme.md`.
