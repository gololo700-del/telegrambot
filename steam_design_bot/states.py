from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    # Шаг 1 — выбор типа иллюстрации
    choosing_illustration = State()

    # Шаг 2 — просмотр примера иллюстрации
    viewing_illus_preview = State()

    # Шаг 3 — выбор типа фона
    choosing_bg = State()

    # Шаг 4 — просмотр примера фона
    viewing_bg_preview = State()

    # Шаг 5 — просмотр счёта
    viewing_invoice = State()

    # Шаг 6 — заявка отправлена, ожидание одобрения
    waiting_approval = State()
