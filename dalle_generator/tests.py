from unittest.mock import patch

from django.test import RequestFactory, TestCase

from .views import DEFAULT_NUM_IMAGES, enhance_prompt, generate_image, parse_num_images


class ImageGenerationViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_enhance_prompt_adds_selected_style(self):
        prompt = enhance_prompt("a mountain cabin", "cinematic")

        self.assertIn("a mountain cabin", prompt)
        self.assertIn("cinematic", prompt)
        self.assertIn("high resolution", prompt)

    def test_parse_num_images_uses_default_for_invalid_value(self):
        self.assertEqual(parse_num_images("abc"), DEFAULT_NUM_IMAGES)
        self.assertEqual(parse_num_images("0"), DEFAULT_NUM_IMAGES)
        self.assertEqual(parse_num_images("5"), DEFAULT_NUM_IMAGES)

    def test_empty_prompt_shows_validation_error(self):
        request = self.factory.get("/generate-image/", {"prompt": ""})

        response = generate_image(request)

        self.assertContains(response, "Please enter a prompt to generate images.")

    @patch.dict("os.environ", {}, clear=True)
    def test_missing_openai_key_shows_configuration_error(self):
        request = self.factory.get("/generate-image/", {"prompt": "a sunset"})

        response = generate_image(request)

        self.assertContains(response, "OpenAI API key is not configured.")
