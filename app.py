from flask import Flask, request, jsonify, render_template
from PIL import Image
import pillow_avif
import io
import os
import re
import base64

app = Flask(__name__)
ALLOWED = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif", ".webp"}

def safe_name(name):
    return re.sub(r'[\\/:*?"<>|]', "_", name).strip() or "imagen"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    files = request.files.getlist("images")
    quality = int(request.form.get("quality", 80))
    output_name = safe_name(request.form.get("output_name", "").strip())

    if not files or files[0].filename == "":
        return "No se recibieron archivos", 400

    valid = [f for f in files if os.path.splitext(f.filename)[1].lower() in ALLOWED]
    if not valid:
        return "Ningún archivo tiene formato válido", 400

    results = []
    for i, f in enumerate(valid):
        if output_name:
            name = output_name if len(valid) == 1 else f"{output_name}_{i + 1}"
        else:
            name = os.path.splitext(f.filename)[0]

        img = Image.open(f.stream).convert("RGB")

        webp_buf = io.BytesIO()
        img.save(webp_buf, "WEBP", quality=quality, method=6)
        results.append({
            "filename": f"{name}.webp",
            "data": base64.b64encode(webp_buf.getvalue()).decode(),
        })

        avif_buf = io.BytesIO()
        img.save(avif_buf, "AVIF", quality=quality)
        results.append({
            "filename": f"{name}.avif",
            "data": base64.b64encode(avif_buf.getvalue()).decode(),
        })

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=False)
