def func1():
    print("Hello from func1")

x = 10

def get_x():
    return x

def set_x(value):

    x = value
    print("new value", x)

def set_g(value):
    global x 
    x = value

def get_x(addon=0):
    return(x + 
           addon)


def show(x:int=1,y:int=2,w:int=3)->None:
    '''Документуючий коментар : відсутність перевантаження компенсується 
        можливістю значень за замовчуванням та зверненням до них за іменем
        на кшталт show(y=5)'''
    print(x,y,w)


def fact(n:int)->int:
    return 1 if n<2 else n*fact(n-1)

def main():
    func1()
    print(get_x())
    set_x(20)
    print(get_x())
    set_g(30)
    print(get_x(1))
    show()
    show(6)
    show(y=7)
    show(8,w="A")

    print(fact(5))

if __name__ == '__main__':
    main()
