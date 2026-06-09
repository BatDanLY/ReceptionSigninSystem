# 📥 Reception Sign-In System

A Flask web application that allows visitors to businesses, schools, offices, and other buildings to easily sign in and out while maintaining a record of current visitors. The system also remembers previous visitors, allowing frequent visitors to sign in more quickly using autocomplete.

---

## Features

* **Sign In** — Visitors can enter their name, company, and email address. Their details are recorded in the list of currently signed-in visitors.
* **Sign Out** — Visitors can enter their name or email address to sign out. Their details are then removed from the list of currently signed-in visitors.
* **Autocomplete** — When a returning visitor begins entering their details, the system searches previous visitor records and can automatically fill in the remaining fields to speed up the sign-in process.
* **Automatic Sign Out** — At a configurable time each day, the server automatically signs out all visitors. This helps ensure visitors who forgot to sign out are removed before the next day.
* **Privacy Focused** — Autocomplete suggestions are only shown when there is a single matching visitor record, reducing the likelihood of previous visitors' details being exposed to others.
* **Dark & Light Mode** — A toggle in the top-right corner allows users to switch between dark and light themes for improved accessibility.

---

## Screenshots

<img width="2514" height="1286" alt="image" src="https://github.com/user-attachments/assets/f07eceec-e7b5-4dd0-9321-65eae414e684" />
<img width="2514" height="1281" alt="image" src="https://github.com/user-attachments/assets/57c1f7cc-2ead-4049-8b0d-238fbf355829" />
<img width="2514" height="1285" alt="image" src="https://github.com/user-attachments/assets/d0d8bbe0-60cc-493a-88b1-67ceaef18150" />
<img width="2514" height="1284" alt="image" src="https://github.com/user-attachments/assets/6c5be787-d40e-44b6-814f-5448b6cc70ab" />
<img width="2514" height="1285" alt="image" src="https://github.com/user-attachments/assets/350b98fb-563c-4e2f-ad9d-a766854e179b" />
<img width="2514" height="1284" alt="image" src="https://github.com/user-attachments/assets/d563339d-ea78-49a6-81b2-12eac209ebd7" />
<img width="2515" height="1286" alt="image" src="https://github.com/user-attachments/assets/67e4bade-2df6-4aa7-b95b-ababb8232d69" />

---

## How It Works

The application runs as a Flask web server. When a user accesses the root URL, they are presented with the main sign-in page.

As a visitor begins entering their details, the frontend waits for a short debounce period before sending a query to the server. The server searches previously stored visitor records for matches based on the information entered. If exactly one matching record is found, the user is offered the option to automatically complete the remaining fields.

When a visitor signs in:

1. If their details are new, they are added to a JSON file containing all visitors who have ever signed in.
2. Their details are also added to a separate JSON file containing all visitors who are currently signed in.

The sign-out process works similarly. The system searches only the list of currently signed-in visitors. Once a visitor enters their name or email address and clicks **Sign Out**, their details are removed from the currently signed-in visitor list.

---

## Compatibility

### Python Requirements

* Python 3.9 or newer (recommended)
* Flask
* Flask-APScheduler

### Browser Support

The web interface is compatible with all modern browsers, including:

* Google Chrome
* Microsoft Edge
* Mozilla Firefox
* Safari

JavaScript must be enabled for autocomplete and other interactive features to function correctly.

---

## License

MIT License
