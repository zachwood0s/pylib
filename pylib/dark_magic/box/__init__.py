import pylib.dark_magic.patch as p
from transformer import AssignTransformer

def auto_unbox(obj):
    return p.patch_with_transformation(AssignTransformer(), obj)