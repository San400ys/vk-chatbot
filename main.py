import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from config import config
from database import Database
from calculators import calculate_state_fee, calculate_penalty
from document_generator import DocumentGenerator
from keyboards import *
from feedback import FeedbackHandler
from utils import parse_number


class VKLegalBot:
    def __init__(self):
        self.vk_session = vk_api.VkApi(token=config.VK_ACCESS_TOKEN)
        self.longpoll = VkBotLongPoll(self.vk_session, config.VK_GROUP_ID)
        self.vk = self.vk_session.get_api()
        self.db = Database(str(config.DATABASE_PATH))
        self.feedback = FeedbackHandler(self.db)
        self.doc_gen = DocumentGenerator()
        self.user_states = {}

    def send(self, user_id: int, text: str, keyboard=None):
        self.vk.messages.send(
            user_id=user_id,
            message=text,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard() if keyboard else None
        )

    def run(self):
        print("✅ Бот запущен!")

        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
                user_id = event.message.from_id
                text = event.message.text.strip()

                user_info = self.vk.users.get(user_ids=user_id)
                user_name = f"{user_info[0].get('first_name', '')} {user_info[0].get('last_name', '')}"

                print(f"📩 {user_name}: {text}")

                if text.lower() in ["начать", "старт", "start", "привет"]:
                    self.send(user_id, "🤖 Добро пожаловать! Я юридический помощник.\nВыберите действие:",
                              get_main_keyboard())

                elif text == "📚 Автор":
                    self.send(user_id, config.AUTHOR_INFO, get_main_keyboard())

                elif text == "📰 Блог":
                    blog_text = "📰 НОВОСТИ\n\n" + "\n\n".join(config.BLOG_POSTS)
                    self.send(user_id, blog_text, get_main_keyboard())

                elif text == "💰 Правовой калькулятор":
                    self.send(user_id, "Выберите тип расчёта:", get_calculator_keyboard())

                elif text == "⚖️ Правовой конструктор":
                    self.send(user_id, "Выберите тип документа:", get_constructor_keyboard())

                elif text == "📩 Обратная связь":
                    self.user_states[user_id] = {'mode': 'feedback', 'step': 1}
                    self.send(user_id, "📞 Введите ваш контакт (телефон, email или ссылку ВК):", get_back_keyboard())

                elif text == "🏛️ Госпошлина в суд":
                    self.user_states[user_id] = {'mode': 'state_fee'}
                    self.send(user_id, "💰 Введите сумму иска в рублях:", get_back_keyboard())

                elif text == "🏠 Пени за ЖКУ":
                    self.user_states[user_id] = {'mode': 'penalty', 'step': 1}
                    self.send(user_id, "🏠 Введите сумму задолженности по ЖКУ в рублях:", get_back_keyboard())

                elif text == "📄 Заявление о судебном приказе":
                    self.user_states[user_id] = {'mode': 'sue_order', 'step': 1, 'data': {}}
                    self.send(user_id, "📝 Введите ФИО взыскателя:", get_back_keyboard())

                elif text == "⚖️ Иск о взыскании ЖКУ":
                    self.user_states[user_id] = {'mode': 'housing_claim', 'step': 1, 'data': {}}
                    self.send(user_id, "🏢 Введите наименование истца (УК/ТСЖ):", get_back_keyboard())

                elif text == "🔙 Назад в меню":
                    self.user_states.pop(user_id, None)
                    self.send(user_id, "Главное меню:", get_main_keyboard())

                else:
                    self.process_input(user_id, text, user_name)

    def process_input(self, user_id: int, text: str, user_name: str):
        state = self.user_states.get(user_id)

        if not state:
            self.send(user_id, "Используйте кнопки меню", get_main_keyboard())
            return

        mode = state.get('mode')

        # Калькулятор госпошлины
        if mode == 'state_fee':
            try:
                amount = parse_number(text)
                fee, formula = calculate_state_fee(amount)
                self.send(user_id,
                          f"⚖️ РАСЧЁТ ГОСПОШЛИНЫ\n\nСумма иска: {amount:,.2f} руб.\n{formula}\n\nИтого: {fee:,.2f} руб.",
                          get_calculator_keyboard())
                del self.user_states[user_id]
            except:
                self.send(user_id, "❌ Ошибка. Введите число (например: 150000)", get_back_keyboard())

        # Калькулятор пени
        elif mode == 'penalty':
            step = state.get('step', 1)
            if step == 1:
                try:
                    debt = parse_number(text)
                    self.user_states[user_id] = {'mode': 'penalty', 'step': 2, 'debt': debt}
                    self.send(user_id, "📅 Введите количество дней просрочки:", get_back_keyboard())
                except:
                    self.send(user_id, "❌ Ошибка. Введите сумму долга.")
            else:
                try:
                    days = int(parse_number(text))
                    debt = state.get('debt', 0)
                    penalty, formula = calculate_penalty(debt, days)
                    self.send(user_id,
                              f"🏠 РАСЧЁТ ПЕНИ\n\nДолг: {debt:,.2f} руб.\nДней: {days}\n{formula}\n\nИтого пени: {penalty:,.2f} руб.",
                              get_calculator_keyboard())
                    del self.user_states[user_id]
                except:
                    self.send(user_id, "❌ Ошибка. Введите количество дней.")

        # Судебный приказ
        elif mode == 'sue_order':
            step = state.get('step', 1)
            data = state.get('data', {})

            if step == 1:
                data['creditor_name'] = text
                self.user_states[user_id] = {'mode': 'sue_order', 'step': 2, 'data': data}
                self.send(user_id, "📍 Введите адрес взыскателя:", get_back_keyboard())
            elif step == 2:
                data['creditor_address'] = text
                self.user_states[user_id] = {'mode': 'sue_order', 'step': 3, 'data': data}
                self.send(user_id, "📝 Введите ФИО должника:", get_back_keyboard())
            elif step == 3:
                data['debtor_name'] = text
                self.user_states[user_id] = {'mode': 'sue_order', 'step': 4, 'data': data}
                self.send(user_id, "📍 Введите адрес должника:", get_back_keyboard())
            elif step == 4:
                data['debtor_address'] = text
                self.user_states[user_id] = {'mode': 'sue_order', 'step': 5, 'data': data}
                self.send(user_id, "💰 Введите сумму долга (цифрами):", get_back_keyboard())
            elif step == 5:
                try:
                    data['debt_amount'] = float(parse_number(text))
                    self.user_states[user_id] = {'mode': 'sue_order', 'step': 6, 'data': data}
                    self.send(user_id, "📋 Введите основание взыскания (например: договор займа):", get_back_keyboard())
                except:
                    self.send(user_id, "❌ Ошибка. Введите число.", get_back_keyboard())
            elif step == 6:
                data['basis'] = text
                doc = self.doc_gen.generate_sue_order(data)
                self.send(user_id, f"📄 ВАШ ДОКУМЕНТ:\n\n{doc}\n\nСохраните и распечатайте.",
                          get_constructor_keyboard())
                del self.user_states[user_id]

        # Иск о взыскании ЖКУ
        elif mode == 'housing_claim':
            step = state.get('step', 1)
            data = state.get('data', {})

            if step == 1:
                data['plaintiff'] = text
                self.user_states[user_id] = {'mode': 'housing_claim', 'step': 2, 'data': data}
                self.send(user_id, "📍 Введите адрес истца:", get_back_keyboard())
            elif step == 2:
                data['plaintiff_address'] = text
                self.user_states[user_id] = {'mode': 'housing_claim', 'step': 3, 'data': data}
                self.send(user_id, "📝 Введите ФИО ответчика (должника):", get_back_keyboard())
            elif step == 3:
                data['defendant'] = text
                self.user_states[user_id] = {'mode': 'housing_claim', 'step': 4, 'data': data}
                self.send(user_id, "📍 Введите адрес ответчика:", get_back_keyboard())
            elif step == 4:
                data['defendant_address'] = text
                self.user_states[user_id] = {'mode': 'housing_claim', 'step': 5, 'data': data}
                self.send(user_id, "📅 Введите период задолженности (например: январь-март 2026):", get_back_keyboard())
            elif step == 5:
                data['period'] = text
                self.user_states[user_id] = {'mode': 'housing_claim', 'step': 6, 'data': data}
                self.send(user_id, "💰 Введите сумму долга (цифрами):", get_back_keyboard())
            elif step == 6:
                try:
                    data['debt_amount'] = float(parse_number(text))
                    self.user_states[user_id] = {'mode': 'housing_claim', 'step': 7, 'data': data}
                    self.send(user_id, "💰 Введите сумму пени (цифрами, можно 0):", get_back_keyboard())
                except:
                    self.send(user_id, "❌ Ошибка. Введите число.", get_back_keyboard())
            elif step == 7:
                try:
                    data['penalty'] = float(parse_number(text))
                    doc = self.doc_gen.generate_housing_claim(data)
                    self.send(user_id, f"📄 ВАШ ДОКУМЕНТ:\n\n{doc}\n\nСохраните и подайте в суд.",
                              get_constructor_keyboard())
                    del self.user_states[user_id]
                except:
                    self.send(user_id, "❌ Ошибка. Введите число.", get_back_keyboard())

        # Обратная связь
        elif mode == 'feedback':
            step = state.get('step', 1)
            if step == 1:
                self.user_states[user_id] = {'mode': 'feedback', 'step': 2, 'contact': text}
                self.send(user_id, "✏️ Введите ваше сообщение:", get_back_keyboard())
            else:
                contact = state.get('contact', '')
                self.db.save_feedback(user_id, user_name, contact, text)
                del self.user_states[user_id]
                self.send(user_id, "✅ Спасибо! Ваше обращение сохранено. Мы свяжемся с вами.", get_main_keyboard())


if __name__ == "__main__":
    bot = VKLegalBot()
    bot.run()