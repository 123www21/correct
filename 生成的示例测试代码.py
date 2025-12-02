# 示例代码（可选，用于测试）
from grading_engine import GradingEngine

if __name__ == "__main__":
    api_key = "your_api_key_here"
    grader = GradingEngine(api_key)
    sample_submission = "这是一篇学生作业，内容关于环境保护的重要性..."
    sample_criteria = {
        "content_relevance": {"weight": 0.4, "description": "内容与主题的相关性"},
        "logical_clarity": {"weight": 0.3, "description": "逻辑清晰度"},
        "language_accuracy": {"weight": 0.3, "description": "语言准确性"}
    }
    result = grader.grade_assignment(sample_submission, sample_criteria)
    if result["error"]:
        print(f"错误：{result['error']}")
    else:
        print(f"得分：{result['score']}")
        print("错误点：", result["errors"])
        print("改进建议：", result["suggestions"])