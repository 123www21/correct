import unittest
import json
import requests
from grading_engine import GradingEngine
from unittest.mock import Mock, patch


class TestGradingEngine(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.grader = GradingEngine(self.api_key)

    @patch("requests.post")
    def test_grade_assignment_success(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "score": 85.5,
            "errors": ["逻辑断层在第二段", "语法错误：时态不一致"],
            "suggestions": ["补充数据支撑论点", "优化句子结构以提升流畅度"]
        }
        mock_post.return_value = mock_response

        submission = "测试作业内容"
        criteria = {"维度1": {"weight": 0.5}, "维度2": {"weight": 0.5}}
        result = self.grader.grade_assignment(submission, criteria)

        self.assertEqual(result["score"], 85.5)
        self.assertEqual(result["errors"], ["逻辑断层在第二段", "语法错误：时态不一致"])
        self.assertEqual(result["suggestions"], ["补充数据支撑论点", "优化句子结构以提升流畅度"])
        self.assertEqual(result["error"], "")  # 验证无错误信息

    @patch("requests.post")
    def test_grade_assignment_default_values(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {}  # 空响应
        mock_post.return_value = mock_response

        submission = "测试作业内容"
        criteria = {"维度": {"weight": 1.0}}  # 合法的评分标准
        result = self.grader.grade_assignment(submission, criteria)

        self.assertEqual(result["score"], 0.0)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["suggestions"], [])
        self.assertEqual(result["error"], "")

    def test_invalid_submission_text(self):
        # 空文本
        result_empty = self.grader.grade_assignment("", {"维度": {"weight": 1.0}})
        self.assertEqual(result_empty["error"], "作业文本不能为空")

        # 非字符串类型（如数字）
        result_non_str = self.grader.grade_assignment(123, {"维度": {"weight": 1.0}})
        self.assertEqual(result_non_str["error"], "作业文本不能为空")

    def test_invalid_criteria(self):
        # 空字典
        result_empty = self.grader.grade_assignment("有效文本", {})
        self.assertEqual(result_empty["error"], "评分标准必须为非空字典")

        # 非字典类型（如列表）
        result_non_dict = self.grader.grade_assignment("有效文本", [])
        self.assertEqual(result_non_dict["error"], "评分标准必须为非空字典")

    @patch("requests.post")
    def test_request_exception(self, mock_post):
        # 模拟超时异常
        mock_post.side_effect = requests.exceptions.Timeout("请求超时")
        result = self.grader.grade_assignment("测试文本", {"维度": {"weight": 1.0}})
        self.assertIn("请求失败：请求超时", result["error"])

        # 模拟连接异常
        mock_post.side_effect = requests.exceptions.ConnectionError("连接失败")
        result = self.grader.grade_assignment("测试文本", {"维度": {"weight": 1.0}})
        self.assertIn("请求失败：连接失败", result["error"])

    @patch("requests.post")
    def test_invalid_json_response(self, mock_post):
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("无效JSON", doc="", pos=0)
        mock_post.return_value = mock_response
        result = self.grader.grade_assignment("测试文本", {"维度": {"weight": 1.0}})
        self.assertEqual(result["error"], "API返回格式错误")

    @patch("requests.post")
    def test_http_error_response(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Unauthorized")
        mock_post.return_value = mock_response
        result = self.grader.grade_assignment("测试文本", {"维度": {"weight": 1.0}})
        self.assertIn("请求失败：401 Unauthorized", result["error"])



if __name__ == "__main__":
    unittest.main()