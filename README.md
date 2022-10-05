# RSA Algorithm Trial
### Remote Sensing in Agriculture

<br>

## Setup

### Dev Setup

creating virtual environment and installing dependencies.

```powershell
$ mkdir .venv
$ pipenv install --dev
```

create `.env` file with `API_KEY` variable.

file:.env
```text
API_KEY=<your spectator api key>
```

from the `main.ipynb` jupyter notebook, select the `pipenv` virtual environment and install kernel if required, and run cells to see the output.

If you want to test the algorithm run the main file.

```powershell
$ pipenv shell
$ python main.py
```

### Normal Setup

creating virtual environment and installing dependencies.

```powershell
$ mkdir .venv
$ pipenv install
```

create `.env` file with `API_KEY` variable.

file:.env
```text
API_KEY=<your spectator api key>
```

run the program by running the following command:

```powershell
$ pipenv run python main.py
```