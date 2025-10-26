from functools import reduce


lam1=lambda:print("I am lambda")
x=10
lam2 = None
lam3 = None
lam4 = None
lam5=None

def apply(func, args):
    return func(args)

def make_lam2()->None:
    global lam2
    lam2=lambda:print("x=",x)

def make_lam3()->None:
    global lam3
    x=20
    lam3=lambda:print("x=",x)

def make_lam4()->None:
    global lam4
    x=40
    lam4=lambda:print("x=",x)
    lam4()
    x=50


strategies = {
    "arithmetic": lambda d: reduce(lambda acc,b: acc+b, d, 0)/len(d),
    "geometric": lambda d: reduce(lambda a,b: a*b, d, 1.0) ** (1.0/len(d)),
    "harmonic": lambda d: len(d)/reduce(lambda acc,b: acc+1/b, d, 0),
    "median": lambda d: sorted(d)[len(d)//2] if len(d) % 2 == 1 else (sorted(d)[len(d)//2-1]+sorted(d)[len(d)//2])/2
}

def min_strategy(strategies, data):
    return min(strategies.items(), key=lambda item: item[1](data))[0]

def max_strategy(strategies, data):
    return max(strategies.items(), key=lambda item: item[1](data))[0]


def main():
    lam1()
    (lambda:print("I am IIFE"))()
    make_lam2()
    lam2()
    x=30
    make_lam3()
    lam3()
    make_lam4()
    lam4()
    lam5=lambda a,b:a+b
    print(lam5(1,2))
    data=(1,2,3,4,5)
    for name, func in strategies.items():
        print(f"{name}:", apply(func, data))
    
    print("Strategy min :", min_strategy(strategies, data))
    print("Strategy max :", max_strategy(strategies, data))


if __name__ == '__main__':
    main()


# Стратегия — это поведенческий паттерн проектирования, 
# который определяет семейство схожих алгоритмов 
# и помещает каждый из них в собственный класс,
#  после чего алгоритмы можно взаимозаменять прямо во время исполнения программы.
