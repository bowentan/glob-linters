FROM python:latest

RUN pip install cpplint clang-format

COPY lint.sh .

RUN chmod +x lint.sh

CMD [ "lint.sh" ]