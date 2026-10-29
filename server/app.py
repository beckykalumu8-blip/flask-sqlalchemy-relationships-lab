
from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///eventwise.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.get("/events")
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


@app.get("/events/<int:id>/sessions")
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


@app.get("/speakers")
def get_speakers():
    speakers = Speaker.query.all()

    return jsonify([
        {
            "id": speaker.id,
            "name": speaker.name
        }
        for speaker in speakers
    ]), 200


@app.get("/speakers/<int:id>")
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


@app.get("/sessions/<int:id>/speakers")
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


if __name__ == "__main__":
    app.run(port=5555, debug=True)

