from flask import Blueprint, jsonify, request
from service.user_service import UserService
from sqlalchemy.exc import IntegrityError

user = Blueprint("user", __name__, url_prefix="/api/v1/user")

@user.route("", methods=["POST"])
def add_user():
    json_data = request.json
    required_fields = ["fullname", "user_name", "email", "password", "birthday", "mobile_number"]
    missing_fields = [field for field in required_fields if field not in json_data]
    if missing_fields:
        return jsonify({"message": f'Required parameter "{missing_fields[0]}" is missing'}), 422

    try:
        print("reached")
        user_result = UserService.create_new_user_record(
            json_data["fullname"],
            json_data["user_name"],
            json_data["email"],
            json_data["password"],
            json_data["birthday"],
            json_data["mobile_number"]
        )
        # Convert User object to dictionary
        user_dict = user_result.__dict__
        # Remove password from the response for security reasons
        user_dict.pop('password', None)
        return "success", 200
    except IntegrityError as e:
        error_message = str(e.orig)
        return jsonify({"error": "Conflict", "error_message": error_message}), 409


@user.route("/add", methods=["POST"])
def get_user_by_id():
    json_data = request.json
    user_id = json_data.get("user_id")
    if not user_id:
        return jsonify({"message": 'Required parameter "user_id" is missing'}), 422

    user_result = UserService.get_user_by_id(
        user_id=user_id
    )
    return jsonify({"data": user_result}), 200


@user.route("/by-credentials", methods=["POST"])
def get_user_by_username_password():
    json_data = request.json
    user_name = json_data.get("user_name")
    if not user_name:
        return jsonify({"message": 'Required parameter "user_name" is missing'}), 422
    password = json_data.get("password")
    if not password:
        return jsonify({"message": 'Required parameter "password" is missing'}), 422

    try:
        user_result = UserService.get_user_by_credentials(
            user_name=user_name,
            password=password
        )
        
        if user_result:
            return user_result, 200
        else:
            return "invalid", 404
    except:
        return "Exception raised",500    