FROM python:3.10-slim

ARG GIT_COMMIT=unspecified
LABEL git_commit=$GIT_COMMIT

WORKDIR /usr/src/app

RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2 \
    && env LANG=C apt-get update -o Acquire::Languages=none -y \
    && env LANG=C apt-get upgrade -o Acquire::Languages=none -y \
    && env LANG=C apt-get install -y --no-install-recommends -o Dpkg::Options::=--force-unsafe-io \
    && pip install pipenv

RUN apt-get update && \
    apt-get install -y ant && \
    apt-get clean;
    
# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;
    
COPY Pipfile* utilities.py config_file.env main.py ./

RUN pipenv requirements > requirements.txt \
    && pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py" ]