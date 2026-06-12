import json
import subprocess
import re
from datetime import datetime
from typing import Set, Dict, List, Tuple

EXACT_MATCHES = {
    "zone_id": "aws_route53_zone",
    "task_definition": "aws_ecs_task_definition",
    "web_acl_id": "aws_wafv2_web_acl",
}

# UPGRADE 1: Resource Hints for fuzzy matching beyond _id / _arn
RESOURCE_HINTS = {
    #"cluster": ["aws_ecs_cluster", "aws_eks_cluster", "aws_msk_cluster", "aws_redshift_cluster"],
    "task_definition": "aws_ecs_task_definition",
    "web_acl": "aws_wafv2_web_acl",
    "certificate": "aws_acm_certificate",
    "role": "aws_iam_role",
    #"policy": ["aws_iam_policy"],
    "topic": "aws_sns_topic",
    "queue": "aws_sqs_queue",
    "bucket": "aws_s3_bucket",
    "log_group": "aws_cloudwatch_log_group",
    "vpc": "aws_vpc",
    "subnet": "aws_subnet"
}

def fetch_terraform_schema() -> dict:
    """Executes the Terraform CLI to extract the official provider schema."""
    print("Extracting official schema from Terraform binary...")
    result = subprocess.run(
        ["terraform", "providers", "schema", "-json"], 
        capture_output=True, 
        text=True, 
        check=True,
        timeout=120
    )
    return json.loads(result.stdout)

def extract_attributes_with_requirements(block: dict, is_parent_required: bool = True) -> List[Tuple[str, bool]]:
    """
    UPGRADE 2: Recursively extracts attributes while tracking if they are hard dependencies.
    If a parent block is optional, all its child attributes are effectively optional.
    """
    attributes = []
    
    # 1. Process top-level attributes in this block
    if "attributes" in block:
        for attr_name, attr_data in block["attributes"].items():
            # An attribute is a 'hard' dependency ONLY if it is required AND its parent block is required
            is_req = attr_data.get("required", False) and is_parent_required
            attributes.append((attr_name, is_req))
            
    # 2. Recurse into nested blocks (e.g., 'listener' inside 'aws_lb')
    if "block_types" in block:
        for block_name, block_data in block["block_types"].items():
            # A block is required if min_items > 0
            min_items = block_data.get("min_items", 0)
            is_block_required = (min_items > 0) and is_parent_required
            
            attributes.extend(
                extract_attributes_with_requirements(block_data["block"], is_block_required)
            )
            
    return attributes

def extract_resource_schema(block: dict) -> dict:
    """
    Captures the FULL per-resource schema shape (recursively) so downstream
    correction can be driven by provider ground-truth instead of hand tables:

      - arguments       : scalar fields -> {type, required}
      - blocks          : nested blocks -> {required, min_items, max_items, ...}
      - attributes      : every readable attribute name (for reference validation)

    `type` is the raw Terraform JSON type (e.g. "string" or ["set","string"]).
    """
    out = {"arguments": {}, "blocks": {}, "attributes": []}

    for name, data in block.get("attributes", {}).items():
        # Every attribute is readable (exported); record it for ref validation.
        out["attributes"].append(name)
        # Configurable arguments are anything not purely computed.
        if data.get("required") or data.get("optional"):
            out["arguments"][name] = {
                "type": data.get("type"),
                "required": bool(data.get("required", False)),
            }

    for name, bdata in block.get("block_types", {}).items():
        min_items = bdata.get("min_items", 0)
        sub = extract_resource_schema(bdata.get("block", {}))
        out["blocks"][name] = {
            "required": min_items > 0,
            "min_items": min_items,
            "max_items": bdata.get("max_items", 0),
            "arguments": sub["arguments"],
            "blocks": sub["blocks"],
            "attributes": sub["attributes"],
        }

    return out


def resolve_dependency(attribute_name: str, valid_resources: Set[str]) -> str | None:
    """Bulletproof 4-stage dynamic resolution logic."""
    
    # STAGE 1: Exact Overrides
    if attribute_name in EXACT_MATCHES:
        return EXACT_MATCHES[attribute_name]

    # STAGE 2: Strict Suffix Filter
    # If it doesn't end in an ID or ARN, it's not a relational dependency. Cures hallucinations.
    if not attribute_name.endswith(("_id", "_ids", "_arn", "_arns", "_name", "_names")):
        return None

    # Strip the relational suffix (e.g., vpc_security_group_ids -> vpc_security_group)
    base_name = re.sub(r'_(id|ids|arn|arns|name|names)$', '', attribute_name)
    derived_resource = f"aws_{base_name}"

    # STAGE 3: Direct Match (e.g., subnet_id -> aws_subnet)
    if derived_resource in valid_resources:
        return derived_resource

    # STAGE 4: Longest-Suffix Match (FIXED INDENTATION)
    # e.g., vpc_security_group -> ends with security_group -> aws_security_group
    for resource in sorted(valid_resources, key=len, reverse=True):
        short_res = resource[4:] # Strip 'aws_'
        if base_name.endswith(short_res):
            return resource

    # STAGE 5: Hint Match 
    # e.g., execution_role_arn -> execution_role -> ends with role -> aws_iam_role
    for hint_key, target_resource in RESOURCE_HINTS.items():
        if base_name.endswith(hint_key):
            if target_resource in valid_resources:
                return target_resource

    return None

