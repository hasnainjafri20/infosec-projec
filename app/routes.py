from flask import Blueprint, render_template, request, flash
from .pqc import generate_keys, encrypt_message, decrypt_message
import base64

bp = Blueprint('main', __name__)

# Store keys and ciphertexts in memory (demo only – secure this in production)
keys = {
    'public': None,
    'private': None,
    'kem_ct': None,
    'aes_cipher': None,
}
message = None  # Default message state

@bp.route('/', methods=['GET', 'POST'])
def index():
    global message
    result = None
    if request.method == 'POST':
        action = request.form.get('action')
        message = request.form.get('message')

        try:
            if action == 'keygen':
                # Generate public/private keys
                public, private = generate_keys()
                keys['public'] = public
                keys['private'] = private
                keys['kem_ct'] = None
                keys['aes_cipher'] = None
                result = 'Keys generated successfully.'

            elif action == 'encrypt':
                if not keys['public']:
                    flash('Generate keys first.', 'warning')
                else:
                    # Encrypt the message
                    kem_ct, aes_cipher = encrypt_message(keys['public'], message)
                    keys['kem_ct'] = kem_ct
                    keys['aes_cipher'] = aes_cipher
                    result = (
                        f"KEM Ciphertext (base64): {base64.b64encode(kem_ct).decode()}<br>"
                        f"AES Ciphertext (base64): {base64.b64encode(aes_cipher).decode()}"
                    )

            elif action == 'decrypt':
                if not keys['private'] or not keys['kem_ct'] or not keys['aes_cipher']:
                    flash('Run keygen and encrypt first.', 'warning')
                else:
                    # Decrypt the message
                    decrypted = decrypt_message(keys['private'], keys['kem_ct'], keys['aes_cipher'])
                    result = f"Original message: {decrypted}"

            else:
                flash('Unknown action.', 'danger')

        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')

    return render_template('index.html', result=result, keys=keys, message=message)
