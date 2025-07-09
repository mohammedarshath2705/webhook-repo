#  Webhook Receiver — GitHub Webhooks & MongoDB Integration

A Flask-based backend service designed to receive GitHub webhook events, store them in MongoDB, and display live updates through an API and auto-refreshing frontend UI.  

Built as part of a developer assessment task.

---

##  Features

 Receives GitHub Webhook Events:
- **Push**
- **Pull Request**
- **Merge (on PR close with merge)**

 Stores event data in **MongoDB** with the following schema:
- `request_id`
- `author`
- `action` (PUSH / PULL_REQUEST / MERGE)
- `from_branch`
- `to_branch`
- `timestamp` (formatted UTC time)

 API Endpoints:
- `POST /webhook` → receives webhooks from GitHub
- `GET /events` → returns formatted event messages
- `GET /ui` → simple web UI that refreshes every 15 seconds to display the latest activity  

---

##  Tech Stack

- **Python 3**
- **Flask**
- **Flask-PyMongo**
- **MongoDB**
- **Ngrok**
- **GitHub Webhooks**

---

##  How It Works

1. GitHub webhooks from the `action-repo` are sent to this receiver.
2. The receiver handles **Push**, **Pull Request**, and **Merge** events.
3. Each event is stored in **MongoDB** with a clean, structured schema.
4. An auto-refreshing web UI polls data every 15 seconds via the `/events` API.
5. Messages are displayed in the format:
   - **Push:** `"Author" pushed to "branch" on timestamp`
   - **Pull Request:** `"Author" submitted a pull request from "branch" to "branch" on timestamp`
   - **Merge:** `"Author" merged branch "branch" to "branch" on timestamp`

---

##  How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/webhook-repo.git
   cd webhook-repo
2. **Set up a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
4. **Start MongoDB**
   ```bash
   mongod
5. **Run the Flask application**
   ```bash
   python run.py
6. **Expose your local server using ngrok**
   ```bash
   ngrok http 5000
7. **Add the ngrok URL to your action-repo webhook settings**
   ```bash
   https://your-ngrok-url.ngrok-free.app/webhook

## API Endpoints

| Method | Route      | Description                                                 |
| :----- | :--------- | :---------------------------------------------------------- |
| POST   | `/webhook` | Receives webhook events from GitHub                         |
| GET    | `/events`  | Returns formatted event messages as JSON                    |
| GET    | `/ui`      | Web UI displaying event activity, auto-refreshing every 15s |


## Example Event Messages 

- "Arshath" pushed to "main" on 9th July 2025 - 6:50 PM UTC

- "Arshath" submitted a pull request from "feature-branch" to "main" on 9th July 2025 - 7:00 PM UTC

- "Arshath" merged branch "feature-branch" to "main" on 9th July 2025 - 7:15 PM UTC

##  Purpose

This project was developed to demonstrate:

- Real-time webhook event processing

- MongoDB data storage and querying

- Auto-refreshing frontend event stream

- Clean, production-ready backend API design
