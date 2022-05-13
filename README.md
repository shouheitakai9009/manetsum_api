# ツムツム管理API

## インストール方法
1. `source env/bin/activate` でvenvに入る
2. `pip install -r requirements.txt` でパッケージインスコ
3. `python manage.py migrate` でDB作成（※Sequel AceってMysqlクライアントが結構いい もしくは `mysql.server start & mysql -u root`でCUI入る）
4. `python manage.py loaddata api/fixtures/character.json` でseedデータ投入
5. `python manage.py runserver` で起動