class Point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

    def __str__(self):
        return "(%.2f,%.2f)" % (
            self.x, self.y)
    

    def __repr__(self):
        return "(%f,%f)" % (
            self.x, self.y)
    

    

def main():
    p1 = Point()
    print(p1)
    d={'p2':Point()}
    print(d)


if __name__ == "__main__":
    main()
