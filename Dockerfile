FROM public.ecr.aws/lambda/python:3.9

# Instalar dependencias del sistema necesarias para Prophet
RUN yum update -y && \
    yum install -y gcc gcc-c++ make && \
    yum clean all

# Crear y activar un directorio de trabajo
WORKDIR /var/task

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY src/ ./src/


# Establecer variables de entorno
ENV PYTHONPATH=/var/task
ENV PYTHONUNBUFFERED=1

# Establecer el handler
CMD [ "src.lambda_handler.lambda_handler" ]
