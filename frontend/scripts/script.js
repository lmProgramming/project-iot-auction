document.addEventListener("DOMContentLoaded", () => {
  const API_URL = "https://backend.example.com/api";

  // Creating new user
  document
    .getElementById("create-user-form")
    .addEventListener("submit", async (event) => {
      event.preventDefault();

      const username = document.getElementById("username").value;
      const pass = document.getElementById("pass").value;

      const userData = { username, pass };

      try {
        const response = await fetch(`${API_URL}/users`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(userData),
        });

        if (response.ok) {
          alert("Użytkownik został utworzony!");
          event.target.reset();
        } else {
          alert("Wystąpił błąd podczas tworzenia użytkownika.");
        }
      } catch (error) {
        console.error("Błąd:", error);
      }
    });

  // Creating new auction
  document
    .getElementById("create-auction-form")
    .addEventListener("submit", async (event) => {
      event.preventDefault();

      const itemName = document.getElementById("item-name").value;
      const startingPrice = parseFloat(
        document.getElementById("starting-price").value
      );

      if (startingPrice < 0) {
        alert("Kwota musi być dodatnia");
        return;
      }

      const auctionData = { itemName, startingPrice };

      try {
        const response = await fetch(`${API_URL}/auctions`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(auctionData),
        });

        if (response.ok) {
          alert("Aukcja została utworzona!");
          event.target.reset();
        } else {
          alert("Wystąpił błąd podczas tworzenia aukcji.");
        }
      } catch (error) {
        console.error("Błąd:", error);
      }
    });

  // Adding money
  document
    .getElementById("add-money-form")
    .addEventListener("submit", async (event) => {
      event.preventDefault();

      const userId = document.getElementById("user-id").value;
      const amount = parseFloat(document.getElementById("amount").value);

      if (amount < 0) {
        alert("Kwota pieniędzy nie może być ujemna");
        return;
      }

      const moneyData = { userId, amount };

      try {
        const response = await fetch(`${API_URL}/users/${userId}/add-money`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(moneyData),
        });

        if (response.ok) {
          alert("Pieniądze zostały dodane!");
          event.target.reset();
        } else {
          alert("Wystąpił błąd podczas dodawania pieniędzy.");
        }
      } catch (error) {
        console.error("Błąd:", error);
      }
    });
});
