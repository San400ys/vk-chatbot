from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def get_main_keyboard() -> VkKeyboard:
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("📚 Авторы", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("📰 Блог", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("💰 Правовой калькулятор", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("⚖️ Правовой конструктор", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("📩 Обратная связь", color=VkKeyboardColor.NEGATIVE)
    return keyboard

def get_calculator_keyboard() -> VkKeyboard:
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("🏛️ Госпошлина в суд", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("🏠 Пени за ЖКУ", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("🔙 Назад в меню", color=VkKeyboardColor.SECONDARY)
    return keyboard

def get_constructor_keyboard() -> VkKeyboard:
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("📄 Заявление о судебном приказе", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("⚖️ Иск о взыскании ЖКУ", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("🔙 Назад в меню", color=VkKeyboardColor.SECONDARY)
    return keyboard

def get_back_keyboard() -> VkKeyboard:
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("🔙 Назад в меню", color=VkKeyboardColor.SECONDARY)
    return keyboard