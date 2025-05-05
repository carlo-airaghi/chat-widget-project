import json
import logging
from pathlib import Path

from flask import Blueprint, request, jsonify, send_from_directory
from jinja2 import Template
from openai import OpenAIError

from utils import safe_float_water_requirement, log_openai_usage


# ── Helpers ──────────────────────────────────────────────────────────────
def render_prompt(template_path: Path, **vars):
    with template_path.open(encoding="utf-8") as f:
        tmpl = Template(f.read())
    return tmpl.render(**vars)


def first_assistant_reply(response):
    """
    Iterate over response.output and return the first assistant message’s text.
    Works whether or not the model used tools.
    """
    for item in response.output:
        if getattr(item, "role", None) == "assistant" and hasattr(item, "content"):
            # content is always a list (assistant can stream multiple blocks)
            return item.content[0].text
    return None


# ── Blueprint factory ────────────────────────────────────────────────────
def create_blueprint(openai_client, conversation_manager, cfg):
    chat_bp = Blueprint("chat_bp", __name__)

    # ─────────────────────────────────────────────────────────────────────
    @chat_bp.route("/chat", methods=["POST"])
    def chat():
        data      = request.get_json() or {}
        question  = (data.get("message") or "").strip()
        user_data = data.get("user", {}) or {}

        customer_id = user_data.get("Customer_ID")
        if not customer_id:
            return jsonify({"reply": "Please provide a valid Customer_ID."}), 400
        if not question:
            return jsonify({"reply": "Please provide a message."}), 400

        # ---- Render system prompt --------------------------------------
        prompt_vars = {
            "question":                    question,
            "customer_id":                 customer_id,
            "customer_name":               user_data.get("Name", ""),
            "customer_surname":            user_data.get("Surname", ""),
            "customer_age":                user_data.get("Age", ""),
            "customer_sesso":              user_data.get("Sesso", ""),
            "customer_weight":             user_data.get("Weight", ""),
            "customer_height":             user_data.get("Height", ""),
            "customer_water_requirement":  safe_float_water_requirement(user_data.get("Weight")),
            "customer_distretto_carente1": user_data.get("customerDistrettoCarente1", ""),
            "customer_distretto_carente2": user_data.get("customerDistrettoCarente2", ""),
            "customer_percentuale_massa_grassa": user_data.get("PercentualeMassaGrassa", ""),
            "customer_dispendio_calorico": user_data.get("DispendioCalorico", ""),
            "customer_kcal":               user_data.get("Kcal", ""),
            "customer_fats":               user_data.get("Fats", ""),
            "customer_proteins":           user_data.get("Proteins", ""),
            "customer_carbs":              user_data.get("Carbs", ""),
            "customer_diet_type":          user_data.get("DietType", ""),
            "customer_macroblocco":        user_data.get("Macroblocco", ""),
            "customer_week":               user_data.get("Week", ""),
            "customer_day":                user_data.get("Day", ""),
            "customer_exercise_selected":  user_data.get("ExerciseSelected", ""),
            "customer_country":            user_data.get("Country", ""),
            "customer_city":               user_data.get("City", ""),
            "customer_province":           user_data.get("Province", ""),
            "customer_sub_expire":         user_data.get("subExpire", ""),
            "customer_sub_type":           user_data.get("SubType", ""),
            "customer_settimana_test_esercizi": user_data.get("SettimanaTestEsercizi", ""),
            "customer_settimana_test_pesi":     user_data.get("SettimanaTestPesi", ""),
            "customer_workout_della_settimna":  json.dumps(user_data.get("WorkoutDellaSettimna", {}), ensure_ascii=False),
            "conversation_history":        conversation_manager.get_history(customer_id),
        }

        sys_prompt = render_prompt(
            Path(cfg["PROMPTS_FOLDER"]) / "prompt_template.txt",
            **prompt_vars
        )

        # ---- Build messages --------------------------------------------
        messages = [
            {"role": "system", "content": sys_prompt},
            *conversation_manager.get_history(customer_id),
            {"role": "user", "content": question},
        ]

        # ---- File‑search tool & config ----------------------------------
        tools = [{
            "type": "file_search",
            "vector_store_ids": [cfg["OPENAI_VECTOR_STORE_ID"]],
        }]

        try:
            response = openai_client.responses.create(
                model              = cfg["OPENAI_MODEL"],
                input              = messages,
                tools              = tools,
                temperature        = 1.0,
                max_output_tokens  = 2048,
                top_p              = 1.0,
                store              = True,
            )

            # Full JSON‑serialisable dump for your Docker logs
            logging.info("Full OpenAI response: %s", response.model_dump())

            reply = first_assistant_reply(response)
            if reply is None:
                logging.error("No assistant reply found in OpenAI response!")
                return jsonify({"reply": "Sorry, I didn’t receive a valid answer."}), 502

            # Persist in conversation history
            conversation_manager.add_message(customer_id, "assistant", reply)

            # Log token usage
            log_openai_usage(response)

            return jsonify({"reply": reply})

        except OpenAIError as e:
            logging.error("OpenAI API error: %s", e, exc_info=True)
            return jsonify({"reply": "OpenAI error, please try again later."}), 502
        except Exception as e:
            logging.error("Unhandled error in /chat: %s", e, exc_info=True)
            return jsonify({"reply": "Sorry, an error occurred. Please try again later."}), 500

    # ─────────────────────────────────────────────────────────────────────
    @chat_bp.route("/history/<customer_id>", methods=["GET"])
    def get_conversation_history(customer_id):
        return jsonify({"history": conversation_manager.get_history(customer_id)}), 200

    @chat_bp.route("/deleteHistory/<customer_id>", methods=["DELETE"])
    def delete_history(customer_id):
        if conversation_manager.delete_history(customer_id) is not None:
            return jsonify({"success": True, "message": "Conversation history deleted."}), 200
        return jsonify({"success": False, "message": "No conversation history found for this user."}), 404

    # Static file helper
    @chat_bp.route("/static/<path:filename>")
    def serve_static(filename):
        return send_from_directory(cfg["STATIC_FOLDER"], filename)

    @chat_bp.route("/health")
    def health():
        return "ok", 200

    return chat_bp
