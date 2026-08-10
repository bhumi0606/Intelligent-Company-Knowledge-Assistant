from app.tools.current_date import get_current_date
from app.tools.list_documents import tool_list_uploaded_document
from app.tools.summarize_document import summarize_document
from app.tools.search_documents import search_document

tools = [
    {
        'type':'function',
        'function': {
            'name':'search_document',
            'description':"Search the company's related document for relevent chunks",
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
            'description':'list all uploaded documents'
        }
    },
    {
        'type':'function',
        'function':{
            'name':'get_current_date',
            'description':'return current date'
        }
    }
]

tool_mapping = {
    "search_document": search_document,
    "summarize_document": summarize_document,
    "tool_list_uploaded_document": tool_list_uploaded_document,
    "get_current_date":get_current_date
}