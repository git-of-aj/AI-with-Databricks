---
name: azure-cloud-cost-optimization
description: Analyze Azure cloud costs, identify the highest-cost services, and use web research to find current, service-specific cost optimization opportunities.
---
version: 1.0.0
author: ai-agent
tags:
  - azure
  - cloud-cost
  - finops
  - cost-optimization
  - azure-cost-management
  - cloud-finops

triggers:
  - azure cost analysis
  - azure cloud costs
  - cloud cost optimization
  - azure cost optimization
  - find expensive azure services
  - reduce azure costs
  - azure finops

entrypoint:
  script: scripts/azure_cost_report.py
  command: python scripts/azure_fetch_billing.py

capabilities:
  - Run Azure Cost Management cost report
  - Identify top Azure services by cost
  - Calculate service cost percentages
  - Research Azure cost optimization recommendations
  - Rank potential cost-saving opportunities

workflow:
  - Run the Azure cost reporting script.
  - Parse the YTD and current-month cost information.
  - Identify the top 3 to 5 highest-cost Azure services.
  - Calculate each service's share of total YTD cost.
  - Use web search to research current optimization guidance for the highest-cost services.
  - Prefer Microsoft Azure and Microsoft Learn sources.
  - Produce prioritized, actionable cost-saving recommendations.

web_research:
  required: true
  preferred_domains:
    - learn.microsoft.com
    - azure.microsoft.com
  search_strategy:
    - Search specifically for the identified high-cost Azure service.
    - Search for current Azure cost optimization best practices.
    - Check relevant right-sizing, autoscaling, reservation, savings plan, storage tiering, and unused-resource guidance.
  rules:
    - Do not recommend a feature merely because it exists.
    - Recommendations must be relevant to the identified expensive service.
    - Prefer current official Microsoft guidance.
    - Do not claim guaranteed savings.

analysis:
  priority:
    - Highest YTD cost
    - Highest percentage of total YTD cost
    - Highest potential optimization opportunity
  default_services_to_research: 3
  calculate_service_share: true
  formula: "service_cost / total_ytd_cost * 100"

output:
  format: markdown
  sections:
    - Azure Cost Summary
    - Top Cost Drivers
    - Cost-Saving Opportunities
    - Priority Actions
    - Sources

recommendation_fields:
  - service
  - ytd_cost
  - percentage_of_ytd_cost
  - observed_cost_driver
  - recommendation
  - potential_impact
  - risk
  - rationale
  - source

safety_rules:
  - Never invent Azure cost data.
  - Never invent resource utilization data.
  - Never claim a resource is idle or oversized unless the available data supports it.
  - Never claim savings are guaranteed.
  - Clearly distinguish observed cost data from general optimization guidance.
  - Do not make production changes automatically.
  - Treat recommendations as opportunities to investigate.

failure_handling:
  script_failure: Report the error and do not fabricate cost information.
  missing_cost_data: Report that cost analysis could not be completed.
  web_research_failure: Provide the cost analysis and explicitly state that optimization guidance could not be verified.

expected_script_output:
  ytd_cost: true
  monthly_cost: true
  monthly_budget: true
  budget_percentage: true
  top_services: 5
  currency: true

