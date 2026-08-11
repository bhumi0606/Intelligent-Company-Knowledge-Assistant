from unittest.mock import MagicMock, patch
import pytest

from app.tools.calculator import tool_calculator
from app.tools.current_date import get_current_date
from app.tools.tool_schemas import tools, tool_mapping
from app.agents.router import create_intent_prompt, detect_intent

# ---------- Tool Tests ----------

def test_calculator_basic_operations():
    assert tool_calculator("12 + 30") == 42.0
    assert tool_calculator("50 - 15") == 35.0
    assert tool_calculator("10 * 4") == 40.0
    assert tool_calculator("50 / 5") == 10.0
    assert tool_calculator("2 ** 3") == 8.0
    assert tool_calculator("10 % 3") == 1.0


def test_calculator_invalid_expression():
    with pytest.raises(ValueError):
        tool_calculator("abc + def")


def test_current_date():
    result = get_current_date()
    assert isinstance(result, str)
    assert len(result.split("-")) == 3  


def test_tool_schemas_and_mappings():
    assert isinstance(tools, list)
    assert len(tools) == 5

    expected_tools = {"search_document", "summarize_document", "tool_list_uploaded_document", "get_current_date", "tool_calculator"}
    registered_tools = {t["function"]["name"] for t in tools}
    assert registered_tools == expected_tools

    for tool in tools:
        fname = tool["function"]["name"]
        assert fname in tool_mapping


# ---------- Router Intent Detection Tests ----------

def test_intent_prompt_creation():
    prompt = create_intent_prompt("How many leaves can I take?")
    assert "hr" in prompt
    assert "it" in prompt
    assert "finance" in prompt
    assert "general" in prompt
    assert "How many leaves can I take?" in prompt


@patch("app.agents.router.client")
def test_detect_intent_hr(mock_client):
    fake_choice = MagicMock()
    fake_choice.message.content = "hr"
    fake_response = MagicMock()
    fake_response.choices = [fake_choice]

    mock_client.chat.completions.create.return_value = fake_response

    intent = detect_intent("How many casual leaves?")
    assert intent == "hr"


# ---------- Base Agent Tool Calling Tests ----------

@patch("app.agents.base.client")
def test_agent_tool_calling(mock_client):
    from app.agents.base import BaseAgent
    agent = BaseAgent(name="test_agent", system_prompt="Test System Prompt")
    
    fake_message = MagicMock()
    fake_message.tool_calls = None
    fake_response = MagicMock()
    fake_response.choices = [MagicMock(message=fake_message)]

    mock_client.chat.completions.create.return_value = fake_response

    answer, citations, chunks = agent.tool_calling("Hello", history=[])
    assert answer is None
    assert citations == []
    assert chunks == []
