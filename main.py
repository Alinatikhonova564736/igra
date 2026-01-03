import random
import time

class Move: #Класс ход
    ROCK = "камень"
    SCISSORS = "ножницы"
    PAPER = "бумага"

    ALL_MOVES = [ROCK, SCISSORS, PAPER]

    BEATS = {     # Кто что бьет
        ROCK: SCISSORS,
        SCISSORS: PAPER,
        PAPER: ROCK
    }

class Player: #Класс игрок

    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, points=1): #Добавляем очки игрокам
        self.score += points

    def reset(self): #Сброс статистики игрокам
        self.score = 0

class ComputerPlayer(Player): #Класс игрок - компьютер

    def __init__(self, name="Компьютер"):
        super().__init__(name)

    def make_move(self): # Делаем случайный ход
        return random.choice(Move.ALL_MOVES)


class Game: #Класс самой игры

    def __init__(self):
        self.human = Player("Игрок")
        self.computer = ComputerPlayer()
        self.rounds_played = 0
        self.max_rounds = None

    def determine_winner(self, human_move, computer_move): #Определяем кто победил
        if human_move == computer_move:
            return "draw"

        if Move.BEATS[human_move] == computer_move:
            return "win"
        else:
            return "lose"

    def play_round(self, human_move): #Игра в 1 РАУНД
        if human_move not in Move.ALL_MOVES:
            return None, None, "invalid"

        computer_move = self.computer.make_move()
        result = self.determine_winner(human_move, computer_move)

        # Обновляем счет
        if result == "win":
            self.human.add_score()
        elif result == "lose":
            self.computer.add_score()

        self.rounds_played += 1

        return computer_move, result, "success"

    def get_round_result_text(self, human_move, computer_move, result): # Результат раунда
        texts = {
            "win": f" {human_move.upper()} бьет {computer_move} - Вы победили!",
            "lose": f" {computer_move.upper()} бьет {human_move} - Вы проиграли!",
            "draw": f" Оба выбрали {human_move} - Ничья!",
            "invalid": " Неверный ход! Выберите камень, ножницы или бумагу."
        }
        return texts.get(result, "")

    def show_help(self): #Cправка по игре
        print("\n" + "=" * 50)
        print("ПРАВИЛА ИГРЫ 'КАМЕНЬ-НОЖНИЦЫ-БУМАГА':")
        print("=" * 50)
        print(" Камень бьет ножницы")
        print(" Ножницы бьют бумагу")
        print(" Бумага бьет камень")
        print(" Если оба игрока выбрали одинаковый ход - ничья")
        print("\nКОМАНДЫ:")
        print(" камень, ножницы, бумага - сделать ход")
        print(" помощь - показать эту справку")
        print(" сброс - начать игру заново")
        print(" выход - закончить игру")
        print("=" * 50)

    def reset_game(self): #Сброс игры
        self.human.reset()
        self.computer.reset()
        self.rounds_played = 0
        print("\n✓ Игра сброшена! Начинаем заново!")

    def play(self): # Основной игровой цикл
        print("=" * 50)
        print("ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'КАМЕНЬ-НОЖНИЦЫ-БУМАГА'!")
        print("=" * 50)
        print("Введите 'помощь' для просмотра команд")

        while True:
            print(f"\nРаунд {self.rounds_played + 1}")
            print(f"Счет: {self.human.name} {self.human.score} : {self.computer.score} {self.computer.name}")

            command = input("\nВаш ход (или команда): ").lower().strip()

            if command == "выход":
                print(f"\nИгра окончена! Финальный счет: {self.human.score} : {self.computer.score}")
                print("Спасибо за игру!")
                break

            elif command == "помощь":
                self.show_help()

            elif command == "сброс":
                self.reset_game()

            elif command in Move.ALL_MOVES:
                print(f"\nВы выбрали: {command.upper()}")

                # Добавляем небольшую задержку
                print("Компьютер думает", end="")
                for _ in range(3):
                    time.sleep(0.3)
                    print(".", end="", flush=True)
                print()

                computer_move, result, status = self.play_round(command)

                if status == "success":
                    result_text = self.get_round_result_text(command, computer_move, result)
                    print(result_text)

                    # Проверяем, не достигли ли мы максимума раундов
                    if self.max_rounds and self.rounds_played >= self.max_rounds:
                        print(f"\n✧ Игра завершена! Достигнут лимит в {self.max_rounds} раундов! ✧")
                        print(f"Финальный счет: {self.human.score} : {self.computer.score}")

                        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
                        if play_again == "да":
                            self.reset_game()
                        else:
                            print("\nСпасибо за игру!")
                            break
                else:
                    print(" Ошибка: неверный ход!")

            else:
                print(" Неизвестная команда. Введите 'помощь' для просмотра доступных команд")


