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
<img src="https://github.com/robmarkcole/deepstack-web-ui/blob/master/usage.png" width="600">
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
