FROM python:3.12-alpine

WORKDIR /app
COPY prober.py /app/prober.py

USER 65532:65532
EXPOSE 9115
CMD ["python", "/app/prober.py"]
