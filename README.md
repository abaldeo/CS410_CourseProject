# CS410_CourseProject

To install packages using follow these steps:

1. Open a terminal in your dev container.
2. Change the current directory to the `src/backend` directory by running the command
   `cd src/backend`
4. Install the packages using pdm
   `pdm install`

To run a script using pdm, follow these steps:
1. Open a terminal in your dev container.
2. Change the current directory to `src/backend` of your project.
   `cd src/backend`
4. Run the script using pdm
   `pdm run python app/main.py`

To add new backend service, follow these steps:
   1. Add new service folder & the following files under `src/backend/app/api/api_v1/services`
      ```
      │       ├── api
      │       │   ├── api_v1
      │       │   │   └── services
      │       │   │   |  └── service_name
      │       │   │   |  |   └── __init__.py  # export router (critical)
      │       │   │   |  |   └── core.py # define logic
      │       │   │   |  |   └── service.py # define routes
      │       │   │   |  |   └── main.py # use to test locally
      ```
   2. then add router to `__init__.py` in top-level services folder
      ```
      from .service_name import service_name_router # exported router name
      service_router.include_router(service_name_router)      
      ```
   4. To test service independently, update main.py & run
      ```pdm run python service_name/main.py```

## Features

- **FastAPI** with Python 3.8
- **React 16** with Typescript, Redux, and react-router
- Postgres
- SqlAlchemy with Alembic for migrations
- Pytest for backend tests
- Jest for frontend tests
- Perttier/Eslint (with Airbnb style guide)
- Docker compose for easier development
- Nginx as a reverse proxy to allow backend and frontend on the same port

## Development

The only dependencies for this project should be docker and docker-compose.

### Quick Start

The following commands with initalize the app, build and start all the containers, then tail the docker-compose logs

```bash
cd CourseBuddyAI
make open
make init
```

Once you see the following logs, reload your browser

```
CourseBuddyAI-frontend-1  | Starting the development server...
CourseBuddyAI-frontend-1  | Compiled successfully!
```

## The Details

Starting the project with hot-reloading enabled
(the first time it will take a while):

```bash
docker-compose up -d
```

To run the alembic migrations (for the users table):

```bash
docker-compose run --rm backend alembic upgrade head
```

And navigate to http://localhost:8000

_Note: If you see an Nginx error at first with a `502: Bad Gateway` page, you may have to wait for webpack to build the development server (the nginx container builds much more quickly)._

Auto-generated docs will be at
http://localhost:8000/api/docs

### Rebuilding containers:

```
docker-compose build
```

### Restarting containers:

```
docker-compose restart
```

### Bringing containers down:

```
docker-compose down
```

### Frontend Development

Alternatively to running inside docker, it can sometimes be easier
to use npm directly for quicker reloading. To run using npm:

```
cd frontend
npm install
npm start
```

This should redirect you to http://localhost:3000

### Frontend Tests

```
cd frontend
npm install
npm test
```

## Migrations

Migrations are run using alembic. To run all migrations:

```
docker-compose run --rm backend alembic upgrade head
```

To create a new migration:

```
alembic revision -m "create users table"
```

And fill in `upgrade` and `downgrade` methods. For more information see
[Alembic's official documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script).

## Testing

There is a helper script for both frontend and backend tests:

```
./scripts/test.sh
```

### Backend Tests

```
docker-compose run backend pytest
```

any arguments to pytest can also be passed after this command

### Frontend Tests

```
docker-compose run frontend test
```

This is the same as running npm test from within the frontend directory

## Logging

```
docker-compose logs
```

Or for a specific service:

```
docker-compose logs -f name_of_service # frontend|backend|db
```

## Project Layout

```bash
$tree . -d                                                           3:30:31
.
├── backend
│   └── app
│       ├── __pycache__
│       ├── alembic # where migrations are located
│       ├── api
│       │   ├── api_v1
│       │   │   └── routers
│       │   │       └── tests
│       │   │   └── services
│       │   └── dependencies
│       ├── core    # config
│       ├── db      # db models
│       ├── tests   # pytest
│       └── main.py # entrypoint to backend
├── docs
├── frontend
│   ├── extension #chrome extension
│   ├── public
│   └── src
│       ├── __tests__
│       ├── admin
│       │   └── Users
│       ├── config # constants
│       ├── utils
│       ├── views
│       ├── index.tsx   # entrypoint
│       └── App.tsx     # handles routing
├── nginx
└── scripts
```


For testing: If you want to run the extension on chrome, navigate to:
```
./src/frontend/extension
```
From here, run 
```
npm run dev
```
This will create a build folder insie of this directory which contains
```
chrome-mv3-dev
```
Then, to load the extension, navigate to Chrome's manage extension menu and click Load Unpacked, selecting the 
```
chrome-mv3-dev
```
folder
