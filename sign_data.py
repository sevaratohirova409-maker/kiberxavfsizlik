from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

def canonicalize_data_custom(data: dict) -> str:
    items = sorted(data.items())
    return ";".join([f"{k}={v}" for k, v in items])

def sign_data(data, private_key):
    data_string = canonicalize_data_custom(data)
    data_bytes = data_string.encode('utf-8')
    signature = private_key.sign(
        data_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

if __name__ == "__main__":
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    data = {
        "id": 101,
        "name": "Ali",
        "amount": 25000,
        "currency": "UZS",
        "timestamp": "2025-11-29 11:15:00"
    }

    signature = sign_data(data, private_key)

    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    with open("signature.bin", "wb") as f:
        f.write(signature)

    print("✅ Ma'lumot imzolandi va 'signature.bin' fayliga saqlandi.")