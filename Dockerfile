FROM ubuntu:20.04 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

COPY packages.list /root/packages.list
RUN apt-get update && \
    for package in `grep -v "^#" /root/packages.list`; do apt-get install -y ${package}; done

# Install the dependencies into a virtualenv
FROM base AS builder
RUN pip install --upgrade pip pipenv

# Creates virtualenv at /.venv
ENV PIPENV_VENV_IN_PROJECT 1

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv sync

# Copy the virtualenv to the runtime image
FROM base AS runtime

# Create a non-root user to run the application.
RUN mkdir -p /home/app && groupadd app && useradd app -g app
WORKDIR /home/app

# Copy the application code and fix file ownership.
COPY api ./api
COPY scripts/start.sh ./start.sh
RUN chown -R app:app /home/app
#USER app

ENV VIRTUAL_ENV /.venv
ENV PATH "${VIRTUAL_ENV}/bin:${PATH}"
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ENV FLASK_APP=./api/api.py
ENV FLASK_ENV=development

EXPOSE 8001
CMD [ "./start.sh" ]
