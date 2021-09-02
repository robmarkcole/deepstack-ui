FROM python:3.8
LABEL maintainer="Robin Cole @robmarkcole"

EXPOSE 8501

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app /app

ENTRYPOINT [ "streamlit", "run"]
CMD ["deepstack-ui.py"]
