from pylib.pattern import match, _
from functools import partial
import inspect
import types
import ast

def patch_with_transformation(trans, obj):
    return match(
        obj,
        (types.ModuleType, partial(patch_module_with_transformation, trans)),
        (types.FunctionType, partial(patch_function_with_transformation, trans))
    )

def patch_module_with_transformation(trans, module):
    return _patch(trans, module, module.__file__, module.__dict__)

def patch_function_with_transformation(trans, func):
    return _patch(
        trans, 
        func, 
        "<string>", # for now, source mapping isn't supported for this
        func.__globals__
    )


def _patch(trans, obj, file, scope):
    source = inspect.getsource(obj)
    tree = ast.parse(source)
    patched_ast = trans.visit(tree)
    ast.fix_missing_locations(patched_ast)
    patched_code = compile(patched_ast, file, "exec")
    exec(patched_code, scope)
