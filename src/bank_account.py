from datetime import datetime
from src.exceptions import InsufficientFundsError, WithdrawalTimeRestrictionError


class BankAccount:
    '''
    self.account = BankAccount(1000, log_file="transaction_log.txt")

    '''
    def __init__(self, balance=0, log_file=None):
        self.balance = balance
        self.log_file = log_file
        self._log_transaction("Cuenta creada")
        
        
    def _log_transaction(self,message):
        if self.log_file: # Si se cuenta con un log_file, entonces:
            with open(self.log_file,"a") as f: # Abre el archivo en modo append
                f.write(f"{message}\n") # Agregamos el message + salto de línea
            
            
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._log_transaction(f'Deposited {amount}. New balance: {self.balance}')
        return self.balance


    def withdraw(self, amount): # (RETIROS) (8AM-5PM)
        now = datetime.now()
        if now.hour < 8 or now.hour > 17: # Fuera de Horario
            raise WithdrawalTimeRestrictionError("Withdrawals are only allowed from 8am to 5pm")

        if amount > self.balance:
            raise InsufficientFundsError(
                f"Withdrawal of {amount} exceeds balance {self.balance}"
            )
        if amount > 0:
            self.balance -= amount
            self._log_transaction(f"Withdrew {amount}. New balance: {self.balance}")
        return self.balance


    def get_balance(self):
        self._log_transaction(f"Checked balance. Current balance {self.balance}.")
        return self.balance
    
    
    def transfer(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self._log_transaction(f"Transfered {amount}. New balance: {self.balance}.")

        else:
            self._log_transaction(f"Not transfered {amount}. Insufficient founds: {self.balance}")
            
        return self.balance