class TournamentGame(Game): #Класс для турнирной игры


    def __init__(self, rounds=5):
        super().__init__()
        self.max_rounds = rounds
        self.target_score = (rounds // 2) + 1

    def play(self): #Игра с фиксированным количеством раундов
        print("=" * 50)
        print(f"ТУРНИР ДО {self.max_rounds} РАУНДОВ!")
        print(f"Для победы нужно набрать {self.target_score} очков!")
        print("=" * 50)

        while self.rounds_played < self.max_rounds:
            print(f"\nРаунд {self.rounds_played + 1} из {self.max_rounds}")
            print(f"Счет: {self.human.name} {self.human.score} : {self.computer.score} {self.computer.name}")

            # Проверяем, не достиг ли кто-то целевого счета
            if self.human.score >= self.target_score:
                print(f"\n✧✧✧ ВЫ ВЫИГРАЛИ ТУРНИР! ✧✧✧")
                print(f"Финальный счет: {self.human.score} : {self.computer.score}")
                break
            elif self.computer.score >= self.target_score:
                print(f"\n✧✧✧ КОМПЬЮТЕР ВЫИГРАЛ ТУРНИР! ✧✧✧")
                print(f"Финальный счет: {self.human.score} : {self.computer.score}")
                break

            command = input("\nВаш ход (или команда): ").lower().strip()

            if command == "сброс":
                self.reset_game()
                print(f"Турнир до {self.max_rounds} раундов начат заново!")
            elif command == "выход":
                print("\nТурнир прерван!")
                print(f"Текущий счет: {self.human.score} : {self.computer.score}")
                break
            elif command in Move.ALL_MOVES:
                print(f"\nВы выбрали: {command.upper()}")

                computer_move, result, status = self.play_round(command)

                if status == "success":
                    result_text = self.get_round_result_text(command, computer_move, result)
                    print(result_text)

                    # Если сыграли все раунды
                    if self.rounds_played >= self.max_rounds:
                        print(f"\n{'=' * 50}")
                        print("ТУРНИР ЗАВЕРШЕН!")
                        print(f"Финальный счет: {self.human.score} : {self.computer.score}")

                        if self.human.score > self.computer.score:
                            print("✧✧✧ ПОБЕДА ЗА ВАМИ! ✧✧✧")
                        elif self.human.score < self.computer.score:
                            print("✧✧✧ ПОБЕДА ЗА КОМПЬЮТЕРОМ! ✧✧✧")
                        else:
                            print("✧✧✧ НИЧЬЯ! ✧✧✧")

                        play_again = input("\nХотите сыграть еще турнир? (да/нет): ").lower()
                        if play_again == "да":
                            self.reset_game()
                            print(f"\nНовый турнир до {self.max_rounds} раундов!")
                        else:
                            print("\nСпасибо за игру!")
                            break
            else:
                print(" Неизвестная команда. Введите камень, ножницы или бумагу")


def main(): #Главная функция
    print("=" * 50)
    print(" ВЫБЕРИТЕ РЕЖИМ ИГРЫ:")
    print("=" * 50)
    print("1. Бесконечная игра")
    print("2. Турнир (5 раундов)")
    print("3. Турнир (10 раундов)")
    print("=" * 50)

    choice = input("Ваш выбор (1-3): ").strip()

    if choice == "1":
        game = Game()
        game.play()
    elif choice == "2":
        game = TournamentGame(5)
        game.play()
    elif choice == "3":
        game = TournamentGame(10)
        game.play()
    else:
        print("Неверный выбор. Запускаю бесконечную игру...")
        game = Game()
        game.play()


if __name__ == "__main__":
    main()
