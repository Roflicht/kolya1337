from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import uuid

# Константы
API_TOKEN = '8118583402:AAF0vADomGWJkpnyaDre1TSnp29dq1WXnkE'  # Замените на ваш токен бота
STAR_PRICE = 1.83
MIN_PAYOUT = 500
STAR_PRICES = [100, 250, 500, 1000, 2500]
MAIN_MENU_TEXT = (
    "✨ Добро пожаловать!\n"
    "У нас вы можете купить ⭐️ Telegram Stars дешевле, чем в приложении и без KYC верификации\n"
    "Доступна оплата с помощью СБП и криптой\n"
    "Рекомендуем подписаться на наш канал!"
)

# Инициализация бота и роутера
bot = Bot(token=API_TOKEN)
router = Router()
user_states = {}

def create_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='⭐️ Купить себе', callback_data='buy_for_self')
    builder.button(text='⭐️ Подарить', callback_data='gift')
    builder.row()
    builder.button(text='👤 Профиль', callback_data='profile')
    builder.row()
    builder.button(text='👥 Реферальная система', callback_data='referral_system')
    builder.row()
    builder.button(text='🆘 Поддержка', callback_data='support')
    builder.row()
    builder.button(text='👉 Подписаться на наш канал', url='https://t.me/starfall_channel')
    builder.button(text='👉 Открыть вебапп', url='http://w91224il.beget.tech/')
    builder.adjust(2, 1, 1, 1, 1, 1)
    return builder.as_markup()

@router.message(F.text == "/start")
async def send_welcome(message: Message):
    await message.answer(MAIN_MENU_TEXT, reply_markup=create_main_menu_keyboard())

@router.callback_query(F.data == 'back_to_main_menu')
async def process_back_to_main_menu(callback_query: CallbackQuery):
    await callback_query.message.edit_text(MAIN_MENU_TEXT, reply_markup=create_main_menu_keyboard())
    await callback_query.answer()

@router.callback_query(F.data.startswith('pay_'))
async def process_payment(callback_query: CallbackQuery):
    order_id = callback_query.data.split('_')[1]
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад', callback_data='back_to_main_menu')
    await callback_query.message.edit_text(
        f"🎉 Поздравляем! Оплата успешно завершена.\nНомер заказа: {order_id}",
        reply_markup=builder.as_markup()
    )
    await callback_query.answer()

@router.callback_query(F.data == 'cancel_order')
async def process_cancel_order(callback_query: CallbackQuery):
    await callback_query.message.edit_text(MAIN_MENU_TEXT, reply_markup=create_main_menu_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == 'referral_system')
async def process_referral_system(callback_query: CallbackQuery):
    referral_link = "https://t.me/starfallrobot?start=eyJyZWYiOiAzfQ"
    invited_users = 35
    earned = 221.87
    current_balance = 115.30

    builder = InlineKeyboardBuilder()
    if current_balance >= MIN_PAYOUT:
        builder.button(text='Вывести', callback_data='withdraw_balance')
    builder.row()
    builder.button(text='Назад', callback_data='back_to_main_menu')

    text = (
        "👤 Реферальная система\n"
        "Приглашай людей и получай 20% от дохода навсегда\n"
        f"Ваша реферальная ссылка:\n{referral_link}\n"
        "Статистика:\n"
        f"Приглашено: {invited_users} чел.\n"
        f"Заработано: {earned:.2f} RUB\n"
        f"Текущий баланс: {current_balance:.2f} RUB\n"
    )
    if current_balance < MIN_PAYOUT:
        remaining_amount = MIN_PAYOUT - current_balance
        text += f"❌ Для вывода необходимо еще {remaining_amount:.2f} RUB"

    await callback_query.message.edit_text(text, reply_markup=builder.as_markup())
    await callback_query.answer()

@router.callback_query(F.data == 'withdraw_balance')
async def process_withdraw_balance(callback_query: CallbackQuery):
    current_balance = 115.30
    if current_balance < MIN_PAYOUT:
        remaining_amount = MIN_PAYOUT - current_balance
        await callback_query.answer(f"❌ Для вывода необходимо еще {remaining_amount:.2f} RUB", show_alert=True)
    else:
        await callback_query.answer("✅ Запрос на вывод отправлен!", show_alert=True)

