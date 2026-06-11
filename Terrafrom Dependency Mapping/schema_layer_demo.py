"""
Demo for the schema-driven correction layer (uses schema/resource_schema.sample.json).
Run: python schema_layer_demo.py
Shows the four capabilities that would replace hand-maintained normalizers.
"""
import schema_index
import schema_normalizers as sn


def show(title):
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70)


print("schema available:", schema_index.available(),
      "| resources in sample:", len(schema_index._load()))

# 1) BLOCK-AS-ARGUMENT  (replaces volume/capacity_provider_strategy denylists)
show("1. block-as-argument drop (ground truth, no hand table)")
td = '''resource "aws_ecs_task_definition" "ecs_task_definition" {
  family                = var.family
  container_definitions = var.container_definitions
  network_mode          = var.network_mode
  volume                = var.volume
}'''
print("--- before ---\n" + td)
print("--- after ---\n" + sn.drop_block_as_argument("aws_ecs_task_definition", td))

svc = '''resource "aws_ecs_service" "ecs_service" {
  name                       = var.name
  desired_count              = var.desired_count
  capacity_provider_strategy = var.ecs_service_capacity_provider_strategy
}'''
print("--- ecs_service after ---\n" + sn.drop_block_as_argument("aws_ecs_service", svc))

# 2) REQUIRED BLOCKS  (replaces viewer_certificate / default_action injectors)
show("2. required-block detection (min_items > 0)")
cf = 'resource "aws_cloudfront_distribution" "d" {\n  origin {}\n  default_cache_behavior {}\n  restrictions {}\n}'
print("cloudfront missing required blocks:", sn.missing_required_blocks("aws_cloudfront_distribution", cf))
lstn = 'resource "aws_lb_listener" "l" {\n  load_balancer_arn = aws_lb.lb.arn\n}'
print("lb_listener missing required blocks:", sn.missing_required_blocks("aws_lb_listener", lstn))

# 3) INVALID ATTRIBUTE REFS  (replaces ATTRIBUTE_ALIASES hand list)
show("3. invalid attribute references (valid exported attrs per schema)")
refs = '''key_name = aws_key_pair.key_pair.name
source = aws_sqs_queue_redrive_policy.r.arn
ok = aws_key_pair.key_pair.key_name'''
generated = {"aws_key_pair", "aws_sqs_queue_redrive_policy"}
for full, rtype, attr in sn.invalid_attribute_refs(refs, generated):
    print(f"  INVALID {full}  (valid: {sorted(schema_index.valid_attributes(rtype))})")

# 4) VARIABLE TYPE INFERENCE  (replaces suffix heuristics with declared types)
show("4. variable type inference from declared argument types")
lb = '''resource "aws_lb" "lb" {
  subnets         = var.subnets
  security_groups = var.security_groups
  internal        = var.internal
}'''
print("aws_lb:", sn.infer_var_types("aws_lb", lb))
oidc = '''resource "aws_iam_openid_connect_provider" "p" {
  url             = var.oidc_url
  client_id_list  = var.oidc_client_id_list
  thumbprint_list = var.oidc_thumbprint_list
}'''
print("aws_iam_openid_connect_provider:", sn.infer_var_types("aws_iam_openid_connect_provider", oidc))
