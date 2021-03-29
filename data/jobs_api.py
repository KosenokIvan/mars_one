from datetime import date
import flask
from flask import jsonify, make_response, request
from . import db_session
from .jobs import Jobs
from .users import User

blueprint = flask.Blueprint(
    "jobs.api",
    __name__,
    template_folder="templates"
)


@blueprint.route("/api/jobs")
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            "jobs":
                [item.to_dict(only=("id", "team_leader", "job", "work_size", "collaborators",
                                    "start_date", "end_date", "is_finished")) for item in jobs]
        }
    )


@blueprint.route("/api/jobs/<int:job_id>")
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(
        {
            "job": job.to_dict(only=("id", "team_leader", "job", "work_size", "collaborators",
                                     "start_date", "end_date", "is_finished"))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ["team_leader", "job", "work_size",
                  "collaborators", "is_finished"]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    if not db_sess.query(User).filter(User.id == request.json["team_leader"]).first():
        return make_response(jsonify({"error": "team leader not found"}), 404)
    if db_sess.query(Jobs).filter(Jobs.id == request.json.get("id")).first():
        return make_response(jsonify({"error": "id already exists"}), 400)
    job = Jobs(
        team_leader=request.json["team_leader"],
        job=request.json["job"],
        work_size=request.json["work_size"],
        collaborators=request.json["collaborators"],
        end_date=request.json.get("end_date", date.today()),
        is_finished=request.json["is_finished"]
    )
    if request.json.get("id") is not None:
        job.id = request.json["id"]
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({"error": "Not found"}), 404)
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route("/api/jobs/<int:job_id>", methods=["PUT"])
def edit_job(job_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({"error": "Not found"}), 404)
    team_leader = request.json.get("team_leader", job.team_leader)
    if not db_sess.query(User).get(team_leader):
        return make_response(jsonify({"error": "team leader not found"}), 404)
    job.team_leader = team_leader
    job.job = request.json.get("job", job.job)
    job.work_size = request.json.get("work_size", job.work_size)
    job.collaborators = request.json.get("collaborators", job.collaborators)
    job.start_date = request.json.get("start_date", job.start_date)
    job.end_date = request.json.get("end_date", job.end_date)
    job.is_finished = request.json.get("is_finished", job.is_finished)
    db_sess.commit()
    return jsonify({'success': 'OK'})
