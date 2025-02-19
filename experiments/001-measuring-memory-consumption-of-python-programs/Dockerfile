FROM python:3.13

WORKDIR /app

COPY requirements.txt /app/
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

COPY scripts/experiment.sh /app/
RUN chmod +x /app/experiment.sh

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["./experiment.sh", "--"]