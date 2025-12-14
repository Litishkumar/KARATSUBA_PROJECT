import time
import random
import matplotlib.pyplot as plt

# ---------------- Karatsuba Algorithm ----------------
def karatsuba_mul(x, y, counter):
    counter['calls'] += 1
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    m = n // 2

    high1, low1 = divmod(x, 10**m)
    high2, low2 = divmod(y, 10**m)

    z0 = karatsuba_mul(low1, low2, counter)
    z1 = karatsuba_mul((low1 + high1), (low2 + high2), counter)
    z2 = karatsuba_mul(high1, high2, counter)

    return (z2 * 10**(2*m)) + ((z1 - z2 - z0) * 10**m) + z0


# ---------------- Divide-and-Conquer Multiplication ----------------
def divide_and_conquer_mul(x, y, counter):
    counter['calls'] += 1
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    m = n // 2

    high1, low1 = divmod(x, 10**m)
    high2, low2 = divmod(y, 10**m)

    z0 = divide_and_conquer_mul(low1, low2, counter)
    z1 = divide_and_conquer_mul(low1, high2, counter)
    z2 = divide_and_conquer_mul(high1, low2, counter)
    z3 = divide_and_conquer_mul(high1, high2, counter)

    return (z3 * 10**(2*m)) + ((z1 + z2) * 10**m) + z0


# ---------------- Wrappers for API ----------------
def divide_and_conquer(x, y):
    counter_div = {'calls': 0}
    start = time.time()
    result = divide_and_conquer_mul(x, y, counter_div)
    end = time.time()
    return result, counter_div['calls'], (end - start)


def karatsuba(x, y):
    counter_kar = {'calls': 0}
    start = time.time()
    result = karatsuba_mul(x, y, counter_kar)
    end = time.time()
    return result, counter_kar['calls'], (end - start)


