def throw():
    raise ValueError

def throw_msg():
    raise TypeError("Error message")

def throw_ex():
    raise Exception

def no_throw():
    pass


def main():
    try:
        no_throw()
        return
    except ValueError:
        print("ValueError detected")
        return
    except TypeError as err:
        print(err)
    except :
        print("Unknown Error detected")
    else:
        print("Else block")
    finally:
        print("Finally block")


if __name__ == "__main__":
    main()