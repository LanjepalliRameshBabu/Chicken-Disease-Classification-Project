import os
import urllib.request as request
import zipfile
from pathlib import Path
import yaml
from dataclasses import dataclass  # Import dataclass decorator

from cnnClassifier.utils.common import get_size

# Load the config.yaml file
with open('config.yaml', 'r') as file:
    config_data = yaml.safe_load(file)

# Extract configuration parameters
artifacts_root = config_data['artifacts_root']
data_ingestion_config_data = config_data['data_ingestion']

# Create directories if they don't exist
os.makedirs(artifacts_root, exist_ok=True)
os.makedirs(data_ingestion_config_data['root_dir'], exist_ok=True)

# Define DataIngestionConfig dataclass
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path

# Create DataIngestionConfig object
data_ingestion_config = DataIngestionConfig(
    root_dir=Path(data_ingestion_config_data['root_dir']),
    source_URL=data_ingestion_config_data['source_URL'],
    local_data_file=Path(data_ingestion_config_data['local_data_file']),
    unzip_dir=Path(data_ingestion_config_data['unzip_dir'])
)

# Define ConfigurationManager class
class ConfigurationManager:
    def __init__(self, config_filepath, params_filepath):
        self.config = config_filepath
        self.params = params_filepath

# Define DataIngestion class
class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            print(f"{filename} download! with following info: \n{headers}")
        else:
            print(f"File already exists of size: {get_size(self.config.local_data_file)}")

    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)

# Use ConfigurationManager to load configuration parameters
try:
    config = ConfigurationManager(config_filepath='config.yaml', params_filepath='params.yaml')
    data_ingestion = DataIngestion(config=data_ingestion_config)
    data_ingestion.download_file()
    data_ingestion.extract_zip_file()
except Exception as e:
    raise e
