import os
import requests
from dotenv import load_dotenv

load_dotenv()

class PayPalClient:
    def __init__(self):
        self.client_id = os.getenv("PAYPAL_CLIENT_ID")
        self.client_secret = os.getenv("PAYPAL_CLIENT_SECRET")
        self.mode = os.getenv("PAYPAL_MODE", "sandbox")
        
        if self.mode == "live":
            self.base_url = "https://api-m.paypal.com"
        else:
            self.base_url = "https://api-m.sandbox.paypal.com"
            
        self._access_token = None

    def get_access_token(self) -> str:
        if self._access_token:
            return self._access_token
            
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en_US"}
        data = {"grant_type": "client_credentials"}
        
        response = requests.post(
            url,
            headers=headers,
            data=data,
            auth=(self.client_id, self.client_secret)
        )
        
        if response.status_code == 200:
            self._access_token = response.json().get("access_token")
            return self._access_token
        else:
            raise Exception(f"Failed to obtain PayPal access token: {response.text}")

    def create_order(self, amount: str, currency: str = "USD", description: str = "Autonomous Procurement Item") -> dict:
        token = self.get_access_token()
        url = f"{self.base_url}/v2/checkout/orders"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "PayPal-Request-Id": os.urandom(16).hex()
        }
        
        # Using a sandbox test card payment source for immediate autonomous capture
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "description": description,
                    "amount": {
                        "currency_code": currency,
                        "value": amount
                    }
                }
            ],
            "payment_source": {
                "card": {
                    "name": "Miguel Martin Gil",
                    "number": "4111111111111111",
                    "expiry": "2028-12",
                    "security_code": "123"
                }
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Failed to create PayPal order: {response.text}")

    def capture_order(self, order_id: str) -> dict:
        token = self.get_access_token()
        url = f"{self.base_url}/v2/checkout/orders/{order_id}/capture"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.post(url, headers=headers)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Failed to capture PayPal order: {response.text}")
