from datetime import datetime
from typing import Dict, Any


class DocumentGenerator:

    @staticmethod
    def generate_sue_order(data: Dict[str, Any]) -> str:
        now = datetime.now().strftime("%d.%m.%Y")

        # Преобразуем сумму в число, если пришла строкой
        debt_amount = data.get('debt_amount', 0)
        if isinstance(debt_amount, str):
            try:
                debt_amount = float(debt_amount.replace(',', '.'))
            except:
                debt_amount = 0

        return f"""
Мировому судье судебного участка № ___

От взыскателя: {data.get('creditor_name', '_______________')}
Адрес: {data.get('creditor_address', '_______________')}

От должника: {data.get('debtor_name', '_______________')}
Адрес: {data.get('debtor_address', '_______________')}

ЗАЯВЛЕНИЕ О ВЫНЕСЕНИИ СУДЕБНОГО ПРИКАЗА

«{now}»

Цена иска: {debt_amount:,.2f} руб.

Взыскатель просит вынести судебный приказ о взыскании с должника 
задолженности в размере {debt_amount:,.2f} руб.

Основание: {data.get('basis', '_______________')}

На основании ст. 121-127 ГПК РФ,

ПРОШУ:
1. Вынести судебный приказ о взыскании задолженности.
2. Взыскать расходы по уплате госпошлины.

__________________ / {data.get('creditor_name', 'Взыскатель')} /
"""

    @staticmethod
    def generate_housing_claim(data: Dict[str, Any]) -> str:
        now = datetime.now().strftime("%d.%m.%Y")

        # Преобразуем суммы в числа
        debt_amount = data.get('debt_amount', 0)
        penalty = data.get('penalty', 0)

        if isinstance(debt_amount, str):
            try:
                debt_amount = float(debt_amount.replace(',', '.'))
            except:
                debt_amount = 0

        if isinstance(penalty, str):
            try:
                penalty = float(penalty.replace(',', '.'))
            except:
                penalty = 0

        total = debt_amount + penalty

        return f"""
В __________________________ районный суд

Истец: {data.get('plaintiff', '_______________')}
Адрес: {data.get('plaintiff_address', '_______________')}

Ответчик: {data.get('defendant', '_______________')}
Адрес: {data.get('defendant_address', '_______________')}

ИСКОВОЕ ЗАЯВЛЕНИЕ
о взыскании задолженности за жилищно-коммунальные услуги

«{now}»

За период {data.get('period', '_______________')} у ответчика образовалась 
задолженность по оплате ЖКУ в размере {debt_amount:,.2f} руб.

В соответствии со ст. 155 ЖК РФ начислены пени в размере {penalty:,.2f} руб.

Общая сумма: {total:,.2f} руб.

На основании ст. 153, 155 ЖК РФ, ст. 309, 310 ГК РФ,

ПРОШУ СУД:
1. Взыскать задолженность в размере {debt_amount:,.2f} руб.
2. Взыскать пени в размере {penalty:,.2f} руб.
3. Взыскать расходы по уплате госпошлины.

__________________ / Истец /
"""