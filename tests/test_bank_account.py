import os
import unittest
from unittest.mock import patch
from src.bank_account import BankAccount
from src.exceptions import WithdrawalTimeRestrictionError


class BankAccountTests(unittest.TestCase):
    
    # Se ejecuta, siempre, ANTES DE CADA PRUEBA
    def setUp(self) -> None: 
        self.account = BankAccount(1000, log_file="transaction_log.txt")
    
    
    # Se ejecuta, siempre, DESPUÉS DE CADA PRUEBA
    def tearDown(self) -> None:
        # Eliminar el archivo de log después de cada prueba
        if os.path.exists(self.account.log_file):
            os.remove(self.account.log_file)
    

    def _count_lines(self, file_path):
        # Abre el archivo de log y cuenta las líneas
        with open(file_path, 'r') as file:
            return len(file.readlines())
        
        
    def test_deposit(self):
        new_balance = self.account.deposit(500)
        self.assertEqual(new_balance, 1500, "El balance no es igual") # El tercer parámetro es el mensaje de fallo

    @patch("src.bank_account.datetime")
    def test_withdraw(self,mock_datetime):
        mock_datetime.now.return_value.hour = 8  # Ahora el método now devuelve 8
        new_balance = self.account.withdraw(200)
        self.assertEqual(new_balance, 800, "El balance no es igual")
    
    
    def test_get_balance(self):
        self.assertEqual(self.account.get_balance(), 1000)
    
        
    def test_transfer(self):
        self.account.transfer(1700)
        self.assertEqual(self.account.get_balance(), 1000) # El balance se mantiene tras transferencia no realizada.


    def test_transaction_log(self): # Existencia del archivo log
        # Verifica que el archivo de log existe
        self.assertTrue(os.path.exists(self.account.log_file))
        
        # Escribe "Prueba de Archivo existente" en el archivo de log
        self.account._log_transaction("Prueba de Archivo existente")
        
        # Verifica que la línea "Prueba de Archivo existente" fue escrita en el log
        with open(self.account.log_file, 'r') as log_file:
            log_content = log_file.read()
            assert "Prueba de Archivo existente" in log_content


    def test_count_transactions(self):
        # Inicialmente debe haber 1 línea en el archivo de log (por la creación de la cuenta)
        assert self._count_lines(self.account.log_file) == 1
        
        # Después de hacer un depósito, debe haber 2 líneas
        self.account.deposit(500)
        assert self._count_lines(self.account.log_file) == 2
        
    @patch("src.bank_account.datetime")  # Mockea el módulo datetime en el archivo src.bank_account para las pruebas
    def test_withdraw_during_bussines_hours(self, mock_datetime):  # Define una prueba para retiros dentro del horario permitido
        # Configura el mock para que la hora actual simulada sea las 8 AM, dentro del horario de oficina
        mock_datetime.now.return_value.hour = 8  # Ahora el método now devuelve 8
        # Llama al método withdraw para realizar un retiro de 100 unidades
        new_balance = self.account.withdraw(100)  # RETIRO
        # Verifica que el nuevo saldo sea 900, después del retiro (asumiendo un saldo inicial de 1000)
        self.assertEqual(new_balance, 900)  

    @patch("src.bank_account.datetime")  # Mockea nuevamente el módulo datetime para esta prueba específica
    def test_withdraw_disallow_before_bussines_hours(self, mock_datetime):  # Define una prueba para retiros antes del horario de oficina
        # Configura el mock para que la hora actual simulada sea las 7 AM, fuera del horario permitido
        mock_datetime.now.return_value.hour = 20  # Ahora el método now devuelve 7
        # Verifica que al intentar retirar fuera del horario permitido se lanza la excepción WithdrawalTimeRestrictionError
        with self.assertRaises(WithdrawalTimeRestrictionError):  # SI se da una excepción pasa la prueba con OK
            self.account.withdraw(100)  # Intenta realizar un retiro de 100 unidades

    @patch("src.bank_account.datetime")  # Mockea el módulo datetime para la última prueba
    def test_withdraw_disallow_after_bussines_hours(self, mock_datetime):  # Define una prueba para retiros después del horario de oficina
        # Configura el mock para que la hora actual simulada sea las 6 PM (18 horas), fuera del horario permitido
        mock_datetime.now.return_value.hour = 20  # Ahora el método now devuelve 18
        # Verifica que se lanza la excepción WithdrawalTimeRestrictionError al intentar retirar después del horario permitido
        with self.assertRaises(WithdrawalTimeRestrictionError): # Entra en un contexto donde espera una excepción específic
            # Si la excepción esperada (WithdrawalTimeRestrictionError) ocurre dentro del bloque with, 
            # entonces el contexto gestionado por self.assertRaises la captura, y la prueba pasa satisfactoriamente.            
            self.account.withdraw(100)  # Intenta realizar un retiro de 100 unidades
    
    '''
    El método assertRaises de unittest se utiliza para verificar que, en un bloque de código determinado, 
    se lance una excepción específica. Si la excepción ocurre como se espera, la prueba se considera exitosa y se marca como OK. 
    En cambio, si la excepción no ocurre, la prueba fallará.
    '''
    
    def test_deposit_multiple_ammounts(self):
        test_cases = [
            {"ammount": 100, "expected": 1100},
            {"ammount": 3000, "expected": 4100},
            {"ammount": 4500, "expected": 8600},
        ]
        for case in test_cases:
            with self.subTest(case=case):  # Se etiqueta el subTest con cada caso
                new_balance = self.account.deposit(case["ammount"])
                self.assertEqual(new_balance, case["expected"])

    def test_deposit_multiple_ammounts_and_accounts(self):
        test_cases = [
            {"ammount": 100, "expected": 1100},
            {"ammount": 3000, "expected": 4000},
            {"ammount": 4500, "expected": 5500},
        ]
        for case in test_cases:
            with self.subTest(case=case):  # Se etiqueta el subTest con cada caso
                self.account = BankAccount(balance=1000, log_file="Depósitos")
                new_balance = self.account.deposit(case["ammount"])
                self.assertEqual(new_balance, case["expected"])

                    
        