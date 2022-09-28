FROM ubuntu

COPY . /Blogsite
WORKDIR /Blogsite
Run ls .
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  python3-pip \
  python3-dev \
  default-libmysqlclient-dev \
  build-essential \
  gunicorn \
  && rm -rf /var/lib/apt/lists/*
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn","--chdir","/Blogsite", "--bind", ":8000", "--workers", "3", "blog.wsgi:application"]
