# RevasBot

Revas Simulations made simple

Now with __SPEED__

## Requirements

* Newest `Anaconda` or `Miniconda`
* `Microsoft Edge` (HA!)
* `Microsoft Edge Driver`

## Export Anaconda Virtual Environment

```cmd
conda env export --no-builds > environment.yml
```

## Import Anaconda Virtual Environment

```
conda env create -f environment.yml
```

**OR**

```
conda env create -n revasbot -f requirements.txt
```

## Activate Anaconda Virtual Environment

```
conda activate revasbot
```

## Deactivate Anaconda Virtual Environment

```
conda deactivate
```

## Start Bot

```
python ./main.py
```

## Change Python file according to PEP-8 **IN-PLACE**

```
autopep8 <file_name> -i
```

## Check PyLint score

```
pylint <file_name>
```

## Check PyLint score with statistics

```
pylint <file_name> -r y
```
