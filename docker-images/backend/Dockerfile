FROM alpine:3.9
RUN apk add --update python3 && python3 -m ensurepip && rm -r /usr/lib/python*/ensurepip && pip3 install --upgrade pip setuptools
RUN apk add bash
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt
COPY app.py /usr/src/app/
EXPOSE 5000
CMD python3 /usr/src/app/app.py &
