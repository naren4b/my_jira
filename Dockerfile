FROM python:3.12.4-alpine3.20
COPY app.py ./
COPY requirements.txt ./ 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
ENV USERID=userid
ENV PASSWORD=password
ENV URI=url


ENTRYPOINT [ "python", "app.py" ]
