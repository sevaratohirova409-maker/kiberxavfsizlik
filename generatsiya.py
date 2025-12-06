from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024, 
   )
    public_key = private_key.public_key()
    return private_key, public_key

def save_keys_to_files(private_key, public_key,
                       private_filename="private_key.pem",
                       public_filename="public_key.pem"):
    # Shaxsiy kalit
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()  # faqat sinov uchun
    )
    with open(private_filename, "wb") as f:
        f.write(pem_private_key)
    print(f"   Shaxsiy kalit '{private_filename}' fayliga saqlandi.")

    # Ommaviy kalit
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(public_filename, "wb") as f:
        f.write(pem_public_key)
    print(f"   Ommaviy kalit '{public_filename}' fayliga saqlandi.")

if __name__ == "__main__":
    # Kalitlarni yaratish
    private_key, public_key = generate_rsa_keys()

    # Faylga saqlash
    save_keys_to_files(private_key, public_key)

    print("✅ Kalit generatsiya va saqlash jarayoni tugadi.")