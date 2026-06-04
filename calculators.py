from config import config
from typing import Tuple


def calculate_state_fee(claim_amount: float) -> Tuple[float, str]:
    if claim_amount <= 0:
        return 0, "Сумма иска должна быть положительной"

    prev_max = 0
    for max_amount, base_fee, rate in config.STATE_FEE_BRACKETS:
        if claim_amount <= max_amount:
            if rate == 0:
                fee = base_fee
                formula = f"{base_fee} руб."
            else:
                excess = claim_amount - prev_max
                fee = base_fee + (excess * rate)
                formula = f"{base_fee} + ({excess} × {rate * 100}%) = {fee:.2f} руб."

            if fee > config.MAX_STATE_FEE:
                fee = config.MAX_STATE_FEE
                formula += f" (ограничено {config.MAX_STATE_FEE} руб.)"

            return round(fee, 2), formula
        prev_max = max_amount

    return 0, "Ошибка расчёта"


def calculate_penalty(debt_amount: float, days_overdue: int) -> Tuple[float, str]:
    if debt_amount <= 0:
        return 0, "Сумма долга должна быть положительной"
    if days_overdue <= 0:
        return 0, "Дни просрочки должны быть положительными"

    daily_rate = config.REFINANCING_RATE / 365

    if days_overdue <= 90:
        rate = config.PENALTY_RATE_1_90
        rate_desc = "1/300"
    elif days_overdue <= 180:
        rate = config.PENALTY_RATE_91_180
        rate_desc = "1/170"
    else:
        rate = config.PENALTY_RATE_181_PLUS
        rate_desc = "1/130"

    penalty = debt_amount * daily_rate * rate * days_overdue
    formula = f"{debt_amount:.2f} × {daily_rate:.6f} × {rate_desc} × {days_overdue} = {penalty:.2f} руб."

    return round(penalty, 2), formula
