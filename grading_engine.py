import requests
import json
from requests.exceptions import RequestException

class GradingEngine:
    def __init__(self, api_key, api_base_url="https://doubao.com/", timeout=10):
        self.api_key = api_key
        self.api_base_url = api_base_url.rstrip("/")
        self.timeout = timeout

    def grade_assignment(self, submission_text, criteria):

        if not isinstance(submission_text, str) or not submission_text.strip():
            return {"error": "作业文本不能为空", "score": 0.0, "errors": [], "suggestions": []}
        if not isinstance(criteria, dict) or len(criteria) == 0:
            return {"error": "评分标准必须为非空字典", "score": 0.0, "errors": [], "suggestions": []}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "submission_text": submission_text.strip(),
            "criteria": criteria
        }

        try:
            response = requests.post(
                f"{self.api_base_url}/grading",
                headers=headers,
                data=json.dumps(payload),
                timeout=self.timeout
            )
            response.raise_for_status()
            response_data = response.json()
        except RequestException as e:
            return {"error": f"请求失败：{str(e)}", "score": 0.0, "errors": [], "suggestions": []}
        except json.JSONDecodeError:
            return {"error": "API返回格式错误", "score": 0.0, "errors": [], "suggestions": []}

        return {
            "error": "",
            "score": float(response_data.get("score", 0.0)),
            "errors": response_data.get("errors", []),
            "suggestions": response_data.get("suggestions", [])
        }

