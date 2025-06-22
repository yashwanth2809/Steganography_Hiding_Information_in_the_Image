# 🔒 StegoShield - LSB + AES Steganography Web App

**StegoShield** is a secure and user-friendly web application built with **Streamlit** that allows you to hide secret messages inside images using **Least Significant Bit (LSB) steganography** combined with **AES encryption**. The app also offers an optional **QR code feature** to securely share encryption passwords.

---

## 📌 Features

- 🖼️ Upload PNG/BMP images (lossless formats)
- 🔐 AES encryption with password protection
- 🧠 LSB steganography for hiding messages in image pixels
- 🔍 Decode and decrypt secret messages
- 📷 Optional QR code generation for password sharing
- 🌐 Simple and interactive Streamlit web UI

---

## 🚀 How It Works

1. **Encrypt** the secret message using AES with a password.
2. **Convert** the encrypted message to binary.
3. **Embed** the binary data into the image pixels via LSB technique.
4. **Optionally generate** a QR code containing the password.
5. **Decode** the message by extracting binary data and decrypting it using the password or QR code.

---

## 🛠 Requirements

- Python 3.8+
- Works on Windows, Mac, or Linux
- Web browser: Chrome, Firefox, Edge recommended

### Python Libraries Used:

- `streamlit`
- `pillow`
- `numpy`
- `pycryptodome`
- `qrcode`
- `pyzbar`

Install all dependencies using:

```bash
pip install -r requirements.txt

git clone https://github.com/your-username/StegoShield.git
cd StegoShield

pip install -r requirements.txt

streamlit run app.py

├── app.py               # Main application code
├── requirements.txt     # Required Python libraries
└── README.md            # Project documentation






---

### ✅ What You Should Do Next:
1. Replace this new `README.md` content into your GitHub repo.
2. Optionally add screenshots into a `/screenshots` folder and link them under the **📸 Screenshots** section.
3. (Optional) Add a `LICENSE` file if you want to officially declare the project open-source.

---

If you'd like, I can generate this as a ready-to-upload file for you. Let me know!
