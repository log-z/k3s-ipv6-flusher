FROM python:3-slim

WORKDIR /usr/local/k3s-ipv6-flusher

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "app.py" ]
