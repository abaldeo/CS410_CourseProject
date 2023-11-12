## Backend Development

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
 

## Fixing Issues with PDM 

If you run into issues adding packages with pdm, try running these commands
```
/home/vscode/.local/share/pdm/venv/bin/python -m pip install -U 
/home/vscode/.local/share/pdm/venv/bin/python -m pip install --upgrade pip
pdm fix
```


Also you can avoid having to use pdm run command everything by adding this

```echo "source /workspaces/CS410_CourseProject/src/backend/.venv/bin/activate" >> ~/.bashrc```