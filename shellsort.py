import random
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import timeit


def generate_array(n, min, max):
    a = [i for i in range(min, max+1)]
    random.shuffle(a)

    return a[:n]


def find_hibbard_sequence(n):
    a = []
    k = 1
    t = 2 ** k - 1
    while t < n:
        a.append(t)
        k += 1
        t = 2 ** k - 1

    a.reverse()
    return a


def shell_sort(array):
    arr = array
    seq = []
    k = 1
    t = 2 ** k - 1
    while t < len(arr):
        seq.append(t)
        k += 1
        t = 2 ** k - 1

    comparings = len(seq) + 1
    swaps = 0
    for m in range(len(seq)-1, -1, -1):
        interval = seq[m]
        for i in range(interval, len(arr)):
            comparings += 1
            temp = arr[i]
            j = i
            while j >= interval and arr[j - interval] > temp:
                comparings += 1
                arr[j] = arr[j - interval]
                j -= interval
                swaps += 1

            comparings += 1

            arr[j] = temp

    return arr, comparings, swaps


def bubble_sort(array):
    comparings, swaps = 0, 0
    abc = array
    for i in range(len(array) - 1):
        comparings += 1
        for j in range(len(array) - 1):
            comparings += 2
            if abc[j] > abc[j + 1]:
                abc[j], abc[j + 1] = abc[j + 1], abc[j]
                swaps += 1
        comparings += 1

    comparings += 1
    return abc, comparings, swaps


def improved_bubble_sort(array):
    abc = array
    comparings, swaps = 0, 0
    k = len(array) - 1
    comparings += 1
    swapped = False
    while k > 0:
        for j in range(k):
            comparings += 2
            if abc[j] > abc[j + 1]:
                swapped = True
                abc[j], abc[j + 1] = abc[j + 1], abc[j]
                swaps += 1
        k -= 1
        comparings += 1

        if not swapped:
            break

        swapped = False
    comparings += 1

    return abc, comparings, swaps


NUMS = [10]
LOG_SCALE = False

def test():
    arr_best = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    arr_random = [1, 5, 3, 6, 8, 2, 7, 8, 10, 9]
    arr_worst = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    # for k1, v1 in {"best": arr_best, "random": arr_random, "worst": arr_worst}.items():
    #     print(v1)
    #     for k2, v2 in {"bubble": bubble_sort, "impr_bubble": improved_bubble_sort, "shell": shell_sort}.items():
    #         a, b, c = v2(v1)
    #
    #         print(f'{k2}\n\n{len(v1)} elements\n{b} comparings\n{c} swaps')
    #         print(a)
    #
    #     print("\n\n")

    hibb_arr1 = [2*i for i in range(50)]
    hibb_arr2 = [2*i - 1 for i in range(50, 0, -1)]
    hibb_arr1 += hibb_arr2

    print(hibb_arr1)
    arr, comp, swaps = shell_sort(hibb_arr1)
    print(f'"Hibbard shell sort\n\n100 elements\n{comp} comparings\n{swaps} swaps')
    print(arr)
    print("\n\n")
    mod_arr = [i for i in range(100, 0, -1)]
    print(mod_arr)
    arr, comp, swaps = shell_sort(mod_arr)
    print(f'Modified bubble sort\n\n100 elements\n{comp} comparings\n{swaps} swaps')
    print(arr)

def main():
    test()
    return
    best_data = {}
    random_data = {}
    worst_data = {}
    data = []
    for sort_name, sort_ in {"Бульбашка": bubble_sort, "Модифікована бульбашка": improved_bubble_sort, "Сортування Шелла": shell_sort}.items():
        for n in NUMS:
            for name, array in {
                "Best": [a for a in range(n)],
                "Random": generate_array(n, 1, 50000),
                "Worst": [a for a in range(n, 0, -1)]
            }.items():
                start = timeit.default_timer()
                a, comparing, swaps = sort_(array)
                stop = timeit.default_timer()
                t = stop - start
                print(f'{name}\n\n{n} elements\n{t}s\n{comparing} comparings\n{swaps} swaps')
                if len(a) <= 1000:
                    print(a)

                if name == "Best":
                    best_data[n] = t
                elif name == "Random":
                    random_data[n] = t
                else:
                    worst_data[n] = t

            best_df = pd.DataFrame(list(best_data.items()), columns=['Quantity', 'Time'])
            random_df = pd.DataFrame(list(random_data.items()), columns=['Quantity', 'Time'])
            worst_df = pd.DataFrame(list(worst_data.items()), columns=['Quantity', 'Time'])

            best_df['Type'] = f'Best-{sort_name}'
            random_df['Type'] = f'Random-{sort_name}'
            worst_df['Type'] = f'Worst-{sort_name}'

        data.append(best_df)
        data.append(random_df)
        data.append(worst_df)

    combined_df = pd.concat(data)

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=combined_df, x='Quantity', y='Time', hue='Type', style='Type', markers=True,
    palette={'Best-Бульбашка': 'green',
             'Best-Модифікована бульбашка': 'green',
             'Best-Сортування Шелла': 'green',
             'Random-Бульбашка': 'blue',
             'Random-Модифікована бульбашка': 'blue',
             'Random-Сортування Шелла': 'blue',
             'Worst-Бульбашка': 'red',
             'Worst-Модифікована бульбашка': 'red',
             'Worst-Сортування Шелла': 'red',
    })
    plt.title('Графік часу виконання алгоритмів сортування на різних наборах даних')
    plt.xlabel('Кількість елементів в масиві')
    plt.ylabel('Час (секунди)')
    if LOG_SCALE:
        plt.xscale('log')
        plt.yscale('log')
    plt.gca().xaxis.set_major_formatter(ScalarFormatter())
    plt.gca().yaxis.set_major_formatter(ScalarFormatter())
    plt.legend(title='Варіант послідовності')
    plt.show()




if __name__ == '__main__':
    main()

