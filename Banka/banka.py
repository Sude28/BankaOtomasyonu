#SudeTelli21360859017

import json 
class Account:
    def __init__(self,account_type,account_name,balance):
        self._account_type = account_type
        self._account_name = account_name
        self._balance = balance
        
    @property
    def account_type(self):
        return self._account_type
    
    @account_type.setter
    def account_type(self, account_type):
        if account_type not in ["SavingAccount", "NormalAccount"]:
            raise ValueError("Hesap türü yalnızca SavingAccount veya NormalAccount olabilir.")
        self._account_type = account_type

    
    @property
    def account_name(self):
        return self._account_name
    
    @property
    def balance(self):
        return self._balance
     
    @balance.setter
    def balance(self,new_balance):
        if new_balance < 0:
            raise ValueError("Hesap bakiyesi negatif olamaz.")
        self._balance = new_balance
        
   
     
class SavingAccount(Account):
    def __init__(self,account_type,account_name,balance):
        super().__init__("SavingAccount",account_name,balance)

    def close_account(self):
        deduction = self._balance * 0.10
        self._balance -= deduction
        print(f"{self.account_name} adlı hesap kapatıldı. Elde edilen para miktarı: {deduction} TL")
        
class NormalAccount(Account):
    def __init__(self,account_type, account_name, balance):
        super().__init__("NormalAccount", account_name, balance)
    def close_account(self):
        print(f"{self.account_name} adlı hesap kapatıldı. Elde edilen para miktarı: {self.balance} TL")      
        
        
class Transaction:
    def __init__(self, account, amount):
        self.account = account
        self.amount = amount
     
    @staticmethod
    def paraDondur(func):
        def wrapper(self,miktar):
            return func(self,miktar)
        return wrapper
    
    @paraDondur
    def paraCek(self,miktar):
        return -1*miktar
                   
    @paraDondur
    def paraEkle(self,miktar):
        return miktar
    
    def paraGuncelle(self,islem_metodu,miktar):
        self.account._balance +=  islem_metodu(miktar)   
               
               
def close_account(accounts, account_name):
    for account in accounts:
        if account.account_name == account_name:
            print(f"{account_name} adlı hesap kapatıldı. Elde edilen para miktarı: {account.balance} TL")
            accounts.remove(account)  
            break
        else:
            print(f"{account_name} adlı hesap bulunamadı.")
            
def hesapAc(account_type,account_name,balance):
    if account_type not in ["SavingAccount", "NormalAccount"]:
       raise ValueError("Hesap türü yalnızca SavingAccount veya NormalAccount olabilir.")
   
    if balance < 0:
       raise ValueError("Hesap bakiyesi negatif olamaz.")
   
    if account_type == "SavingAccount":
        hesap = SavingAccount(account_type,account_name, balance)
    else:
        hesap = NormalAccount(account_type,account_name, balance)
    return hesap


def save_account(accounts):
    with open("accounts.json", "w") as file:
        account_data = []
        for account in accounts:
            account_data.append({
                "type": account.account_type,
                "name": account.account_name,
                "balance": account.balance
            })
        json.dump(account_data, file)

def load_account():
    with open("accounts.json", "r") as file:
        account_data = json.load(file)
        accounts = []
        for data in account_data:
            if data["type"] == "SavingAccount":
                account = SavingAccount(data["type"], data["name"], data["balance"])
            else:
                account = NormalAccount(data["type"], data["name"], data["balance"])
            accounts.append(account)
        return accounts

def main():
    accounts = []
    while True:
        print("\n>>>>>>İŞLEM MENÜSÜ<<<<<<")
        print("1. Hesap oluştur")
        print("2. Hesap kapat")
        print("3. Kaydet ve Yükle")
        print("4. Para Çekme")
        print("5. Para Yatırma")
        print("6. Hesapları Göster")
        print("0. Çıkış")
        
        secim = input("Yapmak istediğiniz işlemi seçiniz: ")
        
        if secim=="1":
            account_type = input("Hesap türünü seçin (SavingAccount/NormalAccount): ")
            account_name = input("Hesap adını girin: ")
            balance = float(input("Başlangıç bakiyesini girin: "))
            
            try:
                hesap = hesapAc(account_type, account_name, balance)
                accounts.append(hesap)
                print("Hesap oluşturuldu.")

            except ValueError as e:
                print(f"Hesap oluşturulamadı: {str(e)}")
                
        elif secim =="2":
            account_name = input("Kapatmak istediğiniz hesabın adını girin: ")
            close_account(accounts,account_name)
            
        elif secim == "3":    
            save_account(accounts)
            print("Hesaplar kaydedildi.")
            accounts = load_account()
            print("Hesaplar yüklendi.")
            
        elif secim == "4":
            input_str = input("Örnek>> HesapAdi : Miktar giriniz: ")
            try:
                account_name, amount_str = input_str.split(":")
                account_name = account_name.strip()
                amount = float(amount_str.strip())
        
                for account in accounts:
                    if account.account_name == account_name:
                        transaction = Transaction(account, amount)
                        transaction.paraGuncelle(transaction.paraCek, amount)
                        print(f"{account_name} adlı hesaptan {amount} TL çekildi.")
                        break
                else:
                    print(f"{account_name} adlı hesap bulunamadı.")
            except ValueError:
                print("Geçersiz giriş formatı. Lütfen tekrar deneyin.") 
                
        elif secim == "5": 
            input_str = input("Örnek>> HesapAdi : Miktar giriniz: ")
            try:
                account_name, amount_str = input_str.split(":")
                account_name = account_name.strip()
                amount = float(amount_str.strip())
        
                for account in accounts:
                    if account.account_name == account_name:
                        transaction = Transaction(account, amount)
                        transaction.paraGuncelle(transaction.paraEkle, amount)
                        print(f"{amount} TL, {account_name} adlı hesaba yatırıldı.")
                        break
                else:
                    print(f"{account_name} adlı hesap bulunamadı.")  
            except ValueError:
                print("Geçersiz giriş formatı. Lütfen tekrar deneyin.")   
                
        elif secim == "6":    
            for account in accounts:  
                print(f"{account.account_type} - {account.account_name} - Bakiye: {account.balance} TL")  
                
        elif secim == "0":
            print("Programdan çıkılıyor.")
            break

        else:
            print("Geçersiz bir seçenek girdiniz. Lütfen tekrar deneyin.")

main()