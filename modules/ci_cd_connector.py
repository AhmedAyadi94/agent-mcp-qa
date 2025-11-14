import requests
import json
from typing import Dict, Optional

class JenkinsConnector:
    def __init__(self, base_url: str, username: str, api_token: str):
        """
        Initialise la connexion avec Jenkins
        """
        self.base_url = base_url.rstrip('/')
        self.auth = (username, api_token)
    
    def trigger_build(self, job_name: str, parameters: Optional[Dict] = None) -> Dict:
        """
        Declenche un job Jenkins
        """
        url = f"{self.base_url}/job/{job_name}/buildWithParameters" if parameters else f"{self.base_url}/job/{job_name}/build"
        
        try:
            response = requests.post(url, auth=self.auth, data=parameters or {})
            if response.status_code in [200, 201]:
                return {"status": "success", "message": f"Build triggered for {job_name}"}
            else:
                return {"status": "error", "message": f"Failed to trigger build: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_build_status(self, job_name: str, build_number: int) -> Dict:
        """
        Recupere le statut d'un build Jenkins
        """
        url = f"{self.base_url}/job/{job_name}/{build_number}/api/json"
        
        try:
            response = requests.get(url, auth=self.auth)
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "building": data.get('building', False),
                    "result": data.get('result', 'UNKNOWN'),
                    "duration": data.get('duration', 0)
                }
            else:
                return {"status": "error", "message": f"Failed to get build status: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def download_artifact(self, job_name: str, build_number: int, artifact_path: str, output_path: str) -> Dict:
        """
        Telecharge un artifact depuis Jenkins
        """
        url = f"{self.base_url}/job/{job_name}/{build_number}/artifact/{artifact_path}"
        
        try:
            response = requests.get(url, auth=self.auth)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return {"status": "success", "message": f"Artifact downloaded to {output_path}"}
            else:
                return {"status": "error", "message": f"Failed to download artifact: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

class GitLabConnector:
    def __init__(self, base_url: str, private_token: str):
        """
        Initialise la connexion avec GitLab CI
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {"PRIVATE-TOKEN": private_token}
    
    def trigger_pipeline(self, project_id: str, ref: str = "main", variables: Optional[Dict] = None) -> Dict:
        """
        Declenche un pipeline GitLab CI
        """
        url = f"{self.base_url}/api/v4/projects/{project_id}/pipeline"
        payload = {"ref": ref}
        
        if variables:
            payload["variables"] = [{'key': k, 'value': v} for k, v in variables.items()]
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            if response.status_code == 201:
                data = response.json()
                return {"status": "success", "pipeline_id": data.get('id'), "web_url": data.get('web_url')}
            else:
                return {"status": "error", "message": f"Failed to trigger pipeline: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_pipeline_status(self, project_id: str, pipeline_id: int) -> Dict:
        """
        Recupere le statut d'un pipeline GitLab CI
        """
        url = f"{self.base_url}/api/v4/projects/{project_id}/pipelines/{pipeline_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "pipeline_status": data.get('status'),
                    "ref": data.get('ref'),
                    "duration": data.get('duration')
                }
            else:
                return {"status": "error", "message": f"Failed to get pipeline status: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_jobs(self, project_id: str, pipeline_id: int) -> Dict:
        """
        Recupere la liste des jobs d'un pipeline
        """
        url = f"{self.base_url}/api/v4/projects/{project_id}/pipelines/{pipeline_id}/jobs"
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                jobs = response.json()
                return {
                    "status": "success",
                    "jobs": [{"id": j.get('id'), "name": j.get('name'), "status": j.get('status')} for j in jobs]
                }
            else:
                return {"status": "error", "message": f"Failed to get jobs: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
