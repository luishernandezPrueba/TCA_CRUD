# TCA Project - Student Management System

Sistema de gestión de estudiantes desarrollado con FastAPI y MySQL.

## Descripción

API REST para la administración de estudiantes y su información relacionada (correos electrónicos, teléfonos y direcciones).

## Tecnologías

- **Backend:** FastAPI
- **Base de datos:** MySQL (async)
- **ORM:** SQLAlchemy 2.0
- **Frontend:** HTML, CSS, JavaScript + Jinja2 Templates
- **Deployment:** Railway

## Estructura del Proyecto

```
app/
├── src/
│   ├── app.py                 # Punto de entrada de la aplicación
│   ├── database/
│   │   ├── database.py        # Configuración de conexión a BD
│   │   └── init_db.py         # Inicialización de tablas
│   ├── models/                # Modelos SQLAlchemy
│   │   ├── student.py
│   │   ├── address.py
│   │   ├── email.py
│   │   └── phone.py
│   ├── schemas/               # Schemas Pydantic
│   ├── services/              # Lógica 
│   ├── routes/                # Endpoints de la API
│   ├── static/                # Archivos estáticos (CSS, JS)
│   └── templates/             # Templates HTML
├── requirements.txt
├── Procfile
└── railway.json
```

## Instalación Local

### Prerrequisitos

- Python 3.11+
- MySQL 8.0+

### Pasos

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd TCA_Proyect
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   cd app
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   
   Crear archivo `app/src/.env`:
   ```env
   DATABASE_URL=mysql+asyncmy://usuario:contraseña@localhost:3306/students
   ```

5. **Inicializar la base de datos**
   ```bash
   cd src
   python -c "from database.init_db import init_db; init_db()"
   ```

6. **Ejecutar la aplicación**
   ```bash
   uvicorn app:app --reload
   ```

7. **Acceder a la aplicación**
   - Frontend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## API Endpoints

### Estudiantes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/students` | Listar todos los estudiantes |
| GET | `/api/v1/students/{id}` | Obtener un estudiante por ID |
| GET | `/api/v1/students/lastName/{lastName}` | Buscar por apellido |
| POST | `/api/v1/students` | Crear estudiante |
| PATCH | `/api/v1/students/{id}` | Actualizar estudiante |
| DELETE | `/api/v1/students/{id}` | Eliminar estudiante |

### Correos Electrónicos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/emails` | Listar todos los correos |
| GET | `/api/v1/emails/student/{student_id}` | Correos de un estudiante |
| POST | `/api/v1/emails` | Crear correo |
| PATCH | `/api/v1/emails/{email}` | Actualizar correo |
| DELETE | `/api/v1/emails/{email}` | Eliminar correo |

### Teléfonos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/phones` | Listar todos los teléfonos |
| GET | `/api/v1/phones/student/{student_id}` | Teléfonos de un estudiante |
| POST | `/api/v1/phones` | Crear teléfono |
| PATCH | `/api/v1/phones/{phone_id}` | Actualizar teléfono |
| DELETE | `/api/v1/phones/{phone_id}` | Eliminar teléfono |

### Direcciones
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/addresses` | Listar todas las direcciones |
| GET | `/api/v1/addresses/student/{student_id}` | Direcciones de un estudiante |
| POST | `/api/v1/addresses` | Crear dirección |
| PATCH | `/api/v1/addresses/{address_id}` | Actualizar dirección |
| DELETE | `/api/v1/addresses/{address_id}` | Eliminar dirección |

## Modelo de Datos

```
┌─────────────┐       ┌─────────────┐
│   Student   │       │    Email    │
├─────────────┤       ├─────────────┤
│ student_id  │──┐    │ email (PK)  │
│ first_name  │  │    │ email_type  │
│ middle_name │  ├───<│ student_id  │
│ last_name   │  │    └─────────────┘
│ gender      │  │
│ created_at  │  │    ┌─────────────┐
│ updated_at  │  │    │    Phone    │
└─────────────┘  │    ├─────────────┤
                 │    │ phone_id    │
                 ├───<│ phone       │
                 │    │ phone_type  │
                 │    │ country_code│
                 │    │ area_code   │
                 │    │ student_id  │
                 │    └─────────────┘
                 │
                 │    ┌─────────────┐
                 │    │   Address   │
                 │    ├─────────────┤
                 └───<│ address_id  │
                      │ address_line│
                      │ city        │
                      │ state       │
                      │ zip_postcode│
                      │ student_id  │
                      └─────────────┘
```

## Deployment en Railway

## Funcionalidades

- ✅ Alta de estudiantes
- ✅ Alta de datos relacionados (correo, teléfono, dirección)
- ✅ Listado de estudiantes
- ✅ Detalle de estudiante
- ✅ Modificación de estudiante y datos relacionados
- ✅ Eliminación de estudiante e información relacionada
- ✅ Eliminación de elementos asociados individualmente


