import os
import logging
from django.shortcuts import render
from openai import OpenAI

logger = logging.getLogger(__name__)

ALLOWED_SIZES = ["256x256", "512x512", "1024x1024"]
DEFAULT_SIZE = "512x512"
DEFAULT_STYLE = "realistic"
DEFAULT_NUM_IMAGES = 2
MAX_NUM_IMAGES = 4

STYLE_PRESETS = {
    "realistic": "realistic, high quality, natural lighting, detailed composition",
    "cinematic": "cinematic, dramatic lighting, ultra detailed, professional photography",
    "anime": "anime style, vibrant colors, expressive details, clean illustration",
    "cyberpunk": "cyberpunk style, neon lights, futuristic city atmosphere",
    "painting": "digital painting, artistic brush strokes, rich colors, gallery quality",
}


def parse_num_images(value):
    try:
        num_images = int(value)
    except (TypeError, ValueError):
        return DEFAULT_NUM_IMAGES

    if 1 <= num_images <= MAX_NUM_IMAGES:
        return num_images

    return DEFAULT_NUM_IMAGES


def get_image_form_data(request):
    prompt = request.GET.get("prompt", "").strip()
    size = request.GET.get("size", DEFAULT_SIZE)
    style = request.GET.get("style", DEFAULT_STYLE)
    num_images = parse_num_images(request.GET.get("num_images", DEFAULT_NUM_IMAGES))

    if size not in ALLOWED_SIZES:
        size = DEFAULT_SIZE

    if style not in STYLE_PRESETS:
        style = DEFAULT_STYLE

    return prompt, size, style, num_images


def enhance_prompt(prompt, style):
    style_text = STYLE_PRESETS.get(style, STYLE_PRESETS["realistic"])
    return f"{prompt}, {style_text}, sharp focus, high resolution"


def get_template_context(images=None, error_message=None, prompt="", size=DEFAULT_SIZE, style=DEFAULT_STYLE, num_images=DEFAULT_NUM_IMAGES):
    return {
        "images": images or [],
        "error_message": error_message,
        "prompt": prompt,
        "size": size,
        "style": style,
        "num_images": num_images,
        "styles": STYLE_PRESETS.keys(),
        "allowed_sizes": ALLOWED_SIZES,
    }


def generate_image(request):
    images = []
    error_message = None

    prompt, size, style, num_images = get_image_form_data(request)

    if request.GET and not prompt:
        error_message = "Please enter a prompt to generate images."
        return render(
            request,
            "dalle_generator/generate_image.html",
            get_template_context(images, error_message, prompt, size, style, num_images),
        )

    if not request.GET:
        return render(request, "dalle_generator/generate_image.html", get_template_context())

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        error_message = "OpenAI API key is not configured. Please set OPENAI_API_KEY."
        return render(
            request,
            "dalle_generator/generate_image.html",
            get_template_context(images, error_message, prompt, size, style, num_images),
        )

    try:
        client = OpenAI(api_key=api_key)

        final_prompt = enhance_prompt(prompt, style)

        response = client.images.generate(
            model="dall-e-2",
            prompt=final_prompt,
            size=size,
            n=num_images,
        )

        images = [image.url for image in response.data]

    except Exception:
        logger.exception("Image generation failed")
        error_message = "Image generation failed. Please check your API key or try again."

    return render(
        request,
        "dalle_generator/generate_image.html",
        get_template_context(images, error_message, prompt, size, style, num_images),
    )
