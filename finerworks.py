"""
Simple Python module to provide abstractions to Finerworks' REST API.
"""
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

    def order(self, recipient=None, addr=None, validate=None, test=None, po=None):
        """
        Submit a FinerWorks Order via REST API.
        """
        item = {
            "": ,
            "recipient": recipient,
            "test_mode": test,
        }

        if po:
            item["order_po"]

        req = self._http_req("/submit_orders")

    def order_update(self):
        """
        Update a FinerWorks Order via REST API.
        """
        pass  # pylint: disable=unnecessary-pass

    def order_status(self, id):
        """
        Retrieve FinerWorks Order Status via REST API.
        """
        
        id_list = [id]
        orders = {
            "order_ids": id_list
        }
        req = self._http_req("/fetch_order_status", orders)
        return req

    def order_statuses(self):
        """
        Retrieve order status id mapping options via REST API.
        """

        req = self._http_req("/list_order_status_definitions")
        return req

    def order_shipping(self):
        """
        Retrieve Order Shipping options via REST API.
        """
        pass  # pylint: disable=unnecessary-pass

    def customer_update(self):
        """
        Update Customer Info via REST API.
        """
        pass  # pylint: disable=unnecessary-pass

    def address_validate(self, recipient):
        """
        Validate Customer Address for Shipping via REST API.
        """
        req = self._http_req("/validate_recipient_address", body=recipient)
        return req

    def product(self):
        """
        Get Product Details via REST API.
        """
        pass  # pylint: disable=unnecessary-pass

    def product_images(self, query=""):
        """
        Query Product Images via REST API.
        """
        filter = {
            "search_filter": query
        }
        req = self._http_req("/list_images", body=filter)
        return req
