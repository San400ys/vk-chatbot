from database import Database
from typing import Dict


class FeedbackHandler:
    def __init__(self, db: Database):
        self.db = db
        self.user_states: Dict[int, str] = {}

    def process_feedback(self, user_id: int, user_name: str, text: str) -> str:
        state = self.user_states.get(user_id)

        if state is None or state == 'awaiting_contact':
            self.user_states[user_id] = 'awaiting_message'
            return "📞 Введите ваш контакт (телефон, email или ссылку ВК):"

        elif state == 'awaiting_message':
            contact_info = text
            self.user_states[user_id] = 'awaiting_text'
            return "✏️ Введите текст вашего сообщения или вопроса:"

        elif state == 'awaiting_text':
            message = text
            self.db.save_feedback(user_id, user_name, self.user_states.get('temp_contact', ''), message)
            del self.user_states[user_id]
            return "✅ Спасибо! Ваше обращение отправлено. Мы свяжемся с вами."

        return "❌ Ошибка. Попробуйте снова."
