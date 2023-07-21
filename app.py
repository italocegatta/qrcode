import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO
import pyshorteners as ps


def generate_qr(data, logo=None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,  # Maior tamanho dos pixels do QR code
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    if logo is not None:
        # logo = logo.resize((int(img_qr.size[0]*0.3), int(img_qr.size[1]*0.3)), Image.LANCZOS)  # Melhor interpolação
        pos = (
            (img_qr.size[0] - logo.size[0]) // 2,
            (img_qr.size[1] - logo.size[1]) // 2,
        )
        img_qr.paste(logo, pos)
    return img_qr


st.title("Gerador de QR Code")

title = st.text_input("Insira o nome do arquivo de saída")

url = st.text_input("Insira o link do arquivo")

if st.button("Gerar QR Code"):
    url_short = ps.Shortener().tinyurl.short(url)
    st.write(f"Link curto:{url_short}")

    logo_path = "logo.png"
    logo = Image.open(logo_path)

    img_qr = generate_qr(url_short, logo)
    img_byte_arr = BytesIO()
    img_qr.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    
    st.download_button(
        label="Download QR Code",
        data=img_byte_arr,
        file_name=title + ".png",
        mime="image/png",
    )

    st.image(img_qr, use_column_width=True)
