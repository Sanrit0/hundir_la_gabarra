import variables as var
import funciones as fun
import time

print(var.msg1)
time.sleep(1)
while True:

    print(var.msg2)
    opcion = int(input('opcion: '))

    if opcion == 2:
        break

    if opcion == 1:
        fun.jugar()

    fun.borrar_print()