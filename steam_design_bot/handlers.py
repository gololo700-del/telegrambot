from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID, ADMIN_USERNAME
from keyboards import (
    main_menu_kb, illustration_type_kb, after_preview_kb,
    bg_type_kb, after_bg_preview_kb, invoice_kb,
    admin_order_kb, portfolio_back_kb, requirements_back_kb,
)
from states import OrderStates

router = Router()

# ─────────────────────────────────────────────────────────────────────────────
#  ПУТИ К ФОТО-ПРИМЕРАМ
#  Положи свои картинки в папку media/ рядом с bot.py и замени имена файлов
# ─────────────────────────────────────────────────────────────────────────────
PHOTO_ILLUS_VERTICAL   = "media/illus_vertical.jpg"    # пример вертикальной иллюстрации
PHOTO_ILLUS_HORIZONTAL = "media/illus_horizontal.jpg"  # пример горизонтальной иллюстрации
PHOTO_BG_ANIMATED      = "media/bg_animated.jpg"       # пример анимированного фона (скриншот/гиф-превью)
PHOTO_BG_STATIC        = "media/bg_static.jpg"         # пример обычного фона
PHOTO_PORTFOLIO_1      = "media/portfolio_1.jpg"       # пример работы в портфолио


# ─────────────────────────────────────────────────────────────────────────────
#  /start
# ─────────────────────────────────────────────────────────────────────────────
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Привет! Я бот по <b>индивидуальному оформлению профилей Steam</b>.\n\n"
        "Здесь ты можешь оставить заявку на оформление — я подберу фон, "
        "иллюстрацию и аватарку специально под твой стиль, и покажу, "
        "как всё будет выглядеть на готовом примере.\n\n"
        "Выбирай, что тебя интересует 👇",
        parse_mode="HTML",
        reply_markup=main_menu_kb(),
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Условия и требования
# ─────────────────────────────────────────────────────────────────────────────
@router.callback_query(F.data == "show_requirements")
async def show_requirements(call: CallbackQuery):
    text = (
        "📋 <b>Как работает оформление</b>\n\n"
        "Я подбираю под тебя:\n"
        "• 🖼 Иллюстрацию для профиля\n"
        "• 🎨 Фон профиля\n"
        "• 🖼 Аватарку\n"
        "• 📝 Всё оформление на твой вкус\n\n"
        "После подбора я показываю готовый пример как будет выглядеть профиль "
        "и даю пошаговый гайд по установке.\n\n"
        "⚠️ <b>Важно знать:</b>\n"
        "• Минимальный уровень Steam — <b>10 лвл</b>\n"
        "• Фоны и иллюстрации ты <b>покупаешь сам</b> в Steam (я их не оплачиваю)\n"
        "• Для анимированного фона нужно <b>2000 Steam поинтов</b>\n"
        "• Для обычного фона — оплата в рублях на торговой площадке Steam\n\n"
        "Моя услуга — это подбор, оформление и гайд.\n"
        "Стоимость — <b>250 руб</b> или <b>200 звёзд Telegram ⭐</b>"
    )
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=requirements_back_kb())
    await call.answer()


# ─────────────────────────────────────────────────────────────────────────────
#  Портфолио
# ─────────────────────────────────────────────────────────────────────────────
@router.callback_query(F.data == "show_portfolio")
async def show_portfolio(call: CallbackQuery):
    await call.message.answer_photo(
        photo=FSInputFile(PHOTO_PORTFOLIO_1),
        caption=(
            "💼 <b>Пример работы</b>\n\n"
            "Полностью индивидуальное оформление профиля Steam — "
            "иллюстрация, фон и аватарка подобраны под стиль клиента."
        ),
        parse_mode="HTML",
        reply_markup=portfolio_back_kb(),
    )
    await call.answer()


