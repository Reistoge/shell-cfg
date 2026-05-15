import random
import string
import json
import os
from datetime import datetime
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
class PasswordManager:
    def __init__(self, history_file=None):
        if history_file is None:
            # Use the script's directory for the history file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            history_file = os.path.join(script_dir, "password_history.json")
        self.history_file = history_file
        self.password_history = self.load_history()
        self.security_questions = [
            "¿Actividad que menos le gusta realizar?",
            "¿En qué ciudad naciste?",
            "¿Profesión u oficio que deseaba ser cuando niño(a)?",
            "¿Cómo se llama tu mejor amigo de la infancia?",
            "¿Cuál es el nombre de tu escuela primaria?",
            "¿Cuál es tu color favorito?",
            "¿En qué mes naciste?",
            "¿Cuál es tu película favorita?",
            "¿Cuál es el apellido de soltera de tu madre?",
            "¿Cuál es tu número de la suerte?"
        ]
    
    def load_history(self):
        """Carga el historial de contraseñas desde archivo"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Migrar formato antiguo si existe
                    if "passwords" in data and isinstance(data["passwords"], list) and len(data["passwords"]) > 0:
                        if isinstance(data["passwords"][0], str):
                            # Convertir formato antiguo a nuevo
                            old_passwords = data["passwords"]
                            data["passwords"] = []
                            for pwd in old_passwords:
                                data["passwords"].append({
                                    "password": pwd,
                                    "tag": "Sin etiqueta",
                                    "date": datetime.now().isoformat()
                                })
                    return data
            except:
                return {"passwords": [], "security_qa": []}
        return {"passwords": [], "security_qa": []}
    
    def save_history(self):
        """Guarda el historial de contraseñas en archivo"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.password_history, f, ensure_ascii=False, indent=2)
    
    def generate_password(self):
        """Genera una contraseña de 8 caracteres que cumple todos los requisitos"""
        while True:
            # Asegurar al menos un carácter de cada tipo requerido
            password_chars = []
            
            # Al menos una mayúscula
            password_chars.append(random.choice(string.ascii_uppercase))
            
            # Al menos una minúscula
            password_chars.append(random.choice(string.ascii_lowercase))
            
            # Al menos un número
            password_chars.append(random.choice(string.digits))
            
            # Completar hasta 8 caracteres con caracteres alfanuméricos
            remaining_chars = 8 - len(password_chars)
            all_chars = string.ascii_letters + string.digits
            
            for _ in range(remaining_chars):
                password_chars.append(random.choice(all_chars))
            
            # Mezclar los caracteres para evitar patrones predecibles
            random.shuffle(password_chars)
            password = ''.join(password_chars)
            
            # Verificar que no esté en las últimas 4 contraseñas
            recent_passwords = [entry["password"] if isinstance(entry, dict) else entry for entry in self.password_history["passwords"][-4:]]
            if password not in recent_passwords:
                return password
    
    def validate_password(self, password, check_duplicates=True, min_length=8, max_length=None):
        """Valida que la contraseña cumple los requisitos (flexible para contraseñas existentes)"""
        if max_length is None:
            max_length = min_length
            
        if len(password) < min_length:
            return False, f"La contraseña debe tener al menos {min_length} caracteres"
        
        if max_length > min_length and len(password) > max_length:
            return False, f"La contraseña no debe exceder {max_length} caracteres"
        
        if min_length == max_length and len(password) != min_length:
            return False, f"La contraseña debe tener exactamente {min_length} caracteres"
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        # Para contraseñas generadas, mantener requisito alfanumérico estricto
        if min_length == 8 and max_length == 8:
            is_alnum = password.isalnum()
            if not is_alnum:
                return False, "La contraseña debe ser alfanumérica (solo letras y números)"
        
        if not has_upper:
            return False, "La contraseña debe contener al menos una mayúscula"
        if not has_lower:
            return False, "La contraseña debe contener al menos una minúscula"
        if not has_digit:
            return False, "La contraseña debe contener al menos un número"
        
        if check_duplicates:
            recent_passwords = [entry["password"] if isinstance(entry, dict) else entry for entry in self.password_history["passwords"][-4:]]
            if password in recent_passwords:
                return False, "La contraseña no puede ser igual a las últimas 4 contraseñas"
        
        return True, "Contraseña válida"
    
    def select_security_questions(self):
        """Permite al usuario seleccionar 3 preguntas de seguridad"""
        print("\n--- SELECCIÓN DE PREGUNTAS DE SEGURIDAD ---")
        print("Selecciona 3 preguntas de seguridad de la siguiente lista:")
        
        for i, question in enumerate(self.security_questions, 1):
            print(f"{i}. {question}")
        
        selected_questions = []
        qa_pairs = []
        
        while len(selected_questions) < 3:
            try:
                choice = int(input(f"\nSelecciona la pregunta #{len(selected_questions) + 1} (1-{len(self.security_questions)}): "))
                
                if 1 <= choice <= len(self.security_questions):
                    if choice not in selected_questions:
                        selected_questions.append(choice)
                        question = self.security_questions[choice - 1]
                        answer = input(f"Respuesta para '{question}': ").strip()
                        
                        if answer:
                            qa_pairs.append({
                                "question": question,
                                "answer": answer,
                                "date": datetime.now().isoformat()
                            })
                            print(f"✓ Pregunta {len(selected_questions)} guardada")
                        else:
                            selected_questions.pop()
                            print("❌ La respuesta no puede estar vacía")
                    else:
                        print("❌ Ya seleccionaste esa pregunta, elige otra")
                else:
                    print(f"❌ Número inválido. Debe estar entre 1 y {len(self.security_questions)}")
                    
            except ValueError:
                print("❌ Por favor ingresa un número válido")
        
        return qa_pairs
    
    def add_password(self, password, tag, security_qa=None, is_existing=False):
        """Añade una nueva contraseña al historial con etiqueta"""
        password_entry = {
            "password": password,
            "tag": tag,
            "date": datetime.now().isoformat(),
            "type": "existing" if is_existing else "generated"
        }
        self.password_history["passwords"].append(password_entry)
        
        # Ya no se limita la cantidad de contraseñas almacenadas
        
        if security_qa:
            self.password_history["security_qa"] = security_qa
        
        self.save_history()
    
    def show_password_history(self):
        """Muestra el historial de contraseñas"""
        if not self.password_history.get("passwords") or len(self.password_history["passwords"]) == 0:
            print("\n--- NO HAY HISTORIAL DE CONTRASEÑAS ---")
            return
            
        print("\n--- HISTORIAL DE CONTRASEÑAS ---")
        for i, entry in enumerate(self.password_history["passwords"], 1):
            if isinstance(entry, dict):
                date_str = entry.get("date", "Fecha desconocida")
                if date_str != "Fecha desconocida":
                    try:
                        # Handle different datetime formats
                        if 'T' in date_str:
                            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        else:
                            date_obj = datetime.fromisoformat(date_str)
                        date_formatted = date_obj.strftime("%d/%m/%Y %H:%M")
                    except Exception as e:
                        date_formatted = "Fecha inválida"
                else:
                    date_formatted = date_str
                
                # Mostrar tipo de contraseña (generada o existente)
                password_type = entry.get('type', 'generated')
                type_indicator = "📋" if password_type == "existing" else "🔐"
                
                tag = entry.get('tag', 'Sin etiqueta')
                password = entry.get('password', 'N/A')
                
                print(f"{i}. {type_indicator} [{tag}] {bcolors.OKCYAN} {password} {bcolors.ENDC} - {date_formatted}")
            else:
                # Formato antiguo
                print(f"{i}. 🔐 [Sin etiqueta] {entry} - Fecha desconocida")

    def search_passwords_by_tag(self, search_term):
        """Busca contraseñas por etiqueta"""
        if not self.password_history.get("passwords") or len(self.password_history["passwords"]) == 0:
            return []
            
        found_passwords = []
        search_term_lower = search_term.lower().strip()
        
        for i, entry in enumerate(self.password_history["passwords"]):
            if isinstance(entry, dict):
                tag = entry.get('tag', 'Sin etiqueta').lower()
                password = entry.get('password', '')
                
                # Search in both tag and password
                if search_term_lower in tag or search_term_lower in password.lower():
                    found_passwords.append((i + 1, entry))
            else:
                # Formato antiguo - solo buscar en contraseña
                if search_term_lower in entry.lower() or search_term_lower in 'sin etiqueta':
                    found_passwords.append((i + 1, {
                        "password": entry, 
                        "tag": "Sin etiqueta", 
                        "date": "Fecha desconocida",
                        "type": "generated"
                    }))
        
        return found_passwords
    
    def update_password_tag(self, password_index, new_tag):
        """Actualiza la etiqueta de una contraseña específica"""
        if 1 <= password_index <= len(self.password_history["passwords"]):
            entry = self.password_history["passwords"][password_index - 1]
            if isinstance(entry, dict):
                entry["tag"] = new_tag
                entry["date"] = datetime.now().isoformat()  # Actualizar fecha de modificación
            else:
                # Convertir formato antiguo a nuevo
                self.password_history["passwords"][password_index - 1] = {
                    "password": entry,
                    "tag": new_tag,
                    "date": datetime.now().isoformat()
                }
            self.save_history()
            return True
        return False
    
    def delete_password(self, password_index):
        """Elimina una contraseña del historial"""
        if 1 <= password_index <= len(self.password_history["passwords"]):
            removed_entry = self.password_history["passwords"].pop(password_index - 1)
            self.save_history()
            return removed_entry
        return None
    
    def get_password_by_index(self, password_index):
        """Obtiene una contraseña específica por su índice"""
        if 1 <= password_index <= len(self.password_history["passwords"]):
            entry = self.password_history["passwords"][password_index - 1]
            if isinstance(entry, dict):
                return entry
            else:
                # Formato antiguo
                return {"password": entry, "tag": "Sin etiqueta", "date": "Fecha desconocida"}
        return None
    
    def show_security_questions(self):
        """Muestra las preguntas de seguridad guardadas"""
        if not self.password_history.get("security_qa") or len(self.password_history["security_qa"]) == 0:
            print("\n--- NO HAY PREGUNTAS DE SEGURIDAD CONFIGURADAS ---")
            print("Usa la opción 8 del menú para configurar tus preguntas de seguridad")
            return
            
        print("\n--- PREGUNTAS DE SEGURIDAD ---")
        for i, qa in enumerate(self.password_history["security_qa"], 1):
            if isinstance(qa, dict):
                date_str = qa.get("date", "Fecha desconocida")
                if date_str != "Fecha desconocida":
                    try:
                        # Handle different datetime formats
                        if 'T' in date_str:
                            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        else:
                            date_obj = datetime.fromisoformat(date_str)
                        date_formatted = date_obj.strftime("%d/%m/%Y %H:%M")
                    except Exception as e:
                        date_formatted = "Fecha inválida"
                else:
                    date_formatted = date_str
                
                question = qa.get('question', 'Pregunta desconocida')
                answer = qa.get('answer', 'Sin respuesta')
                
                print(f"{i}. {question}")
                print(f"   Respuesta: {answer}")
                print(f"   Fecha: {date_formatted}")
                print()

