
import random
import hashlib
import os
from datetime import datetime
import matplotlib.pyplot as plt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Constants
q = 2**80 - 1  # Large prime number (>80 bits)
P = random.randint(1, q)  # Generator of cyclic group G

# Hash functions
def H(data):
    return int(hashlib.sha256(data.encode()).hexdigest(), 16) % q

def H1(data):
    return int(hashlib.sha1(data.encode()).hexdigest(), 16) % q

# Generate private and public keys
def generate_keys():
    sk = random.randint(1, q)  # Private key
    pk = (sk * P) % q  # Public key
    return sk, pk

# Generate shared key (Diffie-Hellman method)
def generate_shared_key(sk, pk_other):
    shared_key = (sk * pk_other) % q
    return hashlib.sha256(str(shared_key).encode()).digest()  # 256-bit key for AES

# AES-256 encryption
def aes_encrypt(shared_key, plaintext):
    iv = os.urandom(16)  # Generate a random IV
    cipher = Cipher(algorithms.AES(shared_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return iv + ciphertext  # IV + ciphertext


# AES-256 decryption
def aes_decrypt(shared_key, ciphertext):
    iv = ciphertext[:16]  # Extract IV
    actual_ciphertext = ciphertext[16:]  # Extract ciphertext
    cipher = Cipher(algorithms.AES(shared_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(actual_ciphertext) + decryptor.finalize()
    return decrypted_message.decode()

# Signature generation
def generate_signature(sk, data):
    return (1 / sk) * H(data) * P

# Signature aggregation
def aggregate_signatures(sig1, sig2):
    return sig1 + sig2

# Challenge generation
def generate_challenge(k):
    return H(str(k) + "challenge")

# Sensor readings simulation
def get_sensor_readings():
    R1 = random.uniform(20.0, 35.0)  # Temperature
    R2 = random.uniform(40.0, 60.0)  # Humidity
    R3 = random.choice(["Rain", "Clear Skies", "Storm"])
    R4 = random.uniform(0.0, 100.0)  # Growth monitoring
    R5 = random.choice(["Sandy", "Loamy", "Clay"])  # Soil type
    return R1, R2, R3, R4, R5

# Generate current timestamp
def get_timestamp():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# Function to draw the chart for overheads
def draw_overhead_chart(comm_overhead_bytes, comp_overhead_ms):
    labels = ['Communication Overhead (bytes)', 'Computation Overhead (ms)']
    values = [comm_overhead_bytes,comp_overhead_ms]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=['blue', 'orange'])
    plt.title('Overheads in AKA Protocol')
    plt.xlabel('Type of Overhead')
    plt.ylabel('Overhead Value')
    plt.show()

# Main function
def main():
    # Initialize control system (CS) and entities (A and B)
    sk_cs, pk_cs = generate_keys()
    sk_a, pk_a = generate_keys()
    sk_b, pk_b = generate_keys()

    # Generate sensor readings
    R1, R2, R3, R4, R5 = get_sensor_readings()
    print(f"Sensor Readings: R1 (Temp): {R1}°C, R2 (Humidity): {R2}%, R3 (Weather): {R3}, R4 (Growth): {R4}%, R5 (Soil Type): {R5}")

    # Generate timestamp
    timestamp = get_timestamp()
    print(f"Timestamp: {timestamp}")

    # Generate shared keys between A and B
    shared_key_a_b = generate_shared_key(sk_a, pk_b)
    shared_key_b_a = generate_shared_key(sk_b, pk_a)  # Should be identical to shared_key_a_b

    # Prepare data for encryption and signatures
    data = f"{timestamp}{R1}{R2}{R3}{R4}{R5}"
    encrypted_message = aes_encrypt(shared_key_a_b, data)
    print(f"Encrypted Message: {encrypted_message}")

    # Decrypt on the other side (B side)
    decrypted_message = aes_decrypt(shared_key_b_a, encrypted_message)
    print(f"Decrypted Message: {decrypted_message}")

    # Generate signatures for A and B
    sig_a = generate_signature(sk_a, data)
    sig_b = generate_signature(sk_b, data)
    aggregated_signature = aggregate_signatures(sig_a, sig_b)

    # Generate challenges
    k = random.randint(1, q)
    challenge_a = generate_challenge(k)
    challenge_b = generate_challenge(k)

    # Placeholder values for overheads in ms and bytes
    comm_overhead_bytes = 118    # Example value in bytes 
    comp_overhead_ms = 4.2  # Example value in milliseconds

    # Draw the overhead chart
    draw_overhead_chart(comm_overhead_bytes, comp_overhead_ms)

    print(f"Private and Public Keys:\n  CS Private: {sk_cs}, CS Public: {pk_cs}\n  A Private: {sk_a}, A Public: {pk_a}\n  B Private: {sk_b}, B Public: {pk_b}")
    print(f"Signature A: {sig_a}\nSignature B: {sig_b}\nAggregated Signature: {aggregated_signature}")
    print(f"Challenge A: {challenge_a}\nChallenge B: {challenge_b}")
    print(f"Shared Key (A -> B): {shared_key_a_b.hex()}\nShared Key (B -> A): {shared_key_b_a.hex()}")

if __name__ == "__main__":
    main()
