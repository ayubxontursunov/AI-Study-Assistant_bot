from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from app.db import get_user,save_user
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

# from run import bot
from app.language import language_data
from aiogram import Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext



class Registration(StatesGroup):
    choosing_language = State()
    choosing_name = State()


LANGUAGES = {
    "Русский 🇷🇺 ": "Русский",
    "English 🇺🇸 ": "English",
}
router = Router()
@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):

    user_data = get_user(message.from_user.id)
    if user_data:
        user_name = user_data["name"]
        language = user_data["language"]

        await message.answer(
            f"{language_data[language]['Response'][4]} {user_name}! {language_data[language]['Response'][5]}\n\n"
            f"{language_data[language]['Response'][6]}"

        )
        return

    await message.answer(
        "Здравствуйте! Чтобы пользоваться нашим ботом, вам необходимо пройти регистрацию."
        "\n\nДля начала, пожалуйста, выберите язык обслуживания.\n\n"
        "_______________________\n\n"
        "Hello! To use our bot, you need to register first."
        "\n\nPlease start by choosing your preferred language.",
        reply_markup=ReplyKeyboardRemove()
    )

    keyboard_builder = InlineKeyboardBuilder()
    for lang_name, lang_code in LANGUAGES.items():
        keyboard_builder.button(text=lang_name, callback_data=lang_code)
    keyboard_builder.adjust(1)

    await message.answer(
        "Выберите ваш язык | Choose language:",
        reply_markup=keyboard_builder.as_markup()
    )
    await state.set_state(Registration.choosing_language)


@router.callback_query(Registration.choosing_language, F.data.in_(LANGUAGES.values()))
async def change_language(callback_query: CallbackQuery, state: FSMContext):
    selected_lang = callback_query.data
    await state.update_data(language=selected_lang)

    # Only one of these is needed
    # await callback_query.message.edit_reply_markup(reply_markup=None)

    await callback_query.message.answer(language_data[selected_lang]["Response"][0])
    await state.set_state(Registration.choosing_name)


@router.message(Registration.choosing_name)
async def get_name(message: Message, state: FSMContext):
    user_name = message.text.strip()

    await state.update_data(name=user_name)
    data = await state.get_data()
    language = data.get("language")
    name =data.get("name")
    save_user(message.from_user.id, name, language)

    await state.clear()

    await message.answer(
        f"{language_data[language]['Response'][1]} {name}! {language_data[language]['Response'][2]}\n"
        f"{language_data[language]['Response'][3]} {language}"
    )
    await message.answer(
        f"{language_data[language]['Response'][4]} {name}! {language_data[language]['Response'][5]}\n\n"
        f"{language_data[language]['Response'][6]}"

    )


@router.message(Command("help"))
async def help_handler(message: Message):
    user_data = get_user(message.from_user.id)
    # print(message.from_user.id)
    if user_data:
        user_name = user_data["name"]
        language = user_data["language"]
        help_text = language_data[language]["help_text"]


    else: help_text = (
            "👋 **Welcome to the AI Study Assistant Bot!**\n\n"
            "I can help you with explaining various topics. Here are the commands you can use:\n\n"
    
            "/start - Begin or restart the registration process. If you're already registered, I will greet you and let you ask any topic you'd like explained.\n\n"
    
            "/help - This command. It gives you information on how to use the bot and the available commands.\n\n"
    
            "/edituser – Update your user information.\n\n"
    
            "After registration, you can ask me about any topic you'd like to learn or need explained. Simply ask your question, and I'll give you a detailed explanation!"
        )
    await message.answer(help_text,parse_mode="Markdown")

@router.message(Command("edituser"))
async def edit_handler(message: Message,state: FSMContext):
    user = get_user(message.from_user.id)
    name = user['name']
    language = user['language']

    if not user:
        await message.answer("❗ Пожалуйста, начните с /start.\n❗ Please start with /start.")
        return

    keyboard_builder = InlineKeyboardBuilder()
    for lang_name, lang_code in LANGUAGES.items():
        keyboard_builder.button(text=lang_name, callback_data=lang_code)
    keyboard_builder.adjust(1)

    await message.answer(
        "Выберите ваш язык | Choose language:",
        reply_markup=keyboard_builder.as_markup()
    )
    await state.set_state(Registration.choosing_language)




@router.message()
async def echo_handler(message: Message):
    if message.text.startswith("/"):
        return
    user = get_user(message.from_user.id)
    name = user['name']
    language = user['language']

    if not user:
        await message.answer("❗ Пожалуйста, начните с /start.\n❗ Please start with /start.")
        return

    # User is registered — treat input as a topic
    topic = message.text.strip()
    if not topic:
        await message.answer(language_data[language]["Response"][7])
        return



    await message.answer(language_data[language]["Response"][8])

    try:
        from tutor import explanation_agent, Runner, Explanation
        result = await Runner.run(explanation_agent, topic)
        explanation: Explanation = result.final_output

        response = f"📌 *{explanation.topic}*\n\n"
        response += f"{language_data[language]['ai_response'][0]}\n{explanation.explanation}\n\n"

        if explanation.key_formulas:
            response += f"{language_data[language]['ai_response'][1]}\n" + "\n".join(f"- {f}" for f in explanation.key_formulas) + "\n\n"
        if explanation.examples:
            response += f"{language_data[language]['ai_response'][2]}\n" + "\n".join(f"- {e}" for e in explanation.examples) + "\n\n"
        if explanation.resources:
            response += f"{language_data[language]['ai_response'][3]}\n" + "\n".join(f"- {r}" for r in explanation.resources)

        await message.answer(response, parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"{language_data[language]['ai_response'][4]} {str(e)}")

