from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from app.keyboard.keyboard import keyboard_gen
from app.state.status import Status
from app.handler.game import game
from app.source import dataset
from random import randint

options = ["5", "10", "15", "20"]
router = Router()


@router.message(Command(commands=["start"]))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Hello this is Mini Quiz\nIf you would like to play please click Play button", reply_markup=keyboard_gen(["Play"]))


@router.message(F.text.lower() == "play")
async def play(message: Message, state: FSMContext):
    await message.answer("Please choose number of quiz to play:",
                         reply_markup=keyboard_gen(options))
    await state.set_state(Status.set_number_of_quiz)


@router.message(Status.set_number_of_quiz, F.text.in_(options))
async def set_number_of_quiz(message: Message, state: FSMContext):
    quizes = [dataset.copy().pop(randint(0, len(dataset.copy()) - 1)) for _ in range(int(message.text))]
    await state.update_data(quizes=quizes)
    await state.update_data(num_quiz=int(message.text))
    await state.update_data(count=0)
    await state.update_data(score=0)
    await message.answer(text="Wonderful, let's start ...", reply_markup=ReplyKeyboardRemove())
    await game(message=message, state=state)


@router.message(Command(commands=["cancel"]))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Canceled!", reply_markup=ReplyKeyboardRemove())
