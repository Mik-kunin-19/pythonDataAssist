import numpy as np
import pandas as pd
import types

def attribute_tree(obj, prefix="", show_simple_list_elements=False):
    """
    print_data_attributes - a function designed to characterize created object's attributes in a tree-like structure
    Useful to inspect nested elements and callable attributes as well as their dtypes and keys of nested dicts
    Arguments:
    obj - name of the object to inspect
    prefix - default "" - sets a substring preceeding the object structure tree on each line. 
                          Useful for recursive creation of log files to determine which objects' tree is being referred to.
    show_simple_list_elements - default False - argument determining whether to list all elements of each list if the list is
                                composed of simple elements (no nested structures like other lists or dicts or 
                                initiated objects or dataframes). Kept at default False not to overflow tree structure.
    """
    from collections import defaultdict    
    def is_numeric(val):
        return isinstance(val, (int, float, np.integer, np.floating))
        
    def summarize_dataframe(df):
        num_cols = df.select_dtypes(include=[np.number]).shape[1]
        cat_cols = df.select_dtypes(include=['category']).shape[1]
        str_cols = df.select_dtypes(include=['object', 'string']).apply(lambda col: col.map(type).eq(str).all()).sum()
        return f"(rows={df.shape[0]}, cols={df.shape[1]}, numeric={num_cols}, categorical={cat_cols}, str={str_cols})"

    def format_type(val):
        if isinstance(val, list):
            return f"list (len={len(val)})"
        elif isinstance(val, dict):
            return f"dict (len={len(val)})"
        elif isinstance(val, tuple):
            return f"tuple (len={len(val)})"
        elif isinstance(val, np.ndarray):
            return f"ndarray, shape={val.shape}"
        elif isinstance(val, pd.DataFrame):
            return f"DataFrame {summarize_dataframe(val)}"
        elif isinstance(val, pd.Series):
            summary = f"Series (len={len(val)}, dtype={val.dtype})"
            if val.dtype.name == 'category':
                summary += f", categories={len(val.cat.categories)}"
            elif val.dtype == object:
                if val.map(type).eq(str).all():
                    summary += f", str-unique={val.nunique()}"
            elif pd.api.types.is_numeric_dtype(val):
                summary += f", numeric min={val.min()}, max={val.max()}"
            return summary
        else:
            return type(val).__name__

    def describe_list(lst, indent):
        num_str = sum(isinstance(x, str) for x in lst)
        num_num = sum(is_numeric(x) for x in lst)
        num_complex = sum(isinstance(x, (dict, list, tuple, pd.DataFrame, pd.Series)) for x in lst)

        print(f"{indent}|-- strings: {num_str}, numerics: {num_num}, complex: {num_complex}")

        if not show_simple_list_elements and num_complex == 0:
            return

        if all(isinstance(x, dict) for x in lst) and len(lst) > 1:
            grouped = defaultdict(list)
            for i, d in enumerate(lst):
                key_tuple = tuple(sorted(d.keys()))
                grouped[key_tuple].append((i, d))

            for key_struct, items in grouped.items():
                indices = [i for i, _ in items]
                example = items[0][1]
                print(f"{indent}|-- Elements {indices[0]}-{indices[-1]}: dicts with keys: {key_struct}")
                for key in key_struct:
                    val = example[key]
                    print(f"{indent}|   |-- {key}: type = {format_type(val)}")
                    explore_nested(val, indent + "|   |   ")
        else:
            for idx, item in enumerate(lst):
                print(f"{indent}|-- [{idx}] type = {format_type(item)}")
                explore_nested(item, indent + "|   ")
                if show_simple_list_elements and not isinstance(item, (list, dict, tuple)):
                    print(f"{indent}|   |-- value = {repr(item)}")

    def describe_dict(dct, indent):
        for key, val in dct.items():
            print(f"{indent}|-- {key}: type = {format_type(val)}")
            explore_nested(val, indent + "|   ")

    def describe_tuple(tpl, indent):
        for idx, val in enumerate(tpl):
            print(f"{indent}|-- ({idx}): type = {format_type(val)}")
            explore_nested(val, indent + "|   ")

    def explore_nested(val, indent):
        if isinstance(val, list):
            describe_list(val, indent)
        elif isinstance(val, dict):
            describe_dict(val, indent)
        elif isinstance(val, tuple):
            describe_tuple(val, indent)
        elif isinstance(val, pd.DataFrame):
            print(f"{indent}|-- DataFrame {summarize_dataframe(val)}")
        elif isinstance(val, pd.Series):
            print(f"{indent}|-- {format_type(val)}")

    # Top-level attributes of the object
    for attr_name in dir(obj):
        if attr_name.startswith('_'):
            continue
        try:
            attr_value = getattr(obj, attr_name)
        except Exception:
            continue
        if callable(attr_value):
            continue

        print(f"{prefix}{attr_name}: type = {format_type(attr_value)}")
        explore_nested(attr_value, prefix + "|   ")
