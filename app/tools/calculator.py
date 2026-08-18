from langsmith import traceable

@traceable(name="tool calculator", project_name="Intelligent-Company-Knowledge-Assistant")
def tool_calculator(expression: str):
    try:
        expression = expression.strip()

        if '**' in expression:
                    a, b = expression.split('**')
                    return float(a) ** float(b)
        
        if '+' in expression:
            a, b = expression.split('+')
            return float(a) + float(b)

        if '-' in expression:
            a, b = expression.split('-')
            return float(a) - float(b)

        if '*' in expression:
            a, b = expression.split('*')
            return float(a) * float(b)

        if '/' in expression:
            a, b = expression.split('/')
            if b == 0:
                raise ValueError("Can not divide by zero")
            return float(a) / float(b)

        if '%' in expression:
            a, b = expression.split('%')
            if b == 0:
                raise ValueError("can not modulo by zero")
            return float(a) % float(b)

    except Exception as e:
        raise ValueError(f"Invalid expression: {expression}")