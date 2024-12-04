#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 19 16:37:47 2024

@author: duartemateus
"""

"""
conta_li = Conta("li","1234")
conta_li.levantar(10)
conta_li.definir_pin("123aA#")
conta_li.depositar(-10)
conta_li.depositar(10)
conta_li.levantar(-5)
conta_li.levantar(5)
conta_li.consulta()
conta_li.historico()
"""

class Conta():
    
    i = 1
    
   
    
    def __init__(self,nome,NIF):
        self.nome = nome
        self.nif = NIF
        self._pin = ""
        self._saldo = 0
        self.numero_da_conta = Conta.i
        Conta.i+= 1
        self.historico_de_operacoes = []
        self.j = 1
    
    def levantar(self,valor,check=True):
        if check:
            if self._pin == "":
                print("Palavra passe nao definida.")
            elif valor <= 0:
                print("Levantamento invalido.")
            elif self._saldo >= valor:    
                self._saldo -= valor
                self.historico_de_operacoes += [f"Operacao numero:  {self.j} Valor:  -{valor}"]
                self.j += 1
            else:
                print("Saldo insuficiente em conta.")
        else:  
            self._saldo -= valor
            self.historico_de_operacoes += [f"Operacao numero:  {self.j} Valor:  -{valor}"]
            self.j += 1
    
    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            self.historico_de_operacoes += [f"Operacao numero:  {self.j} Valor:  {valor}"]
            self.j += 1
        else:
            print("Deposito invalido.")
    
    def historico(self): # nao existe atributo???
        for item in self.historico_de_operacoes:
            print(item)
        print(f'Saldo atual: {self._saldo}')
    
    def consulta(self):
        return self._saldo
    
    def definir_pin(self,PIN): #não imprime todas ao mesmo tempo????
        valido = True
        if len(PIN) < 6:
            print("Palavra passe precisa ter tamanho minimo de 6.")
            valido = False
        if len(PIN) > 8:
            print("Palavra passe nao pode ter tamanho superior a 8.")
            valido = False
        if PIN.lower() == PIN:
            print("Palavra passe precisa conter uma letra maiuscula.")
            valido = False
        if PIN.upper() == PIN:
            print("Palavra passe precisa conter uma letra minuscula.")
            valido = False
        if '$' not in PIN and '@' not in PIN and '#' not in PIN and '%' not in PIN and '!' not in PIN and '*' not in PIN:
            print("Palavra passe precisa conter pelo menos um caratere especial [\'$\', \'@\', \'#\', \'%\', \'!\', \'*\'] .")
            valido = False
        if valido:
            self._pin = PIN
    
    def acesso(self,PIN):
        if PIN == self._pin:
            return True
        else:
            return False

class EBank: 
    def __init__(self,nome):
        self.nome = nome
        self._contas = {}
        self._pendentes = []
    
    def abrir_conta(self,nome,NIF):
        conta = Conta(nome,NIF)
        self._contas[conta.numero_da_conta] = conta
        return conta
        
    def aceder_conta(self,numero,PIN):
        if numero not in self._contas:
            print("Numero de conta invalido.")
        elif self._contas[numero].acesso(""):
            print("Palavra passe nao definida.")
        elif not self._contas[numero].acesso(PIN):
            print("Palavra passe invalida.")
        else:
            return self._contas[numero]
    
    def numero_de_contas_ativas(self):
        return len(self._contas)
           
    def encerrar_conta(self, numero, PIN):
        if numero not in self._contas:
            print("Numero de conta invalido.")
        elif self._contas[numero].acesso(""):
            print("Palavra passe nao definida.")
        elif not self._contas[numero].acesso(PIN):
            print("Palavra passe invalida.")
        else:
            self._contas.pop(numero)
    
    def transferencia(self,origem,destino,valor,inst):
        if origem not in self._contas or destino not in self._contas or valor<= 0 :
            print("Transferencia invalida.")
        elif inst and self._contas[origem].consulta() >= valor:
            self._contas[origem].levantar(valor)
            self._contas[destino].depositar(valor)
        elif inst and self._contas[origem].consulta() < valor:
            print("Transferencia invalida.")
        else:
            self._pendentes += [(origem,destino,valor)]
    
    def processamento(self):
        for item in self._pendentes:
            origem,destino,valor=item
            if origem not in self._contas or destino not in self._contas or valor<= 0 :
                print("Transferencia invalida.")
            else:
               self._contas[origem].levantar(valor,False)
               self._contas[destino].depositar(valor)
        self._pendentes = []
            
                