# ─────────────────────────────────────────────────────────────────────────────
#  Шаг 1 — Начало заказа / выбор иллюстрации
# ─────────────────────────────────────────────────────────────────────────────
@router.callback_query(F.data == "start_order")
async def start_order(call: CallbackQuery, state: FSMContext):
    await state.set_state(OrderStates.choosing_illustration)
    await call.message.edit_text(
        "🎨 <b>Шаг 1 из 3 — Тип иллюстрации</b>\n\n"
        "Выбери формат иллюстрации для своего профиля:",
        parse_mode="HTML",
        reply_markup=illustration_type_kb(),
    )
    await call.answer()


# ─────────────────────────────────────────────────────────────────────────────
#  Шаг 1 — Просмотр примера иллюстрации
# ─────────────────────────────────────────────────────────────────────────────
@router.callback_query(F.data.in_({"illus_vertical", "illus_horizontal"}), OrderStates.choosing_illustration)
async def show_illus_preview(call: CallbackQuery, state: FSMContext):
    is_vertical = call.data == "illus_vertical"
    await state.update_data(illustration_type="vertical" if is_vertical else "horizontal")
    await state.set_state(OrderStates.viewing_illus_preview)

    label   = "вертикальная" if is_vertical else "горизонтальная"
    photo   = PHOTO_ILLUS_VERTICAL if is_vertical else PHOTO_ILLUS_HORIZONTAL
    back_cb = "back_to_illus_choice"

    await call.message.answer_photo(
        photo=FSInputFile(photo),
        caption=(
            f"👆 <b>Пример — {label} иллюстрация</b>\n\n"
            "Именно в таком формате будет оформлена твоя иллюстрация в профиле.\n\n"
            "Нравится? Продолжай или вернись назад 👇"
        ),
        parse_mode="HTML",
        reply_markup=after_preview_kb(back_cb),
    )
    await call.answer()


@router.callback_query(F.data == "back_to_illus_choice")
async def back_to_illus_choice(call: CallbackQuery, state: FSMContext):
    await state.set_state(OrderStates.choosing_illustration)
    await call.message.edit_text(
        "🎨 <b>Шаг 1 из 3 — Тип иллюстрации</b>\n\n"
        "Выбери формат иллюстрации для своего профиля:",
        parse_mode="HTML",
        reply_markup=illustration_type_kb(),
    ) if call.message.photo is None else await call.message.answer(
        "🎨 <b>Шаг 1 из 3 — Тип иллюстрации</b>\n\n"
        "Выбери формат иллюстрации для своего профиля:",
        parse_mode="HTML",
        reply_markup=illustration_type_kb(),
    )
    await call.answer()


# ─────────────────────────────────────────────────────────────────────────────
#  Шаг 2 — Выбор фона
# ─────────────────────────────────────────────────────────────────────────────
@router.callback_query(F.data == "choose_bg_type")
async def choose_bg_type(call: CallbackQuery, state: FSMContext):
    await state.set_state(OrderStates.choosing_bg)
    await call.message.answer(
        "🖼 <b>Шаг 2 из 3 — Тип фона</b>\n\n"
        "Выбери, какой фон хочешь для профиля:\n\n"
        "✨ <b>Анимированный</b> — требует <b>2000 Steam поинтов</b> (ты покупаешь сам)\n"
        "🖼 <b>Обычный</b> — покупается за рубли в Steam (ты покупаешь сам)\n\n"
        "⚠️ Я подбираю и показываю варианты — покупку ты делаешь самостоятельно.",
        parse_mode="HTML",
        reply_markup=bg_type_kb(),
    )
    await call.answer()