def main():
    print("=== GENERADOR DE CONTRASEÑAS SEGURAS ===")
    password_manager = PasswordManager()
    
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        
        print("1. Generar nueva contraseña")
        print("2. Agregar contraseña existente")
        print("3. Ver historial de contraseñas")
        print("4. Buscar contraseñas por etiqueta")
        print("5. Modificar etiqueta de contraseña")
        print("6. Eliminar contraseña")
        print("7. Ver preguntas de seguridad")
        print("8. Configurar preguntas de seguridad")
        print("9. Salir")
        
        choice = input("\nSelecciona una opción (1-9): ").strip()
    
        if choice == '1':
            print("\n--- GENERANDO NUEVA CONTRASEÑA ---")
            
            # Solicitar etiqueta para la contraseña
            tag = input("Ingresa una etiqueta para identificar esta contraseña (ej: Gmail, Facebook, Banco): ").strip()
            if not tag:
                tag = "Sin etiqueta"
            
            new_password = password_manager.generate_password()
            
            print(f"\n✓ Nueva contraseña generada: {new_password}")
            print(f"✓ Etiqueta asignada: {tag}")
            
            # Validar la contraseña
            is_valid, message = password_manager.validate_password(new_password)
            print(f"Validación: {message}")
            
            # Preguntar si quiere configurar preguntas de seguridad
            setup_questions = input("\n¿Deseas configurar preguntas de seguridad? (s/n): ").strip().lower()
            security_qa = None
            
            if setup_questions in ['s', 'si', 'sí', 'y', 'yes']:
                security_qa = password_manager.select_security_questions()
                print("\n✓ Preguntas de seguridad configuradas correctamente")
            
            # Guardar la contraseña con etiqueta
            password_manager.add_password(new_password, tag, security_qa, is_existing=False)
            print("✓ Contraseña guardada en el historial")
            
        elif choice == '2':
            print("\n--- AGREGAR CONTRASEÑA EXISTENTE ---")
            
            # Solicitar la contraseña existente
            existing_password = input("Ingresa la contraseña existente: ").strip()
            if not existing_password:
                print("❌ La contraseña no puede estar vacía")
                continue
            
            # Solicitar etiqueta para la contraseña
            tag = input("Ingresa una etiqueta para identificar esta contraseña (ej: Gmail, Facebook, Banco): ").strip()
            if not tag:
                tag = "Sin etiqueta"
            
            # Validar la contraseña existente (más flexible)
            print("\n--- VALIDANDO CONTRASEÑA ---")
            print("Selecciona el tipo de validación:")
            print("1. Validación estricta (8 caracteres, solo alfanumérica)")
            print("2. Validación flexible (mínimo 6 caracteres, permite símbolos)")
            print("3. no validar (solo agregar al historial)")
            
            validation_choice = input("Selecciona el tipo de validación (1-3): ").strip()
            
            if validation_choice == '1':
                is_valid, message = password_manager.validate_password(existing_password, check_duplicates=False)
            elif validation_choice == '2':
                is_valid, message = password_manager.validate_password(existing_password, check_duplicates=False, min_length=6, max_length=50)
            elif validation_choice == '3':
                is_valid = True
                message = "Validación omitida, contraseña agregada directamente al historial"
            else:
                print("❌ Opción inválida. Usando validación flexible por defecto.")
                is_valid, message = password_manager.validate_password(existing_password, check_duplicates=False, min_length=6, max_length=50)
            
            print(f"Validación: {message}")
            
            if is_valid:
                # Verificar si ya existe en el historial
                recent_passwords = [entry["password"] if isinstance(entry, dict) else entry for entry in password_manager.password_history["passwords"]]
                if existing_password in recent_passwords:
                    print("⚠️  ADVERTENCIA: Esta contraseña ya existe en tu historial")
                    overwrite = input("¿Deseas agregarla de todos modos? (s/n): ").strip().lower()
                    if overwrite not in ['s', 'si', 'sí', 'y', 'yes']:
                        print("Operación cancelada")
                        continue
                
                # Preguntar si quiere configurar preguntas de seguridad
                setup_questions = input("\n¿Deseas configurar preguntas de seguridad? (s/n): ").strip().lower()
                security_qa = None
                
                if setup_questions in ['s', 'si', 'sí', 'y', 'yes']:
                    security_qa = password_manager.select_security_questions()
                    print("\n✓ Preguntas de seguridad configuradas correctamente")
                
                # Guardar la contraseña existente
                password_manager.add_password(existing_password, tag, security_qa, is_existing=True)
                print(f"\n✓ Contraseña existente agregada: {existing_password}")
                print(f"✓ Etiqueta asignada: {tag}")
                print("✓ Contraseña guardada en el historial")
            else:
                print(f"❌ La contraseña no cumple los requisitos: {message}")
                print("\nConsejos para contraseñas seguras:")
                print("- Al menos una mayúscula, una minúscula y un número")
                print("- Mínimo 6 caracteres de longitud")
                print("- Evita información personal")
                
        elif choice == '3':
            password_manager.show_password_history()
            
        elif choice == '4':
            print("\n--- BUSCAR CONTRASEÑAS POR ETIQUETA ---")
            search_term = input("Ingresa el término de búsqueda: ").strip()
            if search_term:
                found_passwords = password_manager.search_passwords_by_tag(search_term)
                if found_passwords:
                    print(f"\n✓ Se encontraron {len(found_passwords)} contraseña(s):")
                    for index, entry in found_passwords:
                        date_str = entry.get("date", "Fecha desconocida")
                        if date_str != "Fecha desconocida":
                            try:
                                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                                date_formatted = date_obj.strftime("%d/%m/%Y %H:%M")
                            except:
                                date_formatted = "Fecha inválida"
                        else:
                            date_formatted = date_str
                        print(f"{index}. [{entry.get('tag', 'Sin etiqueta')}] {bcolors.OKCYAN} {entry.get('password', 'N/A')} {bcolors.ENDC} - {date_formatted}")
                else:
                    print("❌ No se encontraron contraseñas con esa etiqueta")
            else:
                print("❌ Debes ingresar un término de búsqueda")
                
        elif choice == '5':
            print("\n--- MODIFICAR ETIQUETA DE CONTRASEÑA ---")
            password_manager.show_password_history()
            if password_manager.password_history["passwords"]:
                try:
                    index = int(input("\nIngresa el número de la contraseña a modificar: "))
                    current_entry = password_manager.get_password_by_index(index)
                    if current_entry:
                        print(f"Contraseña actual: [{current_entry.get('tag', 'Sin etiqueta')}] {current_entry.get('password', 'N/A')}")
                        new_tag = input("Ingresa la nueva etiqueta: ").strip()
                        if new_tag:
                            if password_manager.update_password_tag(index, new_tag):
                                print("✓ Etiqueta actualizada correctamente")
                            else:
                                print("❌ Error al actualizar la etiqueta")
                        else:
                            print("❌ La etiqueta no puede estar vacía")
                    else:
                        print("❌ Número de contraseña inválido")
                except ValueError:
                    print("❌ Por favor ingresa un número válido")
                    
        elif choice == '6':
            print("\n--- ELIMINAR CONTRASEÑA ---")
            password_manager.show_password_history()
            if password_manager.password_history["passwords"]:
                try:
                    index = int(input("\nIngresa el número de la contraseña a eliminar: "))
                    entry_to_delete = password_manager.get_password_by_index(index)
                    if entry_to_delete:
                        print(f"Contraseña a eliminar: [{entry_to_delete.get('tag', 'Sin etiqueta')}] {entry_to_delete.get('password', 'N/A')}")
                        confirm = input("¿Estás seguro de eliminar esta contraseña? (s/n): ").strip().lower()
                        if confirm in ['s', 'si', 'sí', 'y', 'yes']:
                            removed_entry = password_manager.delete_password(index)
                            if removed_entry:
                                print("✓ Contraseña eliminada correctamente")
                            else:
                                print("❌ Error al eliminar la contraseña")
                        else:
                            print("Operación cancelada")
                    else:
                        print("❌ Número de contraseña inválido")
                except ValueError:
                    print("❌ Por favor ingresa un número válido")
                    
        elif choice == '7':
            password_manager.show_security_questions()
            
        elif choice == '8':
            security_qa = password_manager.select_security_questions()
            password_manager.password_history["security_qa"] = security_qa
            password_manager.save_history()
            print("\n✓ Preguntas de seguridad actualizadas")
            
        elif choice == '9':
            print("\n¡Hasta luego! Mantén tus contraseñas seguras.")
            break
            
        else:
            print("❌ Opción inválida. Por favor selecciona 1-9.")

if __name__ == "__main__":
    main()
