from app.tools.calculator import tool_calculator
from app.tools.current_date import get_current_date
from app.tools.list_documents import tool_list_uploaded_document
from app.tools.summarize_document import summarize_document
from app.tools.search_documents import search_document

tools = [
    {
        'type':'function',
        'function': {
            'name':'search_document',
            'description':"""Search the company knowledge base for relevant document content.

            Use this tool for company-specific questions about policies,
            rules, procedures, and information contained in company documents.

            For HR questions, search HR-related documents.
            For IT questions, search IT-related documents.
            For Finance questions, search Finance-related documents.

            """,
            'parameters':{
                'type':'object',
                'properties':{
                    'query':{
                        'type':'string'
                    },
                    'top_k':{
                        'type':'integer'
                    },
                    'document_filter':{
                        'type':'string'
                    }
                },
                'required':["query"]
            }
        }
    },
    {
        'type':'function',
        'function':{
            'name':'summarize_document',
            'description':'Summarize document in 4-5 sentences. Use this tool when the user asks for a summary of an entire document or policy.',
            'parameters':{
                'type':'object',
                'properties':{
                    'filename':{
                        'type':'string'
                    }
                },
                'required':["filename"]
            }
        }       
    },
    {
        'type':'function',
        'function':{
            'name':'tool_list_uploaded_document',
            'description':'List uploaded document names. Use only when the user asks which documents are available.'
        }
    },
    {
        'type':'function',
        'function':{
            'name':'get_current_date',
            'description':'return current date'
        }
    },
    {
        'type':'function',
        'function':{
            'name':'tool_calculator',
            'description':""" Use this tool whenever the user asks to calculate, solve,
                    or find the answer to a mathematical expression.
                    This includes natural-language questions such as
                    'What is 12 + 30?', 'How much is 50 divided by 5?',
                    or 'Solve 10 * 4'.
                    Supports addition, subtraction, multiplication, division,
                    modulo, and power.""",
            'parameters':{
                'type':'object',
                'properties':{
                    'expression':{
                        'type':'string'
                    }
                },
                'required':["expression"]
            }
        }
    }
]

tool_mapping = {
    "search_document": search_document,
    "summarize_document": summarize_document,
    "tool_list_uploaded_document": tool_list_uploaded_document,
    "get_current_date":get_current_date,
    "tool_calculator": tool_calculator
}