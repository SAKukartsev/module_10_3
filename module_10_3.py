import threading
from random import randint
from time import sleep


class Bank:
    lock = threading.Lock()

    def __init__(self, balance):
        super().__init__()
        self.balance = balance

    def deposit(self):
        for i in range(10):
            sleep(0.001)
            rand_deposit = randint(50, 500)
            self.balance += rand_deposit
            print(f'Пополнение: {rand_deposit}. Баланс: {self.balance} {self.lock.locked()}')
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()

    def take(self):
        for i in range(10):
            sleep(0.001)
            rand_take = randint(50, 500)
            print(f'Запрос на {rand_take} {self.lock.locked()}')
            if rand_take <= self.balance:
                self.balance -= rand_take
                print(f'Снятие: {rand_take}. Баланс: {self.balance} {self.lock.locked()}')
            else:
                self.lock.acquire()
                print(f'Запрос отклонён, недостаточно средств {self.lock.locked()}')


bk = Bank(0)

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
