#CONTAINER TEMPLATE
FROM python:3.9-slim-bookworm

RUN echo $PATH

WORKDIR /opt/python_generic

#install requirements
COPY requirements.txt /opt/python_generic
RUN pip install -r requirements.txt

# copy the script
COPY python-generic /opt/python_generic

# add the script callers to path
ENV PATH="/opt/python_generic/bin:$PATH"