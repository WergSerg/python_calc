
def Welcom():
    string='Калькулятор'
    print (string)
    len_string = int(len(string))
    print('|'*len_string)
     
    return len_string
    
def Calculator():
    print(" "*10)
    operator = input ("введите оператор ")
    print(" "*10)
    namber_1 = int(input("превое число: "))
    print(" "*10)
    namber_2 = int(input("второе число: "))
    
    if operator =='+':
        print ('{}+{}='.format(namber_1,namber_2),namber_1+namber_2 )
    elif operator =='-':
        print ('{}-{}='.format(namber_1,namber_2),namber_1-namber_2 )
    elif operator =='*':
        print ('{}*{}='.format(namber_1,namber_2),namber_1*namber_2 )
    elif operator =='/':
        print ('{}/{}='.format(namber_1,namber_2),namber_1/namber_2 )
    else:
        print("нет такого оператора")
        Continued()
    Continued()


def Continued():
    
    string_2='хотите продолжить?'
    string_3='введите да или нет'
    print(" "*10)
    print(string_2)
    print(string_3)

    count=input()
    if count=='да':
        Calculator()
    elif count=='нет':
        print("прощай")
    else:
        print("неверно")
        Continued() 
    input()

Welcom()       
Calculator()


input()

