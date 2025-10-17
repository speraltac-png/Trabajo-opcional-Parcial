import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("/home/santiago-peralta/Documentos/bibloUnal/biblioteca-parcial-firebase-adminsdk-fbsvc-dc1e53d6a9.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://biblioteca-parcial-default-rtdb.firebaseio.com/'})


class Biblioteca:
    def __init__(self):
        self.__catalogo = []
        self.__usuarios = []
        self.__administradores = []

    def registrar_libros(self, libro):
        self.__catalogo.append(libro)

    def mostrar_catalogo(self):
        if not self.__catalogo:
            print("No hay libros en el catálogo.")
        else:
            for i, libro in enumerate(self.__catalogo, 1):
                print(f"{i}. {libro}")

    def registrar_usuario(self, nombre, apellido, edad, documento, clave, nombre_usuario):
        usuario = Usuario(nombre, apellido, edad, documento, clave, nombre_usuario, self)
        self.__usuarios.append(usuario)
        return usuario

    def registrar_administrador(self, nombre, apellido, edad, documento, clave, nombre_usuario):
        admin = Administrador(nombre, apellido, edad, documento, clave, nombre_usuario, self)
        self.__administradores.append(admin)
        return admin

    def mostrarMenu(self):
        while True:
            tipo_usuario = int(input("\n1. Usuario 2. Administrador 3. Salir\n>>> "))
            if tipo_usuario == 3:
                break

            if tipo_usuario == 1:
                registro = int(input("1. Registrarse 2. Iniciar sesión \n>>> "))
                if registro == 1:
                    nombre = input("Nombre: ")
                    apellido = input("Apellido: ")
                    edad = input("Edad: ")
                    documento = input("Documento: ")
                    nombre_usuario = input("Nombre de usuario: ")
                    clave = input("Clave: ")
                    self.registrar_usuario(nombre, apellido, edad, documento, clave, nombre_usuario)
                    print("Usuario registrado con éxito")

                elif registro == 2:
                    nombre_de_usuario = input("Nombre de usuario: ")
                    clave_usuario = input("Clave: ")
                    usuario_encontrado = None
                    for u in self.usuarios:
                        if u.validar_usuario(nombre_de_usuario, clave_usuario):
                            usuario_encontrado = u
                            break

                    if usuario_encontrado:
                        print("Ingreso correcto")
                        while True:
                            opcion = int(input("\n1. Pedir libro 2. Devolver libro 3. Mostrar perfil 4. Salir\n>>> "))
                            if opcion == 1:
                                titulo = input("Título del libro a pedir: ")
                                usuario_encontrado.pedir_libro(titulo)
                            elif opcion == 2:
                                titulo = input("Título del libro a devolver: ")
                                usuario_encontrado.devolver_libro(titulo)
                            elif opcion == 3:
                                usuario_encontrado.mostrar_perfil()
                            elif opcion == 4:
                                break
                    else:
                        print("Clave o usuario incorrectos, inténtelo de nuevo.")

            elif tipo_usuario == 2:
                registro = int(input("1. Registrarse 2. Iniciar sesión \n>>> "))
                if registro == 1:
                    nombre = input("Nombre: ")
                    apellido = input("Apellido: ")
                    edad = input("Edad: ")
                    documento = input("Documento: ")
                    nombre_administrador = input("Nombre de administrador: ")
                    clave = input("Clave: ")
                    self.registrar_administrador(nombre, apellido, edad, documento, clave, nombre_administrador)
                    print("Administrador registrado con éxito")

                elif registro == 2:
                    usuario_admin = input("Nombre de administrador: ")
                    clave_admin = input("Clave: ")

                    admin_encontrado = None
                    for a in self.administradores:
                        if a.validar_usuario(usuario_admin, clave_admin):
                            admin_encontrado = a
                            break

                    if admin_encontrado:
                        print("Ingreso correcto")
                        while True:
                            opciones_admin = int(input(
                                "\n1. Agregar libros 2. Eliminar libros 3. Mostrar catálogo 4. Mostrar usuarios 5. Salir\n>>> "
                            ))
                            if opciones_admin == 1:
                                categoria = input("Categoría del libro: ")
                                titulo = input("Título del libro: ")
                                autor = input("Autor del libro: ")
                                numero_paginas = input("Número de páginas: ")
                                admin_encontrado.agregar_libro(categoria, titulo, autor, numero_paginas)
                            elif opciones_admin == 2:
                                titulo = input("Título del libro a eliminar: ")
                                admin_encontrado.eliminar_libro(titulo)
                            elif opciones_admin == 3:
                                admin_encontrado.mostrar_catalogo()
                            elif opciones_admin == 4:
                                admin_encontrado.mostrar_usuarios()
                            elif opciones_admin == 5:
                                break
                    else:
                        print("Clave o usuario incorrectos, inténtelo de nuevo.")

    def guardar_datos(self):
        datos = {
            "usuarios": [u.hacerDiccionario() for u in self.__usuarios],
            "administradores": [a.hacerDiccionario() for a in self.__administradores],
            "catalogo": [l.hacerDiccionario() for l in self.__catalogo]
        }
        db.reference("/biblioteca").set(datos)

    def cargar_datos(self):
        ref = db.reference("/biblioteca")
        datos = ref.get() or {}

        self.__usuarios.clear()
        self.__administradores.clear()
        self.__catalogo.clear()

        for datos_libros in datos.get("catalogo", []):
            libro = Libro(datos_libros["categoria"],datos_libros["titulo"],datos_libros["autor"],datos_libros["numero_paginas"]
            )
            libro.disponible = datos_libros.get("disponible")
            self.__catalogo.append(libro)

        for datos_usuarios in datos.get("usuarios", []):
            usuario = Usuario(datos_usuarios["nombre"],datos_usuarios["apellido"],datos_usuarios["edad"],datos_usuarios["documento"],datos_usuarios["clave"],datos_usuarios["nombre_usuario"],
                self
            )
            for titulo in datos_usuarios.get("libros_prestados", []):
                for libro in self.__catalogo:
                    if libro.titulo == titulo:
                        libro.disponible = False
                        usuario.libros_prestados.append(libro)
                        break

            self.__usuarios.append(usuario)

        for datos_admin in datos.get("administradores", []):
            admin = Administrador(datos_admin["nombre"],datos_admin["apellido"],datos_admin["edad"],datos_admin["documento"],datos_admin["clave"],datos_admin["nombre_usuario"],self)
            self.__administradores.append(admin)

    @property
    def catalogo(self):
        return self.__catalogo

    @property
    def usuarios(self):
        return self.__usuarios

    @property
    def administradores(self):
        return self.__administradores


class Libro:
    def __init__(self, categoria, titulo, autor, numero_paginas):
        self.categoria = categoria
        self.titulo = titulo
        self.autor = autor
        self.numero_paginas = numero_paginas
        self.disponible = True

    def hacerDiccionario(self):
        return {
            "categoria": self.categoria,
            "titulo": self.titulo,
            "autor": self.autor,
            "numero_paginas": self.numero_paginas,
            "disponible": self.disponible
        }

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"[{self.categoria}] {self.titulo} - {self.autor} ({self.numero_paginas} págs) - {estado}"


class Persona:
    def __init__(self, nombre, apellido, edad, documento, clave, nombre_usuario, biblioteca):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.documento = documento
        self.__clave = clave
        self.nombre_usuario = nombre_usuario
        self.biblioteca = biblioteca

    def hacerDiccionario(self):
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "edad": self.edad,
            "documento": self.documento,
            "clave": self.clave,
            "nombre_usuario": self.nombre_usuario
        }

    @property
    def clave(self):
        return self.__clave

    @clave.setter
    def clave(self, valor):
        self.__clave = valor

    def validar_usuario(self, nombre_usuario, clave):
        return self.nombre_usuario == nombre_usuario and self.clave == clave


