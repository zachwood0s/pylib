import ast
import six
from pylib.pattern import _, match

# __box__(self, right_side):
# __unbox__(self, left_side):

__all__ = [
    'AssignTransformer'
]

BOX_SIGNATURE = "__box__"
UNBOX_SIGNATURE = "__unbox__"
SENTINEL = []

# =====================================
# Helper Methods
# =====================================

def gen_method_call(node, method_name, *args):
  return ast.Call(
    func=ast.Attribute(
      value=node,
      attr=method_name,
      ctx=ast.Load()
    ),
    args=list(args),
    keywords=[],
    startargs=None,
    kwargs=None
  )

def gen_box_call(node, rhs):
  return gen_method_call(node, BOX_SIGNATURE, rhs) 

def gen_unbox_call(node):
  return gen_method_call(node, UNBOX_SIGNATURE)

def gen_print(string):
  return ast.Print(dest=None, values=[ast.Str(string)], nl=True)

def gen_func_call(func_name, *args):
  return ast.Call(
    func=ast.Name(id=func_name, ctx=ast.Load()),
    args=list(args),
    keywords=[],
    startargs=None,
    kwargs=None
  )

def gen_hasattr_call(node, attr):
  return gen_func_call("hasattr", node, ast.Str(s=attr))

def convert_name(node, ctx):
  return match(
    node,
    (ast.Name, ast.Name(id=node.id, ctx=ctx)),
    (_, node)
  )

# =====================================
# Converters
# =====================================

def gen_rhs(rhs):
  return ast.IfExp(
    test=gen_hasattr_call(rhs, UNBOX_SIGNATURE),
    body=gen_unbox_call(rhs),
    orelse=rhs
  )

def convert_assign_py2(lhs, rhs):
  loaded = convert_name(lhs, ast.Load())
  return ast.TryExcept(
    body=[
      ast.Expr(loaded),
    ],
    handlers=[
      ast.ExceptHandler(
        type=None,
        name=None,
        body=[
          ast.Assign([lhs], rhs),
        ]
      )
    ],
    orelse=[
      ast.If(
        test=gen_hasattr_call(loaded, BOX_SIGNATURE),
        body=[
          ast.Expr(gen_box_call(loaded, rhs)),
        ],
        orelse=[
          ast.Assign([lhs], rhs),
        ]
      )
    ]
  )

def convert_assign_py3(lhs, rhs):
  pass

def convert_assign(lhs, rhs):
  return convert_assign_py3(lhs, rhs) if six.PY3 else convert_assign_py2(lhs, rhs)



class AssignTransformer(ast.NodeTransformer):
    def generic_visit(self, node):
        ast.NodeTransformer.generic_visit(self, node)
        return node

    def visit_Assign(self, node):
        rhs = node.value
        new_rhs = gen_rhs(rhs)
        replaced = [convert_assign(t, new_rhs) for t in node.targets]

        ast.fix_missing_locations(new_rhs)
        ast.copy_location(new_rhs, node)
        for r in replaced:
          ast.copy_location(r, node)
          ast.fix_missing_locations(r)

        return replaced


"""
--Transforms:--

a = b

--Into:--

try:
  a
except:
  a = b.__unbox__() if hasattr(b, '__unbox__') else b
else:
  if hasattr(a, "__box__"):
    a.__box__(b.__unbox__() if hasattr(b, '__unbox__') else b)
  else:
    a = b.__unbox__() if hasattr(b, '__unbox__') else b
"""