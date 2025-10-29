class Point:
    x=0
    y=0












def main():
    p1 = Point()
    print(f"Point p1: x={p1.x}, y={p1.y}")
    Point.x = 10
    print(f"Point p1: x={p1.x}, y={p1.y}")
    p2 = Point()
    print(f"Point p2: x={p2.x}, y={p2.y}")
    p1.x=20
    print(f" x={p1.x}, x={p2.x}")
    del p1.x  # видалення обєктного поля, статичне залишається
    print(f" x={p1.x}, x={p2.x}")


if __name__ == "__main__":
    main()
