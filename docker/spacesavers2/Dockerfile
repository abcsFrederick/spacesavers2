FROM nciccbr/ccbr_ubuntu_base_20.04:v6

# build time variables
ARG BUILD_DATE="000000"
ENV BUILD_DATE=${BUILD_DATE}
ARG BUILD_TAG="000000"
ENV BUILD_TAG=${BUILD_TAG}
ARG REPONAME="000000"
ENV REPONAME=${REPONAME}

# install pandoc
RUN mamba install pandoc

# install R packages
COPY r-packages.txt /data2/
RUN R -e 'install.packages(readLines("r-packages.txt"), repos="http://cran.us.r-project.org")'

# install quarto
ENV QUARTO_VERSION="1.3.450"
ADD https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.tar.gz /opt2
WORKDIR /opt2
RUN tar -xzvf quarto-${QUARTO_VERSION}-linux-amd64.tar.gz
ENV PATH="/opt2/quarto-${QUARTO_VERSION}/bin/:${PATH}"
RUN quarto check

# Save Dockerfile in the docker
COPY Dockerfile /opt2/Dockerfile_${REPONAME}.${BUILD_TAG}
RUN chmod a+r /opt2/Dockerfile_${REPONAME}.${BUILD_TAG}

# cleanup
WORKDIR /data2
RUN apt-get clean && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
