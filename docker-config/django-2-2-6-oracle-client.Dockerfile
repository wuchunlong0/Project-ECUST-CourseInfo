FROM maodouzi/django:v2.2.6

RUN pip install cx-Oracle \
    && mkdir -p /opt/oracle \
    && cd /opt/oracle \
    && wget https://download.oracle.com/otn_software/linux/instantclient/193000/instantclient-basic-linux.x64-19.3.0.0.0dbru.zip \
    && unzip instantclient-basic-linux.x64-19.3.0.0.0dbru.zip \
    && apt-get install -y libaio1 libaio-dev \
    && sh -c "echo /opt/oracle/instantclient_19_3 > /etc/ld.so.conf.d/oracle-instantclient.conf" \
    && ldconfig \
    && mkdir -p /opt/oracle/instantclient_12_2/network/admin
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_19_3
