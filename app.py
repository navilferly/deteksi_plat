import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import qrcode
from detect_plate import detect_plate
from ocr_utils import read_plate_text

st.set_page_config(page_title="🚘 Deteksi Plat Nomor", page_icon="🚗", layout="centered")
st.markdown("<h1 style='text-align: center;'>🚘 Deteksi Plat Nomor Kendaraan</h1>", unsafe_allow_html=True)

st.sidebar.header("⚙️ Pengaturan")
ocr_method = st.sidebar.selectbox("Metode OCR", ["Tesseract (default)", "EasyOCR"])

uploaded_file = st.file_uploader("📤 Upload gambar kendaraan", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    st.image(image, caption="📸 Gambar Asli", use_column_width=True)

    with st.spinner("🔍 Mendeteksi plat..."):
        plate_img, box = detect_plate(image_cv)

    if plate_img is not None:
        # OCR
        text = read_plate_text(plate_img, method=ocr_method)

        # Gambar hasil anotasi
        x, y, w, h = box
        cv2.rectangle(image_cv, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image_cv, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
        result_img = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)

        st.image(result_img, caption="✅ Deteksi Plat", use_column_width=True)
        st.success(f"🚗 Nomor Plat Terdeteksi: **{text}**")

        # Download hasil gambar anotasi
        result_pil = Image.fromarray(result_img)
        img_buf = BytesIO()
        result_pil.save(img_buf, format="PNG")
        st.download_button("⬇️ Download Gambar Hasil", img_buf.getvalue(), file_name="hasil_deteksi.png", mime="image/png")

        # QR Code
        qr = qrcode.make(text)
        qr_buf = BytesIO()
        qr.save(qr_buf)
        st.markdown("### 📎 QR Code dari Nomor Plat")
        st.image(qr, width=150)
        st.download_button("⬇️ Download QR Code", qr_buf.getvalue(), file_name=f"qr_{text}.png", mime="image/png")

    else:
        st.warning("⚠️ Plat nomor tidak terdeteksi.")
