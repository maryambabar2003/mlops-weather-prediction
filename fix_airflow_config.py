import configparser
import os

os.environ['AIRFLOW_HOME'] = r'D:\MLOPsProject\airflow'
cfg_path = r'D:\MLOPsProject\airflow\airflow.cfg'

c = configparser.ConfigParser()
c.read(cfg_path)

print('Before:', c.get('database', 'sql_alchemy_conn', fallback='NOT FOUND'))

# Set the absolute path with forward slashes only
c.set('database', 'sql_alchemy_conn', 'sqlite:///D:/MLOPsProject/airflow/airflow.db')

with open(cfg_path, 'w') as f:
    c.write(f)

print('After:', c.get('database', 'sql_alchemy_conn'))
print('Config file updated successfully!')

