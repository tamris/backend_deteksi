from fastapi import APIRouter, File, UploadFile
from PIL import Image
import numpy as np
import io

from model.batik_model import model, label_kelas
from model.motif_makna import motif_makna  # import kamus makna motif

router = APIRouter()

@router.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    try:
        # Baca dan proses gambar
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image = image.resize((128, 128))
        img_array = np.expand_dims(np.array(image), axis=0).astype("float32") / 255.0

        # Prediksi menggunakan model
        predictions = model.predict(img_array)
        predicted_class = int(np.argmax(predictions, axis=1)[0])
        label = label_kelas[predicted_class]
        confidence = float(np.max(predictions))

        # Ambil makna dari kamus (default jika tidak ditemukan)
        makna = motif_makna.get(label, "Makna untuk motif ini belum tersedia.")

        return {
            "success": True,
            "label": label,
            "confidence": round(confidence, 4),
            "makna": makna
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
