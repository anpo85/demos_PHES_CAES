import streamlit as st

st.title("Démo : Lecture & signature de PDF")

# Affichage PDF
pdf_file = st.file_uploader("Choisir un PDF", type=["pdf"])
if pdf_file is not None:
    # nécessite pip install PyMuPDF
    import fitz  # PyMuPDF
    import io
    from PIL import Image

    pdf_reader = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page_number in range(pdf_reader.page_count):
        page = pdf_reader.load_page(page_number)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        st.image(img, caption=f"Page {page_number+1}")

st.markdown("---")
st.header("Zone de signature")

# Zone de dessin signature (nécessite st_canvas)
from streamlit_drawable_canvas import st_canvas

canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0)",  # Transparent background
    stroke_width=2,
    stroke_color="#000000",
    background_color="#FFF3",
    height=150,
    width=450,
    drawing_mode="freedraw",
    key="canvas",
)

if canvas_result.image_data is not None:
    st.image(canvas_result.image_data, caption="Votre signature")

if canvas_result.image_data is not None and pdf_file is not None:
    st.success("🔒 Signature dessinée ! (ici pas d'insertion dans PDF pour la démo)")

st.info("Pour une insertion de la signature dans le PDF et synchronisation temps réel, il faut développer une solution plus avancée, avec backend + WebSocket + traitement PDF en temps réel.")