FROM mcr.microsoft.com/playwright:v1.56.1-noble

# Install Python3, venv and pip (some Playwright images don't include python)
USER root
RUN apt-get update && apt install python3 python3-pip python3-venv -y

WORKDIR /app

# COPY .env_for_container /app/.env
COPY requirements.txt /app/requirements.txt

# Create a virtualenv and install dependencies into it to avoid
# Debian's "externally-managed-environment" (PEP 668) protection.
ENV VENV_PATH=/opt/venv
RUN python3 -m venv ${VENV_PATH} \
	&& ${VENV_PATH}/bin/python -m pip install --upgrade pip setuptools wheel \
	&& ${VENV_PATH}/bin/pip install --no-cache-dir -r /app/requirements.txt

# Make venv python first on PATH at runtime
ENV PATH="${VENV_PATH}/bin:$PATH"

COPY main.py /app/main.py

# Install Playwright browser binaries (Chromium) into the virtualenv so
# Playwright can find the executable at runtime. Try with system deps first
# then fall back to a simple install if the with-deps option fails.
RUN ${VENV_PATH}/bin/python -m playwright install chromium --with-deps || \
	${VENV_PATH}/bin/python -m playwright install chromium

CMD ["python", "main.py"]



