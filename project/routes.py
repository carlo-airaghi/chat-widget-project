from flask import Blueprint, request, jsonify, current_app, send_from_directory
from utils import ConversationManager, diet_check

def create_blueprint(diet_pipeline, final_pipeline, conversation_manager):
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

        # Packing the custom fields into JSON for le pipeline.
        diet_pipeline_data = {
            "retriever": {"query": question},
            "prompt_builder": {
                "diet_reply": "0",  # Inizialmente 0, verrà aggiornato nel loop.
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
        }
        final_pipeline_data = {
            "retriever": {"query": question},
            "prompt_builder": {
                "question": question,
                "diet_reply": "0",  # Verrà aggiornato con il risultato del ciclo diet.
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
                "customer_macroblocco": customer_macroblocco,
                "customer_week": customer_week,
                "customer_day": customer_day,
                "customer_exercise_selected": customer_exercise_selected,
                "customer_country": customer_country,
                "customer_city": customer_city,
                "customer_province": customer_province,
                "customer_sub_expire": customer_sub_expire,
                "customer_sub_type": customer_sub_type,
                "customer_settimana_test_esercizi": customer_settimana_test_esercizi,
                "customer_settimana_test_pesi": customer_settimana_test_pesi,
                "customer_workout_della_settimna": customer_workout_della_settimna,
                "conversation_history": recent_messages
            }
        }

        try:
            # Prima fase: Chiamata iterativa alla diet pipeline.
            diet_reply = "0"
            exit_loop = False

            # Converti i target nutrizionali in float.
            try:
                target_kcal = float(diet_pipeline_data["prompt_builder"].get("customer_kcal", 0))
                target_proteins = float(diet_pipeline_data["prompt_builder"].get("customer_proteins", 0))
                target_grassi = float(diet_pipeline_data["prompt_builder"].get("customer_fats", 0))
                target_carbs = float(diet_pipeline_data["prompt_builder"].get("customer_carbs", 0))
            except Exception as e:
                current_app.logger.error("Error converting target values: %s", e, exc_info=True)
                target_kcal = target_proteins = target_grassi = target_carbs = 0

            for iteration in range(3):
                try:
                    diet_results = diet_pipeline.run(diet_pipeline_data)
                    diet_reply = diet_results["llm"]["replies"][0]
                    current_app.logger.info(f"Iteration {iteration + 1}: diet_reply received: {diet_reply}")
                    exit_loop, parsed_result = diet_check(
                        diet_reply,
                        target_kcal,
                        target_proteins,
                        target_grassi,
                        target_carbs
                    )
                    current_app.logger.info(f"Iteration {iteration + 1}: exit_loop = {exit_loop}")
                    if exit_loop:
                        current_app.logger.info(f"Exiting diet loop at iteration {iteration + 1}.")
                        break
                except Exception as e:
                    current_app.logger.error("Error during diet pipeline iteration: %s", e, exc_info=True)
                    break

            # Aggiorno il campo "diet_reply" per il final pipeline.
            final_pipeline_data["prompt_builder"]["diet_reply"] = diet_reply

            # Seconda fase: Chiamata al final pipeline (GPT‑4) utilizzando la dieta ottenuta.
            final_results = final_pipeline.run(final_pipeline_data)
            final_reply = final_results["llm"]["replies"][0]

            # Aggiungo la risposta finale alla cronologia della conversazione.
            conversation_manager.add_message(customer_id, "assistant", final_reply)
            return jsonify({'reply': final_reply})
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
