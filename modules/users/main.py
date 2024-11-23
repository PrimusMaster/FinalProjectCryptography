from modules.users.engine import *

user = User()


while True:
    print("1-Añadir Usuario")
    print("2-Actualizar usuario")
    print("3-Eliminar Usuarios")
    print("4-Ver usuarios")
    print("5-Salir")
    option = int(input("Digita una opcion: "))

    match option:

        case 1:
            print("Añadir usuario")
            name = input("Digita el nombre del usuario: ")
            password = input("Digita una contraseña: ")
            email = input("Digita el correo del usuario: ")
            area = input("Digita el area del usuario: ")
            age = int(input("Digita la edad del usuario: "))
            user.create_user(name,password, email, area, age)

        case 2:
            print("Actualizar usuario")
            id = input("Digita el id del usuario a actualizar: ")
            field = input("Digita el nombre del campo a actualizar: ")
            value = input("Digita el nuevo valor del campo: ")
            fields_to_update = {field: value}
            user.update_user(id, **fields_to_update)

        case 3:
            print("Eliminar usuario")
            id = input("Digita el id del usuario a eliminar: ")
            user.delete_user(id)

        case 4:
            user.view_users()

        case 5:
            break

        case _:
            print("Opcion no valida")

