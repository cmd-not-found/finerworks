import json
import requests


class FinerWorks:
    """
    FinerWorks API object.
    """

    def __init__(self, web_api_key, app_key):
        """
        Initialize FinerWorks API with required values.
        """
        self.web_api_key = web_api_key
        self.app_key = app_key
        self.base_url = "https://api.finerworks.com/v3"

    def _http_req(self, suffix, body=None):
        """
        Execute HTTP API requests for Finerworks REST API.
        """
        headers = {
            "web_api_key": self.web_api_key,
            "app_key": self.app_key,
            "Content-Type": "application/json",
        }

        resp = requests.request(
            method="POST",
            url=self.base_url + suffix,
            headers=headers,
            data=json.dumps(body),
        )

        if resp.status_code == 200:
            return resp.json()
        else:
            raise ConnectionError(
                "Could Not Connect. Status Code: {0}".format(resp.status_code)
            )

    def login(self):
        """
        Attempt to authenticate to API and test connection.
        """
        if not self.web_api_key:
            raise TypeError("Missing web_api_key")
        if not self.app_key:
            raise TypeError("Missing app_key")

        req = self._http_req("/test_my_credentials")
        return req

    def order(self):
        """
        Submit a FinerWorks Order via REST API.
        """
        pass

    def order_update(self):
        """
        Update a FinerWorks Order via REST API.
        """
        pass
    
    def order_status(self, ids):
        """
        Retrieve FinerWorks Order Status via REST API.
        """
        assert type(ids) == list
        assert len(ids) == 1
        orders = {
            "order_ids": ids
        }
        req = self._http_req("/fetch_order_status", orders)
        return req

    def order_shipping(self):
        """
        Retrieve Order Shipping options via REST API.
        """
        pass

    def customer_update(self):
        """
        Update Customer Info via REST API.
        """
        pass

    def address_validate(self):
        """
        Validate Customer Address for Shipping via REST API.
        """
        pass

    def product(self):
        """
        Get Product Details via REST API.
        """
        pass

    def product_images(self):
        """
        Query Product Images via REST API.
        """
        pass