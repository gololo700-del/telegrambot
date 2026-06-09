from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ── Главное меню ──────────────────────────────────────────────────────────────
def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎨 Заказать оформление", callback_data="start_order")],
        [InlineKeyboardButton(text="📋 Условия и требования",  callback_data="show_requirements")],
        [InlineKeyboardButton(text="💬 Примеры работ",        callback_data="show_portfolio")],
    ])


# ── Выбор типа иллюстрации ────────────────────────────────────────────────────
def illustration_type_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Вертикальная иллюстрация", callback_data="illus_vertical")],
        [InlineKeyboardButton(text="🖥 Горизонтальная иллюстрация", callback_data="illus_horizontal")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")],
    ])


# ── После просмотра примера иллюстрации ──────────────────────────────────────
def after_preview_kb(back_cb: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Продолжить", callback_data="choose_bg_type")],
        [InlineKeyboardButton(text="◀️ Назад",      callback_data=back_cb)],
    ])


# ── Выбор типа фона ───────────────────────────────────────────────────────────
def bg_type_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✨ Анимированный фон (2000 Steam поинтов)", callback_data="bg_animated")],
        [InlineKeyboardButton(text="🖼 Обычный фон (за рубли)",                 callback_data="bg_static")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_illus_choice")],
    ])


# ── После просмотра примера фона ─────────────────────────────────────────────
def after_bg_preview_kb(back_cb: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Продолжить к оплате", callback_data="show_invoice")],
        [InlineKeyboardButton(text="◀️ Назад",               callback_data=back_cb)],
    ])


# ── Итоговый счёт ─────────────────────────────────────────────────────────────
def invoice_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Согласен — отправить заявку", callback_data="submit_order")],
        [InlineKeyboardButton(text="◀️ Назад",                       callback_data="back_to_bg_choice")],
    ])


# ── Кнопки для администратора ─────────────────────────────────────────────────
def admin_order_kb(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Одобрить",  callback_data=f"approve_{user_id}")],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{user_id}")],
    ])


# ── Портфолио (пример) ────────────────────────────────────────────────────────
def portfolio_back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎨 Заказать оформление", callback_data="start_order")],
        [InlineKeyboardButton(text="◀️ Назад в меню",        callback_data="back_to_main")],
    ])


# ── Требования / назад ────────────────────────────────────────────────────────
def requirements_back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎨 Заказать оформление", callback_data="start_order")],
        [InlineKeyboardButton(text="◀️ Назад в меню",        callback_data="back_to_main")],
    ])
