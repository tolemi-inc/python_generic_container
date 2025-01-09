#CONTAINER TEMPLATE
FROM python:3.9-slim-bookworm

RUN echo $PATH

WORKDIR /opt/python-generic

#install requirements
COPY requirements.txt /opt/python-generic
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN pip install playwright
RUN playwright install --with-deps

# copy the script
COPY python-generic /opt/python-generic

# add the script callers to path
ENV PATH="/opt/python-generic/bin:$PATH"