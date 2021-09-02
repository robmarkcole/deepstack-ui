FROM ubuntu:20.04
LABEL maintainer="Robin Cole @robmarkcole"

EXPOSE 8501

WORKDIR /root
SHELL ["/bin/bash", "-c"]
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y apt-utils
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN apt-get install -y build-essential git wget sudo pkg-config curl dbus cmake vim nano python3 python3-pip python3-setuptools libjemalloc-dev libboost-dev libboost-filesystem-dev libboost-system-dev libboost-regex-dev autoconf flex bison libssl-dev llvm-10
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN pip install --upgrade pip
RUN pip install numpy==1.17.3 cython pygments==2.4.1
RUN export ARROW_HOME=/usr/local/lib
RUN export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

WORKDIR /root
RUN wget --no-check-certificate https://github.com/apache/arrow/archive/apache-arrow-3.0.0.tar.gz
RUN tar -xvf apache-arrow-3.0.0.tar.gz
RUN mkdir -p /root/arrow-apache-arrow-3.0.0/cpp/build
WORKDIR /root/arrow-apache-arrow-3.0.0/cpp/build
RUN cmake -DCMAKE_INSTALL_PREFIX=$ARROW_HOME -DCMAKE_INSTALL_LIBDIR=lib -DARROW_WITH_BZ2=ON -DARROW_WITH_ZLIB=ON -DARROW_WITH_ZSTD=ON -DARROW_WITH_LZ4=ON -DARROW_WITH_SNAPPY=ON -DARROW_PARQUET=ON -DARROW_PYTHON=ON -DARROW_BUILD_TESTS=OFF ..
RUN make -j4
RUN make install
WORKDIR /root/arrow-apache-arrow-3.0.0/python
RUN python setup.py build_ext --build-type=release --with-parquet
RUN python setup.py install

WORKDIR /root
RUN rm -R *
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get remove -y build-essential wget pkg-config apt-utils cmake vim nano libjemalloc-dev libboost-dev libboost-filesystem-dev libboost-system-dev libboost-regex-dev autoconf flex bison libssl-dev
RUN apt-get autoremove -y

RUN mkdir -p /app
COPY app /app
WORKDIR /app

ENTRYPOINT [ "streamlit", "run"]
CMD ["deepstack-ui.py"]
