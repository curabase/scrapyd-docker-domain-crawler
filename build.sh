docker build -t domain_crawler .
docker tag domain_crawler localhost:5000/domain_crawler
docker push localhost:5000/domain_crawler
