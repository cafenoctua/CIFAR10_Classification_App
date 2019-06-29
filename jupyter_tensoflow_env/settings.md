# コンテナに入る
docker exec -it jupyter_tensorflow /bin/sh -c "[ -e /bin/bash ] && /bin/bash || /bin/sh"

# パスワード設定
- dockerコンテナ内部にexecで入り以下コマンドを実行
``` パスワード設定コマンド
python -c 'from notebook.auth import passwd;print(passwd())'

export JUPYTERTOKEN="YOUR_PASSWORD_HASH_VALUE"
```

# Jupyter実行
start-notebook.sh \
--NotebookApp.password=$JUPYTERTOKEN --port Your docker-compose setting ports