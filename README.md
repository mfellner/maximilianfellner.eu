##### Description

This is the source code of maximilianfellner.eu.

It is based on an **AngularJS** frontend in JavaScript and a **Flask** backend in Python.

##### Development

###### [Vagrant](http://www.vagrantup.com) Setup

```bash
vagrant up
```

###### Manual Setup

Pull git submodules.

```bash
git submodule init
git submodule update
```

Install Python dependencies.

```bash
virtualenv .
source bin/activate
pip install -r requirements.txt
```

Intall node dependencies.

```bash
node install
```

###### Debug

```bash
python wsgi.py db upgrade
python wsgi.py assets build
python wsgi.py runserver
```
