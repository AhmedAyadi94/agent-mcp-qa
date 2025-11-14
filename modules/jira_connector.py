import requests
import json
from typing import Dict, List, Optional

class JiraConnector:
    def __init__(self, base_url: str, email: str, api_token: str):
        """
        Initialise la connexion avec Jira
        """
        self.base_url = base_url.rstrip('/')
        self.auth = (email, api_token)
        self.headers = {"Content-Type": "application/json"}
    
    def create_issue(self, project_key: str, summary: str, description: str, 
                     issue_type: str = "Bug", priority: str = "Medium") -> Dict:
        """
        Cree un nouveau ticket Jira
        """
        url = f"{self.base_url}/rest/api/3/issue"
        
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": description}]
                        }
                    ]
                },
                "issuetype": {"name": issue_type},
                "priority": {"name": priority}
            }
        }
        
        try:
            response = requests.post(url, auth=self.auth, headers=self.headers, json=payload)
            if response.status_code == 201:
                data = response.json()
                return {
                    "status": "success",
                    "issue_key": data.get('key'),
                    "issue_id": data.get('id'),
                    "self": data.get('self')
                }
            else:
                return {"status": "error", "message": f"Failed to create issue: {response.status_code}", "details": response.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_issue(self, issue_key: str) -> Dict:
        """
        Recupere les details d'un ticket Jira
        """
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        
        try:
            response = requests.get(url, auth=self.auth, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                fields = data.get('fields', {})
                return {
                    "status": "success",
                    "key": data.get('key'),
                    "summary": fields.get('summary'),
                    "status": fields.get('status', {}).get('name'),
                    "assignee": fields.get('assignee', {}).get('displayName') if fields.get('assignee') else None,
                    "priority": fields.get('priority', {}).get('name')
                }
            else:
                return {"status": "error", "message": f"Failed to get issue: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def update_issue(self, issue_key: str, fields_to_update: Dict) -> Dict:
        """
        Met a jour un ticket Jira
        """
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        
        payload = {"fields": fields_to_update}
        
        try:
            response = requests.put(url, auth=self.auth, headers=self.headers, json=payload)
            if response.status_code == 204:
                return {"status": "success", "message": f"Issue {issue_key} updated successfully"}
            else:
                return {"status": "error", "message": f"Failed to update issue: {response.status_code}", "details": response.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def add_comment(self, issue_key: str, comment_text: str) -> Dict:
        """
        Ajoute un commentaire a un ticket Jira
        """
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/comment"
        
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": comment_text}]
                    }
                ]
            }
        }
        
        try:
            response = requests.post(url, auth=self.auth, headers=self.headers, json=payload)
            if response.status_code == 201:
                data = response.json()
                return {"status": "success", "comment_id": data.get('id')}
            else:
                return {"status": "error", "message": f"Failed to add comment: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def transition_issue(self, issue_key: str, transition_name: str) -> Dict:
        """
        Change le statut d'un ticket Jira
        """
        transitions_url = f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions"
        
        try:
            response = requests.get(transitions_url, auth=self.auth, headers=self.headers)
            if response.status_code != 200:
                return {"status": "error", "message": "Failed to get available transitions"}
            
            transitions = response.json().get('transitions', [])
            transition_id = None
            
            for t in transitions:
                if t.get('name', '').lower() == transition_name.lower():
                    transition_id = t.get('id')
                    break
            
            if not transition_id:
                return {"status": "error", "message": f"Transition '{transition_name}' not found"}
            
            payload = {"transition": {"id": transition_id}}
            response = requests.post(transitions_url, auth=self.auth, headers=self.headers, json=payload)
            
            if response.status_code == 204:
                return {"status": "success", "message": f"Issue {issue_key} transitioned to {transition_name}"}
            else:
                return {"status": "error", "message": f"Failed to transition issue: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def link_issues(self, inward_issue: str, outward_issue: str, link_type: str = "Relates") -> Dict:
        """
        Cree un lien entre deux tickets Jira
        """
        url = f"{self.base_url}/rest/api/3/issueLink"
        
        payload = {
            "type": {"name": link_type},
            "inwardIssue": {"key": inward_issue},
            "outwardIssue": {"key": outward_issue}
        }
        
        try:
            response = requests.post(url, auth=self.auth, headers=self.headers, json=payload)
            if response.status_code == 201:
                return {"status": "success", "message": f"Issues linked successfully"}
            else:
                return {"status": "error", "message": f"Failed to link issues: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
