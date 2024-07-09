from datetime import datetime, timedelta, timezone
import base64
import hmac
import hashlib
import jwt
import os

api_key = os.getenv('API_KEY')
key_id = os.getenv('KEY_ID')
aud_url = os.getenv('AUD_URL')

def generate_jwt():
        if not isKeyAvailable(api_key, key_id, aud_url):
            print(
                "\nOne or more of the following environment variables are missing,\n"
                "API_KEY\n"
                "KEY_ID\n"
                "AUD_URL\n"
            )
            return

        # Get the current UTC time as a timezone-aware datetime object
        curr_time = datetime.now(timezone.utc)
        payload = {
            "aud": aud_url,
            "iat": curr_time,
            "exp": curr_time + timedelta(seconds=30000),
            "iss": key_id,
            "metadata": {
                "reason": "fetch usages",
                "requesterip": "127.0.0.1",
                "date-time": curr_time.strftime("%m/%d/%Y, %H:%M:%S"),
                "user-agent": "curl"
            }
        }
        signature = base64.b64encode(hmac.new(bytes(api_key, 'UTF-8'), bytes(key_id, 'UTF-8'), digestmod=hashlib.sha512).digest())
        token = jwt.encode(payload, signature, algorithm='HS512',
                     headers={"kid": key_id})
        print("Token: {}" .format(token))

def isKeyAvailable(api_key, key_id, aud_url):
    if (api_key and key_id and aud_url):
        return True
    return False

generate_jwt()
