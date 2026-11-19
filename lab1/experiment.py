import numpy as np
import subprocess
import time
import os
import matplotlib.pyplot as plt


sizes = [200, 400, 800, 1200, 1600, 2000]
results = []


cpp_executable = "./matrix_mult" 

print("Начинаем эксперименты")

for n in sizes:
    print(f"\nТестирование размера {n}x{n}")
    
    file_a = f"A_{n}.txt"
    file_b = f"B_{n}.txt"
    file_res_cpp = f"result_cpp_{n}.txt"
    

    if not os.path.exists(file_a):
        print("Генерация матриц")
        A = np.random.rand(n, n)
        B = np.random.rand(n, n)
        

        np.savetxt(file_a, A, header=str(n), comments='', fmt='%.4f')
        np.savetxt(file_b, B, header=str(n), comments='', fmt='%.4f')
    

    print("Запуск main.cpp программы...")
    process = subprocess.run([cpp_executable, file_a, file_b], capture_output=True, text=True)
    

    if process.returncode != 0:
        print("Ошибка C++:", process.stderr)
        break


    cpp_time = 0.0
    for line in process.stdout.split('\n'):
        if line.startswith("TIME_CPP:"):
            cpp_time = float(line.split(":")[1].strip())
    
    print(f"Время выполнения main.cpp: {cpp_time:.4f} сек.")


    print("Верификация с помощью NumPy")

    A_verify = np.loadtxt(file_a, skiprows=1)
    B_verify = np.loadtxt(file_b, skiprows=1)

    C_cpp = np.loadtxt(file_res_cpp, skiprows=1)
    

    C_python = np.dot(A_verify, B_verify)
    

    if np.allclose(C_cpp, C_python, rtol=1e-3, atol=1e-5):
        print("Верификация пройдена успешно!")
        status = "OK"
    else:
        print("Ошибка: Результаты не совпадают!")
        status = "FAIL"
        
    results.append({
        "size": n,
        "time": cpp_time,
        "status": status
    })


print("\nПостроение графика")
x = [r["size"] for r in results]
y = [r["time"] for r in results]

plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', linestyle='-', color='b', label='Время выполнения (C++)')
plt.title('Зависимость времени перемножения матриц от размера')
plt.xlabel('Размер матрицы (N x N)')
plt.ylabel('Время (секунды)')
plt.grid(True)
plt.legend()
plt.savefig('performance_plot.png')
print("График сохранен как performance_plot.png")


print("\nТаблица для README.md:")
print("| Размер матрицы | Время выполнения (сек) | Статус верификации |")
print("| :--- | :--- | :--- |")
for r in results:
    print(f"| {r['size']}x{r['size']} | {r['time']:.4f} | {r['status']} |")