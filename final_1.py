from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import hashlib
import zipfile
import io
import os
import time


def extract(a):
    ex_wav = []
    with zipfile.ZipFile(a, 'r') as b:
        for fi_in in b.infolist():
            if fi_in.filename.endswith('.wav'):
                extr = b.read(fi_in.filename)
                ex_wav.append((fi_in.filename, extr))
    return ex_wav

def audio_encryption(a, key):
    ex_wav = io.BytesIO()
    chunk_size = 64 * 1024  
    iv = os.urandom(16)  

    cipher = AES.new(key, AES.MODE_CBC, iv)

    ex_wav.write(iv)  
    first_chunk = True  

    while True:
        chunk = a.read(chunk_size)
        if len(chunk) == 0:
            break
        elif len(chunk) % 16 != 0:
            chunk = pad(chunk, 16)

        if first_chunk:
            first_chunk = False
            xor_chunk = chunk 
        else:
            chunk = bytes(x ^ y for x, y in zip(chunk, xor_chunk))

        b = cipher.encrypt(chunk)
        ex_wav.write(b)

    return ex_wav.getvalue()

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
    zip_file = "cryp.zip"
    encrypted_zip = "encrypted_audio.zip"
    decrypted_zip = "decrypted_audio.zip"
    key = hashlib.sha256(b"a904uewA6473AQbe").digest()[:16]

    start_time = time.time()  

    extracted = extract(zip_file)
    print(f"{len(extracted)} WAV file(s) extracted from ZIP.")

    with zipfile.ZipFile(encrypted_zip, 'w') as encrypted_zip_ref, zipfile.ZipFile(decrypted_zip, 'w') as decrypted_zip_ref:
        for filename, wav_data in extracted:
            e_data = audio_encryption(io.BytesIO(wav_data), key)

            d_data = audio_decryption(io.BytesIO(e_data), key)

            encrypted_zip_ref.writestr(filename.replace('.wav', '_encrypted.wav'), e_data)
            decrypted_zip_ref.writestr(filename.replace('.wav', '_decrypted.wav'), d_data)

    end_time = time.time() 
    time_taken = end_time - start_time
    print(f"Time taken: {time_taken:.2f} seconds")

if __name__ == "__main__":
    main()