# ---------------- Benchmark Function (Console Mode) ----------------
def benchmark_with_input(x, y):
    digits = [10, 50, 100, 200, 500]
    divide_times, karatsuba_times = [], []
    divide_calls, karatsuba_calls = [], []

    for d in digits:
        a = random.randint(10**(d-1), 10**d - 1)
        b = random.randint(10**(d-1), 10**d - 1)

        counter_div = {'calls': 0}
        start = time.time()
        divide_and_conquer_mul(a, b, counter_div)
        end = time.time()
        divide_times.append(end - start)
        divide_calls.append(counter_div['calls'])

        counter_kar = {'calls': 0}
        start = time.time()
        karatsuba_mul(a, b, counter_kar)
        end = time.time()
        karatsuba_times.append(end - start)
        karatsuba_calls.append(counter_kar['calls'])

    # Menu Loop
    while True:
        print("\n--- Choose a Graph ---")
        print("1. Execution Time (Line)")
        print("2. Recursive Calls (Line)")
        print("3. Speedup Factor (Line)")
        print("4. Execution Time (Bar)")
        print("5. Recursive Calls (Bar)")
        print("6. Execution Time Share (Pie)")
        print("7. Recursive Calls Share (Pie)")
        print("8. Execution Time Histogram")
        print("9. Recursive Calls Histogram")
        print("10. Combined Subplots (Time, Calls, Speedup)")
        print("0. Exit")

        choice = int(input("Enter choice: "))

        if choice == 0:
            break

        elif choice == 1:
            plt.plot(digits, divide_times, label="Divide")
            plt.plot(digits, karatsuba_times, label="Karatsuba")
            plt.xlabel("Digits"); plt.ylabel("Time (s)")
            plt.title("Execution Time"); plt.legend(); plt.show()

        elif choice == 2:
            plt.plot(digits, divide_calls, label="Divide")
            plt.plot(digits, karatsuba_calls, label="Karatsuba")
            plt.xlabel("Digits"); plt.ylabel("Calls")
            plt.title("Recursive Calls"); plt.legend(); plt.show()

        elif choice == 3:
            speedup = [d/k if k != 0 else 0 for d, k in zip(divide_times, karatsuba_times)]
            plt.plot(digits, speedup, marker="o", color="purple")
            plt.xlabel("Digits"); plt.ylabel("Speedup Factor")
            plt.title("Speedup (Divide ÷ Karatsuba)"); plt.show()

        elif choice == 4:
            plt.bar(digits, divide_times, width=20, label="Divide")
            plt.bar(digits, karatsuba_times, width=10, label="Karatsuba")
            plt.xlabel("Digits"); plt.ylabel("Time (s)")
            plt.title("Execution Time (Bar)"); plt.legend(); plt.show()

        elif choice == 5:
            plt.bar(digits, divide_calls, width=20, label="Divide")
            plt.bar(digits, karatsuba_calls, width=10, label="Karatsuba")
            plt.xlabel("Digits"); plt.ylabel("Calls")
            plt.title("Recursive Calls (Bar)"); plt.legend(); plt.show()

        elif choice == 6:
            labels = ["Divide", "Karatsuba"]
            values = [sum(divide_times), sum(karatsuba_times)]
            plt.pie(values, labels=labels, autopct="%1.1f%%")
            plt.title("Execution Time Share"); plt.show()

        elif choice == 7:
            labels = ["Divide", "Karatsuba"]
            values = [sum(divide_calls), sum(karatsuba_calls)]
            plt.pie(values, labels=labels, autopct="%1.1f%%")
            plt.title("Recursive Calls Share"); plt.show()

        elif choice == 8:
            plt.hist([divide_times, karatsuba_times], label=["Divide", "Karatsuba"])
            plt.xlabel("Time (s)"); plt.ylabel("Frequency")
            plt.title("Execution Time Histogram"); plt.legend(); plt.show()

        elif choice == 9:
            plt.hist([divide_calls, karatsuba_calls], label=["Divide", "Karatsuba"])
            plt.xlabel("Calls"); plt.ylabel("Frequency")
            plt.title("Recursive Calls Histogram"); plt.legend(); plt.show()

        elif choice == 10:
            speedup = [d/k if k != 0 else 0 for d, k in zip(divide_times, karatsuba_times)]
            fig, axs = plt.subplots(1, 3, figsize=(15, 5))

            axs[0].plot(digits, divide_times, label="Divide")
            axs[0].plot(digits, karatsuba_times, label="Karatsuba")
            axs[0].set_title("Execution Time"); axs[0].set_xlabel("Digits"); axs[0].set_ylabel("Time (s)")
            axs[0].legend()

            axs[1].plot(digits, divide_calls, label="Divide")
            axs[1].plot(digits, karatsuba_calls, label="Karatsuba")
            axs[1].set_title("Recursive Calls"); axs[1].set_xlabel("Digits"); axs[1].set_ylabel("Calls")
            axs[1].legend()

            axs[2].plot(digits, speedup, marker="o", color="purple")
            axs[2].set_title("Speedup Factor"); axs[2].set_xlabel("Digits"); axs[2].set_ylabel("Divide ÷ Karatsuba")

            plt.tight_layout()
            plt.show()


# ---------------- Main ----------------
if __name__ == "__main__":
    print("\n--- Custom Input Test ---")
    x = int(input("Enter first number: "))
    y = int(input("Enter second number: "))

    counter_div = {'calls': 0}
    res_div = divide_and_conquer_mul(x, y, counter_div)
    print(f"\n[Divide-and-Conquer]\nResult = {res_div}\nRecursive Calls = {counter_div['calls']}")

    counter_kar = {'calls': 0}
    res_kar = karatsuba_mul(x, y, counter_kar)
    print(f"\n[Karatsuba]\nResult = {res_kar}\nRecursive Calls = {counter_kar['calls']}")

    benchmark_with_input(x, y)
