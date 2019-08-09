import ast
from pylib.pattern import match, _
import astor

# __box__(self, right_side):
# __unbox__(self, left_side):

__all__ = [
    'AssignTransformer'
]

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

def gen_box_call(obj_name, rhs):
  return gen_method_call(obj_name, "__box__", rhs) 

def gen_unbox_call(node):
  return gen_method_call(node, "__unbox__")

def gen_rhs(rhs):
  return ast.IfExp(
    test=ast.Call(
      func=ast.Name(id='hasattr', ctx=ast.Load()),
      args=[
        rhs,
        ast.Str(s='__unbox__'),
      ],
      keywords=[],
      startargs=None,
      kwargs=None
    ),
    body=gen_unbox_call(rhs),
    orelse=rhs
  )

class AssignTransformer(ast.NodeTransformer):
    def generic_visit(self, node):
        ast.NodeTransformer.generic_visit(self, node)
        return node

    def visit_Assign(self, node):
        rhs = node.value
        new_rhs = gen_rhs(rhs)
        ast.copy_location(new_rhs, node)
        ast.fix_missing_locations(new_rhs)
        node.value = new_rhs
        return node