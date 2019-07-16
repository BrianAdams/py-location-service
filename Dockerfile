FROM python:3

# Install process tools
RUN apt-get update && apt-get -y install procps \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash loco

RUN mkdir /opt/loco
RUN chown -R loco:loco /opt/loco
RUN chmod 755 /opt/loco

USER loco
ENV PATH "$PATH:/home/loco/.local/bin" 
WORKDIR /opt/loco

# Install Python dependencies from requirements.txt if it exists
COPY requirements.txt* /opt/loco
RUN if [ -f "requirements.txt" ]; then pip install --user -r requirements.txt && rm requirements.txt*; fi


# Set the default shell to bash instead of sh
ENV SHELL /bin/bash
EXPOSE 8000

COPY loco /opt/loco

WORKDIR /opt
CMD uvicorn --workers 2 loco.loco_fastapi.service:app --host 0.0.0.0

