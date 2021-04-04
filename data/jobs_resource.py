from datetime import date
from flask import jsonify
from flask_restful import abort, Resource
from . import db_session
from .jobs import Jobs
from .jobs_parser import parser
from .users_resource import abort_if_user_not_found


def abort_if_job_not_found(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        abort(404, mesage=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(job_id)
        return jsonify({"job": job.to_dict(only=("id", "team_leader",
                                                 "job", "work_size",
                                                 "collaborators", "start_date",
                                                 "end_date", "is_finished"))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(job_id)
        db_sess.delete(job)
        db_sess.commit()
        return jsonify({"success": "OK"})

    def put(self, job_id):
        args = parser.parse_args()
        abort_if_job_not_found(job_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(job_id)
        team_leader = args["team_leader"] if args["team_leader"] is not None else job.team_leader
        abort_if_user_not_found(team_leader)
        job.team_leader = team_leader
        job.job = args["job"] if args["job"] is not None else job.job
        job.work_size = args["work_size"] if args["work_size"] is not None else job.work_size
        job.collaborators = args["collaborators"] if args["collaborators"] is not None \
            else job.collaborators
        job.end_date = date.fromordinal(args["end_date"]) if args["end_date"] is not None \
            else job.end_date
        job.is_finished = args["is_finished"] if args["is_finished"] is not None else job.is_finished
        db_sess.commit()
        return jsonify({"success": "OK"})


class JobsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).all()
        return jsonify({"jobs": [job.to_dict(only=("id", "team_leader",
                                                   "job", "work_size",
                                                   "collaborators", "start_date",
                                                   "end_date", "is_finished"))
                                 for job in jobs]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        abort_if_user_not_found(args["team_leader"])
        job = Jobs(
            team_leader=args["team_leader"],
            job=args["job"],
            work_size=args["work_size"],
            collaborators=args["collaborators"],
            end_date=date.fromordinal(args["end_date"]),
            is_finished=args["is_finished"]
        )
        if args["id"] is not None:
            if db_sess.query(Jobs).get(args["id"]):
                abort(400, message=f"Job {args['id']} already exist")
            job.id = args["id"]
        db_sess.add(job)
        db_sess.commit()
        return jsonify({"success": "OK"})
