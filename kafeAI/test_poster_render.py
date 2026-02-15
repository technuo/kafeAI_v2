from poster_agent import PosterRenderer
import os

# Mock data based on user feedback
promo_data = {
    "promotion_id": "TEST_WRAP",
    "theme": "Hand-drawn Delight",
    "marketing_copy_headline": "WHIMSICAL BURGER BUNDLE",
    "marketing_copy_body": "Enjoy our signature hand-drawn style meal with a hearty burger, crispy fries, and a refreshing drink. Perfect for a cozy afternoon!",
    "discount_type": "COMBO DEAL",
    "price_promo": "89"
}

renderer = PosterRenderer()
with open("generated_assets/prototype_bg.png", "rb") as f:
    img_data = f.read()

saved_path = renderer.process(img_data, promo_data, "test_render_final.png")
print(f"Test poster saved at: {saved_path}")
