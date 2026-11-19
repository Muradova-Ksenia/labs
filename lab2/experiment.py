import numpy as np
import subprocess
import os
import matplotlib.pyplot as plt

sizes = [200, 400, 800, 1200, 1600, 2000]
thread_counts = [1, 2, 4, 8]
results = {}

print("Начинаем эксперименты для OpenMP")

for n in sizes:
    print(f"\nТестирование размера {n}x{n}")
    
    file_a = f"A_{n}.txt"
    file_b = f"B_{n}.txt"
    
    if not os.path.exists(file_a):
        print("Генерация матриц")
        A = np.random.rand(n, n)
        B = np.random.rand(n, n)
        np.savetxt(file_a, A, header=str(n), comments='', fmt='%.4f')
        np.savetxt(file_b, B, header=str(n), comments='', fmt='%.4f')
        
    results[n] = {}

    for threads in thread_counts:
        print(f"Запуск с {threads} поток(ами)")
        
        process = subprocess.run(["./matrix_mult", file_a, file_b, str(threads)], capture_output=True, text=True)
        
        if process.returncode != 0:
            print("Ошибка main.cpp:", process.stderr)
            continue

        cpp_time = 0.0
        for line in process.stdout.split('\n'):
            if line.startswith("TIME_CPP:"):
                cpp_time = float(line.split(":")[1].strip())
        
        print(f"Время: {cpp_time:.4f} сек.")
        results[n][threads] = cpp_time

print("\nПостроение графиков")
plt.figure(figsize=(12, 7))

for n in sizes:
    threads_list = list(results[n].keys())
    times_list = list(results[n].values())
    plt.plot(threads_list, times_list, marker='o', label=f'{n}x{n}')

plt.title('Зависимость времени перемножения от количества потоков (OpenMP)')
plt.xlabel('Количество потоков')
plt.ylabel('Время (секунды)')
plt.xticks(thread_counts)
plt.grid(True)
plt.legend()
plt.savefig('performance_plot_threads.png')
print("График сохранен как performance_plot_threads.png")

print("\nТаблица для README.md:")
print("| Размер | 1 поток | 2 потока | 4 потока | 8 потоков | Ускорение (1->8) |")
print("| :--- | :--- | :--- | :--- | :--- | :--- |")
for n in sizes:
    t1 = results[n].get(1, 0)
    t2 = results[n].get(2, 0)
    t4 = results[n].get(4, 0)
    t8 = results[n].get(8, 0)
    
    speedup = t1 / t8 if t8 > 0 else 0
    
    print(f"| {n}x{n} | {t1:.4f} | {t2:.4f} | {t4:.4f} | {t8:.4f} | {speedup:.2f}x |")