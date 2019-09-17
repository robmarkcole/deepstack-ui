# deepstack-web-ui
Unofficial web UI for working with Deepstack.

Run deepstack object detection:

```
$ docker run -e VISION-DETECTION=True -d \
      -v localstorage:/datastore -p 5000:5000 \
      -e API-KEY="Mysecretkey" \
       --name deepstack deepquestai/deepstack:noavx
```

Edit the deepstack credentials in `app/server.py` and run the app:
```
$ python3 app/server.py serve
```

<p align="center">
<img src="https://github.com/robmarkcole/deepstack-web-ui/blob/master/usage.jpg" width="500">
</p>

## Development
Use venv:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade -r requirements.txt
```

## References
* This code is a fork of https://github.com/render-examples/fastai-v3
