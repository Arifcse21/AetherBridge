FROM python:3.12-bookworm

ENV PYTHONNUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /task_service

COPY  ../ /task_service/

RUN python -m venv /opt/venv
RUN ls -la /opt/venv/bin
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install -U pip gunicorn && \
    pip install -r /task_service/requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "TaskService.wsgi:application"]