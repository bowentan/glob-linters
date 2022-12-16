FROM python:3.11.1-slim

WORKDIR /glob-linters
COPY . .
RUN pip install --no-cache-dir .

CMD ["glob-linters"]
# ENTRYPOINT ["glob_linters"]