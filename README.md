# Programa biblioteca con base de datos en tiempo real

Este proyecto implementa un sistema de **gestión de biblioteca** en Python, utilizando **Programación Orientada a Objetos (POO)** y **Firebase Realtime Database** para almacenar la información de forma persistente.

## Características principales

- Registro e inicio de sesión de **usuarios** y **administradores**.
- Administración de un **catálogo de libros**.
- Préstamo y devolución de libros.
- Persistencia de datos con **Firebase** (catálogo, usuarios, administradores y libros prestados).
- Validación de credenciales mediante herencia (`Persona` → `Usuario` / `Administrador`).
- Sin pérdida de información al cerrar el programa.

## Estructura de clases

### Clase `Biblioteca`
- Administra usuarios, administradores y libros.
- Permite registrar, mostrar y guardar datos.
- Interactúa con Firebase para **guardar y cargar información**.
- Al iniciar: carga todos los datos desde la base.
- Al salir: guarda los datos actualizados en Firebase.

### Clase `Libro`
- Representa cada libro del catálogo.
- Atributos: `categoria`, `titulo`, `autor`, `numero_paginas`, `disponible`.
- Método `hacerDiccionario()` para convertir en formato JSON.

### Clase `Persona` (superclase)
- Contiene datos comunes: nombre, apellido, edad, documento, clave y nombre de usuario.
- Método `validar_usuario()` para verificar credenciales.
- Método `hacerDiccionario()` básico para serializar datos comunes.

### Clase `Usuario` (hereda de `Persona`)
- Puede **pedir** y **devolver libros**.
- Atributo `libros_prestados`, que guarda los títulos de los libros prestados.
- Método `hacerDiccionario()` sobrescrito para incluir los libros prestados.
- Método `mostrar_perfil()` con información personal y libros actuales.

### Clase `Administrador` (hereda de `Persona`)

## Persistencia de datos

El sistema usa Firebase Realtime Database para guardar toda la información en el nodo `/biblioteca`.

Ejemplo del formato de almacenamiento:

```json
{
  "usuarios": [
    {
      "nombre": "Santiago",
      "apellido": "Peralta",
      "edad": "22",
      "documento": "12345",
      "clave": "abc123",
      "nombre_usuario": "santi",
      "libros_prestados": ["1984", "El origen de las especies"]
    }
  ],
  "administradores": [
    {
      "nombre": "Laura",
      "apellido": "García",
      "edad": "28",
      "documento": "67890",
      "clave": "admin123",
      "nombre_usuario": "laura_admin"
    }
  ],
  "catalogo": [
    {
      "categoria": "Ciencia Ficción",
      "titulo": "1984",
      "autor": "George Orwell",
      "numero_paginas": "250",
      "disponible": false
    }
  ]
}
```
##instalacion 

Clona este repositorio o copia el código:
```
git clone https://github.com/tuusuario/biblioteca-unal.git
cd biblioteca-unal
```
Instala las dependencias necesarias:
```
pip install firebase-admin

```
Actualiza esta línea en el código con la ruta correcta a tu archivo:
```
cred = credentials.Certificate("/ruta/a/tu/archivo-credenciales.json")

```
## Ejecucion
En la terminal del sistema escribe el siguiente comando
```
python main.py

```
##Ejemplo de uso:
### Registro personas
<img width="350" height="506" alt="image" src="https://github.com/user-attachments/assets/952dbec7-113c-44b7-b6ae-44d6182b7f3c" />
<img width="377" height="307" alt="image" src="https://github.com/user-attachments/assets/11b77ed4-02c1-48f0-895b-ada9c29b4fa3" />
<img width="377" height="307" alt="image" src="https://github.com/user-attachments/assets/7ee85831-5bde-4801-aa41-a9f3ee6c4c7f" />

### Registro libros e inicio de sesion
<img width="696" height="327" alt="image" src="https://github.com/user-attachments/assets/3316c00b-369c-4a59-8d91-3a1e7086a031" />
<img width="334" height="225" alt="image" src="https://github.com/user-attachments/assets/fc7890ef-989d-475b-a79b-cf782a42ef5a" />

## Prestamo de libros, información de usuarios y catalogo
<img width="744" height="291" alt="image" src="https://github.com/user-attachments/assets/17b86a6f-1a7d-48c8-b381-2bbfdec8a70d" />
<img width="519" height="301" alt="image" src="https://github.com/user-attachments/assets/8dc5e1b1-3f51-4824-861b-58633bc79b05" />


## Resumen de funciones

- Puede **agregar**, **eliminar** y **mostrar libros** del catálogo.
- Puede **listar usuarios registrados**.
