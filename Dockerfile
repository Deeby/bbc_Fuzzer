FROM debian:jessie

RUN apt-get update \
        && apt-get install -y --no-install-recommends --fix-missing \
        git \
        ca-certificates \
        gcc \
        build-essential \
        make \
        wget

WORKDIR /src

RUN git clone https://github.com/aoh/radamsa.git

WORKDIR /src/radamsa

RUN make \
        && make install

WORKDIR /

RUN mkdir seed && mkdir testcase

VOLUME ["/seed", "/testcase"]

CMD /usr/bin/radamsa -r /seed -n inf -o /testcase/%n
