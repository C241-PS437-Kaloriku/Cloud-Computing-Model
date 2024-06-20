# How To Run Models API
1. Clone repository
2. Install requirements ["pip install -r requirements.txt"]
3. Run the Models API ["python main.py"]
   
## If you want to deploy it to Cloud Run
### 1. Install GCLOUD SDK
https://cloud.google.com/sdk/docs/install 
### 2. Deploy
```
gcloud run deploy --source . --port 8080
```
