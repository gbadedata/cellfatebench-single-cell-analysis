FROM mambaorg/micromamba:1.5.10

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY environment.yml /tmp/environment.yml

RUN micromamba install -y -n base -f /tmp/environment.yml \
    && micromamba clean --all --yes

COPY . /app

RUN chown -R $MAMBA_USER:$MAMBA_USER /app

USER $MAMBA_USER

ENV PYTHONPATH=/app/src

CMD ["make", "pipeline"]
