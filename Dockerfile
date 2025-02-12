FROM python:3.10

# 作業ディレクトリを設定
WORKDIR /app

RUN apt-get update &&\
    apt-get -y install locales &&\
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

# poetryをインストール
RUN pip install poetry

# Poetryのパスの設定
ENV PATH /root/.local/bin:$PATH

# Poetryが仮想環境を生成しないようにする
RUN poetry config virtualenvs.create false

# Dockerへファイルをコピー
COPY ./ ./

# pyproject.toml, poetry.lockをコピー・インストール
RUN poetry install

# Cloud Functions の実行環境をエミュレート（ホットリロードしたいので、flaskアプリとして起動）
# CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=8080", "--reload"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
# CMD ["functions-framework --target hello_world --source src/flocky_gcp/main.py --port 5000"]