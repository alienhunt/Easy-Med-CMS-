# pull python 3 image from docker hub or from local fs
FROM python:3.8

LABEL name="Pragyanshu Rai" \
email="pragyanshur@gmail.com"

# -----------------------------------------------------------------------------------------


ENV PYTHONBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 
ENV DJ_PORT=8000
ENV MY_PHONE_NUMBER="+917893153980"

# create a directory 'apps'
RUN mkdir /apps

# add all the files in the apps directory
ADD . /apps/ 

# make /apps the pwd
WORKDIR /apps

# run a pip command to install everything listed in the requirements.txt file
# install environment dependencies
# Install project dependencies
RUN pip install -r requirements.txt; \
pip3 install --upgrade pip; \
apt-get autoremove; 

# expose container port number
EXPOSE 8000

CMD gunicorn CMS.wsgi:application --bind 0.0.0.0:$DJ_PORT
# CMD [ "pip", "freeze" ]