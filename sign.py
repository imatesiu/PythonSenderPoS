import hashlib
import base64
import datetime
import os
import sys


def create_signature(data, private_key):
    # Calculate the hash of the document content (SHA-256 used here)
    content_hash = hashlib.sha256(data.encode()).digest()
    print(content_hash.decode(errors='replace'))
    print(private_key)
    # Simulate signing with a private key (replace with actual signing logic)
    signature = base64.b64encode(content_hash + private_key).decode()

    return signature

def sign_pdf(file_path, private_key):
    # Read the content of the PDF file
    with open(file_path, 'rb') as file:
        pdf_content = file.read().decode(errors='replace')
    print(pdf_content)
    # Creating a signature placeholder
    signature_placeholder = "/ByteRange [0 0 0 0]/Contents <FEFF00>"

    # Generating the signature
    signature = create_signature(pdf_content, private_key)

    # Replace the signature placeholder with the actual signature
    signed_pdf = pdf_content.replace(signature_placeholder, f"/ByteRange [0 {len(signature)} 0 {len(pdf_content)}]/Contents {signature}")

    # Save the signed PDF to a new file
    signed_file_path = file_path.replace('.pdf', '_signed.pdf')
    with open(signed_file_path, 'wb') as signed_file:
        signed_file.write(signed_pdf.encode())

    return signed_file_path

# Example usage
file_to_sign = "embedded-file.pdf"
private_key_bytes = os.urandom(32)

# Print the private key in hexadecimal format
private_key = private_key_bytes.hex()

signed_pdf_path = sign_pdf(file_to_sign, private_key)
print(f"PDF signed and saved to: {signed_pdf_path}")
