# CS410_CourseProject

## Overview

CourseBuddyAI is a Chrome extension designed to enhance the Coursera Online Learning Platform, allowing students to upload lecture transcripts and slides for automated summarization. These documents will be indexed in a vector database. Subsequently, we will employ the Retrieval Augmentation Generation (RAG) technique, in combination with a large language model like ChatGPT to build a Q&A chatbot interface based on the uploaded course content. The full project proposal and progress reports are stored in this repository under the reports folder. 

## :point_right: **Attention Peer Reviewers & TA's :exclamation:** 
Please see the links below for the project submission grading
1. [Project Proposal](https://github.com/abaldeo/CS410_CourseProject/blob/main/reports/CS410%20Project%20Proposal.pdf)
2. [Project Progess Report](https://github.com/abaldeo/CS410_CourseProject/blob/main/reports/CS410%20Project%20Progress%20Report.pdf)
3. [Project Final Report](https://github.com/abaldeo/CS410_CourseProject/blob/main/reports/CS410%20Project%20Final%20Status%20Report.pdf)
4. [Project Documentation](https://github.com/abaldeo/CS410_CourseProject/blob/main/docs/CS410%20Project%20Documentation.pdf)
5. [Project Presentation Slides](https://github.com/abaldeo/CS410_CourseProject/blob/main/docs/CS410%20Project%20Presentation%20Deck.pdf)
6. [Project Presentation & Demo ] ()
   

## Team Members

**Team Name:** CourseBuddyAI

**Team Members:**

- Avinash Baldeo (@abaldeo2)
- Zach Pohl (@zcpohl2)
- Colton Bailey (@coltonb4)
- ~~Ehsan Sarfaraz (@ehsans3)~~ 
- Kacper Dural (@kdural2)


## Tech Stack

- **FastAPI** with Python 3.11
- **React 16** with Typescript, Redux, and react-router
- Postgres (asyncpg)
- SqlAlchemy with Alembic for migrations
- Pytest for backend tests
- Jest for frontend tests
- Prettier/Eslint (with Airbnb style guide)
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
$tree . -d                                                           
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

