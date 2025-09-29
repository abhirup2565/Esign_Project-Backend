FROM python:3.13.5

#set a directory for the app
WORKDIR /usr/src/app

#copy all the file from container
COPY . .

#install dependency
RUN pip install --no-cache-dir -r requirements.txt

# tell the port number the container should expose
EXPOSE 8000
