# Generador de Contraseñas Seguras

Este programa te ayuda a generar y administrar contraseñas seguras que cumplen con los siguientes requisitos:
- Exactamente 8 caracteres (para contraseñas generadas)
- Al menos una letra mayúscula
- Al menos una letra minúscula  
- Al menos un número
- Solo caracteres alfanuméricos (para contraseñas generadas)
- No puede repetir las últimas 4 contraseñas

## Características principales

- **Generación automática**: Crea contraseñas que cumplen todos los requisitos
- **Gestión de contraseñas existentes**: Permite agregar y organizar contraseñas que ya tienes
- **Sistema de etiquetas**: Organiza tus contraseñas por servicio (Gmail, Facebook, etc.)
- **Historial completo**: Mantiene un registro de las últimas 20 contraseñas
- **Preguntas de seguridad**: Sistema adicional de recuperación
- **Búsqueda por etiquetas**: Encuentra rápidamente tus contraseñas
- **Validación flexible**: Diferentes niveles de validación para contraseñas existentes

### Opciones del menú

**1. Generar nueva contraseña**
- Solicita una etiqueta para identificar la contraseña (ej: Gmail, Facebook, Banco)
- Crea automáticamente una contraseña que cumple todos los requisitos
- Te permite configurar preguntas de seguridad
- Guarda la contraseña con su etiqueta en el historial

**2. Agregar contraseña existente**
- Permite añadir contraseñas que ya tienes y usas
- Ofrece dos tipos de validación: estricta (8 caracteres alfanuméricos) o flexible (mínimo 6 caracteres, permite símbolos)
- Verifica si la contraseña ya existe en tu historial
- Asigna etiquetas para organizar tus contraseñas
- Opción de configurar preguntas de seguridad

**3. Ver historial de contraseñas**
- Muestra todas las contraseñas guardadas con sus etiquetas y fechas
- Formato: 🔐 [Etiqueta] Contraseña - Fecha (para contraseñas generadas)
- Formato: 📋 [Etiqueta] Contraseña - Fecha (para contraseñas existentes agregadas)

**4. Buscar contraseñas por etiqueta**
- Permite buscar contraseñas usando términos de búsqueda
- Busca en las etiquetas de forma parcial (no necesitas escribir la etiqueta completa)

**5. Modificar etiqueta de contraseña**
- Permite cambiar la etiqueta de una contraseña existente
- Útil para reorganizar y renombrar tus contraseñas

**6. Eliminar contraseña**
- Permite eliminar contraseñas del historial
- Incluye confirmación para evitar eliminaciones accidentales

**7. Ver preguntas de seguridad**
- Muestra las preguntas y respuestas de seguridad actuales

**8. Configurar preguntas de seguridad**
- Te permite seleccionar 3 preguntas de una lista de 10 opciones
- Guarda tus respuestas de forma segura

**9. Salir**
- Cierra el programa

## Archivos generados

El programa crea un archivo `password_history.json` que almacena:
- Historial de contraseñas (últimas 20) con etiquetas y tipos
- Preguntas y respuestas de seguridad
- Fechas de creación y modificación

### Formato del archivo JSON:
```json
{
  "passwords": [
    {
      "password": "A7bN9mP2",
      "tag": "Gmail",
      "date": "2025-06-22T10:30:00",
      "type": "generated"
    },
    {
      "password": "MiContraseña123!",
      "tag": "Facebook",
      "date": "2025-06-22T11:00:00",
      "type": "existing"
    }
  ],
  "security_qa": [
    {
      "question": "¿En qué ciudad naciste?",
      "answer": "Santiago",
      "date": "2025-06-22T10:30:00"
    }
  ]
}
```

## Características de seguridad

- **Validación automática**: Verifica que cada contraseña cumpla los requisitos mínimos
- **Validación flexible**: Para contraseñas existentes, permite diferentes niveles de validación
- **No repetición**: Evita generar contraseñas iguales a las últimas 4
- **Detección de duplicados**: Avisa si intentas agregar una contraseña que ya existe
- **Almacenamiento local**: Los datos se guardan solo en tu computador
- **Preguntas de seguridad**: Sistema adicional de recuperación
- **Organización por etiquetas**: Mantén tus contraseñas organizadas por servicio

## Tipos de contraseñas

### Contraseñas generadas (🔐)
- Creadas automáticamente por el programa
- Cumplen estrictamente todos los requisitos (8 caracteres alfanuméricos)
- Garantía de seguridad máxima

### Contraseñas existentes (📋)
- Contraseñas que ya tienes y quieres agregar al sistema
- Validación flexible: mínimo 6 caracteres, permite símbolos
- Útil para consolidar todas tus contraseñas en un solo lugar

## Uso recomendado

1. **Para nuevas cuentas**: Usa la opción "Generar nueva contraseña"
2. **Para cuentas existentes**: Usa "Agregar contraseña existente" para organizar tus contraseñas actuales
3. **Organización**: Usa etiquetas descriptivas como "Gmail", "BancoChile", "Netflix", etc.
4. **Seguridad**: Configura preguntas de seguridad para recuperación adicional
5. **Mantenimiento**: Usa las opciones de búsqueda y modificación para mantener tu historial organizado
