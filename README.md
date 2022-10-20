build image:

```shell
docker build . -t sbertest:local
```

run service:

```shell
docker run --rm -p 5000:5000 sbertest:local
```

make requests:

```shell
curl localhost:5000/import/xlsx
```

```shell
curl localhost:5000/export/sql
curl localhost:5000/export/sql?lag_num=5
```

```shell
curl localhost:5000/export/pandas
curl localhost:5000/export/pandas?lag_num=5
```

