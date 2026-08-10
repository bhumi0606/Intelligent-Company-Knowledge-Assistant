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
    }
]

tool_mapping = {
    "search_document": search_document,
}