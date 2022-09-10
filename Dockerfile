FROM python:latest

RUN pip install cpplint clang-format

COPY lint.sh /lint.sh

RUN chmod +x /lint.sh

ENTRYPOINT [ "/lint.sh" ]