class Usuario(Persona):
    def __init__(self, nombre, apellido, edad, documento, clave, nombre_usuario, biblioteca):
        super().__init__(nombre, apellido, edad, documento, clave, nombre_usuario, biblioteca)
        self.libros_prestados = []

    def hacerDiccionario(self):
        datos = super().hacerDiccionario()
        datos["libros_prestados"] = [libro.titulo for libro in self.libros_prestados]
        return datos

    def pedir_libro(self, titulo):
        for libro in self.biblioteca.catalogo:
            if libro.titulo == titulo and libro.disponible:
                libro.disponible = False
                self.libros_prestados.append(libro)
                print(f"Has pedido el libro: {libro.titulo}")
                return
        print("El libro no está disponible.")

    def devolver_libro(self, titulo):
        for libro in self.libros_prestados:
            if libro.titulo == titulo:
                libro.disponible = True
                self.libros_prestados.remove(libro)
                print(f"Has devuelto el libro: {libro.titulo}")
                return
        print("No tienes este libro en préstamo.")

    def mostrar_perfil(self):
        print(f"Usuario: {self.nombre} {self.apellido}, Edad: {self.edad}, Documento: {self.documento}")
        if self.libros_prestados:
            print("Libros prestados:")
            for libro in self.libros_prestados:
                print(f"- {libro.titulo}")
        else:
            print("No tienes libros prestados.")


class Administrador(Persona):
    def __init__(self, nombre, apellido, edad, documento, clave, nombre_administrador, biblioteca):
        super().__init__(nombre, apellido, edad, documento, clave, nombre_administrador, biblioteca)

    def agregar_libro(self, categoria, titulo, autor, numero_paginas):
        libro_nuevo = Libro(categoria, titulo, autor, numero_paginas)
        self.biblioteca.registrar_libros(libro_nuevo)
        print(f"Libro '{titulo}' agregado al catálogo.")

    def eliminar_libro(self, titulo):
        for libro in self.biblioteca.catalogo:
            if libro.titulo == titulo:
                self.biblioteca.catalogo.remove(libro)
                print(f"Libro '{titulo}' eliminado del catálogo.")
                return
        print("El libro no existe en el catálogo.")

    def mostrar_catalogo(self):
        self.biblioteca.mostrar_catalogo()

    def mostrar_usuarios(self):
        if not self.biblioteca.usuarios:
            print("No hay usuarios registrados.")
        else:
            print("Usuarios registrados:")
            for u in self.biblioteca.usuarios:
                print(f"- {u.nombre_usuario}")


def main():
    print("Biblioteca - Parcial POO")
    bibloUnal = Biblioteca()
    bibloUnal.cargar_datos() 
    bibloUnal.mostrarMenu()   
    bibloUnal.guardar_datos()

if __name__ == "__main__":
    main()
