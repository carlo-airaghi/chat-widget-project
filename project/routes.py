# routes.py
from flask import Blueprint, request, jsonify, current_app, send_from_directory

def create_blueprint(pipeline, conversation_manager):
    chat_bp = Blueprint('chat_bp', __name__)

    @chat_bp.route('/chat', methods=['POST'])
    def chat():
        data = request.get_json()
        question = data.get('message', '')
        user_data = data.get('user', {})

        # Extract customer fields.
        customer_id = user_data.get('Customer_ID') or None
        customer_name = user_data.get('Name') or ''
        customer_surname = user_data.get('Surname') or ''
        customer_age = user_data.get('Age') or ''
        customer_sesso = user_data.get('Sesso') or ''
        customer_weight = user_data.get('Weight') or ''
        customer_height = user_data.get('Height') or ''
        customer_percentuale_massa_grassa = user_data.get('PercentualeMassaGrassa') or ''
        customer_dispendio_calorico = user_data.get('DispendioCalorico') or ''
        customer_diet_type = user_data.get('DietType') or ''
        customer_macroblocco = user_data.get('Macroblocco') or ''
        customer_week = user_data.get('Week') or ''
        customer_day = user_data.get('Day') or ''
        customer_exercise_selected = user_data.get('ExerciseSelected') or ''
        customer_country = user_data.get('Country') or ''
        customer_city = user_data.get('City') or ''
        customer_province = user_data.get('Province') or ''
        customer_sub_expire = user_data.get('subExpire') or ''
        customer_sub_type = user_data.get('SubType') or ''
        customer_kcal = user_data.get('Kcal') or ''
        customer_fats = user_data.get('Fats') or ''
        customer_proteins = user_data.get('Proteins') or ''
        customer_carbs = user_data.get('Carbs') or ''
        customer_settimana_test_esercizi = user_data.get('SettimanaTestEsercizi') or ''
        customer_settimana_test_pesi = user_data.get('SettimanaTestPesi') or ''
        customer_workout_della_settimna = user_data.get('WorkoutDellaSettimna') or {}
        customer_distretto_carente1 = user_data.get('customerDistrettoCarente1') or ''
        customer_distretto_carente2 = user_data.get('customerDistrettoCarente2') or ''

        if not customer_id:
            return jsonify({'reply': 'Please provide a valid Customer_ID.'}), 400
        if not question:
            return jsonify({'reply': 'Please provide a message.'}), 400

        # Add user's message to the conversation history.
        conversation_manager.add_message(customer_id, "user", question)
        recent_messages = conversation_manager.get_history(customer_id)

        try:
            results = pipeline.run({
                "retriever": {"query": question},
                "prompt_builder": {
                    "question": question,
                    "customer_id": customer_id,
                    "customer_name": customer_name,
                    "customer_surname": customer_surname,
                    "customer_age": customer_age,
                    "customer_sesso": customer_sesso,
                    "customer_weight": customer_weight,
                    "customer_height": customer_height,
                    "customer_distretto_carente1": customer_distretto_carente1,
                    "customer_distretto_carente2": customer_distretto_carente2,
                    "customer_percentuale_massa_grassa": customer_percentuale_massa_grassa,
                    "customer_dispendio_calorico": customer_dispendio_calorico,
                    "customer_kcal": customer_kcal,
                    "customer_fats": customer_fats,
                    "customer_proteins": customer_proteins,
                    "customer_carbs": customer_carbs,
                    "customer_diet_type": customer_diet_type,
                    "conversation_history": recent_messages
                }
            })
            reply = results["llm"]["replies"][0]

            # Add the  reply to the conversation history.
            conversation_manager.add_message(customer_id, "assistant", reply)
            return jsonify({'reply': reply})
        except Exception as e:
            current_app.logger.error("Error in /chat endpoint", exc_info=True)
            return jsonify({'reply': 'Sorry, an error occurred. Please try again later.'}), 500

    @chat_bp.route('/history/<customer_id>', methods=['GET'])
    def get_conversation_history(customer_id):
        history = conversation_manager.get_history(customer_id)
        return jsonify({"history": history}), 200

    @chat_bp.route('/deleteHistory/<customer_id>', methods=['DELETE'])
    def delete_history(customer_id):
        if conversation_manager.delete_history(customer_id) is not None:
            return jsonify({"success": True, "message": "Conversation history deleted."}), 200
        else:
            return jsonify({"success": False, "message": "No conversation history found for this user."}), 404

    @chat_bp.route('/static/<path:filename>')
    def serve_static(filename):
        static_folder = current_app.config.get('STATIC_FOLDER')
        return send_from_directory(static_folder, filename)

    return chat_bp
