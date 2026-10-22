#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)



# Return all events.
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()

    return jsonify([
        {
            "id": event.id,
            "name": event.name,
            "location": event.location
        }
        for event in events
    ]), 200


# Return all sessions belonging to a specific event.
@app.route('/events/<int:id>/sessions', methods=['GET'])
def get_event_sessions(id):
    event = db.session.get(Event, id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    return jsonify([
        {
            "id": session.id,
            "title": session.title,
            "start_time": session.start_time.isoformat()
        }
        for session in event.sessions
    ]), 200


# Return all speakers.
@app.route('/speakers', methods=['GET'])
def get_speakers():
    speakers = Speaker.query.all()

    return jsonify([
        {
            "id": speaker.id,
            "name": speaker.name
        }
        for speaker in speakers
    ]), 200


# Return one speaker and their bio.
@app.route('/speakers/<int:id>', methods=['GET'])
def get_speaker(id):
    speaker = db.session.get(Speaker, id)

    if speaker is None:
        return jsonify({"error": "Speaker not found"}), 404

    return jsonify({
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": (
            speaker.bio.bio_text
            if speaker.bio is not None
            else "No bio available"
        )
    }), 200


# Return all speakers associated with a specific session.
@app.route('/sessions/<int:id>/speakers', methods=['GET'])
def get_session_speakers(id):
    session = db.session.get(Session, id)

    if session is None:
        return jsonify({"error": "Session not found"}), 404

    return jsonify([
        {
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": (
                speaker.bio.bio_text
                if speaker.bio is not None
                else "No bio available"
            )
        }
        for speaker in session.speakers
    ]), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)

