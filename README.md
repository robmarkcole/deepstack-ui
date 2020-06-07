# deepstack-ui
Unofficial UI for working with Deepstack.

Run deepstack object detection:

```
docker run -e VISION-DETECTION=True \
-v localstorage:/datastore \
-p 5000:5000 \
-e API-KEY="" \
--name deepstack \
deepquestai/deepstack:noavx
```

Edit the deepstack credentials in `streamlit-ui.py` and run the app:
```
venv/bin/streamlit run streamlit-ui.py
```

<p align="center">
<img src="https://github.com/robmarkcole/deepstack-ui/blob/master/usage.png" width="800">
</p>

## Run with Docker
From the root dir, build from source:
```
    docker build -t deepstack-ui .
    docker run -p 8501:8501 -e DEEPSTACK_IP='192.168.1.133' deepstack-ui:latest
```

Alternatively run the pre-built image: `docker run -p 8501:8501 -e DEEPSTACK_IP='192.168.1.133' robmarkcole/deepstack-ui:latest`

Then visit [localhost:8501](http://localhost:8501/)

## Development
Use venv:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade -r requirements.txt
```