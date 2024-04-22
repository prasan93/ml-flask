from flask import Blueprint, jsonify, request
from service.user_service import UserService
from groq import Groq
import os

chat = Blueprint("chat", __name__, url_prefix="/api/v1/chat")

@chat.route("", methods=["POST"])
def post_chat():
    json_data = request.json
    user_id = json_data.get("user_id")
    chat    = json_data.get("msg")
    if not user_id or not chat:
        return jsonify({"message": 'Required parameters are missing'}), 422

    user_result = UserService.get_user_by_id(
        user_id=user_id
    )    
    
    if user_result:
        try:
            client = Groq(
                api_key=os.environ.get("GROQ_API_KEY"),
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": str(chat),
                    }
                ],
                model=os.environ.get("model"),
            )
            return chat_completion.choices[0].message.content, 200  
        except Exception as  e:
            return jsonify({"error": "Conflict", "error_message": "LLM backend Server error"}), 409  
    else: 
        return jsonify({"error": "Conflict", "error_message": "User invalid"}), 403       