import tkinter as tk
from tkinter import Menu, messagebox, Entry, filedialog
import subprocess
import webbrowser
# import chardet

class CriptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Criptografia")
        self.root.iconbitmap("favicon.ico")
        self.root.geometry("400x500")
        
        # Crear la barra de menú
        barra_menu = Menu(root)
        self.root.config(menu=barra_menu)

        # Crear los menús
        archivo_menu = Menu(barra_menu, tearoff=0)
        ayuda_menu = Menu(barra_menu, tearoff=0)

        # Agregar las opciones de los menús
        archivo_menu.add_command(label="Limpiar pantalla", command=self.reinicio)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.salir)
        ayuda_menu.add_command(label="Acerca de...", command=self.acerca_de)
        ayuda_menu.add_command(label="Abrir Teoría...", command=self.teoria)
        ayuda_menu.add_command(label="Abrir Codigo Fuente...", command=self.fuente)

        # Agregar los menús a la barra de menú
        barra_menu.add_cascade(label="Archivo", menu=archivo_menu)
        barra_menu.add_cascade(label="Ayuda", menu=ayuda_menu)

        # Crear una variable para almacenar el tipo de cifrado
        self.cipher_type = tk.StringVar(value="Cesar")

        # Crear una variable para almacenar la acción (cifrar o descifrar)
        self.action = tk.StringVar(value="Cifrar")

        # Etiqueta para seleccionar el tipo de cifrado
        self.cipher_label = tk.Label(self.root, text="Seleccione un tipo de cifrado:", font=("Times New Roman",14))
        self.cipher_label.pack()

        # Menú desplegable para elegir entre César y Vigenère
        self.cipher_menu = tk.OptionMenu(self.root, self.cipher_type, "Cesar", "Vigenere")
        self.cipher_menu.pack()

        # Etiqueta para seleccionar la acción
        self.action_label = tk.Label(self.root, text="Seleccione una acción:", font=("Times New Roman",14))
        self.action_label.pack()

        # Menú desplegable para elegir entre Cifrar y Descifrar
        self.action_menu = tk.OptionMenu(self.root, self.action, "Cifrar", "Descifrar")
        self.action_menu.pack()

        # Cuadro de entrada para el texto
        self.text_label = tk.Label(self.root, text="Texto:", font=("Times New Roman",14))
        self.text_label.pack()

        self.text_entry = tk.Entry(self.root, width=40)
        self.text_entry.pack()

        # Cuadro de entrada para la clave
        self.key_label = tk.Label(self.root, text="Clave:", font=("Times New Roman",14))
        self.key_label.pack()

        # Utilizar una función de validación para la clave
        validate_key = self.root.register(self.validate_key)
        self.key_entry = Entry(self.root, width=20, validate="key", validatecommand=(validate_key, "%P"))
        self.key_entry.pack()

        # Botón para cifrar o descifrar
        self.submit_button = tk.Button(self.root, text="Cifrar/Descifrar", command=self.encrypt_decrypt, padx=10, pady=5,foreground="#fff", background="#0d6efd", font=("Times New Roman",14))
        self.submit_button.pack()
        
        # Asociar la tecla "Enter" a la función de cifrar/descifrar
        self.submit_button.bind("<Return>", lambda event=None: self.encrypt_decrypt())
        
        # Cuadro de salida para el resultado
        self.result_label = tk.Label(self.root, text="Resultado:", font=("Times New Roman",14))
        self.result_label.pack()

        self.result_text = tk.Text(self.root, height=10, width=40)
        self.result_text.pack()

        # Definir el abecedario que incluye la letra "ñ"
        self.alphabet = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

    def validate_key(self, key):
        # Validar la clave en función del método seleccionado
        cipher_type = self.cipher_type.get()
        if cipher_type == "Cesar":
            # Si es César, permitir solo números en la clave
            if key.isdigit() or key == "":
                return True
            else:
                messagebox.showerror("Error", "La clave para César debe contener solo números.")
                return False
        elif cipher_type == "Vigenere":
            # Si es Vigenère, permitir solo letras en la clave
            if key.isalpha() or key == "":
                return True
            else:
                messagebox.showerror("Error", "La clave para Vigenère debe contener solo letras.")
                return False

    def validate_fields(self, value, action):
        # Validar los campos de texto y clave para habilitar/deshabilitar el botón
        if self.text_entry.get() and self.key_entry.get():
            self.submit_button.config(state="active")
        else:
            self.submit_button.config(state="disabled")
        return True

    def encrypt_decrypt(self):
        text = self.text_entry.get()
        key = self.key_entry.get()
        cipher_type = self.cipher_type.get()
        action = self.action.get()
        
        # Validar que el texto solo contenga caracteres del abecedario
        if not all(char in self.alphabet for char in text):
            messagebox.showerror("Error", "El texto contiene caracteres no válidos.")
            return

        if cipher_type == "Cesar":
            result = self.cesar_cipher(text, int(key), action)
        else:
            result = self.vigenere_cipher(text, key, action)
        
        # Convertir el resultado a mayúsculas
        result = result.upper()

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

    def cesar_cipher(self, text, key, action):
        result = ""
        for char in text:
            if char in self.alphabet:
                shift = key if action == "Cifrar" else -key
                shifted_char = self.alphabet[(self.alphabet.index(char) + shift) % len(self.alphabet)]
                result += shifted_char
            else:
                result += char
        return result

    def vigenere_cipher(self, text, key, action):
        result = ""
        key_length = len(key)
        for i, char in enumerate(text):
            if char in self.alphabet:
                shift = self.alphabet.index(key[i % key_length])
                shift = shift if action == "Cifrar" else -shift
                shifted_char = self.alphabet[(self.alphabet.index(char) + shift) % len(self.alphabet)]
                result += shifted_char
            else:
                result += char
        return result

    def reinicio(self):
        # Reiniciar la aplicación (borrar datos)
        self.text_entry.delete(0, tk.END)
        self.key_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)

    # Salir de la aplicación
    def salir(self):
        respuesta = messagebox.askquestion(
                    title="Salir", message="¿Desear salir de la aplicación?")
        if respuesta == "yes":
            self.root.destroy()

    def acerca_de(self):
        informacion = "Nombre: César Alonso García Villafaña\nMatrícula: 1859187\nMaestro: Angel Salvador Perez Blanco"
        messagebox.showinfo("Acerca de", informacion)

    def teoria(self):
        try:
            archivo_teoria = "archivo_de_teoria.pdf"  # Ruta al archivo que deseas abrir
            # Abrir el archivo con la aplicación predeterminada
            # subprocess.Popen(['notepad.exe', archivo_teoria], shell=True)
            subprocess.Popen(['start', '', archivo_teoria], shell=True)
            with open(archivo_teoria, 'rb') as archivo:
                contenido = archivo.read().decode('latin1')
        except FileNotFoundError:
            msg = "El archivo solicitado, no fue encontrado en el sistema, en su lugar se abrirá en el navegador web"
            messagebox.showinfo("Acerca de", msg)
            url = "https://online.fliphtml5.com/pxjlm/khki/"
            abrir_pagina_web(url)
        except Exception as e:
            print(f"Ocurrió un error: {str(e)}")      
    
    # Función para abrir el codigo fuente
    def fuente(self):
        url = "http://www.google.com"  # Cambia la URL por la que desees abrir
        abrir_pagina_web(url)

def abrir_pagina_web(url):
    webbrowser.open_new(url)

if __name__ == "__main__":
    root = tk.Tk()
    app = CriptoApp(root)
    root.mainloop()