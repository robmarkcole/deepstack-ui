# deepstack-ui
UI for working with [Deepstack](https://python.deepstack.cc/). Allows uploading an image and performing object detection with Deepstack. The effect of various parameters can be explored, including filtering the classes of object detected, filtering by minimum confidence (%), and spatial filtering using a region of interest (ROI).

<p align="center">
<img src="https://github.com/robmarkcole/deepstack-ui/blob/master/usage.png" width="1000">
</p>

## Run deepstack
Run deepstack object detection:

```
docker run -e VISION-DETECTION=True -p 5000:5000 -e API-KEY="" -e MODE=High deepquestai/deepstack:latest
```

You will need the ip address of the machine running deepstack, which is passed to the Streamlit app using an environment variable.

## Run deepstack-ui with Docker
The `deepstack-ui` is designed to be run in a docker container. The UI picks up the information about your deepstack instance from environment variables which are passed into the container using the `-e VARIABLE=value` approach. All environment variables that can be passed are listed below:
```
- DEEPSTACK_IP : the IP address of your deepstack instance, default "localhost"
- DEEPSTACK_PORT : the PORT of your deepstack instance, default 80
- DEEPSTACK_API_KEY : the API key of your deepstack instance, if you have set one
- DEEPSTACK_TIMEOUT : the timeout to wait for deepstack, default 10 seconds
```

From the root dir, build the deepstack-ui container from source and then run the UI, passing the `DEEPSTACK_IP` environment variable:
```
    docker build -t deepstack-ui .
    docker run -p 8501:8501 -e DEEPSTACK_IP='192.168.1.133' deepstack-ui:latest
```
The UI is now viewable at [http://localhost:8501](http://localhost:8501) (not whatever ip address is shown in the logs, this is the internal docker ip)

Alternatively if you are running deepstack with non default parameters, an example would be:
```
docker run -p 8501:8501 \
-e DEEPSTACK_IP='192.168.1.133' \
-e DEEPSTACK_PORT=5000 \
-e DEEPSTACK_API_KEY='my_key' \
-e DEEPSTACK_TIMEOUT=20 \
robmarkcole/deepstack-ui:latest`
```

### FAQ
Q1: I get the error: `TypeError: cannot unpack non-iterable DeepstackException object`

A1: You probably didn't pass the required environment variables (`DEEPSTACK_IP` etc.)

------

## Development
* Create and activate a venv: `python3 -m venv venv` and `source venv/bin/activate`
* Install requirements: `pip3 install -r requirements.txt`
* Export required environment variables: `export DEEPSTACK_IP='192.168.1.133'`
* Run streamlit from `app` folder: `streamlit run deepstack-ui.py`