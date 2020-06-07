# deepstack-ui
UI for working with [Deepstack](https://python.deepstack.cc/). Allows uploading an image and performing object detection with deepstack. The effect of various parameters can be explored, including filtering the classes of object detected, filtering by minimum confidence (%), and spatial filtering using a regoin of interest (ROI).

<p align="center">
<img src="https://github.com/robmarkcole/deepstack-ui/blob/master/usage.png" width="1000">
</p>

## Run deepstack
Run deepstack object detection:

```
docker run \
-e VISION-DETECTION=True \
-v localstorage:/datastore \
-p 5000:5000 \
-e API-KEY="" \
--name deepstack \
deepquestai/deepstack:noavx
```

You will need the ip address of the machine running deepstack, which is passed to the streamlit app.

## Run with Docker
From the root dir, build from source:
```
    docker build -t deepstack-ui .
    docker run -p 8501:8501 -e DEEPSTACK_IP='192.168.1.133' deepstack-ui:latest
```

Alternatively run the [pre-built](https://hub.docker.com/repository/docker/robmarkcole/deepstack-ui) image:
```
docker run -p 8501:8501 -e DEEPSTACK_IP='192.168.1.133' robmarkcole/deepstack-ui:latest`
```
Or if you are running deepstack with non default parameters, an example would be:
```
docker run -p 8501:8501 \
-e DEEPSTACK_IP='192.168.1.133' \
-e DEEPSTACK_PORT=5000 \
-e DEEPSTACK_API_KEY='my_key' \
-e DEEPSTACK_TIMEOUT=20 \
robmarkcole/deepstack-ui:latest`
```

Then visit [localhost:8501](http://localhost:8501/) (not whatever ip address is shown in the logs, this is the internal docker ip)

### FAQ
Q1: I get the error: `TypeError: cannot unpack non-iterable DeepstackException object`

A1: You probably didn't pass the required environment variables (`DEEPSTACK_IP` etc.)

------