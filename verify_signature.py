from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

def canonicalize_data_custom(data: dict) -> str:
    items = sorted(data.items())
    return ";".join([f"{k}={v}" for k, v in items])

def verify_signature(data, signature, public_key):
    data_string = canonicalize_data_custom(data)
    data_bytes = data_string.encode('utf-8')
    try:
        public_key.verify(
            signature,
            data_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("✅ Imzo TO'G'RI: Ma'lumot buzilmagan va haqiqiy manbadan kelgan.")
        return True
    except Exception as e:
        print(f"❌ Imzo XATO: {e}")
        return False

if __name__ == "__main__":
    # Fayllardan kalit va imzoni yuklash
    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

    with open("signature.bin", "rb") as f:
        signature = f.read()

    # Tekshiriladigan ma'lumot
    data = {
        "id": 101,
        "name": "Ali",
        "amount": 25000,
        "currency": "UZS",
        "timestamp": "2025-11-29 11:15:00"
    }

    # Imzoni tekshirish
    verify_signature(data, signature, public_key)