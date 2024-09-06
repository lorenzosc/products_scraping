This is a project to gather prices from several different types of products and from different sales platforms. The objective is to gather historical data to:
- Analyze prices fluctuation
- Check if promotions are real
- Finding the best cost-effective products, to be able to buy at a low price

The objetive is to use selenium and beautifulSoup for scrapping, pandas for registering of the data, airflow for scheduling the jobs. The analysis to be made will be chosen after some time of data gathering.

If you want to clone to run this, make sure you have docker and docker compose installed. To build the docker image, run

'''
docker build -t image-desired-name:latest .
'''

Afterwards, to run the container, run
'''
docker compose build
docker compose up
'''