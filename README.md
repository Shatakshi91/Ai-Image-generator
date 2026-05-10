# VisionCraft AI - Django AI Image Generator

VisionCraft AI is a Django web app that generates AI images from text prompts. Users can enter an idea, choose an image size, select a visual style, and view generated images in a clean web interface.

## Features

- Generate images from text prompts using the OpenAI API.
- Choose image sizes: `256x256`, `512x512`, or `1024x1024`.
- Apply prompt styles such as realistic, cinematic, anime, cyberpunk, and painting.
- Preview generated images in a responsive grid.
- Download generated images from the browser.
- Show friendly validation and error messages.

## Tech Stack

- Python
- Django
- OpenAI Python SDK
- HTML and CSS
- SQLite for local development

## Project Structure

```text
Ai-Image-generator/
├── dalle_app/                 # Django project settings and URL config
├── dalle_generator/           # Main image generator app
│   ├── templates/             # Django HTML templates
│   ├── views.py               # Prompt validation and image generation view
│   └── tests.py               # Tests to add as the project improves
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## Local Setup

1. Clone the repository.

2. Create and activate a virtual environment.

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Create a `.env` file using `.env.example` as a guide.

```env
DJANGO_SECRET_KEY=replace-this-with-a-local-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
OPENAI_API_KEY=your_openai_api_key_here
```

5. Run database migrations.

```bash
python manage.py migrate
```

6. Start the development server.

```bash
python manage.py runserver
```

7. Open the app in your browser.

```text
http://localhost:8000/generate-image/
```

## Environment Variables

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Secret key used by Django |
| `DJANGO_DEBUG` | Enables or disables debug mode |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated list of allowed hosts |
| `OPENAI_API_KEY` | API key used for image generation |

## Verification

Run Django's project check:

```bash
python manage.py check
```

Run the development server and test:

- Open `/generate-image/`.
- Submit an empty prompt and confirm a validation message appears.
- Submit a valid prompt with each size and style.
- Temporarily remove `OPENAI_API_KEY` and confirm a friendly error appears.

## Future Improvements

- Add automated tests for validation and view behavior.
- Move OpenAI image generation into a service module.
- Move inline CSS into Django static files.
- Add deployment notes for production hosting.
- Remove or reorganize unrelated helper scripts from the repository root.
