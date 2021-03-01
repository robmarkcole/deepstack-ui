FROM malenurse/conda-base
LABEL developer="Robin Cole @robmarkcole"
LABEL docker_maintainer="Zach McDonough @malenurse"

EXPOSE 8501

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir -p /app
COPY app /app
WORKDIR /app

ENTRYPOINT [ "streamlit", "run"]
CMD ["deepstack-ui.py"]
