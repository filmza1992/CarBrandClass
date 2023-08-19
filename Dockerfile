FROM python:3.10.6

# 
WORKDIR /CarBrandClass

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

# 
COPY ./requirements.txt /CarBrandClass/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /CarBrandClass/requirements.txt

# 
COPY ./app /CarBrandClass/app
COPY ./model /CarBrandClass/model

ENV PYTHONPATH "${PYTHONPATH}:/CarBrandClass"

# a
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]