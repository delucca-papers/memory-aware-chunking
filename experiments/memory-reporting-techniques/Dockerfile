FROM memory-profile/experiment

WORKDIR /experiments/memory-reporting-techniques

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY experiment/ ./experiment/
COPY run.sh .
RUN mkdir -p ./output

RUN chown -R experimentuser:experimentuser /experiments/memory-reporting-techniques
USER experimentuser

ENTRYPOINT ["./run.sh"]
