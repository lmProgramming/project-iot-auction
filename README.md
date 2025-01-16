# Project for Internet of Things - Auction

An auction system, that uses Raspberry Pi's RFID reader to read bids, so that an auction winner can be decided. Each auction is about a specific article with a starting price. When someone with a specific card wants to bid, they can put the card to the scanner, which raises the price. This updates the price on all Raspberry Pis, showing on their screens the current price, article name and article photo. When 10 seconds pass without any new bid, a winner is declared and money is deducted from their virtual internal account.

## Architecture

The application is divided into 3 sections:

- backend (Django with MQTT module running on a separate thread)
- frontend (simple HTMLs, to list all models from database and create new objects)
- hardware (Raspberry Pi, which can be emulated on other platforms with keyboard)

## More info

- For more information on how to run the backend, refer to [backend/README.md](backend/README.md)