# ─────────────────────────────────────────────────────────────────────────────
#  Шаг 2 — Просмотр примера фона
# ─────────────────────────────────────────────────────────────────────────────
@router.callback_query(F.data.in_({"bg_animated", "bg_static"}), OrderStates.choosing_bg)
async def show_bg_preview(call: CallbackQuery, state: FSMContext):
    is_animated = call.data == "bg_animated"
    await state.update_data(bg_type="animated" if is_animated else "static")
    await state.set_state(OrderStates.viewing_bg_preview)

    label   = "анимированный" if is_animated else "обычный"
    photo   = PHOTO_BG_ANIMATED if is_animated else PHOTO_BG_STATIC
    back_cb = "back_to_bg_choice"
    note    = "2000 Steam поинтов (покупаешь сам)" if is_animated else "оплата в рублях в Steam (покупаешь сам)"

    await call.message.answer_photo(
        photo=FSInputFile(photo),
        caption=(
            f"👆 <b>Пример — {label} фон</b>\n\n"
            f"💡 Стоимость фона: <b>{note}</b>\n\n"
            "Нравится? Продолжай — я покажу итоговый счёт за мои услуги 👇"
        ),
        parse_mode="HTML",
        reply_markup=after_bg_preview_kb(back_cb),
    )
    await call.answer()


@router.callback_query(F.data == "back_to_bg_choice")
async def back_to_bg_choice(call: CallbackQuery, state: FSMContext):
    await state.set_state(OrderStates.choosing_bg)
    await call.message.answer(
        "🖼 <b>Шаг 2 из 3 — Тип фона</b>\n\n"
        "Выбери, какой фон хочешь для профиля:",
        parse_mode="HTML",
        reply_markup=bg_type_kb(),
    )
    await call.answer()


@router.callback_query(F.data == "back_to_illus_choice", OrderStates.choosing_bg)
async def back_to_illus_from_bg(call: CallbackQuery, state: FSMContext):
    await back_to_illus_choice(call, state)


