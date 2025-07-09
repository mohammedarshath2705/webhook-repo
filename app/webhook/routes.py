from flask import Blueprint, request, jsonify
from ..extensions import mongo
from datetime import datetime
from flask import render_template

webhook_bp = Blueprint('webhook_bp', __name__)

def get_utc_timestamp():
    return datetime.utcnow().strftime("%-d %B %Y - %-I:%M %p UTC")

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400

    event = request.headers.get('X-GitHub-Event')

    if event == "push":
        try:
            pusher_name = data.get("pusher", {}).get("name")
            ref = data.get("ref")
            commit_id = data.get("head_commit", {}).get("id")

            if not pusher_name or not ref or not commit_id:
                return jsonify({"error": "Missing push event data"}), 400

            doc = {
                "request_id": commit_id,
                "author": pusher_name,
                "action": "PUSH",
                "from_branch": None,
                "to_branch": ref.split("/")[-1],
                "timestamp": get_utc_timestamp()
            }
            mongo.db.events.insert_one(doc)

        except Exception as e:
            print("Error in push event:", e)
            return jsonify({"error": str(e)}), 400

    elif event == "pull_request":
        try:
            action_type = data.get("action")
            pr_data = data.get("pull_request")

            if not pr_data or not action_type:
                return jsonify({"error": "Missing pull request event data"}), 400

            if action_type == "opened":
                doc = {
                    "request_id": str(pr_data["id"]),
                    "author": pr_data["user"]["login"],
                    "action": "PULL_REQUEST",
                    "from_branch": pr_data["head"]["ref"],
                    "to_branch": pr_data["base"]["ref"],
                    "timestamp": get_utc_timestamp()
                }
                mongo.db.events.insert_one(doc)

            elif action_type == "closed" and pr_data.get("merged"):
                doc = {
                    "request_id": str(pr_data["id"]),
                    "author": pr_data["user"]["login"],
                    "action": "MERGE",
                    "from_branch": pr_data["head"]["ref"],
                    "to_branch": pr_data["base"]["ref"],
                    "timestamp": get_utc_timestamp()
                }
                mongo.db.events.insert_one(doc)

        except Exception as e:
            print("Error in pull_request event:", e)
            return jsonify({"error": str(e)}), 400

    else:
        print("Unhandled event:", event)
        return jsonify({"message": "Event type not handled"}), 200

    return jsonify({"message": "Event received"}), 200


@webhook_bp.route('/events', methods=['GET'])
def get_events():
    events = list(mongo.db.events.find({}))

    formatted_events = []

    for e in events:
        action = e.get("action")
        author = e.get("author")
        from_branch = e.get("from_branch")
        to_branch = e.get("to_branch")
        timestamp = e.get("timestamp")

        if action == "PUSH":
            message = f'"{author}" pushed to "{to_branch}" on {timestamp}'
        elif action == "PULL_REQUEST":
            message = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
        elif action == "MERGE":
            message = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
        else:
            message = f'Unknown event: {e}'

        formatted_events.append(message)

    return jsonify(formatted_events)



@webhook_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Webhook Receiver Running!"}), 200


@webhook_bp.route('/ui', methods=['GET'])
def show_ui():
    return render_template('events.html')