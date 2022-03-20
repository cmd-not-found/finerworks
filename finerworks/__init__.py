"""
Simple Python module to provide abstractions to Finerworks' REST API.
"""
import json
import requests
from .exceptions import *

class api:  # pylint: disable=invalid-name
    """
    FinerWorks API object.
    """

    def __init__(self, web_api_key=None, app_key=None):
        """
        Initialize FinerWorks API with required values.
        """

        if web_api_key == None and app_key == None:
            raise FinerworksError(
                msg='\n`web_api_key` and `app_key` are required.'
                    '\nRetrieve these values from the Finerworks Account'
                    ' dashboard.'
            )
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

        if resp.status_code == 200:  # pylint: disable=no-else-return
            return resp.json()
        elif resp.status_code == 400:
            return resp.json()
        else:
            raise FinerworksError(
                msg="Could Not Connect. Status Code: {0}".format(resp.status_code)
            )

    @staticmethod
    def _validate_order_id(current_id):
        """
        Validate Order ID type.
        """

        if isinstance(current_id, str):
            try:
                order_id = int(current_id)
            except ValueError:
                raise ValueError(  # pylint: disable=raise-missing-from
                    "Order ID should be an integer and not literal string."
                )
        elif isinstance(current_id, int):
            order_id = current_id
        else:
            raise ValueError("Order ID should be an integer. Unrecognized type.")
        return order_id

    def login(self):
        """
        Attempt to authenticate to API and test connection.
        """

        if not self.web_api_key:
            raise FinerworksError(
                msg="Missing `web_api_key`"
            )
        if not self.app_key:
            raise TypeError(
                msg="Missing `app_key`"
            )

        req = self._http_req("/test_my_credentials")
        return req

    def order_submit(  # pylint: disable=too-many-arguments
        self,
        product=None,
        recipient=None,
        order_no=None,
        shipping_code=None,
        test=True,
        validate_only=False,
        webhook_url=None,
    ):
        """
        Submit a FinerWorks Order via REST API.
        """

        # TODO keyword args
        order = {
            "order_po": order_no,
            "recipient": recipient,
            "order_items": [product],
            "shipping_code": shipping_code,
            "test_mode": test,
            "webhook_order_status_url": webhook_url,
        }

        place_order = {"orders": [order], "validate_only": validate_only}

        req = self._http_req("/submit_orders", place_order)
        return req

    def order_update(self, order_id, status):
        """
        Update a FinerWorks Order via REST API.
        """

        order_id = self._validate_order_id(order_id)
        options = ["pending", "hold", "cancel"]
        if status.lower() not in options:
            raise FinerworksError(
                msg="Order status update not in valid state. Options: {}".format(
                    ",".join(options)
                )
            )
        order_update = {"order_id": order_id, "update_command": status.lower()}
        req = self._http_req("/update_order", order_update)
        return req

    def order_status(self, curr_id):
        """
        Retrieve FinerWorks Order Status via REST API.
        """

        order_id = self._validate_order_id(curr_id)
        orders = {"order_ids": [order_id]}
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
        pass

    def customer_update(self):
        """
        Update Customer Info via REST API.
        """
        pass  # pylint: disable=unnecessary-pass

    def address_validate(self, recipient):
        """
        Validate Customer Address for Shipping via REST API.
        """

        rec = {"recipient": recipient}

        req = self._http_req("/validate_recipient_address", rec)
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

        q_filter = {"search_filter": query}
        req = self._http_req("/list_images", body=q_filter)
        return req

    def frame_collections(self, collection_id=None):
        """
        Query Frame Collections via REST API.
        """

        if not collection_id:
            raise FinerworksError(
                msg="`collection_id` required to query Frame Collection details."
            )
        else:
            c_id = {
                "id": collection_id
            }
            req = self._http_req("/list_collections", body=c_id)
            return req

    def frame_details(self, frame_id=None):
        """
        Query for Specific Frame Details via REST API.
        """

        if not frame_id:
            raise FinerworksError(
                msg="`frame_id` required to query frame details."
            )
        else:
            f_id = {
                "id": frame_id
            }
            req = self._http_req("/frame_details", body=f_id)
            return req

    def frame_mats(self, mat_id=None):
        """
        Query for Frame Mat Options via REST API.
        """

        if not mat_id:
            raise FinerworksError(
                msg="`mat_id` required to query Frame Mat details."
            )
        else:
            m_id = {
                "id": mat_id
            }
            req = self._http_req("/list_mats", body=m_id)
            return req

    def frame_glazing(self, glazing_id=None):
        """
        Query for Frame Glazing Options via REST API.
        """

        if not glazing_id:
            raise FinerworksError(
                msg="`glazing_id` required to query Frame Glazing details."
            )
        else:
            g_id = {
                "id": glazing_id
            }
            req = self._http_req("/list_glazing", body=g_id)
            return req