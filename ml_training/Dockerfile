# ml-training/Dockerfile
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-devel

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 기본적으로 대기 상태, 수동 실행
CMD ["sleep", "infinity"]