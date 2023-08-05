# RISC-V SERVER/BACKEND

## Clone project to development

### 1. Clone project:

```shell
git clone https://github.com/truongthienloc/risc-v-backend.git
cd risc-v-backend
git checkout develop
```

### 2. Create and use env for project:

```shell
pip install virtualenv
virtualenv env
env/Scripts/activate.bat
```

### 3. Install library to project:

```shell
pip install -r requirements.txt
```

### 4. You will code in *app.py*

## Run code in development

```shell
flask run
```

## Prepare before deploying

```shell
pip freeze > requirements.txt
```

## Production

To use this code in production, you create **merge request** to *main* branch