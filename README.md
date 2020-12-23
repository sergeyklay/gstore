# ghsync

A dead simple tool to synchronize organizations' repositories from GitHub.

## Usage

### Sync all repos from all organizations

``` sh
$ python ghsync.py   \
    --token "$TOKEN" \
    --user  "$USER"  \
    --               \
    ~/work
```

### Sync all repos from Acme organization

``` sh
$ python ghsync.py   \
    --token "$TOKEN" \
    --org   Acme     \
    --               \
    ~/work
```

### Sync all repos from Foo, Bar and Baz organizations

``` sh
$ python ghsync.py      \
    --token "$TOKEN"    \
    --org   Foo Bar Baz \
    --                  \
    ~/work
```

## License

This project is open source software licensed under the GNU General Public
Licence version 3.  © 2020 Serghei Iakovlev
