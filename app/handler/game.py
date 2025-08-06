from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from app.state.status import Status
from app.keyboard.keyboard import ResCallbackFab, inline_keyboard_gen, keyboard_gen

router = Router()


@router.message(Status.game_state)
async def game(message: Message, state: FSMContext):
    await message.answer(f"#{(await state.get_data())['count']+1} {(await state.get_data())['quizes'][(await state.get_data())['count']]['question']}:", reply_markup=inline_keyboard_gen((await state.get_data())['quizes'][(await state.get_data())['count']]['options']))


@router.callback_query(ResCallbackFab.filter())
async def callback_res(callback: CallbackQuery, callback_data: ResCallbackFab, state: FSMContext):
    if callback_data.action == (await state.get_data())['quizes'][(await state.get_data())['count']]['correct_answer']:
        await state.update_data(score=int((await state.get_data())['score'])+1)
        await callback.message.answer("✅ Correct!", reply_markup=ReplyKeyboardRemove())
    else:
        await callback.message.answer(f"❌ Wrong! | Correct answer: {(await state.get_data())['quizes'][(await state.get_data())['count']]['correct_answer']}", reply_markup=ReplyKeyboardRemove())
    await callback.answer()

    if (await state.get_data())['num_quiz']-1 > (await state.get_data())['count']:
        await state.update_data(count=int((await state.get_data())['count'])+1)
        await game(message=callback.message, state=state)
    else:
        await final_game(message=callback.message, state=state)


async def final_game(message: Message, state: FSMContext):
    await message.answer(f"Congratulations!\nYou have completed the game with {int(int((await state.get_data())['score'])/int((await state.get_data())['num_quiz'])*100)}% ", reply_markup=ReplyKeyboardRemove())
    await message.answer("Do you want to play again?", reply_markup=keyboard_gen(["Play", "Stop"]))
    await state.clear()


@router.message(F.text == "Stop")
async def finish(message: Message, state: FSMContext):
    await message.answer("Ok, see next time!", reply_markup=ReplyKeyboardRemove())
