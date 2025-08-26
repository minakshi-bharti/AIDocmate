from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 800, 240
TEXT = (
    "AIDocMate Demo\n"
    "Applicant must submit Aadhaar and PAN copies. Fees: Rs. 50.\n"
    "Deadline: 31 March. Eligibility: Students with income < Rs. 2L."
)

img = Image.new("RGB", (WIDTH, HEIGHT), color="white")
draw = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("arial.ttf", 22)
except Exception:
    font = ImageFont.load_default()

draw.multiline_text((20, 20), TEXT, fill="black", font=font, spacing=6)

out_path = "form_sample.png"
img.save(out_path)
print(f"Saved {out_path}") 