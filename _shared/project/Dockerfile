FROM python:{{ python_versions()|first|pyformat(PyFormats.MAJOR_DOT_MINOR_DOT_PATCH_FMT) }}-alpine3.16

RUN apk add --no-cache nginx supervisor

RUN addgroup -S hypothesis && adduser -S -G hypothesis -h /var/lib/hypothesis hypothesis
WORKDIR /var/lib/hypothesis

COPY requirements/prod.txt ./

RUN apk add --no-cache --virtual \
    build-deps \
    build-base \
  && pip install --no-cache-dir -U pip \
  && pip install --no-cache-dir -r prod.txt \
  && apk del build-deps

COPY . .

{% if cookiecutter.get("_directory") == "pyramid-app" %}
EXPOSE {{ cookiecutter.port }}
{% endif %}

USER hypothesis

CMD /usr/bin/supervisord -c /var/lib/hypothesis/conf/supervisord.conf
