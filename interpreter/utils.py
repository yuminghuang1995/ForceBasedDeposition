import logging


def build_thread(name : str, thread_body : str):
    log = logging.getLogger("interpreter.utils")
    thread_body = thread_body.replace('\n', ' ');
    thread_function_def = f"thread {name}(): {thread_body} end\n"
    log.debug(f"Thread definition: {thread_function_def}")
    return thread_function_def


def build_function(name, parameters, function_body):
    log = logging.getLogger("interpreter.utils")
    function_body = function_body.replace('\n', ' ');
    function_def = f"def {name}({parameters}): {function_body} end\n"
    log.debug(f"Function definition: {function_def}")
    return function_def
