# configs
import requests
import webbrowser

BROKER = "localhost"  # to be changed for ip
PORT = 1883
TOPIC_SUBSCRIBE = "auction/news"
TOPIC_PUBLISH = "auction/"
EVENT_NEW = "new_auction"
EVENT_UPDATE = "auction_update"
EVENT_FINISHED = "auction_finished"
EVENT_NOAUCTION = "no_auctions"
API_PORT = 8000


def check_logged_card(card_uuid):
    url = f"http://localhost:{API_PORT}/check_registered/{card_uuid}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["registered"] == True:
            return True
        else:
            webbrowser.open(f"http://localhost:{API_PORT}/register/{card_uuid}/")
            return False
    return False
