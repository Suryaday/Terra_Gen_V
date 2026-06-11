# AUTO-GENERATED (V3 precision) - DO NOT EDIT MANUALLY RESOURCE_DEPENDENCIES = {
    "aws_accessanalyzer_analyzer": {
        "hard": [],
        "optional": []
    },
    "aws_accessanalyzer_archive_rule": {
        "hard": [],
        "optional": []
    },
    "aws_account_alternate_contact": {
        "hard": [],
        "optional": []
    },
    "aws_account_primary_contact": {
        "hard": [],
        "optional": []
    },
    "aws_account_region": {
        "hard": [],
        "optional": []
    },
    "aws_acm_certificate": {
        "hard": [],
        "optional": []
    },
    "aws_acm_certificate_validation": {
        "hard": [],
        "optional": []
    },
    "aws_acmpca_certificate": {
        "hard": [],
        "optional": []
    },
    "aws_acmpca_certificate_authority": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_acmpca_certificate_authority_certificate": {
        "hard": [],
        "optional": []
    },
    "aws_acmpca_permission": {
        "hard": [],
        "optional": []
    },
    "aws_acmpca_policy": {
        "hard": [],
        "optional": []
    },
    "aws_alb": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_alb_listener": {
        "hard": [
            "aws_lb"
        ],
        "optional": [
            "aws_lb_target_group"
        ]
    },
    "aws_alb_listener_certificate": {
        "hard": [],
        "optional": []
    },
    "aws_alb_listener_rule": {
        "hard": [],
        "optional": [
            "aws_lb_target_group"
        ]
    },
    "aws_alb_target_group": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_alb_target_group_attachment": {
        "hard": [
            "aws_lb_target_group"
        ],
        "optional": []
    },
    "aws_ami": {
        "hard": [],
        "optional": []
    },
    "aws_ami_copy": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_ami_from_instance": {
        "hard": [],
        "optional": []
    },
    "aws_ami_launch_permission": {
        "hard": [],
        "optional": []
    },
    "aws_amplify_app": {
        "hard": [],
        "optional": []
    },
    "aws_amplify_backend_environment": {
        "hard": [],
        "optional": []
    },
    "aws_amplify_branch": {
        "hard": [],
        "optional": []
    },
    "aws_amplify_domain_association": {
        "hard": [],
        "optional": []
    },
    "aws_amplify_webhook": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_account": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_api_key": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_authorizer": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_base_path_mapping": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_client_certificate": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_deployment": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_documentation_part": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_documentation_version": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_domain_name": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_domain_name_access_association": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_gateway_response": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_integration": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_integration_response": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_method": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_method_response": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_method_settings": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_model": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_request_validator": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_resource": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_rest_api": {
        "hard": [],
        "optional": [
            "aws_vpc_endpoint"
        ]
    },
    "aws_api_gateway_rest_api_policy": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_rest_api_put": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_stage": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_usage_plan": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_usage_plan_key": {
        "hard": [],
        "optional": []
    },
    "aws_api_gateway_vpc_link": {
        "hard": [],
        "optional": []
    },
    "aws_apigatewayv2_api": {
        "hard": [],
        "optional": []
    },
    "aws_apigatewayv2_api_mapping": {
        "hard": [],
        "optional": []
    },
    "aws_apigatewayv2_authorizer": {
        "hard": [],
        "optional": []
    },
    "aws_apigatewayv2_deployment": {
        "hard": [],
        "optional": []
    },
    "aws_apigatewayv2_domain_name": {
        "hard": [],
        "optional": []
    },
    "aws_apigatewayv2_integration": {
        "hard": [],
        "optional": []
    },
    "aws_apigatewayv2_integration_response": {
        "hard": [],
        "optional": []
    },
    "aws_apigatewayv2_model": {
        "hard": [],
        "optional": []
    },
    "aws_apigatewayv2_route": {
        "hard": [],
        "optional": []
    },
    "aws_apigatewayv2_route_response": {
        "hard": [
            "aws_route"
        ],
        "optional": []
    },
    "aws_apigatewayv2_routing_rule": {
        "hard": [],
        "optional": []
    },
    "aws_apigatewayv2_stage": {
        "hard": [],
        "optional": []
    },
    "aws_apigatewayv2_vpc_link": {
        "hard": [
            "aws_security_group",
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_app_cookie_stickiness_policy": {
        "hard": [
            "aws_lb"
        ],
        "optional": []
    },
    "aws_appautoscaling_policy": {
        "hard": [],
        "optional": []
    },
    "aws_appautoscaling_scheduled_action": {
        "hard": [],
        "optional": []
    },
    "aws_appautoscaling_target": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_appconfig_application": {
        "hard": [],
        "optional": []
    },
    "aws_appconfig_configuration_profile": {
        "hard": [],
        "optional": []
    },
    "aws_appconfig_deployment": {
        "hard": [],
        "optional": []
    },
    "aws_appconfig_deployment_strategy": {
        "hard": [],
        "optional": []
    },
    "aws_appconfig_environment": {
        "hard": [],
        "optional": []
    },
    "aws_appconfig_extension": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_appconfig_extension_association": {
        "hard": [],
        "optional": []
    },
    "aws_appconfig_hosted_configuration_version": {
        "hard": [],
        "optional": []
    },
    "aws_appfabric_app_authorization": {
        "hard": [],
        "optional": []
    },
    "aws_appfabric_app_authorization_connection": {
        "hard": [],
        "optional": []
    },
    "aws_appfabric_app_bundle": {
        "hard": [],
        "optional": []
    },
    "aws_appfabric_ingestion": {
        "hard": [],
        "optional": []
    },
    "aws_appfabric_ingestion_destination": {
        "hard": [],
        "optional": []
    },
    "aws_appflow_connector_profile": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_appflow_flow": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_appintegrations_data_integration": {
        "hard": [
            "aws_kms_key"
        ],
        "optional": []
    },
    "aws_appintegrations_event_integration": {
        "hard": [],
        "optional": []
    },
    "aws_applicationinsights_application": {
        "hard": [],
        "optional": []
    },
    "aws_appmesh_gateway_route": {
        "hard": [],
        "optional": []
    },
    "aws_appmesh_mesh": {
        "hard": [],
        "optional": []
    },
    "aws_appmesh_route": {
        "hard": [],
        "optional": []
    },
    "aws_appmesh_virtual_gateway": {
        "hard": [],
        "optional": []
    },
    "aws_appmesh_virtual_node": {
        "hard": [],
        "optional": []
    },
    "aws_appmesh_virtual_router": {
        "hard": [],
        "optional": []
    },
    "aws_appmesh_virtual_service": {
        "hard": [],
        "optional": []
    },
    "aws_apprunner_auto_scaling_configuration_version": {
        "hard": [],
        "optional": []
    },
    "aws_apprunner_connection": {
        "hard": [],
        "optional": []
    },
    "aws_apprunner_custom_domain_association": {
        "hard": [],
        "optional": []
    },
    "aws_apprunner_default_auto_scaling_configuration_version": {
        "hard": [],
        "optional": []
    },
    "aws_apprunner_deployment": {
        "hard": [],
        "optional": []
    },
    "aws_apprunner_observability_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_apprunner_service": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_apprunner_vpc_connector": {
        "hard": [
            "aws_security_group",
            "aws_subnet"
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
    "aws_appstream_directory_config": {
        "hard": [],
        "optional": []
    },
    "aws_appstream_fleet": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_appstream_fleet_stack_association": {
        "hard": [],
        "optional": []
    },
    "aws_appstream_image_builder": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_appstream_stack": {
        "hard": [],
        "optional": []
    },
    "aws_appstream_user": {
        "hard": [],
        "optional": []
    },
    "aws_appstream_user_stack_association": {
        "hard": [],
        "optional": []
    },
    "aws_appsync_api": {
        "hard": [],
        "optional": []
    },
    "aws_appsync_api_cache": {
        "hard": [],
        "optional": []
    },
    "aws_appsync_api_key": {
        "hard": [],
        "optional": []
    },
    "aws_appsync_channel_namespace": {
        "hard": [],
        "optional": []
    },
    "aws_appsync_datasource": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_appsync_domain_name": {
        "hard": [],
        "optional": []
    },
    "aws_appsync_domain_name_api_association": {
        "hard": [],
        "optional": []
    },
    "aws_appsync_function": {
        "hard": [],
        "optional": []
    },
    "aws_appsync_graphql_api": {
        "hard": [],
        "optional": []
    },
    "aws_appsync_resolver": {
        "hard": [],
        "optional": []
    },
    "aws_appsync_source_api_association": {
        "hard": [],
        "optional": []
    },
    "aws_appsync_type": {
        "hard": [],
        "optional": []
    },
    "aws_arcregionswitch_plan": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_arczonalshift_autoshift_observer_notification_status": {
        "hard": [],
        "optional": []
    },
    "aws_arczonalshift_zonal_autoshift_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_athena_capacity_reservation": {
        "hard": [],
        "optional": []
    },
    "aws_athena_data_catalog": {
        "hard": [],
        "optional": []
    },
    "aws_athena_database": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_athena_named_query": {
        "hard": [],
        "optional": []
    },
    "aws_athena_prepared_statement": {
        "hard": [],
        "optional": []
    },
    "aws_athena_workgroup": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key"
        ]
    },
    "aws_auditmanager_account_registration": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_auditmanager_assessment": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_auditmanager_assessment_delegation": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_auditmanager_assessment_report": {
        "hard": [],
        "optional": []
    },
    "aws_auditmanager_control": {
        "hard": [],
        "optional": []
    },
    "aws_auditmanager_framework": {
        "hard": [],
        "optional": []
    },
    "aws_auditmanager_framework_share": {
        "hard": [],
        "optional": []
    },
    "aws_auditmanager_organization_admin_account_registration": {
        "hard": [],
        "optional": []
    },
    "aws_autoscaling_attachment": {
        "hard": [
            "aws_autoscaling_group"
        ],
        "optional": [
            "aws_elb",
            "aws_lb_target_group"
        ]
    },
    "aws_autoscaling_group": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_launch_configuration",
            "aws_launch_template",
            "aws_lb",
            "aws_lb_target_group",
            "aws_placement_group"
        ]
    },
    "aws_autoscaling_group_tag": {
        "hard": [
            "aws_autoscaling_group"
        ],
        "optional": []
    },
    "aws_autoscaling_lifecycle_hook": {
        "hard": [
            "aws_autoscaling_group"
        ],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_autoscaling_notification": {
        "hard": [],
        "optional": []
    },
    "aws_autoscaling_policy": {
        "hard": [
            "aws_autoscaling_group"
        ],
        "optional": []
    },
    "aws_autoscaling_schedule": {
        "hard": [
            "aws_autoscaling_group"
        ],
        "optional": []
    },
    "aws_autoscaling_traffic_source_attachment": {
        "hard": [
            "aws_autoscaling_group"
        ],
        "optional": []
    },
    "aws_autoscalingplans_scaling_plan": {
        "hard": [],
        "optional": [
            "aws_cloudformation_stack"
        ]
    },
    "aws_backup_framework": {
        "hard": [],
        "optional": []
    },
    "aws_backup_global_settings": {
        "hard": [],
        "optional": []
    },
    "aws_backup_logically_air_gapped_vault": {
        "hard": [],
        "optional": []
    },
    "aws_backup_plan": {
        "hard": [],
        "optional": []
    },
    "aws_backup_region_settings": {
        "hard": [],
        "optional": []
    },
    "aws_backup_report_plan": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_backup_restore_testing_plan": {
        "hard": [],
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
        "hard": [
            "aws_backup_vault"
        ],
        "optional": []
    },
    "aws_backup_vault_notifications": {
        "hard": [
            "aws_backup_vault",
            "aws_sns_topic"
        ],
        "optional": []
    },
    "aws_backup_vault_policy": {
        "hard": [
            "aws_backup_vault"
        ],
        "optional": []
    },
    "aws_batch_compute_environment": {
        "hard": [],
        "optional": [
            "aws_eks_cluster",
            "aws_iam_role",
            "aws_launch_template",
            "aws_placement_group",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_batch_job_definition": {
        "hard": [],
        "optional": []
    },
    "aws_batch_job_queue": {
        "hard": [],
        "optional": []
    },
    "aws_batch_scheduling_policy": {
        "hard": [],
        "optional": []
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
    "aws_bedrock_guardrail_version": {
        "hard": [],
        "optional": []
    },
    "aws_bedrock_inference_profile": {
        "hard": [],
        "optional": []
    },
    "aws_bedrock_model_invocation_logging_configuration": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_bedrock_provisioned_model_throughput": {
        "hard": [],
        "optional": []
    },
    "aws_bedrockagent_agent": {
        "hard": [],
        "optional": []
    },
    "aws_bedrockagent_agent_action_group": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_bedrockagent_agent_alias": {
        "hard": [],
        "optional": []
    },
    "aws_bedrockagent_agent_collaborator": {
        "hard": [],
        "optional": []
    },
    "aws_bedrockagent_agent_knowledge_base_association": {
        "hard": [],
        "optional": []
    },
    "aws_bedrockagent_data_source": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_bedrockagent_flow": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_bedrockagent_knowledge_base": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kendra_index"
        ]
    },
    "aws_bedrockagent_prompt": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_bedrockagentcore_agent_runtime": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_bedrockagentcore_agent_runtime_endpoint": {
        "hard": [],
        "optional": []
    },
    "aws_bedrockagentcore_api_key_credential_provider": {
        "hard": [],
        "optional": []
    },
    "aws_bedrockagentcore_browser": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_bedrockagentcore_code_interpreter": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_bedrockagentcore_gateway": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_bedrockagentcore_gateway_target": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_bedrockagentcore_harness": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_bedrockagentcore_memory": {
        "hard": [],
        "optional": []
    },
    "aws_bedrockagentcore_memory_strategy": {
        "hard": [],
        "optional": []
    },
    "aws_bedrockagentcore_oauth2_credential_provider": {
        "hard": [],
        "optional": []
    },
    "aws_bedrockagentcore_online_evaluation_config": {
        "hard": [],
        "optional": []
    },
    "aws_bedrockagentcore_policy": {
        "hard": [],
        "optional": []
    },
    "aws_bedrockagentcore_policy_engine": {
        "hard": [],
        "optional": []
    },
    "aws_bedrockagentcore_resource_policy": {
        "hard": [],
        "optional": []
    },
    "aws_bedrockagentcore_token_vault_cmk": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_bedrockagentcore_workload_identity": {
        "hard": [],
        "optional": []
    },
    "aws_billing_view": {
        "hard": [],
        "optional": []
    },
    "aws_budgets_budget": {
        "hard": [],
        "optional": [
            "aws_billing_view"
        ]
    },
    "aws_budgets_budget_action": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_instance"
        ]
    },
    "aws_ce_anomaly_monitor": {
        "hard": [],
        "optional": []
    },
    "aws_ce_anomaly_subscription": {
        "hard": [],
        "optional": []
    },
    "aws_ce_cost_allocation_tag": {
        "hard": [],
        "optional": []
    },
    "aws_ce_cost_category": {
        "hard": [],
        "optional": []
    },
    "aws_chatbot_slack_channel_configuration": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_sns_topic"
        ]
    },
    "aws_chatbot_teams_channel_configuration": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_sns_topic"
        ]
    },
    "aws_chime_voice_connector": {
        "hard": [],
        "optional": []
    },
    "aws_chime_voice_connector_group": {
        "hard": [],
        "optional": []
    },
    "aws_chime_voice_connector_logging": {
        "hard": [],
        "optional": []
    },
    "aws_chime_voice_connector_origination": {
        "hard": [],
        "optional": []
    },
    "aws_chime_voice_connector_streaming": {
        "hard": [],
        "optional": []
    },
    "aws_chime_voice_connector_termination": {
        "hard": [],
        "optional": []
    },
    "aws_chime_voice_connector_termination_credentials": {
        "hard": [],
        "optional": []
    },
    "aws_chimesdkmediapipelines_media_insights_pipeline_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_chimesdkvoice_global_settings": {
        "hard": [],
        "optional": []
    },
    "aws_chimesdkvoice_sip_media_application": {
        "hard": [],
        "optional": []
    },
    "aws_chimesdkvoice_sip_rule": {
        "hard": [],
        "optional": []
    },
    "aws_chimesdkvoice_voice_profile_domain": {
        "hard": [
            "aws_kms_key"
        ],
        "optional": []
    },
    "aws_cleanrooms_collaboration": {
        "hard": [],
        "optional": []
    },
    "aws_cleanrooms_configured_table": {
        "hard": [],
        "optional": []
    },
    "aws_cleanrooms_membership": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cloud9_environment_ec2": {
        "hard": [],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_cloud9_environment_membership": {
        "hard": [],
        "optional": []
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
            "aws_iam_role"
        ]
    },
    "aws_cloudformation_stack_instances": {
        "hard": [],
        "optional": []
    },
    "aws_cloudformation_stack_set": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cloudformation_stack_set_instance": {
        "hard": [],
        "optional": []
    },
    "aws_cloudformation_type": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cloudfront_anycast_ip_list": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_cache_policy": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_connection_function": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_connection_group": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_continuous_deployment_policy": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_distribution": {
        "hard": [],
        "optional": [
            "aws_acm_certificate"
        ]
    },
    "aws_cloudfront_distribution_tenant": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_field_level_encryption_config": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_field_level_encryption_profile": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_function": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_key_group": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_key_value_store": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_monitoring_subscription": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_multitenant_distribution": {
        "hard": [],
        "optional": [
            "aws_acm_certificate",
            "aws_lambda_function"
        ]
    },
    "aws_cloudfront_origin_access_control": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_origin_access_identity": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_origin_request_policy": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_public_key": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_realtime_log_config": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_cloudfront_response_headers_policy": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_trust_store": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfront_vpc_origin": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfrontkeyvaluestore_key": {
        "hard": [],
        "optional": []
    },
    "aws_cloudfrontkeyvaluestore_keys_exclusive": {
        "hard": [],
        "optional": []
    },
    "aws_cloudhsm_v2_cluster": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_cloudhsm_v2_hsm": {
        "hard": [],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_cloudsearch_domain": {
        "hard": [],
        "optional": []
    },
    "aws_cloudsearch_domain_service_access_policy": {
        "hard": [],
        "optional": []
    },
    "aws_cloudtrail": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": [
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
    "aws_cloudtrail_organization_delegated_admin_account": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_alarm_mute_rule": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_composite_alarm": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_contributor_insight_rule": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_contributor_managed_insight_rule": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_dashboard": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_event_api_destination": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_event_archive": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_event_bus": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_event_bus_policy": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_event_connection": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_event_endpoint": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cloudwatch_event_permission": {
        "hard": [],
        "optional": []
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
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_cloudwatch_log_account_policy": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_log_anomaly_detector": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_cloudwatch_log_data_protection_policy": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_log_delivery": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_log_delivery_destination": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_log_delivery_destination_policy": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_log_delivery_source": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_log_destination": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_cloudwatch_log_destination_policy": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_log_group": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_cloudwatch_log_index_policy": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_log_metric_filter": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_log_resource_policy": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_log_s3_table_integration_source": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_log_stream": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_log_subscription_filter": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cloudwatch_log_transformer": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_metric_alarm": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_metric_stream": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_cloudwatch_otel_enrichment": {
        "hard": [],
        "optional": []
    },
    "aws_cloudwatch_query_definition": {
        "hard": [],
        "optional": []
    },
    "aws_codeartifact_domain": {
        "hard": [],
        "optional": []
    },
    "aws_codeartifact_domain_permissions_policy": {
        "hard": [],
        "optional": []
    },
    "aws_codeartifact_repository": {
        "hard": [],
        "optional": []
    },
    "aws_codeartifact_repository_permissions_policy": {
        "hard": [],
        "optional": []
    },
    "aws_codebuild_fleet": {
        "hard": [],
        "optional": [
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
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_codebuild_report_group": {
        "hard": [],
        "optional": []
    },
    "aws_codebuild_resource_policy": {
        "hard": [],
        "optional": []
    },
    "aws_codebuild_source_credential": {
        "hard": [],
        "optional": []
    },
    "aws_codebuild_webhook": {
        "hard": [],
        "optional": []
    },
    "aws_codecatalyst_dev_environment": {
        "hard": [],
        "optional": []
    },
    "aws_codecatalyst_project": {
        "hard": [],
        "optional": []
    },
    "aws_codecatalyst_source_repository": {
        "hard": [],
        "optional": []
    },
    "aws_codecommit_approval_rule_template": {
        "hard": [],
        "optional": []
    },
    "aws_codecommit_approval_rule_template_association": {
        "hard": [],
        "optional": []
    },
    "aws_codecommit_repository": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_codecommit_trigger": {
        "hard": [],
        "optional": []
    },
    "aws_codeconnections_connection": {
        "hard": [],
        "optional": []
    },
    "aws_codeconnections_host": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_codedeploy_app": {
        "hard": [],
        "optional": []
    },
    "aws_codedeploy_deployment_config": {
        "hard": [],
        "optional": []
    },
    "aws_codedeploy_deployment_group": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_autoscaling_group"
        ]
    },
    "aws_codeguruprofiler_profiling_group": {
        "hard": [],
        "optional": []
    },
    "aws_codegurureviewer_repository_association": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_codepipeline": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_codepipeline_custom_action_type": {
        "hard": [],
        "optional": []
    },
    "aws_codepipeline_webhook": {
        "hard": [],
        "optional": []
    },
    "aws_codestarconnections_connection": {
        "hard": [],
        "optional": []
    },
    "aws_codestarconnections_host": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_codestarnotifications_notification_rule": {
        "hard": [],
        "optional": []
    },
    "aws_cognito_identity_pool": {
        "hard": [],
        "optional": []
    },
    "aws_cognito_identity_pool_provider_principal_tag": {
        "hard": [],
        "optional": []
    },
    "aws_cognito_identity_pool_roles_attachment": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_cognito_identity_provider": {
        "hard": [],
        "optional": []
    },
    "aws_cognito_log_delivery_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_cognito_managed_login_branding": {
        "hard": [],
        "optional": []
    },
    "aws_cognito_managed_user_pool_client": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cognito_resource_server": {
        "hard": [],
        "optional": []
    },
    "aws_cognito_risk_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_cognito_user": {
        "hard": [],
        "optional": []
    },
    "aws_cognito_user_group": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_cognito_user_in_group": {
        "hard": [],
        "optional": []
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
        "optional": []
    },
    "aws_cognito_user_pool_ui_customization": {
        "hard": [],
        "optional": []
    },
    "aws_comprehend_document_classifier": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_comprehend_entity_recognizer": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_computeoptimizer_enrollment_status": {
        "hard": [],
        "optional": []
    },
    "aws_computeoptimizer_recommendation_preferences": {
        "hard": [],
        "optional": []
    },
    "aws_config_aggregate_authorization": {
        "hard": [],
        "optional": []
    },
    "aws_config_config_rule": {
        "hard": [],
        "optional": []
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
    "aws_config_configuration_recorder_status": {
        "hard": [],
        "optional": []
    },
    "aws_config_conformance_pack": {
        "hard": [],
        "optional": []
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
        "optional": []
    },
    "aws_config_organization_custom_policy_rule": {
        "hard": [],
        "optional": []
    },
    "aws_config_organization_custom_rule": {
        "hard": [
            "aws_lambda_function"
        ],
        "optional": []
    },
    "aws_config_organization_managed_rule": {
        "hard": [],
        "optional": []
    },
    "aws_config_remediation_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_config_retention_configuration": {
        "hard": [],
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
        "optional": []
    },
    "aws_connect_instance_storage_config": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_connect_lambda_function_association": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_connect_phone_number": {
        "hard": [],
        "optional": []
    },
    "aws_connect_phone_number_contact_flow_association": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_connect_queue": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_connect_quick_connect": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_connect_routing_profile": {
        "hard": [
            "aws_instance"
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
    "aws_controltower_baseline": {
        "hard": [],
        "optional": []
    },
    "aws_controltower_control": {
        "hard": [],
        "optional": []
    },
    "aws_controltower_landing_zone": {
        "hard": [],
        "optional": []
    },
    "aws_costoptimizationhub_enrollment_status": {
        "hard": [],
        "optional": []
    },
    "aws_costoptimizationhub_preferences": {
        "hard": [],
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
        "optional": []
    },
    "aws_customerprofiles_domain": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_customerprofiles_profile": {
        "hard": [],
        "optional": []
    },
    "aws_dataexchange_data_set": {
        "hard": [],
        "optional": []
    },
    "aws_dataexchange_event_action": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_dataexchange_revision": {
        "hard": [],
        "optional": []
    },
    "aws_dataexchange_revision_assets": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_datapipeline_pipeline": {
        "hard": [],
        "optional": []
    },
    "aws_datapipeline_pipeline_definition": {
        "hard": [],
        "optional": []
    },
    "aws_datasync_agent": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet",
            "aws_vpc_endpoint"
        ]
    },
    "aws_datasync_location_azure_blob": {
        "hard": [],
        "optional": []
    },
    "aws_datasync_location_efs": {
        "hard": [
            "aws_efs_file_system",
            "aws_security_group",
            "aws_subnet"
        ],
        "optional": []
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
    "aws_datasync_location_hdfs": {
        "hard": [],
        "optional": []
    },
    "aws_datasync_location_nfs": {
        "hard": [],
        "optional": []
    },
    "aws_datasync_location_object_storage": {
        "hard": [],
        "optional": []
    },
    "aws_datasync_location_s3": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_datasync_location_smb": {
        "hard": [],
        "optional": []
    },
    "aws_datasync_task": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_s3_bucket"
        ]
    },
    "aws_datazone_asset_type": {
        "hard": [],
        "optional": []
    },
    "aws_datazone_domain": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_datazone_environment": {
        "hard": [],
        "optional": [
            "aws_account_region"
        ]
    },
    "aws_datazone_environment_blueprint_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_datazone_environment_profile": {
        "hard": [],
        "optional": []
    },
    "aws_datazone_form_type": {
        "hard": [],
        "optional": []
    },
    "aws_datazone_glossary": {
        "hard": [],
        "optional": []
    },
    "aws_datazone_glossary_term": {
        "hard": [],
        "optional": []
    },
    "aws_datazone_project": {
        "hard": [],
        "optional": []
    },
    "aws_datazone_user_profile": {
        "hard": [],
        "optional": []
    },
    "aws_dax_cluster": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_dax_parameter_group": {
        "hard": [],
        "optional": []
    },
    "aws_dax_subnet_group": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_db_cluster_snapshot": {
        "hard": [],
        "optional": []
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
            "aws_db_subnet_group",
            "aws_kms_key",
            "aws_security_group"
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
        "optional": []
    },
    "aws_db_parameter_group": {
        "hard": [],
        "optional": []
    },
    "aws_db_proxy": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_db_proxy_default_target_group": {
        "hard": [
            "aws_db_proxy"
        ],
        "optional": []
    },
    "aws_db_proxy_endpoint": {
        "hard": [
            "aws_db_proxy"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_db_proxy_target": {
        "hard": [
            "aws_db_proxy",
            "aws_lb_target_group"
        ],
        "optional": []
    },
    "aws_db_snapshot": {
        "hard": [],
        "optional": []
    },
    "aws_db_snapshot_copy": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_db_subnet_group": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_default_network_acl": {
        "hard": [],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_default_route_table": {
        "hard": [],
        "optional": []
    },
    "aws_default_security_group": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_default_subnet": {
        "hard": [],
        "optional": []
    },
    "aws_default_vpc": {
        "hard": [],
        "optional": []
    },
    "aws_default_vpc_dhcp_options": {
        "hard": [],
        "optional": []
    },
    "aws_detective_graph": {
        "hard": [],
        "optional": []
    },
    "aws_detective_invitation_accepter": {
        "hard": [],
        "optional": []
    },
    "aws_detective_member": {
        "hard": [],
        "optional": []
    },
    "aws_detective_organization_admin_account": {
        "hard": [],
        "optional": []
    },
    "aws_detective_organization_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_devicefarm_device_pool": {
        "hard": [],
        "optional": []
    },
    "aws_devicefarm_instance_profile": {
        "hard": [],
        "optional": []
    },
    "aws_devicefarm_network_profile": {
        "hard": [],
        "optional": []
    },
    "aws_devicefarm_project": {
        "hard": [],
        "optional": []
    },
    "aws_devicefarm_test_grid_project": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_devicefarm_upload": {
        "hard": [],
        "optional": []
    },
    "aws_devopsguru_event_sources_config": {
        "hard": [],
        "optional": []
    },
    "aws_devopsguru_notification_channel": {
        "hard": [],
        "optional": []
    },
    "aws_devopsguru_resource_collection": {
        "hard": [],
        "optional": []
    },
    "aws_devopsguru_service_integration": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_directory_service_conditional_forwarder": {
        "hard": [],
        "optional": []
    },
    "aws_directory_service_directory": {
        "hard": [],
        "optional": [
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_directory_service_log_subscription": {
        "hard": [],
        "optional": []
    },
    "aws_directory_service_radius_settings": {
        "hard": [],
        "optional": []
    },
    "aws_directory_service_region": {
        "hard": [
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_directory_service_shared_directory": {
        "hard": [],
        "optional": []
    },
    "aws_directory_service_shared_directory_accepter": {
        "hard": [],
        "optional": []
    },
    "aws_directory_service_trust": {
        "hard": [],
        "optional": []
    },
    "aws_dlm_lifecycle_policy": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_dms_certificate": {
        "hard": [],
        "optional": []
    },
    "aws_dms_endpoint": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_dms_event_subscription": {
        "hard": [
            "aws_sns_topic"
        ],
        "optional": []
    },
    "aws_dms_replication_config": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_security_group"
        ]
    },
    "aws_dms_replication_instance": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_security_group"
        ]
    },
    "aws_dms_replication_subnet_group": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_dms_replication_task": {
        "hard": [],
        "optional": []
    },
    "aws_dms_s3_endpoint": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_docdb_cluster": {
        "hard": [],
        "optional": [
            "aws_db_subnet_group",
            "aws_kms_key",
            "aws_security_group"
        ]
    },
    "aws_docdb_cluster_instance": {
        "hard": [],
        "optional": []
    },
    "aws_docdb_cluster_parameter_group": {
        "hard": [],
        "optional": []
    },
    "aws_docdb_cluster_snapshot": {
        "hard": [],
        "optional": []
    },
    "aws_docdb_event_subscription": {
        "hard": [
            "aws_sns_topic"
        ],
        "optional": []
    },
    "aws_docdb_global_cluster": {
        "hard": [],
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
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_drs_replication_configuration_template": {
        "hard": [],
        "optional": []
    },
    "aws_dsql_cluster": {
        "hard": [],
        "optional": []
    },
    "aws_dsql_cluster_peering": {
        "hard": [],
        "optional": []
    },
    "aws_dx_bgp_peer": {
        "hard": [],
        "optional": []
    },
    "aws_dx_connection": {
        "hard": [],
        "optional": []
    },
    "aws_dx_connection_association": {
        "hard": [],
        "optional": []
    },
    "aws_dx_connection_confirmation": {
        "hard": [],
        "optional": []
    },
    "aws_dx_gateway": {
        "hard": [],
        "optional": []
    },
    "aws_dx_gateway_association": {
        "hard": [
            "aws_dx_gateway"
        ],
        "optional": []
    },
    "aws_dx_gateway_association_proposal": {
        "hard": [
            "aws_dx_gateway"
        ],
        "optional": []
    },
    "aws_dx_hosted_connection": {
        "hard": [],
        "optional": []
    },
    "aws_dx_hosted_private_virtual_interface": {
        "hard": [],
        "optional": []
    },
    "aws_dx_hosted_private_virtual_interface_accepter": {
        "hard": [],
        "optional": [
            "aws_dx_gateway",
            "aws_vpn_gateway"
        ]
    },
    "aws_dx_hosted_public_virtual_interface": {
        "hard": [],
        "optional": []
    },
    "aws_dx_hosted_public_virtual_interface_accepter": {
        "hard": [],
        "optional": []
    },
    "aws_dx_hosted_transit_virtual_interface": {
        "hard": [],
        "optional": []
    },
    "aws_dx_hosted_transit_virtual_interface_accepter": {
        "hard": [
            "aws_dx_gateway"
        ],
        "optional": []
    },
    "aws_dx_lag": {
        "hard": [],
        "optional": []
    },
    "aws_dx_macsec_key_association": {
        "hard": [],
        "optional": []
    },
    "aws_dx_private_virtual_interface": {
        "hard": [],
        "optional": [
            "aws_dx_gateway",
            "aws_vpn_gateway"
        ]
    },
    "aws_dx_public_virtual_interface": {
        "hard": [],
        "optional": []
    },
    "aws_dx_transit_virtual_interface": {
        "hard": [
            "aws_dx_gateway"
        ],
        "optional": []
    },
    "aws_dynamodb_contributor_insights": {
        "hard": [],
        "optional": []
    },
    "aws_dynamodb_global_secondary_index": {
        "hard": [],
        "optional": []
    },
    "aws_dynamodb_global_table": {
        "hard": [],
        "optional": []
    },
    "aws_dynamodb_kinesis_streaming_destination": {
        "hard": [],
        "optional": []
    },
    "aws_dynamodb_resource_policy": {
        "hard": [],
        "optional": []
    },
    "aws_dynamodb_table": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_dynamodb_table_export": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_dynamodb_table_item": {
        "hard": [],
        "optional": []
    },
    "aws_dynamodb_table_replica": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_dynamodb_tag": {
        "hard": [],
        "optional": []
    },
    "aws_ebs_default_kms_key": {
        "hard": [],
        "optional": []
    },
    "aws_ebs_encryption_by_default": {
        "hard": [],
        "optional": []
    },
    "aws_ebs_fast_snapshot_restore": {
        "hard": [],
        "optional": []
    },
    "aws_ebs_snapshot": {
        "hard": [],
        "optional": []
    },
    "aws_ebs_snapshot_block_public_access": {
        "hard": [],
        "optional": []
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
    "aws_ebs_volume_copy": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_allowed_images_settings": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_availability_zone_group": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_capacity_block_reservation": {
        "hard": [],
        "optional": []
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
    "aws_ec2_client_vpn_authorization_rule": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_client_vpn_endpoint": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_cloudwatch_log_stream",
            "aws_lambda_function",
            "aws_security_group",
            "aws_vpc"
        ]
    },
    "aws_ec2_client_vpn_network_association": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_ec2_client_vpn_route": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_default_credit_specification": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_fleet": {
        "hard": [],
        "optional": [
            "aws_instance",
            "aws_launch_template",
            "aws_subnet"
        ]
    },
    "aws_ec2_host": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_image_block_public_access": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_instance_connect_endpoint": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_ec2_instance_metadata_defaults": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_instance_state": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_ec2_local_gateway_route": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_local_gateway_route_table": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_local_gateway_route_table_virtual_interface_group_association": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_local_gateway_route_table_vpc_association": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_ec2_managed_prefix_list": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_managed_prefix_list_entry": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_network_insights_access_scope": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_network_insights_analysis": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_network_insights_path": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_secondary_network": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_secondary_subnet": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_serial_console_access": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_subnet_cidr_reservation": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_ec2_tag": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_traffic_mirror_filter": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_traffic_mirror_filter_rule": {
        "hard": [],
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
    "aws_ec2_transit_gateway": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_connect": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_connect_peer": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_default_route_table_association": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_default_route_table_propagation": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_metering_policy": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_metering_policy_entry": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_multicast_domain": {
        "hard": [],
        "optional": []
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
    "aws_ec2_transit_gateway_peering_attachment": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_peering_attachment_accepter": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_policy_table": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_policy_table_association": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_prefix_list_reference": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_route": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_route_table": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_route_table_association": {
        "hard": [],
        "optional": []
    },
    "aws_ec2_transit_gateway_route_table_propagation": {
        "hard": [],
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
        "optional": []
    },
    "aws_ecr_account_setting": {
        "hard": [],
        "optional": []
    },
    "aws_ecr_lifecycle_policy": {
        "hard": [],
        "optional": []
    },
    "aws_ecr_pull_through_cache_rule": {
        "hard": [],
        "optional": []
    },
    "aws_ecr_pull_time_update_exclusion": {
        "hard": [],
        "optional": []
    },
    "aws_ecr_registry_policy": {
        "hard": [],
        "optional": []
    },
    "aws_ecr_registry_scanning_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_ecr_replication_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_ecr_repository": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_ecr_repository_creation_template": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_ecr_repository_policy": {
        "hard": [],
        "optional": []
    },
    "aws_ecrpublic_repository": {
        "hard": [],
        "optional": []
    },
    "aws_ecrpublic_repository_policy": {
        "hard": [],
        "optional": []
    },
    "aws_ecs_account_setting_default": {
        "hard": [],
        "optional": []
    },
    "aws_ecs_capacity_provider": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_ecs_cluster": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_s3_bucket"
        ]
    },
    "aws_ecs_cluster_capacity_providers": {
        "hard": [],
        "optional": []
    },
    "aws_ecs_daemon": {
        "hard": [],
        "optional": []
    },
    "aws_ecs_daemon_task_definition": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_ecs_express_gateway_service": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_ecs_service": {
        "hard": [],
        "optional": [
            "aws_elb",
            "aws_iam_role",
            "aws_kms_key",
            "aws_lb_target_group",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_ecs_tag": {
        "hard": [],
        "optional": []
    },
    "aws_ecs_task_definition": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_ecs_task_set": {
        "hard": [],
        "optional": [
            "aws_lb",
            "aws_lb_target_group",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_efs_access_point": {
        "hard": [],
        "optional": []
    },
    "aws_efs_backup_policy": {
        "hard": [],
        "optional": []
    },
    "aws_efs_file_system": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_efs_file_system_policy": {
        "hard": [],
        "optional": []
    },
    "aws_efs_mount_target": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_security_group"
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
            "aws_instance",
            "aws_network_interface"
        ]
    },
    "aws_eip_association": {
        "hard": [],
        "optional": [
            "aws_instance",
            "aws_network_interface"
        ]
    },
    "aws_eip_domain_name": {
        "hard": [],
        "optional": []
    },
    "aws_eks_access_entry": {
        "hard": [],
        "optional": []
    },
    "aws_eks_access_policy_association": {
        "hard": [],
        "optional": []
    },
    "aws_eks_addon": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_eks_capability": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_eks_cluster": {
        "hard": [
            "aws_iam_role",
            "aws_subnet"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_eks_fargate_profile": {
        "hard": [],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_eks_identity_provider_config": {
        "hard": [],
        "optional": []
    },
    "aws_eks_node_group": {
        "hard": [
            "aws_iam_role",
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_eks_pod_identity_association": {
        "hard": [
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
        "hard": [],
        "optional": []
    },
    "aws_elastic_beanstalk_configuration_template": {
        "hard": [],
        "optional": []
    },
    "aws_elastic_beanstalk_environment": {
        "hard": [],
        "optional": []
    },
    "aws_elasticache_cluster": {
        "hard": [],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_elasticache_global_replication_group": {
        "hard": [],
        "optional": []
    },
    "aws_elasticache_parameter_group": {
        "hard": [],
        "optional": []
    },
    "aws_elasticache_replication_group": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_security_group"
        ]
    },
    "aws_elasticache_reserved_cache_node": {
        "hard": [],
        "optional": []
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
        "optional": []
    },
    "aws_elasticache_user": {
        "hard": [],
        "optional": []
    },
    "aws_elasticache_user_group": {
        "hard": [],
        "optional": []
    },
    "aws_elasticache_user_group_association": {
        "hard": [],
        "optional": []
    },
    "aws_elasticsearch_domain": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_iam_role",
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_elasticsearch_domain_policy": {
        "hard": [],
        "optional": []
    },
    "aws_elasticsearch_domain_saml_options": {
        "hard": [],
        "optional": []
    },
    "aws_elasticsearch_vpc_endpoint": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_elastictranscoder_pipeline": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_elastictranscoder_preset": {
        "hard": [],
        "optional": []
    },
    "aws_elb": {
        "hard": [],
        "optional": [
            "aws_instance",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_elb_attachment": {
        "hard": [
            "aws_elb",
            "aws_instance"
        ],
        "optional": []
    },
    "aws_emr_block_public_access_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_emr_cluster": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_autoscaling_policy",
            "aws_subnet"
        ]
    },
    "aws_emr_instance_fleet": {
        "hard": [],
        "optional": []
    },
    "aws_emr_instance_group": {
        "hard": [],
        "optional": [
            "aws_autoscaling_policy"
        ]
    },
    "aws_emr_managed_scaling_policy": {
        "hard": [],
        "optional": []
    },
    "aws_emr_security_configuration": {
        "hard": [],
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
        "hard": [],
        "optional": []
    },
    "aws_emrcontainers_job_template": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_emrcontainers_virtual_cluster": {
        "hard": [],
        "optional": []
    },
    "aws_emrserverless_application": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_evidently_feature": {
        "hard": [],
        "optional": []
    },
    "aws_evidently_launch": {
        "hard": [],
        "optional": []
    },
    "aws_evidently_project": {
        "hard": [],
        "optional": []
    },
    "aws_evidently_segment": {
        "hard": [],
        "optional": []
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
    "aws_finspace_kx_database": {
        "hard": [],
        "optional": []
    },
    "aws_finspace_kx_dataview": {
        "hard": [],
        "optional": []
    },
    "aws_finspace_kx_environment": {
        "hard": [
            "aws_kms_key"
        ],
        "optional": []
    },
    "aws_finspace_kx_scaling_group": {
        "hard": [],
        "optional": []
    },
    "aws_finspace_kx_user": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_finspace_kx_volume": {
        "hard": [],
        "optional": []
    },
    "aws_fis_experiment_template": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_fis_target_account_configuration": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_flow_log": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_fms_admin_account": {
        "hard": [],
        "optional": []
    },
    "aws_fms_policy": {
        "hard": [],
        "optional": []
    },
    "aws_fms_resource_set": {
        "hard": [],
        "optional": []
    },
    "aws_fsx_backup": {
        "hard": [],
        "optional": []
    },
    "aws_fsx_data_repository_association": {
        "hard": [],
        "optional": []
    },
    "aws_fsx_file_cache": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_kms_key",
            "aws_security_group"
        ]
    },
    "aws_fsx_lustre_file_system": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_kms_key",
            "aws_security_group"
        ]
    },
    "aws_fsx_ontap_file_system": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_kms_key",
            "aws_route_table",
            "aws_security_group"
        ]
    },
    "aws_fsx_ontap_storage_virtual_machine": {
        "hard": [],
        "optional": []
    },
    "aws_fsx_ontap_volume": {
        "hard": [],
        "optional": []
    },
    "aws_fsx_openzfs_file_system": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_kms_key",
            "aws_route_table",
            "aws_security_group"
        ]
    },
    "aws_fsx_openzfs_snapshot": {
        "hard": [],
        "optional": []
    },
    "aws_fsx_openzfs_volume": {
        "hard": [],
        "optional": []
    },
    "aws_fsx_s3_access_point_attachment": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_fsx_windows_file_system": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_kms_key",
            "aws_security_group"
        ]
    },
    "aws_gamelift_alias": {
        "hard": [],
        "optional": []
    },
    "aws_gamelift_build": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_gamelift_fleet": {
        "hard": [],
        "optional": []
    },
    "aws_gamelift_game_server_group": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_gamelift_game_session_queue": {
        "hard": [],
        "optional": []
    },
    "aws_gamelift_script": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_glacier_vault": {
        "hard": [],
        "optional": [
            "aws_sns_topic"
        ]
    },
    "aws_glacier_vault_lock": {
        "hard": [],
        "optional": []
    },
    "aws_globalaccelerator_accelerator": {
        "hard": [],
        "optional": []
    },
    "aws_globalaccelerator_cross_account_attachment": {
        "hard": [],
        "optional": []
    },
    "aws_globalaccelerator_custom_routing_accelerator": {
        "hard": [],
        "optional": []
    },
    "aws_globalaccelerator_custom_routing_endpoint_group": {
        "hard": [],
        "optional": []
    },
    "aws_globalaccelerator_custom_routing_listener": {
        "hard": [],
        "optional": []
    },
    "aws_globalaccelerator_endpoint_group": {
        "hard": [],
        "optional": []
    },
    "aws_globalaccelerator_listener": {
        "hard": [],
        "optional": []
    },
    "aws_glue_catalog": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key"
        ]
    },
    "aws_glue_catalog_database": {
        "hard": [],
        "optional": []
    },
    "aws_glue_catalog_table": {
        "hard": [],
        "optional": []
    },
    "aws_glue_catalog_table_optimizer": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_glue_classifier": {
        "hard": [],
        "optional": []
    },
    "aws_glue_connection": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_subnet"
        ]
    },
    "aws_glue_crawler": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_glue_data_catalog_encryption_settings": {
        "hard": [],
        "optional": []
    },
    "aws_glue_data_quality_ruleset": {
        "hard": [],
        "optional": []
    },
    "aws_glue_dev_endpoint": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_security_group",
            "aws_subnet"
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
        "optional": []
    },
    "aws_glue_partition_index": {
        "hard": [],
        "optional": []
    },
    "aws_glue_registry": {
        "hard": [],
        "optional": []
    },
    "aws_glue_resource_policy": {
        "hard": [],
        "optional": []
    },
    "aws_glue_schema": {
        "hard": [],
        "optional": []
    },
    "aws_glue_security_configuration": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_glue_trigger": {
        "hard": [],
        "optional": []
    },
    "aws_glue_user_defined_function": {
        "hard": [],
        "optional": []
    },
    "aws_glue_workflow": {
        "hard": [],
        "optional": []
    },
    "aws_grafana_license_association": {
        "hard": [],
        "optional": []
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
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_grafana_workspace_api_key": {
        "hard": [],
        "optional": []
    },
    "aws_grafana_workspace_saml_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_grafana_workspace_service_account": {
        "hard": [],
        "optional": []
    },
    "aws_grafana_workspace_service_account_token": {
        "hard": [],
        "optional": []
    },
    "aws_guardduty_detector": {
        "hard": [],
        "optional": []
    },
    "aws_guardduty_detector_feature": {
        "hard": [],
        "optional": []
    },
    "aws_guardduty_filter": {
        "hard": [],
        "optional": []
    },
    "aws_guardduty_invite_accepter": {
        "hard": [],
        "optional": []
    },
    "aws_guardduty_ipset": {
        "hard": [],
        "optional": []
    },
    "aws_guardduty_malware_protection_plan": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_guardduty_member": {
        "hard": [],
        "optional": []
    },
    "aws_guardduty_member_detector_feature": {
        "hard": [],
        "optional": []
    },
    "aws_guardduty_organization_admin_account": {
        "hard": [],
        "optional": []
    },
    "aws_guardduty_organization_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_guardduty_organization_configuration_feature": {
        "hard": [],
        "optional": []
    },
    "aws_guardduty_publishing_destination": {
        "hard": [
            "aws_kms_key"
        ],
        "optional": []
    },
    "aws_guardduty_threatintelset": {
        "hard": [],
        "optional": []
    },
    "aws_iam_access_key": {
        "hard": [],
        "optional": []
    },
    "aws_iam_account_alias": {
        "hard": [],
        "optional": []
    },
    "aws_iam_account_password_policy": {
        "hard": [],
        "optional": []
    },
    "aws_iam_group": {
        "hard": [],
        "optional": []
    },
    "aws_iam_group_membership": {
        "hard": [],
        "optional": []
    },
    "aws_iam_group_policies_exclusive": {
        "hard": [],
        "optional": []
    },
    "aws_iam_group_policy": {
        "hard": [],
        "optional": []
    },
    "aws_iam_group_policy_attachment": {
        "hard": [],
        "optional": []
    },
    "aws_iam_group_policy_attachments_exclusive": {
        "hard": [],
        "optional": []
    },
    "aws_iam_instance_profile": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_iam_openid_connect_provider": {
        "hard": [],
        "optional": []
    },
    "aws_iam_organizations_features": {
        "hard": [],
        "optional": []
    },
    "aws_iam_outbound_web_identity_federation": {
        "hard": [],
        "optional": []
    },
    "aws_iam_policy": {
        "hard": [],
        "optional": []
    },
    "aws_iam_policy_attachment": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_iam_role": {
        "hard": [],
        "optional": []
    },
    "aws_iam_role_policies_exclusive": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_iam_role_policy": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_iam_role_policy_attachment": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_iam_role_policy_attachments_exclusive": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_iam_saml_provider": {
        "hard": [],
        "optional": []
    },
    "aws_iam_security_token_service_preferences": {
        "hard": [],
        "optional": []
    },
    "aws_iam_server_certificate": {
        "hard": [],
        "optional": []
    },
    "aws_iam_service_linked_role": {
        "hard": [],
        "optional": []
    },
    "aws_iam_service_specific_credential": {
        "hard": [],
        "optional": []
    },
    "aws_iam_signing_certificate": {
        "hard": [],
        "optional": []
    },
    "aws_iam_user": {
        "hard": [],
        "optional": []
    },
    "aws_iam_user_group_membership": {
        "hard": [],
        "optional": []
    },
    "aws_iam_user_login_profile": {
        "hard": [],
        "optional": []
    },
    "aws_iam_user_policies_exclusive": {
        "hard": [],
        "optional": []
    },
    "aws_iam_user_policy": {
        "hard": [],
        "optional": []
    },
    "aws_iam_user_policy_attachment": {
        "hard": [],
        "optional": []
    },
    "aws_iam_user_policy_attachments_exclusive": {
        "hard": [],
        "optional": []
    },
    "aws_iam_user_ssh_key": {
        "hard": [],
        "optional": []
    },
    "aws_iam_virtual_mfa_device": {
        "hard": [],
        "optional": []
    },
    "aws_identitystore_group": {
        "hard": [],
        "optional": []
    },
    "aws_identitystore_group_membership": {
        "hard": [],
        "optional": []
    },
    "aws_identitystore_user": {
        "hard": [],
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
            "aws_key_pair",
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
        "optional": [
            "aws_ami"
        ]
    },
    "aws_imagebuilder_workflow": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_inspector2_delegated_admin_account": {
        "hard": [],
        "optional": []
    },
    "aws_inspector2_enabler": {
        "hard": [],
        "optional": []
    },
    "aws_inspector2_filter": {
        "hard": [],
        "optional": []
    },
    "aws_inspector2_member_association": {
        "hard": [],
        "optional": []
    },
    "aws_inspector2_organization_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_inspector_assessment_target": {
        "hard": [],
        "optional": []
    },
    "aws_inspector_assessment_template": {
        "hard": [],
        "optional": []
    },
    "aws_inspector_resource_group": {
        "hard": [],
        "optional": []
    },
    "aws_instance": {
        "hard": [],
        "optional": [
            "aws_ami",
            "aws_iam_instance_profile",
            "aws_kms_key",
            "aws_network_interface",
            "aws_placement_group",
            "aws_security_group",
            "aws_subnet"
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
        "optional": []
    },
    "aws_invoicing_invoice_unit": {
        "hard": [],
        "optional": []
    },
    "aws_iot_authorizer": {
        "hard": [],
        "optional": []
    },
    "aws_iot_billing_group": {
        "hard": [],
        "optional": []
    },
    "aws_iot_ca_certificate": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_iot_certificate": {
        "hard": [],
        "optional": []
    },
    "aws_iot_domain_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_iot_event_configurations": {
        "hard": [],
        "optional": []
    },
    "aws_iot_indexing_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_iot_logging_options": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_iot_policy": {
        "hard": [],
        "optional": []
    },
    "aws_iot_policy_attachment": {
        "hard": [],
        "optional": []
    },
    "aws_iot_provisioning_template": {
        "hard": [],
        "optional": []
    },
    "aws_iot_role_alias": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_iot_thing": {
        "hard": [],
        "optional": []
    },
    "aws_iot_thing_group": {
        "hard": [],
        "optional": []
    },
    "aws_iot_thing_group_membership": {
        "hard": [],
        "optional": []
    },
    "aws_iot_thing_principal_attachment": {
        "hard": [],
        "optional": []
    },
    "aws_iot_thing_type": {
        "hard": [],
        "optional": []
    },
    "aws_iot_topic_rule": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_iot_topic_rule_destination": {
        "hard": [
            "aws_iam_role",
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_ivs_channel": {
        "hard": [],
        "optional": []
    },
    "aws_ivs_playback_key_pair": {
        "hard": [],
        "optional": []
    },
    "aws_ivs_recording_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_ivschat_logging_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_ivschat_room": {
        "hard": [],
        "optional": []
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
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_kendra_index": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_kendra_query_suggestions_block_list": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_kendra_thesaurus": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_key_pair": {
        "hard": [],
        "optional": []
    },
    "aws_keyspaces_keyspace": {
        "hard": [],
        "optional": []
    },
    "aws_keyspaces_table": {
        "hard": [],
        "optional": []
    },
    "aws_kinesis_account_settings": {
        "hard": [],
        "optional": []
    },
    "aws_kinesis_analytics_application": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_kinesis_firehose_delivery_stream": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kinesis_stream",
            "aws_kms_key",
            "aws_msk_cluster",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_kinesis_resource_policy": {
        "hard": [],
        "optional": []
    },
    "aws_kinesis_stream": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_kinesis_stream_consumer": {
        "hard": [],
        "optional": []
    },
    "aws_kinesis_video_stream": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_kinesisanalyticsv2_application": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_kinesisanalyticsv2_application_snapshot": {
        "hard": [],
        "optional": []
    },
    "aws_kms_alias": {
        "hard": [],
        "optional": []
    },
    "aws_kms_ciphertext": {
        "hard": [],
        "optional": []
    },
    "aws_kms_custom_key_store": {
        "hard": [],
        "optional": []
    },
    "aws_kms_external_key": {
        "hard": [],
        "optional": []
    },
    "aws_kms_grant": {
        "hard": [],
        "optional": []
    },
    "aws_kms_key": {
        "hard": [],
        "optional": []
    },
    "aws_kms_key_policy": {
        "hard": [],
        "optional": []
    },
    "aws_kms_replica_external_key": {
        "hard": [],
        "optional": []
    },
    "aws_kms_replica_key": {
        "hard": [],
        "optional": []
    },
    "aws_lakeformation_data_cells_filter": {
        "hard": [],
        "optional": []
    },
    "aws_lakeformation_data_lake_settings": {
        "hard": [],
        "optional": []
    },
    "aws_lakeformation_identity_center_configuration": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_lakeformation_lf_tag": {
        "hard": [],
        "optional": []
    },
    "aws_lakeformation_lf_tag_expression": {
        "hard": [],
        "optional": []
    },
    "aws_lakeformation_opt_in": {
        "hard": [],
        "optional": []
    },
    "aws_lakeformation_permissions": {
        "hard": [],
        "optional": []
    },
    "aws_lakeformation_resource": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_lakeformation_resource_lf_tag": {
        "hard": [],
        "optional": []
    },
    "aws_lakeformation_resource_lf_tags": {
        "hard": [],
        "optional": []
    },
    "aws_lambda_alias": {
        "hard": [],
        "optional": []
    },
    "aws_lambda_capacity_provider": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_lambda_code_signing_config": {
        "hard": [],
        "optional": []
    },
    "aws_lambda_event_source_mapping": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_lambda_function": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key",
            "aws_s3_bucket",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_lambda_function_event_invoke_config": {
        "hard": [],
        "optional": []
    },
    "aws_lambda_function_recursion_config": {
        "hard": [],
        "optional": []
    },
    "aws_lambda_function_url": {
        "hard": [],
        "optional": []
    },
    "aws_lambda_invocation": {
        "hard": [],
        "optional": []
    },
    "aws_lambda_layer_version": {
        "hard": [],
        "optional": [
            "aws_s3_bucket"
        ]
    },
    "aws_lambda_layer_version_permission": {
        "hard": [],
        "optional": []
    },
    "aws_lambda_permission": {
        "hard": [],
        "optional": []
    },
    "aws_lambda_provisioned_concurrency_config": {
        "hard": [],
        "optional": []
    },
    "aws_lambda_runtime_management_config": {
        "hard": [],
        "optional": []
    },
    "aws_launch_configuration": {
        "hard": [],
        "optional": [
            "aws_iam_instance_profile",
            "aws_security_group"
        ]
    },
    "aws_launch_template": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_network_interface",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_lb": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_lb_cookie_stickiness_policy": {
        "hard": [
            "aws_lb"
        ],
        "optional": []
    },
    "aws_lb_listener": {
        "hard": [
            "aws_lb"
        ],
        "optional": [
            "aws_lb_target_group"
        ]
    },
    "aws_lb_listener_certificate": {
        "hard": [],
        "optional": []
    },
    "aws_lb_listener_rule": {
        "hard": [],
        "optional": [
            "aws_lb_target_group"
        ]
    },
    "aws_lb_ssl_negotiation_policy": {
        "hard": [
            "aws_lb"
        ],
        "optional": []
    },
    "aws_lb_target_group": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_lb_target_group_attachment": {
        "hard": [
            "aws_lb_target_group"
        ],
        "optional": []
    },
    "aws_lb_trust_store": {
        "hard": [],
        "optional": []
    },
    "aws_lb_trust_store_revocation": {
        "hard": [],
        "optional": []
    },
    "aws_lex_bot": {
        "hard": [],
        "optional": []
    },
    "aws_lex_bot_alias": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key"
        ]
    },
    "aws_lex_intent": {
        "hard": [],
        "optional": []
    },
    "aws_lex_slot_type": {
        "hard": [],
        "optional": []
    },
    "aws_lexv2models_bot": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_lexv2models_bot_locale": {
        "hard": [],
        "optional": []
    },
    "aws_lexv2models_bot_version": {
        "hard": [],
        "optional": []
    },
    "aws_lexv2models_intent": {
        "hard": [],
        "optional": [
            "aws_kendra_index"
        ]
    },
    "aws_lexv2models_slot": {
        "hard": [],
        "optional": []
    },
    "aws_lexv2models_slot_type": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_s3_bucket"
        ]
    },
    "aws_licensemanager_association": {
        "hard": [],
        "optional": []
    },
    "aws_licensemanager_grant": {
        "hard": [],
        "optional": []
    },
    "aws_licensemanager_grant_accepter": {
        "hard": [],
        "optional": []
    },
    "aws_licensemanager_license_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_bucket": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_bucket_access_key": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_bucket_resource_access": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_certificate": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_container_service": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_container_service_deployment_version": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_database": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_disk": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_disk_attachment": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_lightsail_distribution": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_domain": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_domain_entry": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_instance": {
        "hard": [],
        "optional": [
            "aws_key_pair"
        ]
    },
    "aws_lightsail_instance_public_ports": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_lightsail_key_pair": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_lb": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_lb_attachment": {
        "hard": [
            "aws_instance",
            "aws_lb"
        ],
        "optional": []
    },
    "aws_lightsail_lb_certificate": {
        "hard": [
            "aws_lb"
        ],
        "optional": []
    },
    "aws_lightsail_lb_certificate_attachment": {
        "hard": [
            "aws_lb"
        ],
        "optional": []
    },
    "aws_lightsail_lb_https_redirection_policy": {
        "hard": [
            "aws_lb"
        ],
        "optional": []
    },
    "aws_lightsail_lb_stickiness_policy": {
        "hard": [
            "aws_lb"
        ],
        "optional": []
    },
    "aws_lightsail_static_ip": {
        "hard": [],
        "optional": []
    },
    "aws_lightsail_static_ip_attachment": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_load_balancer_backend_server_policy": {
        "hard": [
            "aws_lb"
        ],
        "optional": []
    },
    "aws_load_balancer_listener_policy": {
        "hard": [
            "aws_lb"
        ],
        "optional": []
    },
    "aws_load_balancer_policy": {
        "hard": [
            "aws_lb"
        ],
        "optional": []
    },
    "aws_location_geofence_collection": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_location_map": {
        "hard": [],
        "optional": []
    },
    "aws_location_place_index": {
        "hard": [],
        "optional": []
    },
    "aws_location_route_calculator": {
        "hard": [],
        "optional": []
    },
    "aws_location_tracker": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_location_tracker_association": {
        "hard": [],
        "optional": []
    },
    "aws_m2_application": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key"
        ]
    },
    "aws_m2_deployment": {
        "hard": [],
        "optional": []
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
        "optional": []
    },
    "aws_macie2_classification_export_configuration": {
        "hard": [
            "aws_kms_key"
        ],
        "optional": []
    },
    "aws_macie2_classification_job": {
        "hard": [],
        "optional": []
    },
    "aws_macie2_custom_data_identifier": {
        "hard": [],
        "optional": []
    },
    "aws_macie2_findings_filter": {
        "hard": [],
        "optional": []
    },
    "aws_macie2_invitation_accepter": {
        "hard": [],
        "optional": []
    },
    "aws_macie2_member": {
        "hard": [],
        "optional": []
    },
    "aws_macie2_organization_admin_account": {
        "hard": [],
        "optional": []
    },
    "aws_macie2_organization_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_main_route_table_association": {
        "hard": [
            "aws_route_table",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_media_convert_queue": {
        "hard": [],
        "optional": []
    },
    "aws_media_package_channel": {
        "hard": [],
        "optional": []
    },
    "aws_media_packagev2_channel_group": {
        "hard": [],
        "optional": []
    },
    "aws_media_store_container": {
        "hard": [],
        "optional": []
    },
    "aws_media_store_container_policy": {
        "hard": [],
        "optional": []
    },
    "aws_medialive_channel": {
        "hard": [],
        "optional": [
            "aws_iam_role",
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
    "aws_medialive_input_security_group": {
        "hard": [],
        "optional": []
    },
    "aws_medialive_multiplex": {
        "hard": [],
        "optional": []
    },
    "aws_medialive_multiplex_program": {
        "hard": [],
        "optional": []
    },
    "aws_memorydb_acl": {
        "hard": [],
        "optional": []
    },
    "aws_memorydb_cluster": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_security_group",
            "aws_sns_topic"
        ]
    },
    "aws_memorydb_multi_region_cluster": {
        "hard": [],
        "optional": []
    },
    "aws_memorydb_parameter_group": {
        "hard": [],
        "optional": []
    },
    "aws_memorydb_snapshot": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_memorydb_subnet_group": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_memorydb_user": {
        "hard": [],
        "optional": []
    },
    "aws_mq_broker": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_mq_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_msk_cluster": {
        "hard": [
            "aws_security_group"
        ],
        "optional": []
    },
    "aws_msk_cluster_policy": {
        "hard": [],
        "optional": []
    },
    "aws_msk_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_msk_replicator": {
        "hard": [
            "aws_msk_cluster",
            "aws_subnet"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_msk_scram_secret_association": {
        "hard": [],
        "optional": []
    },
    "aws_msk_serverless_cluster": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_msk_single_scram_secret_association": {
        "hard": [],
        "optional": []
    },
    "aws_msk_topic": {
        "hard": [],
        "optional": []
    },
    "aws_msk_vpc_connection": {
        "hard": [
            "aws_security_group",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_mskconnect_connector": {
        "hard": [
            "aws_security_group",
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_mskconnect_custom_plugin": {
        "hard": [],
        "optional": []
    },
    "aws_mskconnect_worker_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_mwaa_environment": {
        "hard": [
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_nat_gateway": {
        "hard": [],
        "optional": [
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_nat_gateway_eip_association": {
        "hard": [
            "aws_nat_gateway"
        ],
        "optional": []
    },
    "aws_neptune_cluster": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key",
            "aws_neptune_cluster_parameter_group",
            "aws_neptune_subnet_group",
            "aws_security_group"
        ]
    },
    "aws_neptune_cluster_endpoint": {
        "hard": [],
        "optional": []
    },
    "aws_neptune_cluster_instance": {
        "hard": [],
        "optional": [
            "aws_neptune_parameter_group",
            "aws_neptune_subnet_group"
        ]
    },
    "aws_neptune_cluster_parameter_group": {
        "hard": [],
        "optional": []
    },
    "aws_neptune_cluster_snapshot": {
        "hard": [],
        "optional": []
    },
    "aws_neptune_event_subscription": {
        "hard": [
            "aws_sns_topic"
        ],
        "optional": []
    },
    "aws_neptune_global_cluster": {
        "hard": [],
        "optional": []
    },
    "aws_neptune_parameter_group": {
        "hard": [],
        "optional": []
    },
    "aws_neptune_subnet_group": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_neptunegraph_graph": {
        "hard": [],
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
        "optional": [
            "aws_instance",
            "aws_security_group"
        ]
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
        "hard": [],
        "optional": [
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_networkfirewall_firewall_policy": {
        "hard": [],
        "optional": []
    },
    "aws_networkfirewall_firewall_transit_gateway_attachment_accepter": {
        "hard": [],
        "optional": []
    },
    "aws_networkfirewall_logging_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_networkfirewall_resource_policy": {
        "hard": [],
        "optional": []
    },
    "aws_networkfirewall_rule_group": {
        "hard": [],
        "optional": []
    },
    "aws_networkfirewall_tls_inspection_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_networkfirewall_vpc_endpoint_association": {
        "hard": [
            "aws_vpc"
        ],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_networkflowmonitor_monitor": {
        "hard": [],
        "optional": []
    },
    "aws_networkflowmonitor_scope": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_attachment_accepter": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_attachment_routing_policy_label": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_connect_attachment": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_connect_peer": {
        "hard": [],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_networkmanager_connection": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_core_network": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_core_network_policy_attachment": {
        "hard": [],
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
        "optional": []
    },
    "aws_networkmanager_global_network": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_link": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_link_association": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_prefix_list_association": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_site": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_site_to_site_vpn_attachment": {
        "hard": [
            "aws_vpn_connection"
        ],
        "optional": []
    },
    "aws_networkmanager_transit_gateway_connect_peer_association": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_transit_gateway_peering": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_transit_gateway_registration": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_transit_gateway_route_table_attachment": {
        "hard": [],
        "optional": []
    },
    "aws_networkmanager_vpc_attachment": {
        "hard": [
            "aws_subnet",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_networkmonitor_monitor": {
        "hard": [],
        "optional": []
    },
    "aws_networkmonitor_probe": {
        "hard": [],
        "optional": []
    },
    "aws_notifications_channel_association": {
        "hard": [],
        "optional": []
    },
    "aws_notifications_event_rule": {
        "hard": [],
        "optional": []
    },
    "aws_notifications_managed_notification_account_contact_association": {
        "hard": [],
        "optional": []
    },
    "aws_notifications_managed_notification_additional_channel_association": {
        "hard": [],
        "optional": []
    },
    "aws_notifications_notification_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_notifications_notification_hub": {
        "hard": [],
        "optional": []
    },
    "aws_notifications_organizational_unit_association": {
        "hard": [],
        "optional": []
    },
    "aws_notifications_organizations_access": {
        "hard": [],
        "optional": []
    },
    "aws_notificationscontacts_email_contact": {
        "hard": [],
        "optional": []
    },
    "aws_oam_link": {
        "hard": [],
        "optional": []
    },
    "aws_oam_sink": {
        "hard": [],
        "optional": []
    },
    "aws_oam_sink_policy": {
        "hard": [],
        "optional": []
    },
    "aws_observabilityadmin_centralization_rule_for_organization": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_observabilityadmin_s3_table_integration": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_observabilityadmin_telemetry_enrichment": {
        "hard": [],
        "optional": []
    },
    "aws_observabilityadmin_telemetry_evaluation": {
        "hard": [],
        "optional": []
    },
    "aws_observabilityadmin_telemetry_evaluation_for_organization": {
        "hard": [],
        "optional": []
    },
    "aws_observabilityadmin_telemetry_pipeline": {
        "hard": [],
        "optional": []
    },
    "aws_observabilityadmin_telemetry_rule": {
        "hard": [],
        "optional": []
    },
    "aws_observabilityadmin_telemetry_rule_for_organization": {
        "hard": [],
        "optional": []
    },
    "aws_odb_cloud_autonomous_vm_cluster": {
        "hard": [],
        "optional": [
            "aws_odb_network"
        ]
    },
    "aws_odb_cloud_exadata_infrastructure": {
        "hard": [],
        "optional": []
    },
    "aws_odb_cloud_vm_cluster": {
        "hard": [],
        "optional": [
            "aws_odb_network"
        ]
    },
    "aws_odb_network": {
        "hard": [],
        "optional": []
    },
    "aws_odb_network_peering_connection": {
        "hard": [],
        "optional": [
            "aws_odb_network"
        ]
    },
    "aws_opensearch_application": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_opensearch_authorize_vpc_endpoint_access": {
        "hard": [],
        "optional": []
    },
    "aws_opensearch_domain": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_iam_role",
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_opensearch_domain_policy": {
        "hard": [],
        "optional": []
    },
    "aws_opensearch_domain_saml_options": {
        "hard": [],
        "optional": []
    },
    "aws_opensearch_inbound_connection_accepter": {
        "hard": [],
        "optional": []
    },
    "aws_opensearch_outbound_connection": {
        "hard": [],
        "optional": []
    },
    "aws_opensearch_package": {
        "hard": [
            "aws_s3_bucket"
        ],
        "optional": []
    },
    "aws_opensearch_package_association": {
        "hard": [],
        "optional": []
    },
    "aws_opensearch_vpc_endpoint": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_opensearchserverless_access_policy": {
        "hard": [],
        "optional": []
    },
    "aws_opensearchserverless_collection": {
        "hard": [],
        "optional": []
    },
    "aws_opensearchserverless_collection_group": {
        "hard": [],
        "optional": []
    },
    "aws_opensearchserverless_lifecycle_policy": {
        "hard": [],
        "optional": []
    },
    "aws_opensearchserverless_security_config": {
        "hard": [],
        "optional": []
    },
    "aws_opensearchserverless_security_policy": {
        "hard": [],
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
    "aws_organizations_account": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_organizations_aws_service_access": {
        "hard": [],
        "optional": []
    },
    "aws_organizations_delegated_administrator": {
        "hard": [],
        "optional": []
    },
    "aws_organizations_organization": {
        "hard": [],
        "optional": []
    },
    "aws_organizations_organizational_unit": {
        "hard": [],
        "optional": []
    },
    "aws_organizations_policy": {
        "hard": [],
        "optional": []
    },
    "aws_organizations_policy_attachment": {
        "hard": [],
        "optional": []
    },
    "aws_organizations_resource_policy": {
        "hard": [],
        "optional": []
    },
    "aws_organizations_tag": {
        "hard": [],
        "optional": []
    },
    "aws_osis_pipeline": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_outposts_capacity_task": {
        "hard": [],
        "optional": [
            "aws_instance"
        ]
    },
    "aws_paymentcryptography_key": {
        "hard": [],
        "optional": []
    },
    "aws_paymentcryptography_key_alias": {
        "hard": [],
        "optional": []
    },
    "aws_pinpoint_adm_channel": {
        "hard": [],
        "optional": []
    },
    "aws_pinpoint_apns_channel": {
        "hard": [],
        "optional": []
    },
    "aws_pinpoint_apns_sandbox_channel": {
        "hard": [],
        "optional": []
    },
    "aws_pinpoint_apns_voip_channel": {
        "hard": [],
        "optional": []
    },
    "aws_pinpoint_apns_voip_sandbox_channel": {
        "hard": [],
        "optional": []
    },
    "aws_pinpoint_app": {
        "hard": [],
        "optional": [
            "aws_lambda_function"
        ]
    },
    "aws_pinpoint_baidu_channel": {
        "hard": [],
        "optional": []
    },
    "aws_pinpoint_email_channel": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_pinpoint_email_template": {
        "hard": [],
        "optional": []
    },
    "aws_pinpoint_event_stream": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_pinpoint_gcm_channel": {
        "hard": [],
        "optional": []
    },
    "aws_pinpoint_sms_channel": {
        "hard": [],
        "optional": []
    },
    "aws_pinpointsmsvoicev2_configuration_set": {
        "hard": [],
        "optional": []
    },
    "aws_pinpointsmsvoicev2_event_destination": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_pinpointsmsvoicev2_opt_out_list": {
        "hard": [],
        "optional": []
    },
    "aws_pinpointsmsvoicev2_phone_number": {
        "hard": [],
        "optional": []
    },
    "aws_pipes_pipe": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_placement_group": {
        "hard": [],
        "optional": []
    },
    "aws_prometheus_alert_manager_definition": {
        "hard": [],
        "optional": []
    },
    "aws_prometheus_query_logging_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_prometheus_resource_policy": {
        "hard": [],
        "optional": []
    },
    "aws_prometheus_rule_group_namespace": {
        "hard": [],
        "optional": []
    },
    "aws_prometheus_scraper": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_prometheus_workspace": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_prometheus_workspace_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_proxy_protocol_policy": {
        "hard": [
            "aws_lb"
        ],
        "optional": []
    },
    "aws_qbusiness_application": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_qldb_ledger": {
        "hard": [],
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
    "aws_quicksight_account_settings": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_account_subscription": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_analysis": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_quicksight_custom_permissions": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_dashboard": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_quicksight_data_set": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_data_source": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_instance"
        ]
    },
    "aws_quicksight_folder": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_folder_membership": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_group": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_group_membership": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_iam_policy_assignment": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_ingestion": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_ip_restriction": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_key_registration": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_namespace": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_refresh_schedule": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_role_custom_permission": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
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
    "aws_quicksight_template_alias": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_theme": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_user": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_user_custom_permission": {
        "hard": [],
        "optional": []
    },
    "aws_quicksight_vpc_connection": {
        "hard": [
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_ram_permission": {
        "hard": [],
        "optional": []
    },
    "aws_ram_principal_association": {
        "hard": [],
        "optional": []
    },
    "aws_ram_resource_association": {
        "hard": [],
        "optional": []
    },
    "aws_ram_resource_share": {
        "hard": [],
        "optional": []
    },
    "aws_ram_resource_share_accepter": {
        "hard": [],
        "optional": []
    },
    "aws_ram_resource_share_associations_exclusive": {
        "hard": [],
        "optional": []
    },
    "aws_ram_sharing_with_organization": {
        "hard": [],
        "optional": []
    },
    "aws_rbin_rule": {
        "hard": [],
        "optional": []
    },
    "aws_rds_certificate": {
        "hard": [],
        "optional": []
    },
    "aws_rds_cluster": {
        "hard": [],
        "optional": [
            "aws_db_subnet_group",
            "aws_iam_role",
            "aws_kms_key",
            "aws_security_group"
        ]
    },
    "aws_rds_cluster_activity_stream": {
        "hard": [
            "aws_kms_key"
        ],
        "optional": []
    },
    "aws_rds_cluster_endpoint": {
        "hard": [],
        "optional": []
    },
    "aws_rds_cluster_instance": {
        "hard": [],
        "optional": [
            "aws_db_parameter_group",
            "aws_db_subnet_group"
        ]
    },
    "aws_rds_cluster_parameter_group": {
        "hard": [],
        "optional": []
    },
    "aws_rds_cluster_role_association": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_rds_cluster_snapshot_copy": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_rds_custom_db_engine_version": {
        "hard": [],
        "optional": [
            "aws_kms_key"
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
        "hard": [],
        "optional": []
    },
    "aws_rds_instance_state": {
        "hard": [],
        "optional": []
    },
    "aws_rds_integration": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_rds_reserved_instance": {
        "hard": [],
        "optional": []
    },
    "aws_rds_shard_group": {
        "hard": [],
        "optional": []
    },
    "aws_redshift_authentication_profile": {
        "hard": [],
        "optional": []
    },
    "aws_redshift_cluster": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key",
            "aws_security_group"
        ]
    },
    "aws_redshift_cluster_iam_roles": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_redshift_cluster_snapshot": {
        "hard": [],
        "optional": []
    },
    "aws_redshift_data_share_authorization": {
        "hard": [],
        "optional": []
    },
    "aws_redshift_data_share_consumer_association": {
        "hard": [],
        "optional": []
    },
    "aws_redshift_endpoint_access": {
        "hard": [],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_redshift_endpoint_authorization": {
        "hard": [],
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
        "hard": [],
        "optional": []
    },
    "aws_redshift_hsm_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_redshift_idc_application": {
        "hard": [
            "aws_iam_role"
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
        "hard": [],
        "optional": []
    },
    "aws_redshift_namespace_registration": {
        "hard": [],
        "optional": []
    },
    "aws_redshift_parameter_group": {
        "hard": [],
        "optional": []
    },
    "aws_redshift_partner": {
        "hard": [],
        "optional": []
    },
    "aws_redshift_resource_policy": {
        "hard": [],
        "optional": []
    },
    "aws_redshift_scheduled_action": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_redshift_snapshot_copy": {
        "hard": [],
        "optional": []
    },
    "aws_redshift_snapshot_copy_grant": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_redshift_snapshot_schedule": {
        "hard": [],
        "optional": []
    },
    "aws_redshift_snapshot_schedule_association": {
        "hard": [],
        "optional": []
    },
    "aws_redshift_subnet_group": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_redshift_usage_limit": {
        "hard": [],
        "optional": []
    },
    "aws_redshiftdata_statement": {
        "hard": [],
        "optional": []
    },
    "aws_redshiftserverless_custom_domain_association": {
        "hard": [],
        "optional": []
    },
    "aws_redshiftserverless_endpoint_access": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_security_group"
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
        "hard": [],
        "optional": []
    },
    "aws_redshiftserverless_snapshot": {
        "hard": [],
        "optional": []
    },
    "aws_redshiftserverless_usage_limit": {
        "hard": [],
        "optional": []
    },
    "aws_redshiftserverless_workgroup": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_rekognition_collection": {
        "hard": [],
        "optional": []
    },
    "aws_rekognition_project": {
        "hard": [],
        "optional": []
    },
    "aws_rekognition_stream_processor": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key",
            "aws_sns_topic"
        ]
    },
    "aws_resiliencehub_resiliency_policy": {
        "hard": [],
        "optional": []
    },
    "aws_resourceexplorer2_index": {
        "hard": [],
        "optional": []
    },
    "aws_resourceexplorer2_view": {
        "hard": [],
        "optional": []
    },
    "aws_resourcegroups_group": {
        "hard": [],
        "optional": []
    },
    "aws_resourcegroups_resource": {
        "hard": [],
        "optional": []
    },
    "aws_rolesanywhere_profile": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_rolesanywhere_trust_anchor": {
        "hard": [],
        "optional": []
    },
    "aws_route": {
        "hard": [
            "aws_route_table"
        ],
        "optional": [
            "aws_nat_gateway",
            "aws_network_interface",
            "aws_odb_network",
            "aws_vpc_endpoint",
            "aws_vpc_peering_connection"
        ]
    },
    "aws_route53_cidr_collection": {
        "hard": [],
        "optional": []
    },
    "aws_route53_cidr_location": {
        "hard": [],
        "optional": []
    },
    "aws_route53_delegation_set": {
        "hard": [],
        "optional": []
    },
    "aws_route53_health_check": {
        "hard": [],
        "optional": []
    },
    "aws_route53_hosted_zone_dnssec": {
        "hard": [],
        "optional": []
    },
    "aws_route53_key_signing_key": {
        "hard": [],
        "optional": []
    },
    "aws_route53_query_log": {
        "hard": [
            "aws_cloudwatch_log_group"
        ],
        "optional": []
    },
    "aws_route53_record": {
        "hard": [],
        "optional": []
    },
    "aws_route53_records_exclusive": {
        "hard": [],
        "optional": []
    },
    "aws_route53_resolver_config": {
        "hard": [],
        "optional": []
    },
    "aws_route53_resolver_dnssec_config": {
        "hard": [],
        "optional": []
    },
    "aws_route53_resolver_endpoint": {
        "hard": [
            "aws_security_group",
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_route53_resolver_firewall_config": {
        "hard": [],
        "optional": []
    },
    "aws_route53_resolver_firewall_domain_list": {
        "hard": [],
        "optional": []
    },
    "aws_route53_resolver_firewall_rule": {
        "hard": [],
        "optional": []
    },
    "aws_route53_resolver_firewall_rule_group": {
        "hard": [],
        "optional": []
    },
    "aws_route53_resolver_firewall_rule_group_association": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_route53_resolver_query_log_config": {
        "hard": [],
        "optional": []
    },
    "aws_route53_resolver_query_log_config_association": {
        "hard": [],
        "optional": []
    },
    "aws_route53_resolver_rule": {
        "hard": [],
        "optional": []
    },
    "aws_route53_resolver_rule_association": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_route53_traffic_policy": {
        "hard": [],
        "optional": []
    },
    "aws_route53_traffic_policy_instance": {
        "hard": [],
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
    "aws_route53domains_delegation_signer_record": {
        "hard": [],
        "optional": []
    },
    "aws_route53domains_domain": {
        "hard": [],
        "optional": []
    },
    "aws_route53domains_registered_domain": {
        "hard": [],
        "optional": []
    },
    "aws_route53profiles_association": {
        "hard": [],
        "optional": []
    },
    "aws_route53profiles_profile": {
        "hard": [],
        "optional": []
    },
    "aws_route53profiles_resource_association": {
        "hard": [],
        "optional": []
    },
    "aws_route53recoverycontrolconfig_cluster": {
        "hard": [],
        "optional": []
    },
    "aws_route53recoverycontrolconfig_control_panel": {
        "hard": [],
        "optional": []
    },
    "aws_route53recoverycontrolconfig_routing_control": {
        "hard": [],
        "optional": []
    },
    "aws_route53recoverycontrolconfig_safety_rule": {
        "hard": [],
        "optional": []
    },
    "aws_route53recoveryreadiness_cell": {
        "hard": [],
        "optional": []
    },
    "aws_route53recoveryreadiness_readiness_check": {
        "hard": [],
        "optional": []
    },
    "aws_route53recoveryreadiness_recovery_group": {
        "hard": [],
        "optional": []
    },
    "aws_route53recoveryreadiness_resource_set": {
        "hard": [],
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
        "optional": []
    },
    "aws_rum_metrics_destination": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_s3_access_point": {
        "hard": [],
        "optional": [
            "aws_vpc"
        ]
    },
    "aws_s3_account_public_access_block": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_s3_bucket_abac": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_accelerate_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_acl": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_analytics_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_cors_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_intelligent_tiering_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_inventory": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_lifecycle_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_logging": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_metadata_configuration": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_s3_bucket_metric": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_notification": {
        "hard": [],
        "optional": [
            "aws_lambda_function"
        ]
    },
    "aws_s3_bucket_object": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_s3_bucket_object_lock_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_ownership_controls": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_policy": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_public_access_block": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_replication_configuration": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_s3_bucket_request_payment_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_server_side_encryption_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_versioning": {
        "hard": [],
        "optional": []
    },
    "aws_s3_bucket_website_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_s3_directory_bucket": {
        "hard": [],
        "optional": []
    },
    "aws_s3_object": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_s3_object_copy": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_s3control_access_grant": {
        "hard": [],
        "optional": []
    },
    "aws_s3control_access_grants_instance": {
        "hard": [],
        "optional": []
    },
    "aws_s3control_access_grants_instance_resource_policy": {
        "hard": [],
        "optional": []
    },
    "aws_s3control_access_grants_location": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_s3control_access_point_policy": {
        "hard": [],
        "optional": []
    },
    "aws_s3control_bucket": {
        "hard": [],
        "optional": []
    },
    "aws_s3control_bucket_lifecycle_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_s3control_bucket_policy": {
        "hard": [],
        "optional": []
    },
    "aws_s3control_directory_bucket_access_point_scope": {
        "hard": [],
        "optional": []
    },
    "aws_s3control_multi_region_access_point": {
        "hard": [],
        "optional": []
    },
    "aws_s3control_multi_region_access_point_policy": {
        "hard": [],
        "optional": []
    },
    "aws_s3control_multi_region_access_point_routes": {
        "hard": [],
        "optional": []
    },
    "aws_s3control_object_lambda_access_point": {
        "hard": [],
        "optional": []
    },
    "aws_s3control_object_lambda_access_point_policy": {
        "hard": [],
        "optional": []
    },
    "aws_s3control_storage_lens_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_s3files_access_point": {
        "hard": [],
        "optional": []
    },
    "aws_s3files_file_system": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_s3files_file_system_policy": {
        "hard": [],
        "optional": []
    },
    "aws_s3files_mount_target": {
        "hard": [
            "aws_subnet"
        ],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_s3files_synchronization_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_s3outposts_endpoint": {
        "hard": [
            "aws_security_group",
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_s3tables_namespace": {
        "hard": [],
        "optional": []
    },
    "aws_s3tables_table": {
        "hard": [],
        "optional": []
    },
    "aws_s3tables_table_bucket": {
        "hard": [],
        "optional": []
    },
    "aws_s3tables_table_bucket_policy": {
        "hard": [],
        "optional": []
    },
    "aws_s3tables_table_bucket_replication": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_s3tables_table_policy": {
        "hard": [],
        "optional": []
    },
    "aws_s3tables_table_replication": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_s3vectors_index": {
        "hard": [],
        "optional": []
    },
    "aws_s3vectors_vector_bucket": {
        "hard": [],
        "optional": []
    },
    "aws_s3vectors_vector_bucket_policy": {
        "hard": [],
        "optional": []
    },
    "aws_sagemaker_algorithm": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_sagemaker_app": {
        "hard": [],
        "optional": [
            "aws_sagemaker_image",
            "aws_sagemaker_image_version"
        ]
    },
    "aws_sagemaker_app_image_config": {
        "hard": [],
        "optional": []
    },
    "aws_sagemaker_code_repository": {
        "hard": [],
        "optional": []
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
    "aws_sagemaker_device": {
        "hard": [],
        "optional": [
            "aws_iot_thing"
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
    "aws_sagemaker_endpoint": {
        "hard": [],
        "optional": []
    },
    "aws_sagemaker_endpoint_configuration": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key"
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
    "aws_sagemaker_hub": {
        "hard": [],
        "optional": []
    },
    "aws_sagemaker_human_task_ui": {
        "hard": [],
        "optional": []
    },
    "aws_sagemaker_hyper_parameter_tuning_job": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_sagemaker_image": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_sagemaker_image_version": {
        "hard": [],
        "optional": []
    },
    "aws_sagemaker_labeling_job": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key",
            "aws_security_group",
            "aws_sns_topic",
            "aws_subnet"
        ]
    },
    "aws_sagemaker_mlflow_app": {
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
    "aws_sagemaker_model_card": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_sagemaker_model_card_export_job": {
        "hard": [],
        "optional": []
    },
    "aws_sagemaker_model_package_group": {
        "hard": [],
        "optional": []
    },
    "aws_sagemaker_model_package_group_policy": {
        "hard": [],
        "optional": []
    },
    "aws_sagemaker_monitoring_schedule": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_sagemaker_notebook_instance": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_sagemaker_notebook_instance_lifecycle_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_sagemaker_pipeline": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_sagemaker_project": {
        "hard": [],
        "optional": []
    },
    "aws_sagemaker_servicecatalog_portfolio_status": {
        "hard": [],
        "optional": []
    },
    "aws_sagemaker_space": {
        "hard": [],
        "optional": [
            "aws_sagemaker_image",
            "aws_sagemaker_image_version"
        ]
    },
    "aws_sagemaker_studio_lifecycle_config": {
        "hard": [],
        "optional": []
    },
    "aws_sagemaker_training_job": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_sagemaker_user_profile": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_sagemaker_image",
            "aws_sagemaker_image_version",
            "aws_security_group"
        ]
    },
    "aws_sagemaker_workforce": {
        "hard": [],
        "optional": [
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_sagemaker_workteam": {
        "hard": [],
        "optional": []
    },
    "aws_savingsplans_savings_plan": {
        "hard": [],
        "optional": []
    },
    "aws_scheduler_schedule": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_scheduler_schedule_group": {
        "hard": [],
        "optional": []
    },
    "aws_schemas_discoverer": {
        "hard": [],
        "optional": []
    },
    "aws_schemas_registry": {
        "hard": [],
        "optional": []
    },
    "aws_schemas_registry_policy": {
        "hard": [],
        "optional": []
    },
    "aws_schemas_schema": {
        "hard": [],
        "optional": []
    },
    "aws_secretsmanager_secret": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_secretsmanager_secret_policy": {
        "hard": [],
        "optional": []
    },
    "aws_secretsmanager_secret_rotation": {
        "hard": [],
        "optional": []
    },
    "aws_secretsmanager_secret_version": {
        "hard": [],
        "optional": []
    },
    "aws_secretsmanager_tag": {
        "hard": [],
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
    "aws_securityhub_account": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_account_v2": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_action_target": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_aggregator_v2": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_automation_rule": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_automation_rule_v2": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_configuration_policy": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_configuration_policy_association": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_connector_v2": {
        "hard": [],
        "optional": [
            "aws_instance",
            "aws_kms_key"
        ]
    },
    "aws_securityhub_finding_aggregator": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_insight": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_invite_accepter": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_member": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_organization_admin_account": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_organization_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_product_subscription": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_standards_control": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_standards_control_association": {
        "hard": [],
        "optional": []
    },
    "aws_securityhub_standards_subscription": {
        "hard": [],
        "optional": []
    },
    "aws_securitylake_aws_log_source": {
        "hard": [],
        "optional": []
    },
    "aws_securitylake_custom_log_source": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_securitylake_data_lake": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_securitylake_subscriber": {
        "hard": [],
        "optional": []
    },
    "aws_securitylake_subscriber_notification": {
        "hard": [],
        "optional": []
    },
    "aws_serverlessapplicationrepository_cloudformation_stack": {
        "hard": [],
        "optional": []
    },
    "aws_service_discovery_http_namespace": {
        "hard": [],
        "optional": []
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
    "aws_service_discovery_public_dns_namespace": {
        "hard": [],
        "optional": []
    },
    "aws_service_discovery_service": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalog_budget_resource_association": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalog_constraint": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalog_organizations_access": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalog_portfolio": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalog_portfolio_share": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalog_principal_portfolio_association": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalog_product": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalog_product_portfolio_association": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalog_provisioned_product": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalog_provisioning_artifact": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalog_service_action": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalog_tag_option": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalog_tag_option_resource_association": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalogappregistry_application": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalogappregistry_attribute_group": {
        "hard": [],
        "optional": []
    },
    "aws_servicecatalogappregistry_attribute_group_association": {
        "hard": [],
        "optional": []
    },
    "aws_servicequotas_auto_management": {
        "hard": [],
        "optional": []
    },
    "aws_servicequotas_service_quota": {
        "hard": [],
        "optional": []
    },
    "aws_servicequotas_template": {
        "hard": [],
        "optional": []
    },
    "aws_servicequotas_template_association": {
        "hard": [],
        "optional": []
    },
    "aws_ses_active_receipt_rule_set": {
        "hard": [],
        "optional": []
    },
    "aws_ses_configuration_set": {
        "hard": [],
        "optional": []
    },
    "aws_ses_domain_dkim": {
        "hard": [],
        "optional": []
    },
    "aws_ses_domain_identity": {
        "hard": [],
        "optional": []
    },
    "aws_ses_domain_identity_verification": {
        "hard": [],
        "optional": []
    },
    "aws_ses_domain_mail_from": {
        "hard": [],
        "optional": []
    },
    "aws_ses_email_identity": {
        "hard": [],
        "optional": []
    },
    "aws_ses_event_destination": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_ses_identity_notification_topic": {
        "hard": [],
        "optional": []
    },
    "aws_ses_identity_policy": {
        "hard": [],
        "optional": []
    },
    "aws_ses_receipt_filter": {
        "hard": [],
        "optional": []
    },
    "aws_ses_receipt_rule": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_kms_key"
        ]
    },
    "aws_ses_receipt_rule_set": {
        "hard": [],
        "optional": []
    },
    "aws_ses_template": {
        "hard": [],
        "optional": []
    },
    "aws_sesv2_account_suppression_attributes": {
        "hard": [],
        "optional": []
    },
    "aws_sesv2_account_vdm_attributes": {
        "hard": [],
        "optional": []
    },
    "aws_sesv2_configuration_set": {
        "hard": [],
        "optional": []
    },
    "aws_sesv2_configuration_set_event_destination": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_sesv2_contact_list": {
        "hard": [],
        "optional": []
    },
    "aws_sesv2_dedicated_ip_assignment": {
        "hard": [],
        "optional": []
    },
    "aws_sesv2_dedicated_ip_pool": {
        "hard": [],
        "optional": []
    },
    "aws_sesv2_email_identity": {
        "hard": [],
        "optional": []
    },
    "aws_sesv2_email_identity_feedback_attributes": {
        "hard": [],
        "optional": []
    },
    "aws_sesv2_email_identity_mail_from_attributes": {
        "hard": [],
        "optional": []
    },
    "aws_sesv2_email_identity_policy": {
        "hard": [],
        "optional": []
    },
    "aws_sesv2_tenant": {
        "hard": [],
        "optional": []
    },
    "aws_sesv2_tenant_resource_association": {
        "hard": [],
        "optional": []
    },
    "aws_sfn_activity": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_sfn_alias": {
        "hard": [],
        "optional": []
    },
    "aws_sfn_state_machine": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_shield_application_layer_automatic_response": {
        "hard": [],
        "optional": []
    },
    "aws_shield_drt_access_log_bucket_association": {
        "hard": [],
        "optional": []
    },
    "aws_shield_drt_access_role_arn_association": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_shield_proactive_engagement": {
        "hard": [],
        "optional": []
    },
    "aws_shield_protection": {
        "hard": [],
        "optional": []
    },
    "aws_shield_protection_group": {
        "hard": [],
        "optional": []
    },
    "aws_shield_protection_health_check_association": {
        "hard": [
            "aws_shield_protection"
        ],
        "optional": []
    },
    "aws_shield_subscription": {
        "hard": [],
        "optional": []
    },
    "aws_signer_signing_job": {
        "hard": [],
        "optional": []
    },
    "aws_signer_signing_profile": {
        "hard": [],
        "optional": []
    },
    "aws_signer_signing_profile_permission": {
        "hard": [],
        "optional": []
    },
    "aws_snapshot_create_volume_permission": {
        "hard": [],
        "optional": []
    },
    "aws_sns_platform_application": {
        "hard": [],
        "optional": []
    },
    "aws_sns_sms_preferences": {
        "hard": [],
        "optional": []
    },
    "aws_sns_topic": {
        "hard": [],
        "optional": []
    },
    "aws_sns_topic_data_protection_policy": {
        "hard": [],
        "optional": []
    },
    "aws_sns_topic_policy": {
        "hard": [],
        "optional": []
    },
    "aws_sns_topic_subscription": {
        "hard": [],
        "optional": []
    },
    "aws_spot_datafeed_subscription": {
        "hard": [],
        "optional": []
    },
    "aws_spot_fleet_request": {
        "hard": [],
        "optional": [
            "aws_ami",
            "aws_iam_instance_profile",
            "aws_kms_key",
            "aws_lb",
            "aws_lb_target_group",
            "aws_placement_group",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_spot_instance_request": {
        "hard": [],
        "optional": [
            "aws_ami",
            "aws_iam_instance_profile",
            "aws_kms_key",
            "aws_network_interface",
            "aws_placement_group",
            "aws_security_group",
            "aws_subnet"
        ]
    },
    "aws_sqs_queue": {
        "hard": [],
        "optional": []
    },
    "aws_sqs_queue_policy": {
        "hard": [],
        "optional": []
    },
    "aws_sqs_queue_redrive_allow_policy": {
        "hard": [],
        "optional": []
    },
    "aws_sqs_queue_redrive_policy": {
        "hard": [],
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
            "aws_s3_bucket"
        ]
    },
    "aws_ssm_default_patch_baseline": {
        "hard": [],
        "optional": []
    },
    "aws_ssm_document": {
        "hard": [],
        "optional": []
    },
    "aws_ssm_maintenance_window": {
        "hard": [],
        "optional": []
    },
    "aws_ssm_maintenance_window_target": {
        "hard": [],
        "optional": []
    },
    "aws_ssm_maintenance_window_task": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group",
            "aws_iam_role"
        ]
    },
    "aws_ssm_parameter": {
        "hard": [],
        "optional": []
    },
    "aws_ssm_patch_baseline": {
        "hard": [],
        "optional": []
    },
    "aws_ssm_patch_group": {
        "hard": [],
        "optional": []
    },
    "aws_ssm_resource_data_sync": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_ssm_service_setting": {
        "hard": [],
        "optional": []
    },
    "aws_ssmcontacts_contact": {
        "hard": [],
        "optional": []
    },
    "aws_ssmcontacts_contact_channel": {
        "hard": [],
        "optional": []
    },
    "aws_ssmcontacts_plan": {
        "hard": [],
        "optional": []
    },
    "aws_ssmcontacts_rotation": {
        "hard": [],
        "optional": []
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
        "optional": []
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
    "aws_ssoadmin_application_access_scope": {
        "hard": [],
        "optional": []
    },
    "aws_ssoadmin_application_assignment": {
        "hard": [],
        "optional": []
    },
    "aws_ssoadmin_application_assignment_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_ssoadmin_customer_managed_policy_attachment": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_ssoadmin_customer_managed_policy_attachments_exclusive": {
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
            "aws_instance"
        ],
        "optional": []
    },
    "aws_ssoadmin_managed_policy_attachments_exclusive": {
        "hard": [
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
            "aws_instance"
        ],
        "optional": []
    },
    "aws_ssoadmin_permissions_boundary_attachment": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_ssoadmin_trusted_token_issuer": {
        "hard": [
            "aws_instance"
        ],
        "optional": []
    },
    "aws_storagegateway_cache": {
        "hard": [],
        "optional": []
    },
    "aws_storagegateway_cached_iscsi_volume": {
        "hard": [
            "aws_network_interface"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_storagegateway_file_system_association": {
        "hard": [],
        "optional": []
    },
    "aws_storagegateway_gateway": {
        "hard": [],
        "optional": [
            "aws_cloudwatch_log_group"
        ]
    },
    "aws_storagegateway_nfs_file_share": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_storagegateway_smb_file_share": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_storagegateway_stored_iscsi_volume": {
        "hard": [
            "aws_network_interface"
        ],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_storagegateway_tape_pool": {
        "hard": [],
        "optional": []
    },
    "aws_storagegateway_upload_buffer": {
        "hard": [],
        "optional": []
    },
    "aws_storagegateway_working_storage": {
        "hard": [],
        "optional": []
    },
    "aws_subnet": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_swf_domain": {
        "hard": [],
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
            "aws_subnet"
        ]
    },
    "aws_synthetics_group": {
        "hard": [],
        "optional": []
    },
    "aws_synthetics_group_association": {
        "hard": [],
        "optional": []
    },
    "aws_timestreaminfluxdb_db_cluster": {
        "hard": [
            "aws_security_group"
        ],
        "optional": []
    },
    "aws_timestreaminfluxdb_db_instance": {
        "hard": [
            "aws_security_group"
        ],
        "optional": []
    },
    "aws_timestreamquery_scheduled_query": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": [
            "aws_kms_key"
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
            "aws_kms_key"
        ]
    },
    "aws_transcribe_language_model": {
        "hard": [],
        "optional": []
    },
    "aws_transcribe_medical_vocabulary": {
        "hard": [],
        "optional": []
    },
    "aws_transcribe_vocabulary": {
        "hard": [],
        "optional": []
    },
    "aws_transcribe_vocabulary_filter": {
        "hard": [],
        "optional": []
    },
    "aws_transfer_access": {
        "hard": [],
        "optional": [
            "aws_iam_role"
        ]
    },
    "aws_transfer_agreement": {
        "hard": [],
        "optional": []
    },
    "aws_transfer_certificate": {
        "hard": [],
        "optional": []
    },
    "aws_transfer_connector": {
        "hard": [],
        "optional": []
    },
    "aws_transfer_host_key": {
        "hard": [],
        "optional": []
    },
    "aws_transfer_profile": {
        "hard": [],
        "optional": []
    },
    "aws_transfer_server": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc",
            "aws_vpc_endpoint"
        ]
    },
    "aws_transfer_ssh_key": {
        "hard": [],
        "optional": []
    },
    "aws_transfer_tag": {
        "hard": [],
        "optional": []
    },
    "aws_transfer_user": {
        "hard": [
            "aws_iam_role"
        ],
        "optional": []
    },
    "aws_transfer_web_app": {
        "hard": [],
        "optional": [
            "aws_iam_role",
            "aws_instance",
            "aws_security_group",
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_transfer_web_app_customization": {
        "hard": [],
        "optional": []
    },
    "aws_transfer_workflow": {
        "hard": [],
        "optional": []
    },
    "aws_uxc_account_customizations": {
        "hard": [],
        "optional": []
    },
    "aws_verifiedaccess_endpoint": {
        "hard": [],
        "optional": [
            "aws_kms_key",
            "aws_lb",
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
            "aws_kms_key"
        ]
    },
    "aws_verifiedaccess_instance": {
        "hard": [],
        "optional": []
    },
    "aws_verifiedaccess_instance_logging_configuration": {
        "hard": [
            "aws_verifiedaccess_instance"
        ],
        "optional": []
    },
    "aws_verifiedaccess_instance_trust_provider_attachment": {
        "hard": [
            "aws_verifiedaccess_instance",
            "aws_verifiedaccess_trust_provider"
        ],
        "optional": []
    },
    "aws_verifiedaccess_trust_provider": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_verifiedpermissions_identity_source": {
        "hard": [],
        "optional": []
    },
    "aws_verifiedpermissions_policy": {
        "hard": [],
        "optional": []
    },
    "aws_verifiedpermissions_policy_store": {
        "hard": [],
        "optional": []
    },
    "aws_verifiedpermissions_policy_template": {
        "hard": [],
        "optional": []
    },
    "aws_verifiedpermissions_schema": {
        "hard": [],
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
        "optional": []
    },
    "aws_vpc_block_public_access_exclusion": {
        "hard": [],
        "optional": [
            "aws_subnet",
            "aws_vpc"
        ]
    },
    "aws_vpc_block_public_access_options": {
        "hard": [],
        "optional": []
    },
    "aws_vpc_dhcp_options": {
        "hard": [],
        "optional": []
    },
    "aws_vpc_dhcp_options_association": {
        "hard": [
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_vpc_encryption_control": {
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
        "optional": []
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
        "optional": []
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
        "optional": []
    },
    "aws_vpc_endpoint_service_allowed_principal": {
        "hard": [
            "aws_vpc_endpoint_service"
        ],
        "optional": []
    },
    "aws_vpc_endpoint_service_private_dns_verification": {
        "hard": [],
        "optional": []
    },
    "aws_vpc_endpoint_subnet_association": {
        "hard": [
            "aws_subnet",
            "aws_vpc_endpoint"
        ],
        "optional": []
    },
    "aws_vpc_ipam": {
        "hard": [],
        "optional": []
    },
    "aws_vpc_ipam_organization_admin_account": {
        "hard": [],
        "optional": []
    },
    "aws_vpc_ipam_pool": {
        "hard": [],
        "optional": []
    },
    "aws_vpc_ipam_pool_cidr": {
        "hard": [],
        "optional": []
    },
    "aws_vpc_ipam_pool_cidr_allocation": {
        "hard": [],
        "optional": []
    },
    "aws_vpc_ipam_preview_next_cidr": {
        "hard": [],
        "optional": []
    },
    "aws_vpc_ipam_resource_discovery": {
        "hard": [],
        "optional": []
    },
    "aws_vpc_ipam_resource_discovery_association": {
        "hard": [],
        "optional": []
    },
    "aws_vpc_ipam_scope": {
        "hard": [],
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
    "aws_vpc_network_performance_metric_subscription": {
        "hard": [],
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
        "optional": []
    },
    "aws_vpc_peering_connection_options": {
        "hard": [
            "aws_vpc_peering_connection"
        ],
        "optional": []
    },
    "aws_vpc_route_server": {
        "hard": [],
        "optional": []
    },
    "aws_vpc_route_server_endpoint": {
        "hard": [
            "aws_subnet"
        ],
        "optional": []
    },
    "aws_vpc_route_server_peer": {
        "hard": [],
        "optional": []
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
        "optional": []
    },
    "aws_vpc_security_group_ingress_rule": {
        "hard": [
            "aws_security_group"
        ],
        "optional": []
    },
    "aws_vpc_security_group_rules_exclusive": {
        "hard": [
            "aws_security_group"
        ],
        "optional": []
    },
    "aws_vpc_security_group_vpc_association": {
        "hard": [
            "aws_security_group",
            "aws_vpc"
        ],
        "optional": []
    },
    "aws_vpclattice_access_log_subscription": {
        "hard": [],
        "optional": []
    },
    "aws_vpclattice_auth_policy": {
        "hard": [],
        "optional": []
    },
    "aws_vpclattice_domain_verification": {
        "hard": [],
        "optional": []
    },
    "aws_vpclattice_listener": {
        "hard": [],
        "optional": []
    },
    "aws_vpclattice_listener_rule": {
        "hard": [],
        "optional": []
    },
    "aws_vpclattice_resource_configuration": {
        "hard": [],
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
        "hard": [],
        "optional": []
    },
    "aws_vpclattice_service": {
        "hard": [],
        "optional": []
    },
    "aws_vpclattice_service_network": {
        "hard": [],
        "optional": []
    },
    "aws_vpclattice_service_network_resource_association": {
        "hard": [],
        "optional": []
    },
    "aws_vpclattice_service_network_service_association": {
        "hard": [],
        "optional": []
    },
    "aws_vpclattice_service_network_vpc_association": {
        "hard": [],
        "optional": [
            "aws_security_group"
        ]
    },
    "aws_vpclattice_target_group": {
        "hard": [],
        "optional": []
    },
    "aws_vpclattice_target_group_attachment": {
        "hard": [],
        "optional": []
    },
    "aws_vpn_concentrator": {
        "hard": [],
        "optional": []
    },
    "aws_vpn_connection": {
        "hard": [
            "aws_customer_gateway"
        ],
        "optional": [
            "aws_vpn_concentrator",
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
    "aws_waf_byte_match_set": {
        "hard": [],
        "optional": []
    },
    "aws_waf_geo_match_set": {
        "hard": [],
        "optional": []
    },
    "aws_waf_ipset": {
        "hard": [],
        "optional": []
    },
    "aws_waf_rate_based_rule": {
        "hard": [],
        "optional": []
    },
    "aws_waf_regex_match_set": {
        "hard": [],
        "optional": []
    },
    "aws_waf_regex_pattern_set": {
        "hard": [],
        "optional": []
    },
    "aws_waf_rule": {
        "hard": [],
        "optional": []
    },
    "aws_waf_rule_group": {
        "hard": [],
        "optional": []
    },
    "aws_waf_size_constraint_set": {
        "hard": [],
        "optional": []
    },
    "aws_waf_sql_injection_match_set": {
        "hard": [],
        "optional": []
    },
    "aws_waf_web_acl": {
        "hard": [],
        "optional": []
    },
    "aws_waf_xss_match_set": {
        "hard": [],
        "optional": []
    },
    "aws_wafregional_byte_match_set": {
        "hard": [],
        "optional": []
    },
    "aws_wafregional_geo_match_set": {
        "hard": [],
        "optional": []
    },
    "aws_wafregional_ipset": {
        "hard": [],
        "optional": []
    },
    "aws_wafregional_rate_based_rule": {
        "hard": [],
        "optional": []
    },
    "aws_wafregional_regex_match_set": {
        "hard": [],
        "optional": []
    },
    "aws_wafregional_regex_pattern_set": {
        "hard": [],
        "optional": []
    },
    "aws_wafregional_rule": {
        "hard": [],
        "optional": []
    },
    "aws_wafregional_rule_group": {
        "hard": [],
        "optional": []
    },
    "aws_wafregional_size_constraint_set": {
        "hard": [],
        "optional": []
    },
    "aws_wafregional_sql_injection_match_set": {
        "hard": [],
        "optional": []
    },
    "aws_wafregional_web_acl": {
        "hard": [],
        "optional": []
    },
    "aws_wafregional_web_acl_association": {
        "hard": [],
        "optional": []
    },
    "aws_wafregional_xss_match_set": {
        "hard": [],
        "optional": []
    },
    "aws_wafv2_api_key": {
        "hard": [],
        "optional": []
    },
    "aws_wafv2_ip_set": {
        "hard": [],
        "optional": []
    },
    "aws_wafv2_regex_pattern_set": {
        "hard": [],
        "optional": []
    },
    "aws_wafv2_rule_group": {
        "hard": [],
        "optional": []
    },
    "aws_wafv2_web_acl": {
        "hard": [],
        "optional": []
    },
    "aws_wafv2_web_acl_association": {
        "hard": [],
        "optional": []
    },
    "aws_wafv2_web_acl_logging_configuration": {
        "hard": [],
        "optional": []
    },
    "aws_wafv2_web_acl_rule": {
        "hard": [],
        "optional": []
    },
    "aws_wafv2_web_acl_rule_group_association": {
        "hard": [],
        "optional": []
    },
    "aws_workmail_default_domain": {
        "hard": [],
        "optional": []
    },
    "aws_workmail_domain": {
        "hard": [],
        "optional": []
    },
    "aws_workmail_group": {
        "hard": [],
        "optional": []
    },
    "aws_workmail_organization": {
        "hard": [],
        "optional": [
            "aws_kms_key"
        ]
    },
    "aws_workmail_user": {
        "hard": [],
        "optional": []
    },
    "aws_workspaces_connection_alias": {
        "hard": [],
        "optional": []
    },
    "aws_workspaces_directory": {
        "hard": [],
        "optional": [
            "aws_subnet"
        ]
    },
    "aws_workspaces_ip_group": {
        "hard": [],
        "optional": []
    },
    "aws_workspaces_workspace": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_browser_settings": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_browser_settings_association": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_data_protection_settings": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_data_protection_settings_association": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_identity_provider": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_ip_access_settings": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_ip_access_settings_association": {
        "hard": [],
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
    "aws_workspacesweb_network_settings_association": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_portal": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_session_logger": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_session_logger_association": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_trust_store": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_trust_store_association": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_user_access_logging_settings": {
        "hard": [
            "aws_kinesis_stream"
        ],
        "optional": []
    },
    "aws_workspacesweb_user_access_logging_settings_association": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_user_settings": {
        "hard": [],
        "optional": []
    },
    "aws_workspacesweb_user_settings_association": {
        "hard": [],
        "optional": []
    },
    "aws_xray_encryption_config": {
        "hard": [],
        "optional": []
    },
    "aws_xray_group": {
        "hard": [],
        "optional": []
    },
    "aws_xray_indexing_rule": {
        "hard": [],
        "optional": []
    },
    "aws_xray_resource_policy": {
        "hard": [],
        "optional": []
    },
    "aws_xray_sampling_rule": {
        "hard": [],
        "optional": []
    },
    "aws_xray_trace_segment_destination": {
        "hard": [],
        "optional": []
    }
}