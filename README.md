# RevasBot

Revas Simulations made simple

Now with **SPEED**

***

## Requirements

* Newest `Anaconda` or `Miniconda` **OR** Python 3.9.7
* `Microsoft Edge` (HA!)
* `Microsoft Edge Driver`

***

## Installation

### Anaconda

#### Create Anaconda Virtual Environment

```cmd
conda env create -f environment.yml
```

#### Export Anaconda Virtual Environment

```cmd
conda env export --no-builds > environment.yml
```

#### Activate Anaconda Virtual Environment

```cmd
conda activate revasbot
```

#### Deactivate Anaconda Virtual Environment

```cmd
conda deactivate
```

### pipenv

#### Create pipenv Virtual Environment

```cmd
python -m venv revasbot
```

##### Activate Virtual Environment

###### Unix/macOS

```bash
source env/bin/activate
```

###### Windows

```cmd
.\env\Scripts\activate
```

##### Install packages from `requirements.txt`

```cmd
pip install -r requirements.txt
```

#### Export PIP package list

```cmd
pip freeze > requirements.txt
```

***

## Usage

### Start Bot

```cmd
python -m main
```

At some point, bot will stop working.
Open the terminal where it's working.
You'll be asked to choose the game for the bot.  
After selecting a game, the bot will continue working.

***

## Additional features

### Colorful CMD!
RevasBot uses ANSI codes for colorful messages.
On Windows, if you are using `Command Line`,
you need to install [ansicon](https://github.com/adoxa/ansicon/).

### Change Python file according to PEP-8 **IN-PLACE**

```
autopep8 <file_name> -i
```

### Check PyLint score

```cmd
pylint <module_name>
```

### Check PyLint score with statistics

```cmd
pylint <module_name> -r y
```
