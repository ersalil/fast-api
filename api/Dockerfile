FROM python:3.10.5
COPY requirements.txt /fast-api/api/requirements.txt
WORKDIR /fast-api/api
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000","--reload"]
FROM nginx:1.17-alpine
COPY --from=build /react-console/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]