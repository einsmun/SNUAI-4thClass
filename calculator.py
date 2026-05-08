def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다")
    return a / b

if __name__ == "__main__":
    print("계산기")
    print("연산자: +, -, *, /")
    while True:
        try:
            expr = input("계산식 입력 (종료: q): ")
            if expr == "q":
                break
            a, op, b = expr.split()
            a, b = float(a), float(b)
            if op == "+":
                print(add(a, b))
            elif op == "-":
                print(subtract(a, b))
            elif op == "*":
                print(multiply(a, b))
            elif op == "/":
                print(divide(a, b))
            else:
                print("지원하지 않는 연산자입니다")
        except ValueError as e:
            print(f"오류: {e}")
        except Exception:
            print("올바른 형식으로 입력해 주세요 (예: 3 + 5)")
