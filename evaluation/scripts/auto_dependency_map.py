# AUTO-GENERATED TERRAFORM DEPENDENCY MAP
# DO NOT EDIT MANUALLY

DEPENDENCY_METADATA = {
    "provider": "hashicorp/aws",
    "version": "unknown",
    "generated_at": "2026-05-25T09:43:54.295436Z",
    "resource_count": 1526,
    "mapped_resources": 788
}

RESOURCE_DEPENDENCIES = {
    "aws_acm_certificate_validation": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_acmpca_certificate": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_acmpca_certificate_authority": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_s3_bucket"
        ]
    },
    "aws_acmpca_certificate_authority_certificate": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_acmpca_permission": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_acmpca_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_alb": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_s3_bucket",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_alb_listener": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_iam_policy"
        ]
    },
    "aws_alb_listener_certificate": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_alb_target_group": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_ami_copy": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_amplify_app": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_amplify_domain_association": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_api_gateway_account": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_api_gateway_client_certificate": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_api_gateway_domain_name": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_iam_policy"
        ]
    },
    "aws_api_gateway_rest_api": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_vpc_endpoint"
        ]
    },
    "aws_api_gateway_rest_api_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_api_gateway_stage": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_ecs_cluster",
            "aws_wafv2_web_acl"
        ]
    },
    "aws_apigatewayv2_domain_name": {
        "hard": [
            "aws_acm_certificate",
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_apigatewayv2_route_response": {
        "hard": [
            "aws_route"
        ],
        "optional": []
    },
    "aws_apigatewayv2_stage": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_apigatewayv2_vpc_link": {
        "hard": [
            "aws_security_group",
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_appautoscaling_policy": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_appautoscaling_target": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_appconfig_configuration_profile": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_appconfig_deployment": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_appconfig_environment": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_appconfig_extension": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_appfabric_ingestion_destination": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_appflow_connector_profile": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster",
            "aws_iam_role",
            "aws_s3_bucket"
        ]
    },
    "aws_appflow_flow": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_s3_bucket"
        ]
    },
    "aws_applicationinsights_application": {
        "hard": [],
        "optional": [
            "aws_sns_topic"
        ]
    },
    "aws_appmesh_virtual_gateway": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_appmesh_virtual_node": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_apprunner_custom_domain_association": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_apprunner_service": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_vpc"
        ]
    },
    "aws_apprunner_vpc_connector": {
        "hard": [
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_apprunner_vpc_ingress_connection": {
        "hard": [],
        "optional": [
            "aws_vpc",
            "aws_vpc_endpoint"
        ]
    },
    "aws_appstream_fleet": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_appstream_image_builder": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_appstream_stack": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_appsync_datasource": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster",
            "aws_iam_role"
        ]
    },
    "aws_appsync_domain_name": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_appsync_graphql_api": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_athena_database": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_athena_workgroup": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key",
            "aws_s3_bucket"
        ]
    },
    "aws_auditmanager_assessment": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_auditmanager_assessment_delegation": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_autoscaling_attachment": {
        "hard": [],
        "optional": [
            "aws_lb_target_group"
        ]
    },
    "aws_autoscaling_group": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_launch_template",
            "aws_vpc"
        ]
    },
    "aws_autoscaling_lifecycle_hook": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_autoscaling_notification": {
        "hard": [
            "aws_sns_topic"
        ],
        "optional": []
    },
    "aws_autoscaling_policy": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_autoscalingplans_scaling_plan": {
        "hard": [],
        "optional": [
            "aws_cloudformation_stack",
            "aws_iam_policy"
        ]
    },
    "aws_backup_report_plan": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_backup_restore_testing_selection": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_backup_selection": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_backup_vault": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_backup_vault_lock_configuration": {
        "hard": [],
        "optional": [
            "aws_backup_vault"
        ]
    },
    "aws_backup_vault_notifications": {
        "hard": [
            "aws_sns_topic"
        ],
        "optional": [
            "aws_backup_vault"
        ]
    },
    "aws_backup_vault_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": [
            "aws_backup_vault"
        ]
    },
    "aws_batch_compute_environment": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster",
            "aws_eks_cluster",
            "aws_iam_role",
            "aws_launch_template",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_batch_job_definition": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_batch_job_queue": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_bcmdataexports_export": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_bedrock_custom_model": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_bedrock_guardrail": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_bedrock_model_invocation_logging_configuration": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_iam_role",
            "aws_s3_bucket"
        ]
    },
    "aws_bedrockagent_agent": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_bedrockagent_agent_action_group": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_bedrockagent_data_source": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_kms_key",
            "aws_s3_bucket"
        ]
    },
    "aws_bedrockagent_knowledge_base": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_bedrockagent_prompt": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_budgets_budget": {
        "hard": [],
        "optional": [
            "aws_sns_topic"
        ]
    },
    "aws_budgets_budget_action": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_iam_policy",
            "aws_instance"
        ]
    },
    "aws_chatbot_slack_channel_configuration": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_iam_policy",
            "aws_sns_topic"
        ]
    },
    "aws_chatbot_teams_channel_configuration": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_iam_policy",
            "aws_sns_topic"
        ]
    },
    "aws_chimesdkmediapipelines_media_insights_pipeline_configuration": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_chimesdkvoice_global_settings": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_chimesdkvoice_voice_profile_domain": {
        "hard": [
            "aws_kms_key"
        ],
        "optional": []
    },
    "aws_cleanrooms_membership": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_s3_bucket"
        ]
    },
    "aws_cloud9_environment_ec2": {
        "hard": [],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_cloudcontrolapi_resource": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cloudformation_stack": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_iam_role"
        ]
    },
    "aws_cloudformation_stack_set": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cloudformation_type": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_iam_role"
        ]
    },
    "aws_cloudfront_distribution": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": [
            "aws_acm_certificate",
            "aws_s3_bucket",
            "aws_vpc",
            "aws_wafv2_web_acl"
        ]
    },
    "aws_cloudfront_realtime_log_config": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_cloudfront_response_headers_policy": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_cloudfront_vpc_origin": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_cloudhsm_v2_cluster": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_ecs_cluster",
            "aws_security_group",
            "aws_vpc"
        ]
    },
    "aws_cloudhsm_v2_hsm": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_cloudsearch_domain": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_cloudsearch_domain_service_access_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_cloudtrail": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": [
            "aws_iam_role",
            "aws_kms_key",
            "aws_sns_topic"
        ]
    },
    "aws_cloudtrail_event_data_store": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_cloudwatch_event_bus_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_cloudwatch_event_endpoint": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cloudwatch_event_rule": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cloudwatch_event_target": {
        "hard": [],
        "optional": [
            "aws_ecs_task_definition",
            "aws_iam_role",
            "aws_subnet"
        ]
    },
    "aws_cloudwatch_log_account_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_cloudwatch_log_anomaly_detector": {
        "hard": [
            "aws_cloudwatch_log_group"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_cloudwatch_log_data_protection_policy": {
        "hard": [
            "aws_cloudwatch_log_group",
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_cloudwatch_log_delivery_destination_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_cloudwatch_log_destination": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_cloudwatch_log_destination_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_cloudwatch_log_group": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_cloudwatch_log_index_policy": {
        "hard": [
            "aws_cloudwatch_log_group",
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_cloudwatch_log_metric_filter": {
        "hard": [
            "aws_cloudwatch_log_group"
        ],
        "optional": []
    },
    "aws_cloudwatch_log_resource_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_cloudwatch_log_stream": {
        "hard": [
            "aws_cloudwatch_log_group"
        ],
        "optional": []
    },
    "aws_cloudwatch_log_subscription_filter": {
        "hard": [
            "aws_cloudwatch_log_group"
        ],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cloudwatch_metric_stream": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_cloudwatch_query_definition": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group"
        ]
    },
    "aws_codeartifact_domain": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_codeartifact_domain_permissions_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_codeartifact_repository_permissions_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_codebuild_fleet": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_codebuild_project": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_acm_certificate",
            "aws_s3_bucket",
            "aws_security_group",
            "aws_sqs_queue",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_codebuild_report_group": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_codebuild_resource_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_codecommit_repository": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_codeconnections_host": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_codedeploy_deployment_group": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_ecs_cluster"
        ]
    },
    "aws_codegurureviewer_repository_association": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_s3_bucket"
        ]
    },
    "aws_codepipeline": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_codestarconnections_host": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_cognito_identity_pool_roles_attachment": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_cognito_managed_user_pool_client": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cognito_user_group": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cognito_user_pool": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_cognito_user_pool_client": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cognito_user_pool_domain": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_cloudfront_distribution",
            "aws_s3_bucket"
        ]
    },
    "aws_comprehend_document_classifier": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_comprehend_entity_recognizer": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_config_config_rule": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_config_configuration_aggregator": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_config_configuration_recorder": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_config_conformance_pack": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_config_delivery_channel": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": [
            "aws_sns_topic"
        ]
    },
    "aws_config_organization_conformance_pack": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_config_organization_custom_policy_rule": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_config_organization_custom_rule": {
        "hard": [
            "aws_lambda_function"
        ],
        "optional": []
    },
    "aws_connect_bot_association": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_connect_contact_flow": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_connect_contact_flow_module": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_connect_hours_of_operation": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_connect_instance": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_connect_instance_storage_config": {
        "hard": [
            "aws_instance"
        ],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_connect_lambda_function_association": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_connect_queue": {
        "hard": [
            "aws_instance"
        ],
        "optional": [
            "aws_sqs_queue"
        ]
    },
    "aws_connect_quick_connect": {
        "hard": [
            "aws_instance"
        ],
        "optional": [
            "aws_sqs_queue"
        ]
    },
    "aws_connect_routing_profile": {
        "hard": [
            "aws_instance",
            "aws_sqs_queue"
        ],
        "optional": []
    },
    "aws_connect_security_profile": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_connect_user": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_connect_user_hierarchy_group": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_connect_user_hierarchy_structure": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_connect_vocabulary": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_cur_report_definition": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_customer_gateway": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_customerprofiles_domain": {
        "hard": [],
        "optional": [
            "aws_s3_bucket",
            "aws_sqs_queue"
        ]
    },
    "aws_dataexchange_event_action": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_s3_bucket"
        ]
    },
    "aws_dataexchange_revision_assets": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_s3_bucket"
        ]
    },
    "aws_datasync_agent": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet",
            "aws_vpc_endpoint"
        ]
    },
    "aws_datasync_location_efs": {
        "hard": [
            "aws_efs_file_system",
            "aws_security_group",
            "aws_subnet"
        ],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_datasync_location_fsx_lustre_file_system": {
        "hard": [
            "aws_security_group"
        ],
        "optional": []
    },
    "aws_datasync_location_fsx_ontap_file_system": {
        "hard": [
            "aws_security_group"
        ],
        "optional": []
    },
    "aws_datasync_location_fsx_openzfs_file_system": {
        "hard": [
            "aws_security_group"
        ],
        "optional": []
    },
    "aws_datasync_location_fsx_windows_file_system": {
        "hard": [
            "aws_security_group"
        ],
        "optional": []
    },
    "aws_datasync_location_object_storage": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_datasync_location_s3": {
        "hard": [
            "aws_iam_role",
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_datasync_task": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_iam_role",
            "aws_s3_bucket",
            "aws_sqs_queue"
        ]
    },
    "aws_datazone_domain": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_datazone_environment_blueprint_configuration": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_dax_cluster": {
        "hard": [
            "aws_ecs_cluster",
            "aws_iam_role"
        ],
        "optional": [
            "aws_security_group",
            "aws_sns_topic",
            "aws_subnet"
        ]
    },
    "aws_dax_subnet_group": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_db_cluster_snapshot": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_kms_key",
            "aws_vpc"
        ]
    },
    "aws_db_event_subscription": {
        "hard": [
            "aws_sns_topic"
        ],
        "optional": []
    },
    "aws_db_instance": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key",
            "aws_s3_bucket",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_db_instance_automated_backups_replication": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_db_instance_role_association": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_db_option_group": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_db_proxy": {
        "hard": [
            "aws_iam_role",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_db_proxy_endpoint": {
        "hard": [
            "aws_vpc"
        ],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_db_proxy_target": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster"
        ]
    },
    "aws_db_snapshot": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_vpc"
        ]
    },
    "aws_db_snapshot_copy": {
        "hard": [],
        "optional": [
            "aws_db_snapshot",
            "aws_kms_key",
            "aws_vpc"
        ]
    },
    "aws_db_subnet_group": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_default_network_acl": {
        "hard": [],
        "optional": [
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_default_route_table": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_default_security_group": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_default_subnet": {
        "hard": [],
        "optional": [
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_default_vpc": {
        "hard": [],
        "optional": [
            "aws_default_network_acl",
            "aws_default_route_table",
            "aws_default_security_group",
            "aws_vpc"
        ]
    },
    "aws_devicefarm_test_grid_project": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_devopsguru_notification_channel": {
        "hard": [],
        "optional": [
            "aws_sns_topic"
        ]
    },
    "aws_devopsguru_service_integration": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_directory_service_directory": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_directory_service_log_subscription": {
        "hard": [
            "aws_cloudwatch_log_group"
        ],
        "optional": []
    },
    "aws_directory_service_region": {
        "hard": [
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_dlm_lifecycle_policy": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_dms_certificate": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_dms_endpoint": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_iam_role",
            "aws_kms_key",
            "aws_s3_bucket",
            "aws_sns_topic"
        ]
    },
    "aws_dms_event_subscription": {
        "hard": [
            "aws_sns_topic"
        ],
        "optional": []
    },
    "aws_dms_replication_config": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_kms_key",
            "aws_vpc"
        ]
    },
    "aws_dms_replication_instance": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_dms_replication_subnet_group": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_dms_s3_endpoint": {
        "hard": [
            "aws_iam_role",
            "aws_s3_bucket"
        ],
        "optional": [
            "aws_acm_certificate",
            "aws_kms_key"
        ]
    },
    "aws_docdb_cluster": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster",
            "aws_kms_key",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_docdb_cluster_instance": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_kms_key",
            "aws_subnet"
        ]
    },
    "aws_docdb_cluster_snapshot": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_db_cluster_snapshot",
            "aws_kms_key",
            "aws_vpc"
        ]
    },
    "aws_docdb_event_subscription": {
        "hard": [
            "aws_sns_topic"
        ],
        "optional": []
    },
    "aws_docdb_global_cluster": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_docdb_subnet_group": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_docdbelastic_cluster": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_drs_replication_configuration_template": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_dsql_cluster": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster",
            "aws_vpc"
        ]
    },
    "aws_dsql_cluster_peering": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_dx_gateway_association": {
        "hard": [
            "aws_dx_gateway"
        ],
        "optional": [
            "aws_vpn_gateway"
        ]
    },
    "aws_dx_gateway_association_proposal": {
        "hard": [
            "aws_dx_gateway"
        ],
        "optional": []
    },
    "aws_dx_hosted_private_virtual_interface_accepter": {
        "hard": [],
        "optional": [
            "aws_dx_gateway",
            "aws_vpn_gateway"
        ]
    },
    "aws_dx_hosted_transit_virtual_interface_accepter": {
        "hard": [
            "aws_dx_gateway"
        ],
        "optional": []
    },
    "aws_dx_private_virtual_interface": {
        "hard": [],
        "optional": [
            "aws_dx_gateway",
            "aws_vpn_gateway"
        ]
    },
    "aws_dx_transit_virtual_interface": {
        "hard": [
            "aws_dx_gateway"
        ],
        "optional": []
    },
    "aws_dynamodb_resource_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_dynamodb_table": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_s3_bucket"
        ]
    },
    "aws_dynamodb_table_export": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_dynamodb_table_replica": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_ebs_snapshot": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_ebs_snapshot_copy": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_ebs_snapshot_import": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key",
            "aws_s3_bucket"
        ]
    },
    "aws_ebs_volume": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_ec2_capacity_block_reservation": {
        "hard": [],
        "optional": [
            "aws_placement_group"
        ]
    },
    "aws_ec2_capacity_reservation": {
        "hard": [],
        "optional": [
            "aws_placement_group"
        ]
    },
    "aws_ec2_carrier_gateway": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_ec2_client_vpn_endpoint": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_lambda_function",
            "aws_security_group",
            "aws_vpc"
        ]
    },
    "aws_ec2_client_vpn_network_association": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_ec2_client_vpn_route": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_ec2_fleet": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_instance",
            "aws_launch_template",
            "aws_subnet"
        ]
    },
    "aws_ec2_instance_connect_endpoint": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_network_interface",
            "aws_security_group",
            "aws_vpc"
        ]
    },
    "aws_ec2_instance_state": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_ec2_local_gateway_route_table_vpc_association": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_ec2_subnet_cidr_reservation": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_ec2_traffic_mirror_session": {
        "hard": [
            "aws_network_interface"
        ],
        "optional": []
    },
    "aws_ec2_traffic_mirror_target": {
        "hard": [],
        "optional": [
            "aws_network_interface"
        ]
    },
    "aws_ec2_transit_gateway_multicast_domain_association": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_ec2_transit_gateway_multicast_group_member": {
        "hard": [
            "aws_network_interface"
        ],
        "optional": []
    },
    "aws_ec2_transit_gateway_multicast_group_source": {
        "hard": [
            "aws_network_interface"
        ],
        "optional": []
    },
    "aws_ec2_transit_gateway_policy_table_association": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_ec2_transit_gateway_vpc_attachment": {
        "hard": [
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_ec2_transit_gateway_vpc_attachment_accepter": {
        "hard": [],
        "optional": [
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_ecr_lifecycle_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_ecr_pull_through_cache_rule": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_ecr_registry_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_ecr_repository_creation_template": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_iam_role"
        ]
    },
    "aws_ecr_repository_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_ecrpublic_repository_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_ecs_cluster": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_kms_key",
            "aws_s3_bucket"
        ]
    },
    "aws_ecs_cluster_capacity_providers": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_ecs_service": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster",
            "aws_ecs_task_definition",
            "aws_iam_role",
            "aws_kms_key",
            "aws_subnet"
        ]
    },
    "aws_ecs_task_definition": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_ecs_task_set": {
        "hard": [
            "aws_ecs_cluster",
            "aws_ecs_task_definition"
        ],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_efs_file_system": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_efs_file_system_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_efs_mount_target": {
        "hard": [
            "aws_efs_file_system", "aws_subnet"
        ],
        "optional": [
            "aws_network_interface"
        ]
    },
    "aws_efs_replication_configuration": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_egress_only_internet_gateway": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_eip": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_eip_association": {
        "hard": [],
        "optional": [
            "aws_instance",
            "aws_network_interface"
        ]
    },
    "aws_eks_access_entry": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_eks_access_policy_association": {
        "hard": [
            "aws_ecs_cluster",
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_eks_addon": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_eks_cluster": {
        "hard": [
            "aws_iam_role",
            "aws_subnet"
        ],
        "optional": [
            "aws_acm_certificate",
            "aws_ecs_cluster",
            "aws_security_group",
            "aws_vpc"
        ]
    },
    "aws_eks_fargate_profile": {
        "hard": [
            "aws_ecs_cluster",
            "aws_iam_role"
        ],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_eks_identity_provider_config": {
        "hard": [
            "aws_ecs_cluster"
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
    "aws_eks_pod_identity_association": {
        "hard": [
            "aws_ecs_cluster",
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_elastic_beanstalk_application": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_elastic_beanstalk_application_version": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_elastic_beanstalk_environment": {
        "hard": [],
        "optional": [
            "aws_sqs_queue"
        ]
    },
    "aws_elasticache_cluster": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_security_group",
            "aws_sns_topic",
            "aws_subnet"
        ]
    },
    "aws_elasticache_global_replication_group": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster"
        ]
    },
    "aws_elasticache_replication_group": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster",
            "aws_kms_key",
            "aws_security_group",
            "aws_sns_topic",
            "aws_subnet"
        ]
    },
    "aws_elasticache_serverless_cache": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_elasticache_subnet_group": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_elasticsearch_domain": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_cloudwatch_log_group",
            "aws_iam_policy",
            "aws_iam_role",
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_elasticsearch_domain_saml_options": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_elasticsearch_vpc_endpoint": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_security_group",
            "aws_vpc"
        ]
    },
    "aws_elastictranscoder_pipeline": {
        "hard": [
            "aws_iam_role",
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_elastictranscoder_preset": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_elb": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_s3_bucket",
            "aws_subnet"
        ]
    },
    "aws_emr_cluster": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_ecs_cluster",
            "aws_iam_policy",
            "aws_subnet"
        ]
    },
    "aws_emr_instance_fleet": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_emr_instance_group": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_emr_managed_scaling_policy": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_emr_studio": {
        "hard": [
            "aws_iam_role",
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_emr_studio_session_mapping": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_emrcontainers_job_template": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_kms_key"
        ]
    },
    "aws_emrserverless_application": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_evidently_project": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_s3_bucket"
        ]
    },
    "aws_finspace_kx_cluster": {
        "hard": [
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": [
            "aws_iam_role",
            "aws_s3_bucket"
        ]
    },
    "aws_finspace_kx_environment": {
        "hard": [
            "aws_kms_key"
        ],
        "optional": []
    },
    "aws_finspace_kx_scaling_group": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster"
        ]
    },
    "aws_finspace_kx_user": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_finspace_kx_volume": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster"
        ]
    },
    "aws_fis_experiment_template": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_s3_bucket"
        ]
    },
    "aws_flow_log": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_iam_role",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_fms_policy": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_fsx_backup": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_fsx_file_cache": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_kms_key",
            "aws_network_interface",
            "aws_security_group",
            "aws_vpc"
        ]
    },
    "aws_fsx_lustre_file_system": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_iam_policy",
            "aws_kms_key",
            "aws_network_interface",
            "aws_security_group",
            "aws_vpc"
        ]
    },
    "aws_fsx_ontap_file_system": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_kms_key",
            "aws_network_interface",
            "aws_route_table",
            "aws_security_group",
            "aws_vpc"
        ]
    },
    "aws_fsx_ontap_volume": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_fsx_openzfs_file_system": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_kms_key",
            "aws_network_interface",
            "aws_route_table",
            "aws_security_group",
            "aws_vpc"
        ]
    },
    "aws_fsx_windows_file_system": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_kms_key",
            "aws_network_interface",
            "aws_security_group",
            "aws_vpc"
        ]
    },
    "aws_gamelift_build": {
        "hard": [
            "aws_iam_role",
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_gamelift_fleet": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_iam_policy",
            "aws_iam_role"
        ]
    },
    "aws_gamelift_game_server_group": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_iam_policy",
            "aws_vpc"
        ]
    },
    "aws_gamelift_game_session_queue": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_gamelift_script": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_s3_bucket"
        ]
    },
    "aws_glacier_vault": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_sns_topic"
        ]
    },
    "aws_glacier_vault_lock": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_globalaccelerator_accelerator": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_globalaccelerator_custom_routing_accelerator": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_glue_catalog_table": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_glue_catalog_table_optimizer": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_glue_connection": {
        "hard": [],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_glue_crawler": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_sqs_queue"
        ]
    },
    "aws_glue_data_catalog_encryption_settings": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_glue_dev_endpoint": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_glue_job": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_glue_ml_transform": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_glue_partition": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_glue_resource_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_glue_security_configuration": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_grafana_role_association": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_grafana_workspace": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_grafana_workspace_api_key": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_grafana_workspace_saml_configuration": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_grafana_workspace_service_account": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_guardduty_malware_protection_plan": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_guardduty_publishing_destination": {
        "hard": [
            "aws_kms_key"
        ],
        "optional": []
    },
    "aws_iam_group_policies_exclusive": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_iam_group_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_iam_group_policy_attachment": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_iam_group_policy_attachments_exclusive": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_iam_instance_profile": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_iam_policy_attachment": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_iam_role": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_iam_role_policies_exclusive": {
        "hard": [
            "aws_iam_policy",
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_iam_role_policy": {
        "hard": [
            "aws_iam_policy",
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_iam_role_policy_attachment": {
        "hard": [
            "aws_iam_policy",
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_iam_role_policy_attachments_exclusive": {
        "hard": [
            "aws_iam_policy",
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_iam_server_certificate": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_iam_signing_certificate": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_iam_user_policies_exclusive": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_iam_user_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_iam_user_policy_attachment": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_iam_user_policy_attachments_exclusive": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_imagebuilder_component": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_imagebuilder_container_recipe": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_imagebuilder_distribution_configuration": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key",
            "aws_launch_template",
            "aws_s3_bucket"
        ]
    },
    "aws_imagebuilder_image": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_imagebuilder_image_pipeline": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_imagebuilder_image_recipe": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_imagebuilder_infrastructure_configuration": {
        "hard": [],
        "optional": [
            "aws_s3_bucket",
            "aws_security_group",
            "aws_sns_topic",
            "aws_subnet"
        ]
    },
    "aws_imagebuilder_lifecycle_policy": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_imagebuilder_workflow": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_inspector_assessment_template": {
        "hard": [],
        "optional": [
            "aws_sns_topic"
        ]
    },
    "aws_instance": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_network_interface",
            "aws_spot_instance_request",
            "aws_subnet",
            "aws_vpc",
            "aws_security_group"
        ]
    },
    "aws_internet_gateway": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_internet_gateway_attachment": {
        "hard": [
            "aws_internet_gateway",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_internetmonitor_monitor": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_iot_ca_certificate": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_iot_certificate": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_iot_domain_configuration": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_iam_policy"
        ]
    },
    "aws_iot_logging_options": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_iot_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_iot_policy_attachment": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_iot_provisioning_template": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_iot_role_alias": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_iot_topic_rule": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_iam_role",
            "aws_s3_bucket",
            "aws_sns_topic",
            "aws_sqs_queue"
        ]
    },
    "aws_iot_topic_rule_destination": {
        "hard": [
            "aws_iam_role",
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_ivs_recording_configuration": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_ivschat_logging_configuration": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_s3_bucket"
        ]
    },
    "aws_kendra_data_source": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_s3_bucket"
        ]
    },
    "aws_kendra_experience": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_kendra_faq": {
        "hard": [
            "aws_iam_role",
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_kendra_index": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_iam_policy",
            "aws_kms_key"
        ]
    },
    "aws_kendra_query_suggestions_block_list": {
        "hard": [
            "aws_iam_role",
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_kendra_thesaurus": {
        "hard": [
            "aws_iam_role",
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_kinesis_analytics_application": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_s3_bucket"
        ]
    },
    "aws_kinesis_firehose_delivery_stream": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_ecs_cluster",
            "aws_iam_role",
            "aws_kinesis_stream",
            "aws_kms_key",
            "aws_msk_cluster",
            "aws_s3_bucket",
            "aws_security_group",
            "aws_sns_topic",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_kinesis_resource_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_kinesis_stream": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_kinesis_video_stream": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_kinesisanalyticsv2_application": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_s3_bucket",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_kms_custom_key_store": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_ecs_cluster",
            "aws_vpc"
        ]
    },
    "aws_kms_external_key": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_kms_key": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_kms_key_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_kms_replica_external_key": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_kms_replica_key": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_lakeformation_resource": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_lambda_event_source_mapping": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_sns_topic",
            "aws_sqs_queue"
        ]
    },
    "aws_lambda_function": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_kms_key",
            "aws_s3_bucket",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_lambda_layer_version": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_lambda_layer_version_permission": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_launch_template": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_network_interface",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_lb": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_s3_bucket",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_lb_listener": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_iam_policy"
        ]
    },
    "aws_lb_listener_certificate": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_lb_target_group": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_lb_trust_store": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_lb_trust_store_revocation": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_lex_bot_alias": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key"
        ]
    },
    "aws_lexv2models_bot": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_lexv2models_slot_type": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_s3_bucket"
        ]
    },
    "aws_lightsail_bucket_access_key": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_lightsail_bucket_resource_access": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_lightsail_container_service": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_lightsail_database": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_lightsail_distribution": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_iam_policy"
        ]
    },
    "aws_lightsail_lb_certificate_attachment": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_load_balancer_backend_server_policy": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_load_balancer_listener_policy": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_load_balancer_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_location_geofence_collection": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_location_tracker": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_m2_application": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key"
        ]
    },
    "aws_m2_environment": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_macie2_account": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_macie2_classification_export_configuration": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_s3_bucket"
        ]
    },
    "aws_macie2_classification_job": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_main_route_table_association": {
        "hard": [
            "aws_route_table",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_media_store_container_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_medialive_channel": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_iam_policy",
            "aws_iam_role",
            "aws_network_interface",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_medialive_input": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_memorydb_cluster": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster",
            "aws_kms_key",
            "aws_security_group",
            "aws_sns_topic",
            "aws_subnet"
        ]
    },
    "aws_memorydb_multi_region_cluster": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_memorydb_snapshot": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_memorydb_subnet_group": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_mq_broker": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key",
            "aws_subnet"
        ]
    },
    "aws_msk_cluster": {
        "hard": [
            "aws_ecs_cluster",
            "aws_subnet"
        ],
        "optional": [
            "aws_acm_certificate",
            "aws_cloudwatch_log_group",
            "aws_s3_bucket",
            "aws_vpc"
        ]
    },
    "aws_msk_cluster_policy": {
        "hard": [
            "aws_ecs_cluster",
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_msk_replicator": {
        "hard": [
            "aws_ecs_cluster",
            "aws_iam_role",
            "aws_msk_cluster",
            "aws_sns_topic",
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_msk_scram_secret_association": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_msk_serverless_cluster": {
        "hard": [
            "aws_ecs_cluster",
            "aws_subnet"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_msk_single_scram_secret_association": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_msk_vpc_connection": {
        "hard": [
            "aws_ecs_cluster",
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_mskconnect_connector": {
        "hard": [
            "aws_iam_role",
            "aws_subnet"
        ],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_s3_bucket"
        ]
    },
    "aws_mskconnect_custom_plugin": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_mwaa_environment": {
        "hard": [
            "aws_iam_role",
            "aws_s3_bucket",
            "aws_security_group",
            "aws_subnet"
        ],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_vpc"
        ]
    },
    "aws_nat_gateway": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_network_interface"
        ]
    },
    "aws_neptune_cluster": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster",
            "aws_iam_role",
            "aws_kms_key",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_neptune_cluster_endpoint": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_neptune_cluster_instance": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_kms_key",
            "aws_subnet"
        ]
    },
    "aws_neptune_cluster_snapshot": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_db_cluster_snapshot",
            "aws_kms_key",
            "aws_vpc"
        ]
    },
    "aws_neptune_event_subscription": {
        "hard": [
            "aws_sns_topic"
        ],
        "optional": []
    },
    "aws_neptune_global_cluster": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_neptune_subnet_group": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_network_acl": {
        "hard": [
            "aws_vpc"
        ],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_network_acl_association": {
        "hard": [
            "aws_network_acl",
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_network_acl_rule": {
        "hard": [
            "aws_network_acl"
        ],
        "optional": []
    },
    "aws_network_interface": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_network_interface_attachment": {
        "hard": [
            "aws_instance",
            "aws_network_interface"
        ],
        "optional": []
    },
    "aws_network_interface_permission": {
        "hard": [
            "aws_network_interface"
        ],
        "optional": []
    },
    "aws_network_interface_sg_attachment": {
        "hard": [
            "aws_network_interface",
            "aws_security_group"
        ],
        "optional": []
    },
    "aws_networkfirewall_firewall": {
        "hard": [
            "aws_iam_policy",
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_networkfirewall_firewall_policy": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_networkfirewall_resource_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_networkfirewall_tls_inspection_configuration": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_networkmanager_attachment_accepter": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_networkmanager_connect_attachment": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_networkmanager_connect_peer": {
        "hard": [],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_networkmanager_core_network": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_networkmanager_core_network_policy_attachment": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_networkmanager_customer_gateway_association": {
        "hard": [
            "aws_customer_gateway"
        ],
        "optional": []
    },
    "aws_networkmanager_device": {
        "hard": [],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_networkmanager_dx_gateway_attachment": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_networkmanager_site_to_site_vpn_attachment": {
        "hard": [
            "aws_vpn_connection"
        ],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_networkmanager_transit_gateway_route_table_attachment": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_networkmanager_vpc_attachment": {
        "hard": [
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_networkmonitor_probe": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_oam_sink_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_opensearch_domain": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_cloudwatch_log_group",
            "aws_iam_policy",
            "aws_iam_role",
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_opensearch_domain_saml_options": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_opensearch_package": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_opensearch_vpc_endpoint": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_security_group",
            "aws_vpc"
        ]
    },
    "aws_opensearchserverless_access_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_opensearchserverless_collection": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_opensearchserverless_lifecycle_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_opensearchserverless_security_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_opensearchserverless_vpc_endpoint": {
        "hard": [
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_opsworks_application": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_opsworks_custom_layer": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group"
        ]
    },
    "aws_opsworks_ecs_cluster_layer": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_cloudwatch_log_group"
        ]
    },
    "aws_opsworks_ganglia_layer": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group"
        ]
    },
    "aws_opsworks_haproxy_layer": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group"
        ]
    },
    "aws_opsworks_instance": {
        "hard": [],
        "optional": [
            "aws_ami",
            "aws_ecs_cluster",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_opsworks_java_app_layer": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group"
        ]
    },
    "aws_opsworks_memcached_layer": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group"
        ]
    },
    "aws_opsworks_mysql_layer": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group"
        ]
    },
    "aws_opsworks_nodejs_app_layer": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group"
        ]
    },
    "aws_opsworks_php_app_layer": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group"
        ]
    },
    "aws_opsworks_rails_app_layer": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group"
        ]
    },
    "aws_opsworks_stack": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_default_subnet",
            "aws_vpc"
        ]
    },
    "aws_opsworks_static_web_layer": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group"
        ]
    },
    "aws_organizations_account": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_organizations_organization": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_organizations_policy_attachment": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_osis_pipeline": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_pinpoint_apns_channel": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_pinpoint_apns_sandbox_channel": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_pinpoint_apns_voip_channel": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_pinpoint_apns_voip_sandbox_channel": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_pinpoint_email_channel": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_pinpoint_event_stream": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_pinpointsmsvoicev2_phone_number": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_pipes_pipe": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_acm_certificate",
            "aws_cloudwatch_log_group",
            "aws_ecs_task_definition",
            "aws_s3_bucket",
            "aws_sns_topic",
            "aws_sqs_queue",
            "aws_subnet"
        ]
    },
    "aws_prometheus_scraper": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster",
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_prometheus_workspace": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_kms_key"
        ]
    },
    "aws_qbusiness_application": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_qldb_stream": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_quicksight_analysis": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_quicksight_dashboard": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_quicksight_data_set": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_iam_role"
        ]
    },
    "aws_quicksight_data_source": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster",
            "aws_iam_role",
            "aws_instance",
            "aws_s3_bucket",
            "aws_vpc"
        ]
    },
    "aws_quicksight_iam_policy_assignment": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_quicksight_role_membership": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_quicksight_template": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_quicksight_user": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_quicksight_vpc_connection": {
        "hard": [
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_rds_certificate": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_rds_cluster": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_ecs_cluster",
            "aws_iam_role",
            "aws_kms_key",
            "aws_s3_bucket",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_rds_cluster_activity_stream": {
        "hard": [
            "aws_kms_key"
        ],
        "optional": []
    },
    "aws_rds_cluster_endpoint": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_rds_cluster_instance": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_iam_role",
            "aws_kms_key",
            "aws_subnet"
        ]
    },
    "aws_rds_cluster_role_association": {
        "hard": [
            "aws_ecs_cluster",
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_rds_cluster_snapshot_copy": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_db_cluster_snapshot",
            "aws_kms_key",
            "aws_vpc"
        ]
    },
    "aws_rds_custom_db_engine_version": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_s3_bucket"
        ]
    },
    "aws_rds_export_task": {
        "hard": [
            "aws_iam_role",
            "aws_kms_key",
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_rds_global_cluster": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_rds_integration": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_rds_shard_group": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_redshift_cluster": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_iam_role",
            "aws_kms_key",
            "aws_s3_bucket",
            "aws_vpc"
        ]
    },
    "aws_redshift_cluster_iam_roles": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_redshift_cluster_snapshot": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_redshift_endpoint_access": {
        "hard": [
            "aws_ecs_cluster",
            "aws_subnet"
        ],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_redshift_endpoint_authorization": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_redshift_event_subscription": {
        "hard": [
            "aws_sns_topic"
        ],
        "optional": []
    },
    "aws_redshift_hsm_client_certificate": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_redshift_hsm_configuration": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_redshift_integration": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_redshift_logging": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_redshift_partner": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_redshift_resource_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_redshift_scheduled_action": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_ecs_cluster"
        ]
    },
    "aws_redshift_snapshot_copy": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_redshift_snapshot_copy_grant": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_redshift_snapshot_schedule_association": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_redshift_subnet_group": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_redshift_usage_limit": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_redshiftdata_statement": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster"
        ]
    },
    "aws_redshiftserverless_custom_domain_association": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_redshiftserverless_endpoint_access": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_redshiftserverless_namespace": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key"
        ]
    },
    "aws_redshiftserverless_resource_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_redshiftserverless_snapshot": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_redshiftserverless_workgroup": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_rekognition_stream_processor": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key",
            "aws_s3_bucket",
            "aws_sns_topic"
        ]
    },
    "aws_rolesanywhere_profile": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_iam_role"
        ]
    },
    "aws_rolesanywhere_trust_anchor": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
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
            "aws_vpc_peering_connection"
        ]
    },
    "aws_route53_query_log": {
        "hard": [
            "aws_cloudwatch_log_group"
        ],
        "optional": []
    },
    "aws_route53_record": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_route53_records_exclusive": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_route53_resolver_endpoint": {
        "hard": [
            "aws_security_group",
            "aws_subnet"
        ],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_route53_resolver_firewall_rule_group_association": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_route53_resolver_rule_association": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_route53_traffic_policy_instance": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_route53_vpc_association_authorization": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_route53_zone": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_route53_zone_association": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_route53recoverycontrolconfig_cluster": {
        "hard": [],
        "optional": [
            "aws_ecs_cluster"
        ]
    },
    "aws_route53recoverycontrolconfig_control_panel": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_route53recoverycontrolconfig_routing_control": {
        "hard": [
            "aws_ecs_cluster"
        ],
        "optional": []
    },
    "aws_route_table": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_route_table_association": {
        "hard": [
            "aws_route_table"
        ],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_rum_app_monitor": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_iam_role"
        ]
    },
    "aws_rum_metrics_destination": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_s3_access_point": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": [
            "aws_iam_policy",
            "aws_vpc"
        ]
    },
    "aws_s3_account_public_access_block": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_s3_bucket"
        ]
    },
    "aws_s3_bucket": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_iam_role"
        ]
    },
    "aws_s3_bucket_accelerate_configuration": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_acl": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_analytics_configuration": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_cors_configuration": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_intelligent_tiering_configuration": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_inventory": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_lifecycle_configuration": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_logging": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_metric": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_notification": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": [
            "aws_lambda_function",
            "aws_sns_topic",
            "aws_sqs_queue"
        ]
    },
    "aws_s3_bucket_object": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_s3_bucket_object_lock_configuration": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_ownership_controls": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_policy": {
        "hard": [
            "aws_iam_policy",
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_public_access_block": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_s3_bucket_replication_configuration": {
        "hard": [
            "aws_iam_role",
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_request_payment_configuration": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_server_side_encryption_configuration": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_versioning": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_bucket_website_configuration": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_directory_bucket": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3_object": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_s3_object_copy": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_s3control_access_grants_instance_resource_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_s3control_access_grants_location": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_s3control_access_point_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_s3control_bucket": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3control_bucket_lifecycle_configuration": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3control_bucket_policy": {
        "hard": [
            "aws_iam_policy",
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3control_multi_region_access_point": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_s3control_multi_region_access_point_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_s3control_object_lambda_access_point_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_s3control_storage_lens_configuration": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_s3outposts_endpoint": {
        "hard": [
            "aws_security_group",
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_s3tables_namespace": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3tables_table": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3tables_table_bucket_policy": {
        "hard": [
            "aws_iam_policy",
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_s3tables_table_policy": {
        "hard": [
            "aws_iam_policy",
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_sagemaker_app": {
        "hard": [],
        "optional": [
            "aws_sagemaker_image",
            "aws_sagemaker_image_version"
        ]
    },
    "aws_sagemaker_data_quality_job_definition": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_sagemaker_device_fleet": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_sagemaker_domain": {
        "hard": [
            "aws_iam_role",
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": [
            "aws_kms_key",
            "aws_sagemaker_image",
            "aws_sagemaker_image_version",
            "aws_security_group"
        ]
    },
    "aws_sagemaker_endpoint_configuration": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_sns_topic"
        ]
    },
    "aws_sagemaker_feature_group": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_sagemaker_flow_definition": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_sagemaker_image": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_sagemaker_mlflow_tracking_server": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_sagemaker_model": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_sagemaker_model_package_group_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_sagemaker_notebook_instance": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key",
            "aws_network_interface",
            "aws_subnet"
        ]
    },
    "aws_sagemaker_pipeline": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_s3_bucket"
        ]
    },
    "aws_sagemaker_space": {
        "hard": [],
        "optional": [
            "aws_sagemaker_image",
            "aws_sagemaker_image_version"
        ]
    },
    "aws_sagemaker_user_profile": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_sagemaker_image",
            "aws_sagemaker_image_version"
        ]
    },
    "aws_sagemaker_workforce": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet",
            "aws_vpc",
            "aws_vpc_endpoint"
        ]
    },
    "aws_sagemaker_workteam": {
        "hard": [],
        "optional": [
            "aws_sns_topic",
            "aws_vpc"
        ]
    },
    "aws_scheduler_schedule": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_ecs_task_definition",
            "aws_kms_key",
            "aws_subnet"
        ]
    },
    "aws_schemas_registry_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_secretsmanager_secret": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_kms_key"
        ]
    },
    "aws_secretsmanager_secret_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_security_group": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_security_group_rule": {
        "hard": [
            "aws_security_group"
        ],
        "optional": []
    },
    "aws_securityhub_configuration_policy_association": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_securitylake_custom_log_source": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_securitylake_data_lake": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_securitylake_subscriber": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_s3_bucket"
        ]
    },
    "aws_securitylake_subscriber_notification": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_service_discovery_instance": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_service_discovery_private_dns_namespace": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_service_discovery_service": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_servicecatalog_provisioned_product": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_servicecatalog_service_action": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_ses_configuration_set": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_ses_event_destination": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_sns_topic"
        ]
    },
    "aws_ses_identity_notification_topic": {
        "hard": [],
        "optional": [
            "aws_sns_topic"
        ]
    },
    "aws_ses_identity_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_ses_receipt_filter": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_ses_receipt_rule": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_iam_role",
            "aws_kms_key",
            "aws_s3_bucket",
            "aws_sns_topic"
        ]
    },
    "aws_sesv2_configuration_set": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_sesv2_configuration_set_event_destination": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_sns_topic"
        ]
    },
    "aws_sesv2_contact_list": {
        "hard": [],
        "optional": [
            "aws_sns_topic"
        ]
    },
    "aws_sesv2_email_identity_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_sfn_activity": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_sfn_state_machine": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_shield_drt_access_log_bucket_association": {
        "hard": [
            "aws_iam_role",
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_shield_drt_access_role_arn_association": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_shield_protection_health_check_association": {
        "hard": [
            "aws_shield_protection"
        ],
        "optional": []
    },
    "aws_signer_signing_job": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_signer_signing_profile": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_sns_platform_application": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_sns_topic"
        ]
    },
    "aws_sns_sms_preferences": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_s3_bucket"
        ]
    },
    "aws_sns_topic": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_iam_role"
        ]
    },
    "aws_sns_topic_data_protection_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_sns_topic_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_sns_topic_subscription": {
        "hard": [
            "aws_sns_topic"
        ],
        "optional": [
            "aws_iam_policy",
            "aws_iam_role"
        ]
    },
    "aws_spot_datafeed_subscription": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_spot_fleet_request": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_iam_instance_profile",
            "aws_iam_policy",
            "aws_kms_key",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_spot_instance_request": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_network_interface",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_sqs_queue": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_sqs_queue_policy": {
        "hard": [
            "aws_iam_policy",
            "aws_sqs_queue"
        ],
        "optional": []
    },
    "aws_sqs_queue_redrive_allow_policy": {
        "hard": [
            "aws_iam_policy",
            "aws_sqs_queue"
        ],
        "optional": []
    },
    "aws_sqs_queue_redrive_policy": {
        "hard": [
            "aws_iam_policy",
            "aws_sqs_queue"
        ],
        "optional": []
    },
    "aws_ssm_activation": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_ssm_association": {
        "hard": [],
        "optional": [
            "aws_instance",
            "aws_s3_bucket"
        ]
    },
    "aws_ssm_maintenance_window_task": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_iam_role",
            "aws_s3_bucket"
        ]
    },
    "aws_ssm_resource_data_sync": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_ssmincidents_replication_set": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_ssmincidents_response_plan": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_sns_topic"
        ]
    },
    "aws_ssmquicksetup_configuration_manager": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_ssoadmin_account_assignment": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_ssoadmin_application": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_ssoadmin_customer_managed_policy_attachment": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_ssoadmin_instance_access_control_attributes": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_ssoadmin_managed_policy_attachment": {
        "hard": [
            "aws_iam_policy",
            "aws_instance"
        ],
        "optional": []
    },
    "aws_ssoadmin_permission_set": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_ssoadmin_permission_set_inline_policy": {
        "hard": [
            "aws_iam_policy",
            "aws_instance"
        ],
        "optional": []
    },
    "aws_ssoadmin_permissions_boundary_attachment": {
        "hard": [
            "aws_instance"
        ],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_ssoadmin_trusted_token_issuer": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_storagegateway_cached_iscsi_volume": {
        "hard": [
            "aws_network_interface"
        ],
        "optional": []
    },
    "aws_storagegateway_gateway": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_vpc"
        ]
    },
    "aws_storagegateway_nfs_file_share": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_iam_policy",
            "aws_kms_key",
            "aws_s3_bucket",
            "aws_vpc"
        ]
    },
    "aws_storagegateway_smb_file_share": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_iam_policy",
            "aws_kms_key",
            "aws_s3_bucket",
            "aws_vpc"
        ]
    },
    "aws_storagegateway_stored_iscsi_volume": {
        "hard": [
            "aws_network_interface"
        ],
        "optional": []
    },
    "aws_subnet": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_synthetics_canary": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key",
            "aws_s3_bucket",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_timestreaminfluxdb_db_instance": {
        "hard": [
            "aws_s3_bucket",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_timestreamquery_scheduled_query": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key",
            "aws_s3_bucket",
            "aws_sns_topic"
        ]
    },
    "aws_timestreamwrite_database": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_timestreamwrite_table": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_s3_bucket"
        ]
    },
    "aws_transcribe_language_model": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_transfer_access": {
        "hard": [],
        "optional": [
            "aws_iam_policy",
            "aws_iam_role"
        ]
    },
    "aws_transfer_agreement": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_transfer_certificate": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_transfer_connector": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_transfer_profile": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_transfer_server": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_iam_policy",
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc",
            "aws_vpc_endpoint"
        ]
    },
    "aws_transfer_user": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_transfer_workflow": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_verifiedaccess_endpoint": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_ecs_cluster",
            "aws_iam_policy",
            "aws_kms_key",
            "aws_network_interface",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_verifiedaccess_group": {
        "hard": [
            "aws_verifiedaccess_instance"
        ],
        "optional": [
            "aws_iam_policy",
            "aws_kms_key"
        ]
    },
    "aws_verifiedaccess_instance_logging_configuration": {
        "hard": [
            "aws_verifiedaccess_instance"
        ],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_s3_bucket"
        ]
    },
    "aws_verifiedaccess_instance_trust_provider_attachment": {
        "hard": [
            "aws_verifiedaccess_instance",
            "aws_verifiedaccess_trust_provider"
        ],
        "optional": []
    },
    "aws_verifiedaccess_trust_provider": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_verifiedpermissions_identity_source": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_verifiedpermissions_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_verifiedpermissions_policy_store": {
        "hard": [],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_verifiedpermissions_policy_template": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_verifiedpermissions_schema": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_volume_attachment": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_vpc": {
        "hard": [],
        "optional": [
            "aws_default_network_acl",
            "aws_default_route_table",
            "aws_default_security_group"
        ]
    },
    "aws_vpc_block_public_access_exclusion": {
        "hard": [],
        "optional": [
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_vpc_dhcp_options_association": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_vpc_endpoint": {
        "hard": [
            "aws_vpc"
        ],
        "optional": [
            "aws_iam_policy",
            "aws_network_interface",
            "aws_route_table",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_vpc_endpoint_connection_accepter": {
        "hard": [
            "aws_vpc_endpoint",
            "aws_vpc_endpoint_service"
        ],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_vpc_endpoint_connection_notification": {
        "hard": [],
        "optional": [
            "aws_vpc_endpoint",
            "aws_vpc_endpoint_service"
        ]
    },
    "aws_vpc_endpoint_policy": {
        "hard": [
            "aws_vpc_endpoint"
        ],
        "optional": [
            "aws_iam_policy"
        ]
    },
    "aws_vpc_endpoint_private_dns": {
        "hard": [
            "aws_vpc_endpoint"
        ],
        "optional": []
    },
    "aws_vpc_endpoint_route_table_association": {
        "hard": [
            "aws_route_table",
            "aws_vpc_endpoint"
        ],
        "optional": []
    },
    "aws_vpc_endpoint_security_group_association": {
        "hard": [
            "aws_security_group",
            "aws_vpc_endpoint"
        ],
        "optional": []
    },
    "aws_vpc_endpoint_service": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_vpc_endpoint_service_allowed_principal": {
        "hard": [
            "aws_vpc_endpoint_service"
        ],
        "optional": []
    },
    "aws_vpc_endpoint_subnet_association": {
        "hard": [
            "aws_subnet",
            "aws_vpc_endpoint"
        ],
        "optional": []
    },
    "aws_vpc_ipv4_cidr_block_association": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_vpc_ipv6_cidr_block_association": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_vpc_peering_connection": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_vpc_peering_connection_accepter": {
        "hard": [
            "aws_vpc_peering_connection"
        ],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_vpc_peering_connection_options": {
        "hard": [
            "aws_vpc_peering_connection"
        ],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_vpc_route_server": {
        "hard": [],
        "optional": [
            "aws_sns_topic"
        ]
    },
    "aws_vpc_route_server_endpoint": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_vpc_route_server_peer": {
        "hard": [],
        "optional": [
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_vpc_route_server_propagation": {
        "hard": [
            "aws_route_table"
        ],
        "optional": []
    },
    "aws_vpc_route_server_vpc_association": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_vpc_security_group_egress_rule": {
        "hard": [
            "aws_security_group"
        ],
        "optional": [
            "aws_security_group_rule"
        ]
    },
    "aws_vpc_security_group_ingress_rule": {
        "hard": [
            "aws_security_group"
        ],
        "optional": [
            "aws_security_group_rule"
        ]
    },
    "aws_vpc_security_group_vpc_association": {
        "hard": [
            "aws_security_group",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_vpclattice_auth_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_vpclattice_resource_gateway": {
        "hard": [
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_vpclattice_resource_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_vpclattice_service": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_vpclattice_service_network_vpc_association": {
        "hard": [
            "aws_vpc"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_vpclattice_target_group": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_vpn_connection": {
        "hard": [
            "aws_customer_gateway"
        ],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_vpn_gateway"
        ]
    },
    "aws_vpn_connection_route": {
        "hard": [
            "aws_vpn_connection"
        ],
        "optional": []
    },
    "aws_vpn_gateway": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_vpn_gateway_attachment": {
        "hard": [
            "aws_vpc",
            "aws_vpn_gateway"
        ],
        "optional": []
    },
    "aws_vpn_gateway_route_propagation": {
        "hard": [
            "aws_route_table",
            "aws_vpn_gateway"
        ],
        "optional": []
    },
    "aws_wafregional_web_acl_association": {
        "hard": [
            "aws_wafv2_web_acl"
        ],
        "optional": []
    },
    "aws_wafv2_web_acl_association": {
        "hard": [
            "aws_wafv2_web_acl"
        ],
        "optional": []
    },
    "aws_worklink_fleet": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_worklink_website_certificate_authority_association": {
        "hard": [
            "aws_acm_certificate"
        ],
        "optional": []
    },
    "aws_workspaces_directory": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_iam_role",
            "aws_subnet"
        ]
    },
    "aws_workspacesweb_browser_settings": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    },
    "aws_workspacesweb_network_settings": {
        "hard": [
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_workspacesweb_user_access_logging_settings": {
        "hard": [
            "aws_kinesis_stream"
        ],
        "optional": []
    },
    "aws_xray_resource_policy": {
        "hard": [
            "aws_iam_policy"
        ],
        "optional": []
    }
}
