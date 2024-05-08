#!/bin/bash

# Создаем образ
docker build -t predict-api-image

# Создаем и запускам контейнер
docker run -d --restart always --name predict-api-container -p 8000:8000 predict-api-image 
