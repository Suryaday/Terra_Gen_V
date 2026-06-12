def terraform_type_to_hcl(t):

    if t is None:
        return None

    if isinstance(t, str):

        mapping = {
            "string": "string",
            "number": "number",
            "bool": "bool",
        }

        return mapping.get(t)

    if (isinstance(t, list) and len(t) == 2):

        collection = t[0]

        inner = terraform_type_to_hcl(t[1])

        if inner is None:
            return None

        if collection == "list":
            return f"list({inner})"

        if collection == "set":
            return f"set({inner})"

        if collection == "map":
            return f"map({inner})"

    return None