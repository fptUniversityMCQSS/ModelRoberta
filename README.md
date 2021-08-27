#Install and Start Milvus Store

1.Confirm that the Docker daemon is running in the background:
```
sudo docker info
```
2.Pull Docker Image
```
sudo docker pull milvusdb/milvus:1.0.0-cpu-d030521-1ea92e
```
3.Download Configuration Files
```
mkdir -p /home/$USER/milvus/conf
cd /home/$USER/milvus/conf
wget https://raw.githubusercontent.com/milvus-io/milvus/v1.0.0/core/conf/demo/server_config.yaml
```
4.Start Docker Container
```
sudo docker run -d --name milvus_cpu_1.0.0 \
-p 19530:19530 \
-p 19121:19121 \
-v /home/$USER/milvus/db:/var/lib/milvus/db \
-v /home/$USER/milvus/conf:/var/lib/milvus/conf \
-v /home/$USER/milvus/logs:/var/lib/milvus/logs \
-v /home/$USER/milvus/wal:/var/lib/milvus/wal \
milvusdb/milvus:1.0.0-cpu-d030521-1ea92e
```
5.Confirm the running state of Milvus:
```
sudo docker ps
```


=======================
kiểm tra xem Milvus đã running ở port localhost:19530
=======================

