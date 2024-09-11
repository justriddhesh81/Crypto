from Crypto.Cipher import AES
import hashlib
import zipfile
import io

def extract_encrypted(a):
    ex_wav = []
    with zipfile.ZipFile(a, 'r') as b:
        for fi_in in b.infolist():
            if fi_in.filename.endswith('_encrypted.wav'):
                extr = b.read(fi_in.filename)
                ex_wav.append((fi_in.filename, extr))
    return ex_wav

def audio_decryption(a, key):
    dec_wav = io.BytesIO()

    chunk_size = 64 * 1024  
    a.seek(0) 
    iv = a.read(16)  
    cipher = AES.new(key, AES.MODE_CBC, iv)

    first_chunk = True  

    while True:
        chunk = a.read(chunk_size)
        if len(chunk) == 0:
            break
        dec = cipher.decrypt(chunk)

        if first_chunk:
            first_chunk = False
            xor_chunk = dec 
        else:
            dec = bytes(x ^ y for x, y in zip(dec, xor_chunk))

        dec_wav.write(dec)

    return dec_wav.getvalue()

def main():
    encrypted_zip = "encrypted_audio.zip"
    decrypted_zip = "decrypted_audio.zip"
    key = hashlib.sha256(b"a904uewA6473AQbe").digest()[:16]

    extracted = extract_encrypted(encrypted_zip)
    print(f"{len(extracted)} encrypted WAV file(s) extracted from ZIP.")

    with zipfile.ZipFile(decrypted_zip, 'w') as decrypted_zip_ref:
        for filename, wav_data in extracted:
            d_data = audio_decryption(io.BytesIO(wav_data), key)
            decrypted_zip_ref.writestr(filename.replace('_encrypted.wav', '_decrypted.wav'), d_data)

if __name__ == "__main__":
    main()