@router.callback_query(F.data == 'support')
async def process_support(callback_query: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад', callback_data='back_to_main_menu')
    await callback_query.message.edit_text(
        "👤 Служба поддержки StarFall: @starfall_support_bot\n⏳ Время работы: 08:00-22:00 (UTC +3)",
        reply_markup=builder.as_markup()
    )
    await callback_query.answer()

@router.callback_query(F.data == 'buy_for_self')
async def process_callback_buy_for_self(callback_query: CallbackQuery):
    await process_buy_options(callback_query, "себе")

@router.callback_query(F.data == 'gift')
async def process_gift(callback_query: CallbackQuery):
    user_states[callback_query.from_user.id] = "waiting_for_username"
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад', callback_data='back_to_main_menu')
    await callback_query.message.edit_text(
        "Введите имя пользователя человека, которому хотите подарить звезды\n"
        f"Например, @{callback_query.from_user.username}",
        reply_markup=builder.as_markup()
    )
    await callback_query.answer()

@router.callback_query(F.data == 'profile')
async def process_profile(callback_query: CallbackQuery):
    # Пример данных для профиля
    user_id = callback_query.from_user.id
    total_spent = 92.08  # Пример суммы покупок
    total_purchases = 1  # Пример количества покупок
    
    # Создание клавиатуры с кнопкой "Назад"
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад', callback_data='back_to_main_menu')
    
    # Изменение текста сообщения и клавиатуры
    await callback_query.message.edit_text(
        f"Профиль\n\n"
        f"ID: {user_id} \n\n"
        f"💸 Сумма покупок: {total_spent:.2f} RUB\n"
        f"🔢 Кол-во покупок: {total_purchases}",
        reply_markup=builder.as_markup()
    )
    await callback_query.answer()

@router.message(lambda message: user_states.get(message.from_user.id) == "waiting_for_username")
async def process_username_input(message: Message):
    username = message.text.strip()
    if not username.startswith("@"):
        await message.answer("Пожалуйста, введите корректный тег пользователя, начинающийся с '@'")
        return
    user_states[message.from_user.id] = {"recipient": username}
    await process_buy_options(message, username)

async def process_buy_options(query_or_message, recipient):
    builder = InlineKeyboardBuilder()
    for stars in STAR_PRICES:
        price = stars * STAR_PRICE
        builder.button(text=f'✨{stars} звезд - {price:.2f} ₽', callback_data=f'buy_{stars}')
    builder.row()
    builder.button(text='Или отправьте свое количество в чат', callback_data='custom_amount')
    builder.row()
    builder.button(text='Назад', callback_data='back_to_main_menu')
    builder.adjust(1, 1, 1, 1, 1, 1, 1)

    text = (
        f"⭐️ Telegram Stars\n"
        f"Для покупки звезд {recipient} выбери пакет или отправь своё количество мне в чат\n"
        f"Можно купить от 50 до 1,000,000 ⭐️ за раз\n"
        f"👉 Комиссия снижена в 2 раза при покупке от 250 звезд"
    )

    if isinstance(query_or_message, CallbackQuery):
        await query_or_message.message.edit_text(text, reply_markup=builder.as_markup())
        await query_or_message.answer()
    else:
        await query_or_message.answer(text, reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith('buy_'))
async def process_buy_package(callback_query: CallbackQuery):
    stars = int(callback_query.data.split('_')[1])
    price = stars * STAR_PRICE
    order_id = str(uuid.uuid4())
    builder = InlineKeyboardBuilder()
    builder.button(text='🔗 Перейти к оплате', callback_data=f'pay_{order_id}')
    builder.row()
    builder.button(text='❌ Отменить', callback_data='cancel_order')

    await callback_query.message.edit_text(
        f"✅ Заказ создан\n"
        f"Номер заказа: {order_id}\n"
        f"Способ оплаты: starfall\n"
        f"Сумма к оплате: {price:.2f}₽\n"
        f"Вы покупаете: {stars} telegram звезд\n"
        f"Получатель: вы",
        reply_markup=builder.as_markup()
    )
    await callback_query.answer()

if __name__ == '__main__':
    from aiogram import Dispatcher
    dp = Dispatcher()
    dp.include_router(router)
    dp.run_polling(bot)