import streamlit as st
import io
import base64
from PIL import Image
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import qrcode
from pyzbar.pyzbar import decode

# ─── Streamlit Page Config & Styles ────────────────────────────────────────────
st.set_page_config(
    page_title="StegoShield - LSB + AES Steganography",
    page_icon="🔒",
    layout="wide"
)

st.markdown("""
<style>
    .main {padding: 2rem;}
    .stApp {max-width: 1200px; margin: 0 auto; font-family: 'Segoe UI', sans-serif;}
    h1, h2, h3 {color: #2c3e50; font-weight: 700;}
    .stButton button {
        background-color: #2980b9;
        color: white;
        padding: 0.6em 1.2em;
        border-radius: 8px;
        font-size: 1rem;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #1abc9c;
        color: #fff;
    }
    .success {color: #27ae60; font-weight: bold;}
    .error {color: #e74c3c; font-weight: bold;}
    .stTextInput>div>input, .stTextArea>div>textarea {
        border-radius: 8px;
        padding: 0.6em;
    }
    .download-link a {
        display: inline-block;
        margin-top: 10px;
        padding: 10px 15px;
        background-color: #27ae60;
        color: white;
        text-decoration: none;
        border-radius: 8px;
    }
    .download-link a:hover {
        background-color: #2ecc71;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔒 StegoShield")
st.subheader("Secure LSB Steganography with AES Encryption")
st.markdown("""
Hide your secret messages inside images using LSB steganography and AES encryption.
- **Supports**: PNG images (lossless format required)
- **Security**: AES encryption with password protection
- **Sharing**: Optional QR code for password sharing
""")

# ─── Utility Functions ─────────────────────────────────────────────────────────

def text_to_binary(text: str) -> str:
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_text(binary: str) -> str:
    out = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if byte == '11111110':  # end marker
            break
        out += chr(int(byte, 2))
    return out

def encrypt_message(message: str, password: str) -> str:
    key = password.encode('utf-8')
    if len(key) % 16 != 0:
        key += b'0' * (16 - len(key) % 16)
    key = key[:32]
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pad(message.encode('utf-8'), AES.block_size)
    ct = cipher.encrypt(padded)
    return base64.b64encode(ct).decode('utf-8')

def decrypt_message(encrypted_message: str, password: str) -> str | None:
    try:
        key = password.encode('utf-8')
        if len(key) % 16 != 0:
            key += b'0' * (16 - len(key) % 16)
        key = key[:32]
        cipher = AES.new(key, AES.MODE_ECB)
        data = base64.b64decode(encrypted_message)
        pt = unpad(cipher.decrypt(data), AES.block_size)
        return pt.decode('utf-8')
    except:
        st.error("Decryption failed. Incorrect password or invalid data.")
        return None

def encode_lsb(image: Image.Image, binary_message: str) -> tuple[Image.Image, str|None]:
    arr = np.array(image)
    h, w, c = arr.shape
    binary_message += '11111110'
    if len(binary_message) > h * w * c:
        return None, "Image too small to hold this message."
    flat = arr.flatten()
    for i, bit in enumerate(binary_message):
        flat[i] = (flat[i] & 0b11111110) | int(bit)
    stego = flat.reshape(h, w, c)
    return Image.fromarray(stego.astype(np.uint8)), None

def decode_lsb(image: Image.Image) -> tuple[str|None, str|None]:
    arr = np.array(image).flatten()
    bits = ''
    for b in arr:
        bits += str(b & 1)
        if bits.endswith('11111110'):
            break
    if '11111110' not in bits:
        return None, "No hidden message found."
    return bits[:-8], None

def generate_qr_code(password: str) -> Image.Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(password)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    return qr_img.get_image().convert("RGB") if hasattr(qr_img, "get_image") else qr_img.convert("RGB")

def extract_from_qr(qr_image: Image.Image) -> str | None:
    try:
        decoded = decode(qr_image)
        if decoded:
            return decoded[0].data.decode('utf-8')
        return None
    except:
        return None

def get_image_download_link(img: Image.Image, filename: str, text: str) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    data = base64.b64encode(buf.getvalue()).decode()
    return f'<a href="data:file/png;base64,{data}" download="{filename}">{text}</a>'

# ─── Main App ────────────────────────────────────────────────────────────────

def main():
    tab1, tab2 = st.tabs(["📝 Encode Message", "🔍 Decode Message"])

    with tab1:
        st.header("📤 Hide Secret Message in Image")
        uploaded = st.file_uploader("Upload a PNG or BMP image", type=["png", "bmp"])
        if uploaded:
            orig = Image.open(uploaded)
            if orig.format not in ["PNG", "BMP"]:
                st.error("Unsupported format; use PNG or BMP.")
            else:
                st.image(orig, caption="🖼️ Original Image", use_container_width=True)
                msg = st.text_area("💬 Enter your secret message", height=150)
                pwd = st.text_input("🔑 Enter encryption password", type="password")
                if st.button("🔐 Encode Message"):
                    if not msg:
                        st.error("❗ Please enter a message.")
                    elif not pwd:
                        st.error("❗ Please enter a password.")
                    else:
                        with st.spinner("🔄 Encrypting & embedding…"):
                            ct = encrypt_message(msg, pwd)
                            bin_msg = text_to_binary(ct)
                            stego_img, err = encode_lsb(orig, bin_msg)
                            if err:
                                st.error(err)
                            else:
                                st.success("✅ Message encoded successfully!")
                                st.image(stego_img, caption="🖼️ Stego Image", use_container_width=True)
                                st.markdown(get_image_download_link(stego_img, "stego_image.png", "📥 Download Stego Image"), unsafe_allow_html=True)

                                st.subheader("🔲 Password QR Code (Optional)")
                                st.markdown("Scan this QR to supply the password on decode.")
                                qr_img = generate_qr_code(pwd)
                                st.image(qr_img, caption="Password QR Code", width=300)
                                st.markdown(get_image_download_link(qr_img, "password_qr.png", "📥 Download QR Code"), unsafe_allow_html=True)

    with tab2:
        st.header("📥 Reveal Hidden Message from Image")
        stego_file = st.file_uploader("Upload the stego image", type=["png", "bmp"])
        if stego_file:
            stego = Image.open(stego_file)
            if stego.format not in ["PNG", "BMP"]:
                st.error("Unsupported format; use PNG or BMP.")
            else:
                st.image(stego, caption="🖼️ Stego Image", use_container_width=True)
                st.subheader("🔐 Password Options")
                choice = st.radio("How do you want to provide the password?", ["Manual Entry", "Upload QR Code"])
                pwd, qr_pwd = None, None

                if choice == "Manual Entry":
                    pwd = st.text_input("🔑 Decryption password", type="password")
                else:
                    qr_file = st.file_uploader("Upload password QR code", type=["png", "jpg", "jpeg"])
                    if qr_file:
                        qr_img2 = Image.open(qr_file)
                        qr_pwd = extract_from_qr(qr_img2)
                        if qr_pwd:
                            st.success("✅ Password extracted from QR!")
                        else:
                            st.error("❌ Couldn't read QR. Please try manual entry.")
                            pwd = st.text_input("🔑 Decryption password (backup)", type="password")

                if st.button("🔍 Decode Message"):
                    final_pwd = qr_pwd or pwd
                    if not final_pwd:
                        st.error("❗ Please supply a password or QR.")
                    else:
                        with st.spinner("🔓 Extracting & decrypting…"):
                            bin_msg, err = decode_lsb(stego)
                            if err:
                                st.error(err)
                            else:
                                enc = binary_to_text(bin_msg)
                                pt = decrypt_message(enc, final_pwd)
                                if pt is not None:
                                    st.success("✅ Message decoded successfully!")
                                    st.subheader("📨 Secret Message:")
                                    st.markdown(f"""
                                        <div style='background: #ecf0f1; padding: 15px; border-radius: 8px; font-size: 1.1rem;'>
                                            {pt}
                                        </div>
                                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()



