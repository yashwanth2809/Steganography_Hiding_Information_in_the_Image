# 🔒 StegoShield - LSB + AES Steganography App
![image](https://github.com/user-attachments/assets/b5a7d504-f089-4983-82a5-0e382be76258)
**StegoShield** is a secure and user-friendly web application built using **Streamlit** that allows users to hide secret messages inside images using **Least Significant Bit (LSB) steganography** combined with **AES encryption**. It also offers an optional **QR code feature** to securely share decryption passwords.

---

## 📌 Features

- 🖼️ Upload PNG/BMP images (lossless format)  
- 🔐 AES encryption with password protection  
- 🧠 LSB steganography for hiding messages in image pixels  
- 🔍 Decode & decrypt secret messages securely  
- 📷 Optional QR code generation for password sharing  
- 🌐 Clean and interactive Streamlit web UI

---

## 🚀 How It Works

1. **Encrypt** the secret message using AES with a user-provided password.
2. **Convert** the encrypted text into binary.
3. **Embed** the binary data into the image pixels using LSB.
4. **Optionally generate** a QR code with the password for secure sharing.
5. **Decode** by extracting binary, decrypting it back into the original message.

---

## 🛠 System Requirements

- Python 3.8+
- Works on Windows, Mac, or Linux
- Recommended browser: Chrome, Firefox, Edge

---

## 📚 Libraries Used

- `streamlit`
- `pillow`
- `numpy`
- `pycryptodome`
- `qrcode`
- `pyzbar`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

Run the app using Streamlit:

```bash
streamlit run app.py
```

Then open the link provided in the terminal (usually http://localhost:8501) to access the app in your browser.

---

## 💡 Use Cases

- ✅ Secure communication over open channels  
- ✅ Digital watermarking  

---

## 🖼 Screenshot

![image](https://github.com/user-attachments/assets/be2862e2-cd78-47e1-a692-d85860e4fde6)

![image](https://github.com/user-attachments/assets/4e9bec3d-d21a-49a5-a498-73cc055f957f)

![image](https://github.com/user-attachments/assets/32beedc7-6689-4e47-a912-fdd0ad2979ff)

![image](https://github.com/user-attachments/assets/d590d241-373b-4a0a-b2d0-a0d2a62dcaf2)

![image](https://github.com/user-attachments/assets/e6f07ea3-2f71-4faa-a1c2-f16deb425a9a)

![image](https://github.com/user-attachments/assets/ded66d5b-3a80-4207-964e-ac1583fb2de6)

![image](https://github.com/user-attachments/assets/09802d7b-77f7-4320-bb64-cf7768e2e08c)

![image](https://github.com/user-attachments/assets/d0809354-a675-418f-b72e-53aaaa855080)







