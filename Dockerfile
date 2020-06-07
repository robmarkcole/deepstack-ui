FROM python:3.8
LABEL maintainer="Robin Cole @robmarkcole"

EXPOSE 8501

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir -p /app
COPY app /app
WORKDIR /app

ENTRYPOINT [ "streamlit", "run"]
CMD ["streamlit-ui.py"]