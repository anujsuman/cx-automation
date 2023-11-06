import requests
import config


class WiremockClient:
    def __init__(self):
        self.wiremock_url = config.WIREMOCK_URL
        self.target_base_url = config.TARGET_BASE_URL

    def _send_request(self, method, endpoint, data=None):
       try:
           url = f"{self.wiremock_url}/{endpoint}"
           response = None

           if method == 'GET':
               response = requests.get(url, json=data)
           elif method == 'POST':
               response = requests.post(url, json=data)
           elif method == 'DELETE':
               response = requests.delete(url, json=data)

           return response.json() if response else None

       except Exception:
           return None

    def get_request_count(self, data):
        return self._send_request('POST', '__admin/requests/count', data)

    def get_request(self, data):
        return self._send_request('POST', '__admin/requests/find?limit=100&offset=0', data)

    def delete_all_request(self, data):
        if data is None:
            data = {}
        return self._send_request('DELETE', '__admin/requests', data)

    def get_all_request(self, data):
        return self._send_request('GET', '__admin/requests', data)

    def check_recording(self, data):
        return self._send_request('GET', '__admin/recordings/status', data)

    def start_recording(self):
        data = {
            "targetBaseUrl": self.target_base_url
        }
        return self._send_request('POST', '__admin/recordings/start', data)

    def stop_recording(self):
        return self._send_request('POST', '__admin/recordings/stop')

    def add_mapping(self, mapping_data):
        return self._send_request('POST', "__admin/mappings", mapping_data)

    def save_mapping(self):
        return self._send_request('POST', "__admin/mappings/save", {})

    def delete_all_mapping(self):
        return self._send_request('DELETE', "__admin/mappings")
    
    def reset_wiremock(self):
        return self._send_request('POST', "__admin/reset")


if __name__ == "__main__":
    wiremock_client = WiremockClient()

    print(wiremock_client.get_request_count(None))
    print(wiremock_client.get_request({}))
    print(wiremock_client.delete_all_request({}))
    print(wiremock_client.get_all_request({}))
    print(wiremock_client.check_recording({}))
    print(wiremock_client.start_recording())
    print(wiremock_client.stop_recording())
