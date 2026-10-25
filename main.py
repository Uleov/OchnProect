import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def is_valid_stack(text):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    opening = set(pairs.values())
    for char in text:
        if char in opening:
            stack.append(char)
        elif char in pairs:
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
    return len(stack) == 0

def is_valid_naive(text):
    filtered = "".join(c for c in text if c in "()[]{}")
    while True:
        prev = filtered
        filtered = filtered.replace("()", "").replace("[]", "").replace("{}", "")
        if filtered == prev:
            break
    return len(filtered) == 0

def trace(text):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    opening = set(pairs.values())
    print("Трассировка для строки:", text)
    for char in text:
        if char in opening:
            stack.append(char)
            print(f"Символ '{char}': положили в стек -> {stack}")
        elif char in pairs:
            if not stack or stack[-1] != pairs[char]:
                print(f"Символ '{char}': ошибка! На вершине нет пары. Стек: {stack}")
                return False
            stack.pop()
            print(f"Символ '{char}': сняли пару со стека -> {stack}")
    result = len(stack) == 0
    print("Итог:", result)
    return result

def run_tests():
    tests = [
        ("", True),
        ("(", False),
        ("]", False),
        ("()", True),
        ("{[()]}", True),
        ("{[(])}", False),
        ("((()", False),
        ("def f(x): return x[0]", True)
    ]
    print("=== ТЕСТЫ ===")
    for text, expected in tests:
        res = is_valid_stack(text)
        print(f"Вход: '{text}' -> Результат: {res} (Ожидалось: {expected})")

def run_benchmarks():
    print("\n=== ЗАМЕР ВРЕМЕНИ (СТЕК) ===")
    for n in [100000, 300000, 1000000]:
        data = "()" * (n // 2)
        start = time.perf_counter()
        is_valid_stack(data)
        elapsed = time.perf_counter() - start
        print(f"N = {n}: {elapsed:.4f} сек")

    print("\n=== СРАВНЕНИЕ (40 000 СКОБОК) ===")
    bad_data = "(" * 20000 + ")" * 20000

    start = time.perf_counter()
    is_valid_naive(bad_data)
    t_naive = time.perf_counter() - start

    start = time.perf_counter()
    is_valid_stack(bad_data)
    t_stack = time.perf_counter() - start

    print(f"Наивный метод O(n^2): {t_naive:.4f} сек")
    print(f"Алгоритм на стеке O(n): {t_stack:.4f} сек")
    print(f"Ускорение: в {t_naive / t_stack:.0f} раз")

def main():
    if "--trace" in sys.argv:
        trace("{[()]}")
        print()
        trace("{[(])}")
        return
    run_tests()
    run_benchmarks()

if __name__ == "__main__":
    main()
