# Bot do gry

Projekt studencki wykonywany w ramach przedmiotów Labolatorium Przetwarzania Obrazu oraz Labolatorium Systemów Rozmytych.


### Do uruchomienia potrzebne są:

* python (3.6 <=)
* pipenv

### Uruchomienie projektu:

#### instalacja
```
> pipenv install
```
pipenv ma problemy z mechanizmem lockowania niektórych paczek, jeśli lockowanie trwa zbyt długo można je pominąć:
```
> pipenv install --skip-lock
```

#### setup
```
> pipenv run python setup.py
```
lub
```
> pipenv shell
> python setup.py
```
