# Class for handling communication with IGDB API.
import time
import requests


class IGDBApiWrapper:
    def __init__(self, oa_client_id=None, oa_client_secret=None):
        self.oa_client_id = oa_client_id
        self.oa_client_secret = oa_client_secret
        self.access_token = ""
        self.token_type = ""
        self.token_creation_time = 0
        self.expires_in = 0
        self.headers = {}
        self.sleep_duration = 0.25
        self.can_download = True

        # Api endpoint addresses.
        self.igdb_oauth_url = "https://id.twitch.tv/oauth2/"
        self.igdb_get_url = "https://api.igdb.com/v4/"

        if self.oa_client_id is None or self.oa_client_secret is None \
                or self.oa_client_id == "" or self.oa_client_secret == "":
            print(f"Missing oa_client_id or oa_client_secret!")
            self.can_download = False

    def sleep(self):
        time.sleep(self.sleep_duration)

    # Get or refresh auth token.
    def get_or_refresh_auth_token(self):
        err_message = ""

        if self.can_download:
            data = {
                "client_id": self.oa_client_id,
                "client_secret": self.oa_client_secret,
                "grant_type": "client_credentials"}

            if (time.time() - self.token_creation_time) >= self.expires_in:
                response = requests.post(f"{self.igdb_oauth_url}token", data)

                if response.status_code == 200:
                    self.token_creation_time = time.time()
                    self.access_token = response.json()['access_token']
                    self.expires_in = response.json()['expires_in']
                    self.token_type = response.json()['token_type']
                    self.headers = {
                        "Client-ID": self.oa_client_id,
                        "Authorization": f"Bearer {self.access_token}",
                        "Accept": "application/json"}

                    print("User data correct.")
                else:
                    try:
                        error_code = response.json()["status"]
                        error_description = response.json()["message"]

                        err_message = f"Error: {error_code}, message: {error_description}."
                    except:
                        err_message = "Unknown error."

        return err_message