# ─────────────────────────────────────────────────────────────────────────────
#  Шаг 3 — Итоговый счёт
# ─────────────────────────────────────────────────────────────────────────────
@router.callback_query(F.data == "show_invoice")
async def show_invoice(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    illus = "Вертикальная" if data.get("illustration_type") == "vertical" else "Горизонтальная"
    bg    = "Анимированный (2000 Steam поинтов)" if data.get("bg_type") == "animated" else "Обычный (за рубли в Steam)"

    await state.set_state(OrderStates.viewing_invoice)

    text = (
        "🧾 <b>Шаг 3 из 3 — Итоговый счёт</b>\n\n"
        "<b>Твой заказ:</b>\n"
        f"🎨 Иллюстрация: <b>{illus}</b>\n"
        f"🖼 Фон: <b>{bg}</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "<b>Что входит в услугу:</b>\n"
        "✅ Подбор иллюстрации под твой стиль\n"
        "✅ Подбор фона\n"
        "✅ Подбор / рекомендация аватарки\n"
        "✅ Пример готового профиля\n"
        "✅ Пошаговый гайд по установке\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "⚠️ <b>Важно:</b>\n"
        "• Фон и иллюстрации ты <b>покупаешь сам</b> в Steam\n"
        "• Минимальный уровень аккаунта — <b>10 лвл Steam</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💰 <b>Стоимость моей услуги:</b>\n"
        "   • <b>250 рублей</b>\n"
        "   • или <b>200 звёзд Telegram ⭐</b>\n\n"
        "Согласен? Нажми кнопку — я отправлю заявку мастеру 👇"
    )
    await call.message.answer(text, parse_mode="HTML", reply_markup=invoice_kb())
    await call.answer()


@router.callback_query(F.data == "back_to_bg_choice", OrderStates.viewing_invoice)
async def back_to_bg_from_invoice(call: CallbackQuery, state: FSMContext):
    await back_to_bg_choice(call, state)


# ─────────────────────────────────────────────────────────────────────────────
#  Отправка заявки
# ─────────────────────────────────────────────────────────────────────────────
@router.callback_query(F.data == "submit_order", OrderStates.viewing_invoice)
async def submit_order(call: CallbackQuery, state: FSMContext, bot: Bot):
    data  = await state.get_data()
    user  = call.from_user
    illus = "Вертикальная" if data.get("illustration_type") == "vertical" else "Горизонтальная"
    bg    = "Анимированный" if data.get("bg_type") == "animated" else "Обычный"

    await state.set_state(OrderStates.waiting_approval)

    # — Сообщение клиенту
    await call.message.answer(
        "⏳ <b>Заявка отправлена!</b>\n\n"
        "Я уже получил твой запрос и скоро рассмотрю его.\n"
        "После одобрения тебе придёт уведомление с моим контактом — "
        "напишешь мне для финального согласования оформления.\n\n"
        "🕐 Обычно отвечаю в течение нескольких часов.",
        parse_mode="HTML",
    )
    await call.answer("✅ Заявка отправлена!")

    # — Уведомление админу
    username_str = f"@{user.username}" if user.username else f"нет username, ID: {user.id}"
    admin_text = (
        "🔔 <b>Новая заявка на оформление!</b>\n\n"
        f"👤 Клиент: {user.full_name}\n"
        f"🔗 Контакт: {username_str}\n"
        f"🆔 ID: <code>{user.id}</code>\n\n"
        f"🎨 Иллюстрация: <b>{illus}</b>\n"
        f"🖼 Фон: <b>{bg}</b>\n\n"
        "Одобри или отклони заявку 👇"
    )
    await bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML", reply_markup=admin_order_kb(user.id))


# ─────────────────────────────────────────────────────────────────────────────
#  Одобрение / отклонение заявки (только для админа)
# ─────────────────────────────────────────────────────────────────────────────
@router.callback_query(F.data.startswith("approve_"))
async def approve_order(call: CallbackQuery, bot: Bot):
    if call.from_user.id != ADMIN_ID:
        await call.answer("⛔ Нет доступа", show_alert=True)
        return

    client_id = int(call.data.split("_")[1])

    # — Клиенту
    await bot.send_message(
        client_id,
        f"✅ <b>Твоя заявка одобрена!</b>\n\n"
        f"Напиши мне в личку, чтобы мы начали согласование оформления:\n\n"
        f"👉 @{ADMIN_USERNAME}\n\n"
        f"Не забудь сообщить:\n"
        f"• Ник в Steam\n"
        f"• Пожелания по стилю (цвета, аниме/игры/арт и т.д.)\n"
        f"• Уровень твоего Steam аккаунта (мин. 10 лвл)\n\n"
        f"Жду тебя! 🎨",
        parse_mode="HTML",
    )

    # — Обновляем сообщение у админа
    await call.message.edit_text(
        call.message.text + "\n\n✅ <b>Одобрено</b>",
        parse_mode="HTML",
    )
    await call.answer("✅ Заявка одобрена, клиент уведомлён!")


@router.callback_query(F.data.startswith("reject_"))
async def reject_order(call: CallbackQuery, bot: Bot):
    if call.from_user.id != ADMIN_ID:
        await call.answer("⛔ Нет доступа", show_alert=True)
        return

    client_id = int(call.data.split("_")[1])

    # — Клиенту
    await bot.send_message(
        client_id,
        "❌ <b>К сожалению, заявка не принята.</b>\n\n"
        "Возможно, сейчас нет свободных мест или не выполнены требования.\n\n"
        "Попробуй позже или напиши напрямую: "
        f"@{ADMIN_USERNAME}",
        parse_mode="HTML",
    )

    # — Обновляем у админа
    await call.message.edit_text(
        call.message.text + "\n\n❌ <b>Отклонено</b>",
        parse_mode="HTML",
    )
    await call.answer("❌ Заявка отклонена")


# ─────────────────────────────────────────────────────────────────────────────
#  Назад в главное меню
# ─────────────────────────────────────────────────────────────────────────────
@router.callback_query(F.data == "back_to_main")
async def back_to_main(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(
        "🏠 <b>Главное меню</b>\n\nВыбирай, что тебя интересует 👇",
        parse_mode="HTML",
        reply_markup=main_menu_kb(),
    )
    await call.answer()
