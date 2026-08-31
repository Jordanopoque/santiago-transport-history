# Santiago Transport History

Sistema para la recopilación, almacenamiento y análisis histórico de datos del transporte público de Santiago de Chile, utilizando información GTFS (General Transit Feed Specification).

## 📌 Introducción

**Santiago Transport History** es un proyecto orientado al análisis histórico de la información del transporte público de Santiago de Chile.

El sistema busca recopilar y almacenar diferentes versiones de los datos GTFS publicados para el transporte público, permitiendo posteriormente comparar la evolución de recorridos, paradas, horarios, frecuencias y otros elementos del sistema de transporte a través del tiempo.

El proyecto se encuentra actualmente en etapa de desarrollo. En esta primera fase se ha implementado la infraestructura inicial utilizando **Django, Django REST Framework, MySQL y Docker**, además de la importación de información GTFS a una base de datos relacional.

## 🎯 Objetivos

* Recopilar información histórica del transporte público de Santiago.
* Almacenar los datos GTFS en una base de datos estructurada.
* Mantener diferentes versiones de los datos para permitir análisis históricos.
* Exponer posteriormente la información mediante una API REST.
* Facilitar consultas sobre recorridos, paradas, viajes y horarios.
* Permitir futuras visualizaciones geográficas de los recorridos.
* Analizar cambios en el sistema de transporte a través del tiempo.

## 🛠️ Tecnologías utilizadas

* **Python 3.12**
* **Django 6.1**
* **Django REST Framework**
* **MySQL 8.4**
* **Docker / Docker Compose**
* **Git / GitHub**
* **GTFS (General Transit Feed Specification)**

## 📊 Datos GTFS

Actualmente se está utilizando el conjunto de datos GTFS correspondiente a:

**29 de agosto de 2026**

Los archivos utilizados incluyen:

* `agency.txt`
* `calendar.txt`
* `calendar_dates.txt`
* `feed_info.txt`
* `frequencies.txt`
* `levels.txt`
* `pathways.txt`
* `routes.txt`
* `shapes.txt`
* `stops.txt`
* `stop_times.txt`
* `trips.txt`

Estos datos permiten representar diferentes componentes del sistema de transporte público, incluyendo operadores, recorridos, paradas, viajes, horarios y geometrías de los recorridos.

## 🗄️ Estado actual de la base de datos

Hasta este avance se han implementado e importado correctamente:

| Entidad    | Registros | Estado         |
| ---------- | --------: | -------------- |
| Agencies   |         4 | ✅ Implementado |
| Routes     |       427 | ✅ Implementado |
| Stops      |    12.880 | ✅ Implementado |
| Trips      |         0 | ⏳ Pendiente    |
| Stop Times |         0 | ⏳ Pendiente    |
| Shapes     |         0 | ⏳ Pendiente    |

### Agencias actualmente registradas

* Red Metropolitana de Movilidad
* Metro de Santiago
* EFE Trenes de Chile
* Bus de Acercamiento Aeropuerto

## 🏗️ Arquitectura inicial

Actualmente el proyecto utiliza una arquitectura basada en contenedores:

```text
┌─────────────────────────────┐
│          Cliente            │
│      Navegador / API        │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│       Django / DRF          │
│       Python 3.12           │
│        Puerto 8001          │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│          MySQL 8.4          │
│      transport_history      │
│        Puerto 3307          │
└─────────────────────────────┘
```

Docker Compose permite levantar tanto el backend como la base de datos sin necesidad de instalar Django o MySQL directamente en el sistema operativo.

## 📁 Estructura del proyecto

```text
santiago_transport_history/
│
├── backend/
│   ├── config/
│   ├── transit/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── import_gtfs.py
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   └── views.py
│   │
│   ├── manage.py
│   └── db.sqlite3
│
├── gtfs/
│   └── GTFS_20260829/
│       ├── agency.txt
│       ├── calendar.txt
│       ├── calendar_dates.txt
│       ├── feed_info.txt
│       ├── frequencies.txt
│       ├── levels.txt
│       ├── pathways.txt
│       ├── routes.txt
│       ├── shapes.txt
│       ├── stops.txt
│       ├── stop_times.txt
│       └── trips.txt
│
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```

> `db.sqlite3` se mantiene fuera del control de versiones mediante `.gitignore`, ya que la base de datos utilizada por el proyecto es MySQL.

## 🚀 Ejecución del proyecto

Para iniciar los servicios mediante Docker:

```bash
docker compose up
```

El backend estará disponible en:

```text
http://localhost:8001
```

MySQL estará disponible desde el equipo local mediante:

```text
localhost:3307
```

Para acceder al contenedor de MySQL:

```bash
docker compose exec mysql mysql -u transport_user -ptransport_password transport_history
```

## 📥 Importación de datos GTFS

La importación se realiza mediante un comando personalizado de Django:

```bash
docker compose exec backend python manage.py import_gtfs
```

Actualmente el comando permite importar:

```text
agency.txt
routes.txt
stops.txt
```

y almacenarlos en las tablas correspondientes de MySQL.

## 🔄 Próximos avances

Las siguientes etapas contempladas para el desarrollo son:

* [ ] Importación de `trips.txt`.
* [ ] Importación de `stop_times.txt`.
* [ ] Incorporación de `shapes.txt`.
* [ ] Incorporación de `calendar.txt`.
* [ ] Manejo de diferentes versiones GTFS.
* [ ] Desarrollo de API REST.
* [ ] Endpoints para recorridos y paradas.
* [ ] Consultas históricas.
* [ ] Comparación entre versiones de GTFS.
* [ ] Visualización geográfica de recorridos.
* [ ] Estadísticas y análisis del transporte público.
* [ ] Documentación de la API.
* [ ] Pruebas automatizadas.

## 📌 Estado del proyecto

**Estado:** 🚧 En desarrollo

Este repositorio corresponde a la etapa inicial del proyecto y se irá actualizando progresivamente a medida que se incorporen nuevas funcionalidades y conjuntos de datos históricos.

---

**Santiago Transport History**
Proyecto de análisis y almacenamiento histórico de datos GTFS del transporte público de Santiago de Chile.
