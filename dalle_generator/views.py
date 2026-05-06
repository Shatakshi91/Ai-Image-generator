import os
import logging
from django.shortcuts import render
from django.conf import settings
from openai import OpenAI

logger = logging.getLogger(__name__)

STYLE_PRESETS = {
    "realistic": "realistic, high quality, natural lighting, detailed composition",
    "cinematic": "cinematic, dramatic lighting, ultra detailed, professional photography",
    "anime": "anime style, vibrant colors, expressive details, clean illustration",
    "cyberpunk": "cyberpunk style, neon lights, futuristic city atmosphere",
    "painting": "digital painting, artistic brush strokes, rich colors, gallery quality",
}


def enhance_prompt(prompt, style):
    style_text = STYLE_PRESETS.get(style, STYLE_PRESETS["realistic"])
    return f"{prompt}, {style_text}, sharp focus, high resolution"


def generate_image(request):
    images = []
    error_message = None

    prompt = request.GET.get("prompt", "").strip()
    size = request.GET.get("size", "512x512")
    style = request.GET.get("style", "realistic")
    num_images = int(request.GET.get("num_images", 2))

    allowed_sizes = ["256x256", "512x512", "1024x1024"]

    if size not in allowed_sizes:
        size = "512x512"

    if num_images < 1 or num_images > 4:
        num_images = 2

    if request.GET and not prompt:
        error_message = "Please enter a prompt to generate images."
        return render(request, "dalle_generator/generate_image.html", {
            "images": images,
            "error_message": error_message,
            "prompt": prompt,
            "size": size,
            "style": style,
            "num_images": num_images,
            "styles": STYLE_PRESETS.keys(),
        })

    if not request.GET:
        return render(request, "dalle_generator/generate_image.html", {
            "images": images,
            "styles": STYLE_PRESETS.keys(),
        })

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        final_prompt = enhance_prompt(prompt, style)

        response = client.images.generate(
            model="dall-e-2",
            prompt=final_prompt,
            size=size,
            n=num_images,
        )

        images = [image.url for image in response.data]

    except Exception as e:
        logger.exception("Image generation failed")
        error_message = "Image generation failed. Please check your API key or try again."

    return render(request, "dalle_generator/generate_image.html", {
        "images": images,
        "error_message": error_message,
        "prompt": prompt,
        "size": size,
        "style": style,
        "num_images": num_images,
        "styles": STYLE_PRESETS.keys(),
    })