def main():
    try:
        schema_json = fetch_terraform_schema()

    except subprocess.CalledProcessError as e: 
        print()
        print("TF Schema Extraction Failed")
        print(e.stderr)

        return
    
    except subprocess.TimeoutExpired:
        print()
        print("TF Schema Extraction Timedout")
        return
    
    aws_provider = schema_json.get("provider_schemas", {}).get("registry.terraform.io/hashicorp/aws", {})
    resource_schemas = aws_provider.get("resource_schemas", {})
    
    valid_resources = set(resource_schemas.keys())
    dependency_map: Dict[str, dict] = {}
    
    print(f"Parsing {len(valid_resources)} AWS resources...")

    for resource_name, schema_data in resource_schemas.items():
        hard_deps = set()
        opt_deps = set()
        
        # Extract all attributes and their requirement status
        all_attributes = extract_attributes_with_requirements(schema_data.get("block", {}))
        
        for attr_name, is_req in all_attributes:
            dep_resource = resolve_dependency(attr_name, valid_resources)
            
            if dep_resource and dep_resource != resource_name:
                if is_req:
                    hard_deps.add(dep_resource)
                else:
                    opt_deps.add(dep_resource)
        
        # Clean up: If a resource is a hard dependency, it shouldn't also be listed as optional
        opt_deps = opt_deps - hard_deps
                
        if hard_deps or opt_deps:
            dependency_map[resource_name] = {
                "hard": sorted(list(hard_deps)),
                "optional": sorted(list(opt_deps))
            }

    # ======================================================
    # MANUAL OVERRIDES
    # ======================================================

    MANUAL_OVERRIDES = {

        "aws_ecs_service": {
            "hard": [
                "aws_ecs_cluster",
                "aws_ecs_task_definition"
            ],
            "optional": [
                "aws_lb_target_group"
            ]
        },

        "aws_nat_gateway": {
            "hard": [
                "aws_subnet",
                "aws_eip"
            ],
            "optional": []
        },

        "aws_cloudwatch_event_target": {
            "hard": [
                "aws_cloudwatch_event_rule"
            ],
            "optional": []
        },

        "aws_eks_node_group": {
            "hard": [
                "aws_eks_cluster",
                "aws_iam_role",
                "aws_subnet"
            ],
            "optional": []
        },

        "aws_lb": {
            "hard": [
                "aws_subnet"
            ],
            "optional": [
                "aws_security_group"
            ]
        },

        "aws_lb_listener": {
            "hard": ["aws_lb"],
            "optional": ["aws_acm_certificate", "aws_lb_target_group"]
        },

        "aws_lambda_permission": {
            "hard": [
                "aws_lambda_function"
            ],
            "optional": [
                "aws_cloudwatch_event_rule",
                "aws_s3_bucket",
                "aws_api_gateway_rest_api"
            ]
        }, 

        "aws_route": {
            "hard": [
                "aws_route_table"
            ],
            "optional": [
                "aws_instance",
                "aws_nat_gateway",
                "aws_network_interface",
                "aws_vpc_endpoint",
                "aws_vpc_peering_connection", 
                "aws_internet_gateway"
            ]
        },

        "aws_lambda_function": {
            "hard": ["aws_iam_role"],
            "optional": [
                "aws_kms_key",
                "aws_security_group",
                "aws_subnet",
                "aws_vpc"
            ]
        },
    }

    dependency_map.update(MANUAL_OVERRIDES)

    # UPGRADE 3: Inject Metadata
    provider_version = aws_provider.get("version", "unknown")
    metadata = {
        "provider": "hashicorp/aws",
        "version": provider_version,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "resource_count": len(valid_resources),
        "mapped_resources": len(dependency_map)
    }

    # Output the results
    output_file = "auto_dependency_map.py"
    with open(output_file, "w") as f:
        f.write("# AUTO-GENERATED TERRAFORM DEPENDENCY MAP\n")
        f.write("# DO NOT EDIT MANUALLY\n\n")
        
        f.write(f"DEPENDENCY_METADATA = {json.dumps(metadata, indent=4)}\n\n")
        
        f.write("RESOURCE_DEPENDENCIES = ")
        json.dump(dependency_map, f, indent=4)
        f.write("\n")
        
    print(f"Success! Map generated with {len(dependency_map)} resource relationships.")

    # ======================================================
    # NEW: emit the full per-resource schema (ground truth for
    # schema-driven correction — block-vs-argument, required blocks,
    # valid attributes, argument types). Same schema JSON, no extra fetch.
    # ======================================================
    import os

    resource_schema = {
        name: extract_resource_schema(sd.get("block", {}))
        for name, sd in resource_schemas.items()
    }

    os.makedirs("schema", exist_ok=True)
    schema_out = os.path.join("schema", "resource_schema.json")
    with open(schema_out, "w") as f:
        json.dump(resource_schema, f, indent=2)

    print(f"Success! Resource schema written for {len(resource_schema)} resources -> {schema_out}.")

if __name__ == "__main__":
    main()