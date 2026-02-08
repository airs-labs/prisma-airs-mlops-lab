---
source: pdf_url
url: https://docs.paloaltonetworks.com/content/dam/techdocs/en_US/pdf/ai-runtime-security/ai-runtime-security-release-notes.pdf
title: Prisma AIRS AI Runtime Release Notes
fetched: 2026-02-01T21:28:02.875Z
pages: 37
---
![](images/fetchpdf-1769981278555.pdf-0-full.png)
# Prisma AIRS AI Runtime Release Notes

docs.paloaltonetworks.com


**Contact Information**

Corporate Headquarters:
Palo Alto Networks
3000 Tannery Way
Santa Clara, CA 95054
[www.paloaltonetworks.com/company/contact-support](http://www.paloaltonetworks.com/company/contact-support)


**About the Documentation**

- For the most recent version of this guide or for access to related documentation, visit the Technical
[Documentation portal docs.paloaltonetworks.com.](https://docs.paloaltonetworks.com)

[• To search for a specific topic, go to our search page docs.paloaltonetworks.com/search.html.](https://docs.paloaltonetworks.com/search.html)

- Have feedback or questions for us? Leave a comment on any page in the portal, or write to us at

[documentation@paloaltonetworks.com.](mailto:documentation@paloaltonetworks.com)


**Copyright**

Palo Alto Networks, Inc.
[www.paloaltonetworks.com](https://www.paloaltonetworks.com)


© 2024-2026 Palo Alto Networks, Inc. Palo Alto Networks is a registered trademark of Palo
Alto Networks. A list of our trademarks can be found at [www.paloaltonetworks.com/company/](https://www.paloaltonetworks.com/company/trademarks.html)
[trademarks.html. All other marks mentioned herein may be trademarks of their respective companies.](https://www.paloaltonetworks.com/company/trademarks.html)


**Last Revised**

January 28, 2026


Prisma AIRS AI Runtime Release Notes **2** © 2026 Palo Alto Networks, Inc.


## Table of Contents
##### **Features Introduced...........................................................................................5**

AI Runtime Firewall.....................................................................................................................6
Autoscaling Support........................................................................................................ 6
Decommission Auto-Execute Deployed Firewalls................................................... 6
Multi-Cloud Security Fabric...........................................................................................7
Secure Private Cluster with Prisma AIRS...................................................................7
Discovery Data Deletion................................................................................................8
Optimize Egress Traffic for EKS Containerized Workloads...................................9
Granular Kubernetes Traffic Inspection at the Namespace Level........................9
Secure Serverless Workloads in Cloud Environments..........................................10
Refine Cloud Application Discovery for Enhanced Security............................... 10
Centralized Firewall Management.............................................................................10
Secure Custom AI Models on Private Endpoints...................................................11
Gain Visibility into AI Security Threats.................................................................... 11
Multi-Region Network Intercept................................................................................11
Security Lifecycle Review (SLR) for AWS................................................................12
Streamline Upgrades for Prisma AIRS AI Runtime: Network Intercept............ 12
Extend AI Security to Private Clouds....................................................................... 12
AI Runtime API.......................................................................................................................... 14
AI Agent Discovery....................................................................................................... 14
AI Sessions and and Applications Views..................................................................14
Command Prompt Injection........................................................................................ 15
MCP Threat Detection.................................................................................................15
Securing AI Agents with a Standalone MCP Server..............................................16
Multiple Applications per Deployment Profile....................................................... 17
Unified AI Security Logging........................................................................................ 18
Enhance AI Security with India Region Support.................................................... 18
Malicious Code Extraction from Plain Text.............................................................18
Strengthen Threat Analysis with User IP Data.......................................................19
Enhance Python Application Security with Prisma AIRS SDK............................ 19
API Detection Services for the European Region..................................................19
Automatic Sensitive Data Masking in API Payloads............................................. 20
Protect AI Agent Workflows on Low-Code or No-Code Platforms.................. 20
Prevent Inaccuracies in LLM Outputs with Contextual Grounding................... 21
Define AI Content Boundaries with Custom Topic Guardrails...........................21
Detect Malicious Code in LLM Outputs..................................................................21
Detect Toxic Content in LLM Requests and Responses...................................... 22
Centralized Management of AI Firewalls.................................................................22


Prisma AIRS AI Runtime Release Notes **3** © 2026 Palo Alto Networks, Inc.


Table of Contents


Customize API Security with Centralized Management.......................................23
Automate AI Application Security with Programmatic APIs................................23
Extend Prisma AIRS AI Network Security Across AWS and Azure....................23
Extend AI Network Security to Google Cloud Platform.......................................24
AI Model Security..................................................................................................................... 25
Model Security Adds Support for Two New Model Sources..............................25
Custom Labels for AI Model Security Scan.............................................................25
Local Scan AI Models Directly from Cloud Storages............................................ 26
Customize Security Groups and View Enhanced Scan Results...........................27
Secure AI Models with AI Model Security.............................................................. 27
AI Red Teaming......................................................................................................................... 29
Secure AI Red Teaming with Network Channels...................................................29
Remediation Recommendations for AI Red Teaming Risk Assessment............30
AI Red Teaming Executive Reports...........................................................................31
AI Summary for AI Red Teaming Scans................................................................... 31
Enhanced AI Red Teaming with Brand Reputation Risk Detection................... 32
Error Logs and Partial Scan Reports......................................................................... 32
Automated AI Red Teaming........................................................................................33
##### **Known Issues.................................................................................................... 34** **Addressed Issues..............................................................................................37**


Prisma AIRS AI Runtime Release Notes **4** © 2026 Palo Alto Networks, Inc.


### Features Introduced

Review the Prisma AIRS release notes to learn about all the new features.

   - AI Runtime Firewall

   - AI Runtime API

   - AI Model Security

  - AI Red Teaming


Prisma AIRS AI Runtime Release Notes **5** © 2026 Palo Alto Networks, Inc.


### AI Runtime Firewall

Here are the new Prisma AIRS AI Runtime firewall features.
#### Autoscaling Support


December 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[Configuring Autoscaling feature enables your software firewalls to automatically scale up or down](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/activate-your-ai-runtime-security-license)
based on traffic demands, ensuring optimal resource utilization and cost efficiency. With this
feature, you can configure the firewall to publish CloudWatch metrics which in turn triggers the
Autoscaling events.

With Autoscaling, you can choose between static or dynamic scaling models during deployment.
Dynamic scaling allows you to select from several metrics to base your autoscaling decisions
on, giving you fine-grained control over how your security infrastructure adapts to changing
conditions. This approach ensures that your security posture remains robust during traffic surges
while optimizing license consumption during periods of lower demand. After traffic decreases
and firewalls are deactivated, the system automatically removes the firewalls from inventory and
returns licenses to your pool for future scaling events.
#### Decommission Auto-Execute Deployed Firewalls


December 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[You can decommission deployed firewalls and associated cloud resources through Strata Cloud](https://docs.paloaltonetworks.com/ai-runtime-security/administration/manage-auto-execute-deployed-firewalls)
Manager when your network infrastructure changes or evolves. This Terraform-based autoexecute deployment process allows you to cleanly remove specific firewall deployments, their
underlying cloud resources, and release the Software NGFW credits that were consumed for
licensing those firewalls. You would typically use this feature when reorganizing your network
architecture, scaling down your security infrastructure, or retiring specific firewall instances that
are no longer needed in your environment. The decommissioning process provides you with the
flexibility to optimize your resource allocation and costs while maintaining the ability to deploy
new firewalls in the same cloud account as your requirements change. You can monitor the entire
removal process through the Cloud Task log to track progress and identify any potential issues,
ensuring you have full visibility into the decommissioning workflow. This capability is particularly
valuable when you need to make rapid adjustments to your security posture or when transitioning
between different deployment configurations without impacting your overall cloud account
infrastructure.


Prisma AIRS AI Runtime Release Notes **6** © 2026 Palo Alto Networks, Inc.


#### Multi-Cloud Security Fabric

November 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[You can use Multi-Cloud Security Fabric (MSF) Deployment to fully automate the deployment](http://docs.paloaltonetworks.com/ai-runtime-security/administration/deploy-prisma-airs-runtime-firewalls-with-auto-execute)
of AIRS and VM-Series firewall instances along with the complete networking infrastructure
required for traffic redirection across your cloud environments. This feature eliminates the manual
complexity of creating security VPCs in AWS or VNets in Azure, configuring load balancers,
setting up subnets, and orchestrating cloud-native routing elements that was previously required
when using basic Terraform templates from Strata Cloud Manager.

The automation handles multiple traffic flow scenarios including east-west flows within VPCs or
VNets, between VPCs in single regions, across different regions in the same or multiple clouds,
and north-south flows for internet egress traffic. You can deploy firewalls in any region regardless
of where your applications are located, and the system automatically establishes the necessary
tunnels, route tables, and cloud-native elements to ensure traffic reaches the appropriate firewall
instances for inspection.

You benefit from this feature when you need to secure complex multi-cloud architectures
without investing significant time in manual network configuration. The automated deployment
reduces the risk of configuration errors that can occur when manually setting up VPC peering,
transit gateway routing, and cross-account connectivity. You can redirect traffic from discovered
applications with minimal clicks while maintaining visibility into all orchestration changes through
both cloud dashboards and SCM.

The feature supports both new deployments where new security infrastructure is created and
existing environments where you can integrate existing VM-series firewalls into the automated
traffic paths. You maintain control over the deployment process with options to opt out of
automatic networking setup if you prefer to handle routing configuration manually or if you have
existing networking arrangements that should remain unchanged.

[You can initiate deployments either from the Cloud Asset Map page where application context](https://docs.paloaltonetworks.com/ai-runtime-security/administration/discover-your-cloud-resources/cloud-asset-map)
is automatically populated, or through the traditional deployment interface where you manually
specify source and target details. The system minimizes traffic disruption by establishing tunnels
before modifying route tables and provides end-to-end path tracing capabilities to validate traffic
flows before and after firewall insertion.
#### Secure Private Cluster with Prisma AIRS


November 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


Prisma AIRS AI Runtime Release Notes **7** © 2026 Palo Alto Networks, Inc.


[You can now deploy and manage security infrastructure for private Kubernetes clusters and](https://docs.paloaltonetworks.com/ai-runtime-security/administration/discover-your-cloud-resources/private-cluster-discovery)
across multiple cloud accounts using the enhanced deployment service on Strata Cloud Manager.
This feature addresses the need to secure private cluster traffic that cannot be accessed directly
from the public internet, while providing the flexibility to deploy application workloads and
security components in separate accounts managed by different teams within your organization.

When you deploy Kubernetes workloads in private clusters, you can now use AIRS or VMSeries firewalls for traffic inspection through an enhanced Tag Collector deployment in your
[AWS or Azure environments. The Tag Collector connects to your private clusters to collect](https://docs.paloaltonetworks.com/ai-runtime-security/administration/deploy-a-tag-collector-agent-to-secure-private-clusters)
IP-tag information and forwards this data to the Cloud IP-Tag Service, enabling the Discovery
service to maintain visibility into your container workloads. The generated Terraform templates
accommodate both tag collection and traffic inspection from private clusters, eliminating the
previous limitation that required public cluster endpoints.

You can select applications across multiple cloud accounts and deploy firewalls in different
accounts than your application infrastructure. On AWS, the solution uses Resource Access
Manager to share Transit Gateways across accounts, enabling the Tag Collector to collect IP-tags
from private clusters and forward traffic to AIRS for inspection. Gateway Load Balancer service
principals expose GWLB services across accounts for Kubernetes traffic inspection. On Azure, the
solution leverages virtual network peering between the transit VNET and application VNET, with
private DNS zone access enabling tag collection from private AKS clusters.

The Tag Collector automatically discovers clusters within your environment and generates
monitoring definitions for each identified cluster. It continuously monitors for cluster additions or
removals and communicates configuration changes to the Cloud IP-Tag service.

This enhancement decouples the tag collector Terraform templates, allowing you to deploy them
standalone when generated through the deployment service. You maintain the option to deploy
firewalls and tag collectors in separate accounts from your application account, provided those
accounts are onboarded to Strata Cloud Manager.
#### Discovery Data Deletion


November 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[You can delete historical discovery data for cloud accounts in Prisma AIRS to meet data](https://docs.paloaltonetworks.com/ai-runtime-security/administration/discover-your-cloud-resources/manage-discovery-data)
[compliance requirements when you need to remove collected asset information, flow logs, and](https://docs.paloaltonetworks.com/ai-runtime-security/administration/discover-your-cloud-resources/manage-discovery-data)
audit logs from your environment. This feature addresses regulatory compliance scenarios where
you must permanently remove specific data sets while maintaining operational security coverage.
When you initiate discovery data deletion, the system validates your request and places the cloud
account in an inactive state to prevent new data collection while a background process removes
all associated data from storage systems and discovery databases.

The deletion process handles firewall deployments differently based on their deployment
method. Manually-deployed firewalls continue inspecting traffic during data deletion, ensuring
uninterrupted security coverage, while auto-deployed firewalls stop traffic inspection as the
system undeploys them. You must manually delete the Terraform template associated with
the cloud account regardless of deployment type. For auto-deployed firewalls, deleting the


Prisma AIRS AI Runtime Release Notes **8** © 2026 Palo Alto Networks, Inc.


Terraform template removes the firewall from your deployment, whereas manually deployed
firewalls require separate removal since only the template is deleted. The deletion process runs
asynchronously to maintain system performance, during which you cannot modify account
settings or enable additional monitoring features.

Prisma AIRS maintains audit timestamps throughout the deletion process to track when deletion
was requested and completed, providing the visibility needed for compliance reporting and data
lifecycle management activities. Once deletion completes, the account remains inactive and no
longer collects data until you manually reactivate it through the cloud account interface in Strata
Cloud Manager.
#### Optimize Egress Traffic for EKS Containerized Workloads


August 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


The overlay routing feature for EKS traffic allows Prisma [®] AIRS [™] AI Runtime: Network Intercept
to eliminate traffic hairpinning. This is achieved by enabling direct egress from the intercept to
next-hop destinations like Internet Gateways (IGWs) and NAT Gateways. This new capability
prevents traffic from being double-inspected, which reduces latency, bandwidth usage, and
resource consumption.

[With overlay routing, can now function as a single component for both security inspection and](https://docs.paloaltonetworks.com/ai-runtime-security/administration/deploy-ai-instances-in-public-clouds-as-a-software/add-ai-instance-for-aws)
network address translation, simplifying the network architecture. It consolidates these functions
into a single step, ensuring comprehensive security for containerized workloads while maintaining
an efficient and direct traffic flow.
#### Granular Kubernetes Traffic Inspection at the Namespace Level


August 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


You can apply granular security controls to containerized applications by managing traffic
inspection at the individual Kubernetes namespace level, moving beyond an all-or-nothing
[approach. You can selectively inspect or bypass traffic flows based on CIDR ranges within specific](https://docs.paloaltonetworks.com/ai-runtime-security/administration/deploy-ai-instances-in-public-clouds-as-a-software)
namespaces. This provides an optimized security posture where critical traffic is thoroughly
examined, while known benign traffic can bypass inspection. This selective approach helps
improve performance and resource utilization without compromising security for your Kubernetes
workloads. This enhancement strengthens security for your containerized applications, enabling
more efficient and effective management of your security posture across diverse Kubernetes
workloads.


Prisma AIRS AI Runtime Release Notes **9** © 2026 Palo Alto Networks, Inc.


#### Secure Serverless Workloads in Cloud Environments

August 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


Protect your serverless resources in Azure or AWS environments by defining security boundaries
[for them during cloud account onboarding. Once defined, these newly discovered serverless](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/onboard-and-activate-cloud-account-in-scm)
functions become visible on your application dashboard, integrating with your existing virtual
machine and container workloads for a unified view of your entire cloud environment. This
consolidation of visibility allows you to monitor and manage security for all your compute types
from a single location.

The platform uses the same streamlined workflow you already use for other cloud assets. By
extending this workflow to serverless functions, you can consistently deploy firewall protection,
ensuring comprehensive security coverage as your cloud-native architectures evolve. This
approach provides a repeatable, automated way to secure your dynamic cloud applications,
helping to maintain a strong security posture without the need for manual, per-resource
configurations. The integration of serverless resources into the centralized dashboard simplifies
management and helps you quickly identify and protect newly deployed functions.
#### Refine Cloud Application Discovery for Enhanced Security


August 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


Gain granular control over cloud asset discovery and application organization using tags, subnets,
and namespaces. This feature allows you to define precise application boundaries during cloud
account onboarding, aligning with modern, dynamic cloud architectures. This feature provides
[enhanced application definition options during the cloud account onboarding process.](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/onboard-and-activate-cloud-account-in-scm)
#### Centralized Firewall Management


August 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[You can now deploy and manage](https://docs.paloaltonetworks.com/ai-runtime-security/administration/deploy-vm-series) firewalls directly from, which streamlines the deployment and
monitoring of your entire security infrastructure from a single, unified interface. This centralized
dashboard within consolidates threats detected by both firewalls and AI Runtime: Network
Intercept, giving you a unified view of your security operations.


Prisma AIRS AI Runtime Release Notes **10** © 2026 Palo Alto Networks, Inc.


You can also use the same streamlined workflow to deploy a firewall as you would for other
cloud assets. This capability helps you to accelerate your deployment processes and ensures
consistent protection. Enhanced application details provide clear insights into network traffic flow
paths, showing which firewall platform protects each application and displaying the firewall serial
number and type ( or AI Runtime: Network Intercept).
#### Secure Custom AI Models on Private Endpoints


August 2025

**Supported for:**

   - Prisma AIRS (Managed by Panorama or Strata Cloud Manager)


You can extend AI security inspection to LLMs hosted on privately managed endpoints or input/
[output schemas that are not publicly known. By enabling this support within your AI security](https://docs.paloaltonetworks.com/ai-runtime-security/administration/prevent-network-security-threats/create-ai-security-profile)
[profile, all traffic that matches a security policy rule is forwarded to the AI cloud service for threat](https://docs.paloaltonetworks.com/ai-runtime-security/administration/prevent-network-security-threats/create-ai-security-profile)
inspection, regardless of whether the model is a well-known public service or a custom-built
private one. This ensures comprehensive security for your entire AI ecosystem.

The new AI security profile inspects and secures the AI traffic between AI applications and
LLM models passing through Prisma AIRS: Network intercept that are managed by Strata Cloud
Manager or Panorama. This profile protects against threats such as prompt injections and
sensitive data leakage.
#### Gain Visibility into AI Security Threats


July 2025

**Supported for:**

   - Prisma AIRS (Managed by Panorama)


Gain enhanced visibility into AI-specific threats through an additional AI security report that
[displays comprehensive AI security threat logs](https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/monitoring/view-and-manage-logs/log-types-and-severity-levels/threat-logs) forwarded by Network intercept. This gives you
enhanced visibility into AI model protection, AI application protection, and AI data protection
threats detected based on your AI security profile configurations. You can also filter logs by the
`ai-security` threat type when configuring log forwarding profiles or building custom reports,
enabling targeted analysis and streamlined security operations for AI-specific threats.
#### Multi-Region Network Intercept


July 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


Prisma AIRS AI Runtime Release Notes **11** © 2026 Palo Alto Networks, Inc.


[Prisma AIRS AI Runtime: Network intercept now supports deployment across multiple regions,](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/ai-runtime-security-api-intercept-overview)
including US, UK, India, Canada, and Singapore. This expansion enables you to deploy the Prisma
AIRS AI Runtime: Network intercepts on tenant service groups (TSG) in your preferred regions.
#### Security Lifecycle Review (SLR) for AWS


June 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


Gain comprehensive visibility, control, and protection for your AWS environment without
[deployment of an inline firewall. The Security Lifecycle Review (SLR) for AWS, within AI Runtime](https://docs.paloaltonetworks.com/ai-runtime-security/administration/deploy-slr-for-aws)
Security: Network intercept when deployed in the SLR mode, protects your inbound, outbound,
and east-west traffic using mirrored traffic between the application Elastic Network Interfaces
(ENIs). This non-inline deployment method allows security monitoring and enforcement without
altering the existing data path. The platform can generate detailed reports and threat logs based
on this analyzed traffic, providing insights into potential security incidents.

By leveraging mirrored traffic, you gain crucial threat detection and prevention capabilities for
all directions of traffic flow, without the need to re-architect your network or introduce latency
associated with inline deployments. This simplifies security operations while enhancing your
ability to identify and respond to threats effectively, all while maintaining the agility of your cloud
environment.
#### Streamline Upgrades for Prisma AIRS AI Runtime: Network Intercept


April 2025

**Supported for:**

   - Prisma AIRS (Managed by PAN-OS or Panorama)


You can now upgrade your **Prisma** **[®]** **AIRS** **[™]** **AI Runtime: Network Intercept** to maintain
protection against AI-specific threats. The platform now supports multiple upgrade paths,
providing flexibility and ensuring continuous security.

The firewall image format, with a `*.aingfw` [extension, ensures compatibility specifically with](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/upgrade-airs-image)
the environment. This dedicated `*.aingfw` format ensures compatibility with environments
protecting AI workloads while simplifying security operations.
#### Extend AI Security to Private Clouds


April 2025

**Supported for:**


Prisma AIRS AI Runtime Release Notes **12** © 2026 Palo Alto Networks, Inc.


   - Prisma AIRS (Managed by Panorama or Strata Cloud Manager)


You can secure and monitor AI workloads that are deployed in private clouds, such as those built
[on ESXi and KVM servers. This capability extends protection to your AI applications and models](https://docs.paloaltonetworks.com/ai-runtime-security/administration/deploy-airs-on-private-clouds)
even when they interact with public cloud Large Language Model (LLM) providers. By protecting
the traffic between your private cloud workloads and external LLMs, you can safeguard against
data exfiltration, prompt injection, and other threats specific to AI interactions. This functionality
is essential for organizations with hybrid cloud strategies. It ensures that security is not a barrier
to leveraging AI, allowing you to maintain control and visibility over your AI ecosystem regardless
of where your data and applications are located.

To enable this, the Prisma AIRS [™] AI Runtime: Network intercept can be manually deployed and
bootstrapped in your private cloud environment. This deployment provides a crucial security layer
for AI workloads that reside outside of public cloud infrastructure. Once deployed, the firewall
can be centrally managed by either Strata [™] Cloud Manager or Panorama, allowing for consistent
policy enforcement and monitoring across your entire network.


Prisma AIRS AI Runtime Release Notes **13** © 2026 Palo Alto Networks, Inc.


### AI Runtime API

Here are the new Prisma AIRS AI Runtime API features.
#### AI Agent Discovery


November 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[Prisma AIRS supports AI Agent Discovery to track enterprise AI agents you create using simple,](https://docs.paloaltonetworks.com/ai-runtime-security/administration/agent-discovery)
no-code/low-code tools provided by cloud providers. Think of this process by creating an
_inventory_ and a _security guard_ for your AI bots (or, _agents_ ); these processes are built on cloud
platforms like AWS Bedrock and Azure AI Foundry/Open AI.

AI Agent Discovery addresses two main objectives:

  - **Determine what AI agents exist.** This part of the process, referred to as _configuration discovery_,
involves finding the blueprint of each agent, including its name, description, the brain
(Foundation Model) it uses, what it knows (Knowledge Bases), and what it can _do_ (Tools).

  - **Determine how the AI agents are used** . This part of the process, referred to as runtime
interactions, involves watching the agent while it's working to see if it talks to another agent,
uses a tool, or asks its brain (model) a question. This is primarily supported for AWS agents
using their activity logs.

AI Agent Discovery supports SaaS and enterprise AI agents. With this functionality you can
discover agents from an onboarded cloud account and secure them using the AI Runtime API
Intercept workflow.


_At this release, only AWS Bedrock agents and Azure AI Foundry Service (and Azure_
_OpenAI Assistants) are supported._
#### AI Sessions and and Applications Views


October 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


The new AI Applications and AI Sessions features provide security practitioners with enhanced
visibility into AI-enabled application security. This enables real-time insights into AI applications
and their conversational sessions, allowing for proactive detection and prevention of security
profile violations. These features address the limitation of traditional security views by grouping
related API calls into coherent sessions, offering a comprehensive understanding of AI application
behavior.


Prisma AIRS AI Runtime Release Notes **14** © 2026 Palo Alto Networks, Inc.


Key capabilities include:

  - **AI Sessions** : View grouped, sequential API calls representing full conversations or interactions.

  - **AI Applications** : Access an inventory of all protected AI applications, showing violation trends
and associated security profiles.

[For more information, see Use the Prisma AIRS AI Sessions and API Application Views.](https://docs.paloaltonetworks.com/ai-runtime-security/administration/api-intercept-create-configure-security-profile/use-the-ai-sessions-and-application-views)
#### Command Prompt Injection


October 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[You can detect command injection attacks in AI applications using the Malicious Code Detection](https://docs.paloaltonetworks.com/ai-runtime-security/administration/detect-and-alert-on-malicious-traffic)
[capabilities in Prisma AIRS. This feature identifies command injection scripts within prompts,](https://docs.paloaltonetworks.com/ai-runtime-security/administration/detect-and-alert-on-malicious-traffic)
responses, and MCP content that may attempt to execute malicious commands in your
environment. When you enable Malicious Code detection in your AI security profile, the system
extracts and analyzes code blocks from content, including encoded scripts using Base64, ROT13,
hexadecimal, and compressed formats.

You should enable this protection if you are using agent tools, MCP servers, or code generation
applications where input could contain embedded commands. The detection service extracts code
snippets from content using machine learning models, then analyzes those snippets through ATP
services to identify command injection patterns. You can configure the feature alongside existing
malicious code detection for known malware scripts.

You will need this feature if you are processing user-generated content, integrating with external
AI services, or generating executable code, as it prevents attackers from injecting commands that
could execute in your development environment or production systems. The detection capability
is available in both synchronous and asynchronous scan APIs, allowing you to integrate protection
into existing AI application workflows.
#### MCP Threat Detection


September 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


Prisma AIRS protects your AI agents from supply chain attacks by adding support for Model
Context Protocol (MCP) tools. This feature adds security scanning capabilities to the MCP
ecosystem, specifically targeting two critical threats:

   - Context poisoning via tool definition, tool input (request) and tool output (response)
[manipulation. This prevents malicious actors from tampering with MCP tool definitions that](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#tool)


Prisma AIRS AI Runtime Release Notes **15** © 2026 Palo Alto Networks, Inc.


could trick AI agents into performing harmful actions like leaking sensitive data or executing
dangerous commands.

   - Exposed credentials and identity leakage. This detects and blocks sensitive data (tokens,
credentials, API keys) from being exposed through MCP tool interactions.

This functionality provides a number of benefits:

   - Zero-touch security. No new UI or profile configuration required.

   - Comprehensive threat detection. Leverages existing detection services (DLP, prompt injection,
toxic content, etc.).

   - Real-time protection. Works with both synchronous and asynchronous scanning APIs.

   - Supply chain security. Validates tool descriptions, inputs and outputs as part of MCP
communication.

It ensures that as AI agents become more powerful and autonomous through MCP tools, they
cannot be weaponized against your organization through compromised or malicious tools in the
MCP ecosystem.

This feature represents a broader initiative to secure AI agents that use MCP for tool integration,
ensuring that MCP-based AI systems remain secure against manipulation and data exposure
[attacks. For more information, Detect MCP Threats.](https://docs.paloaltonetworks.com/ai-runtime-security/administration/prevent-network-security-threats/detect-mcp-threats.html)
#### Securing AI Agents with a Standalone MCP Server


September 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


The Prisma AIRS Model Context Protocol (MCP) server is a standalone remote server that
addresses significant integration challenges in securing agentic AI applications with easy
deployment. You can use this service to protect your AI applications without the complex
infrastructure dependencies or extensive code changes that traditional security solutions require.

[The Prisma AIRS MCP server in the Palo Alto Networks cloud environment serves as a centralized](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/prisma-airs-mcp-server-for-centralized-ai-agent-security)
security gateway for AI agent interactions. The server validates all tool invocations through the
MCP and provides real-time Threat Detection on tool inputs, outputs, and tool descriptions or
schemas. The Prisma AIRS MCP server empowers you within the MCP ecosystem by delivering
security-focused building blocks for AI and copilot workflows. Its universal, easy-to-integrate
interface works with any MCP client, enabling AI agents to translate plain-language user requests
into secure, powerful workflows.


Prisma AIRS AI Runtime Release Notes **16** © 2026 Palo Alto Networks, Inc.


![](images/fetchpdf-1769981278555.pdf-16-0.png)

When you implement the MCP server as a tool, you only need to specify the protocol type,
URL, and API key in your configuration file to automatically scan all external MCP server calls
for vulnerabilities. This minimal setup enables you to detect various threats including prompt
injection, MCP context poisoning, and exposed credentials without disrupting your development
workflow. The service is valuable for low-code or no-code platforms where inserting security
between the AI agent and its tool calls would otherwise be challenging. You can protect your AI
applications with features such as AI Application Protection, AI Model Protection, and AI Data
Protection, each designed to safeguard specific aspects of your AI workflows.

The Prisma AIRS MCP server integrates with your existing API infrastructure, enabling you to
view comprehensive scan logs through familiar interfaces. This integration ensures you maintain
visibility into security events while simplifying your security operations.
#### Multiple Applications per Deployment Profile


September 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[Prisma AIRS API allows you to associate multiple applications with a single deployment profile,](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/ai-runtime-security-api-intercept-overview/onboard-api-runtime-security-api-intercept-in-scm)
removing the need to create separate deployment profiles for each application.

With this feature, you can associate up to 20 applications with a single deployment profile,
significantly simplifying management while maintaining consistent security policies. When
creating a new application, you can either select an existing activated deployment profile or
activate a new one before establishing the association. This flexibility helps you organize your
applications based on shared security requirements or business functions.


_All applications associated with a single deployment profile consume the daily API calls_
_quota tied to that deployment profile. When setting this value in CSP, consider how many_
_applications (max allowed is 20) you plan to associate with this deployment profile._


You can easily modify which deployment profile an application uses through the application edit
view, allowing you to adapt as your security needs evolve. The application detail and list views
clearly display which deployment profile each application is linked to, providing transparency


Prisma AIRS AI Runtime Release Notes **17** © 2026 Palo Alto Networks, Inc.


and helping you maintain proper governance. This capability is fully supported through both
Strata Cloud Manager and API endpoints, enabling you to programmatically manage multiple
applications per deployment profile for automation and integration scenarios.
#### Unified AI Security Logging


August 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


API scan events, including blocked threats, now integrate with the, providing a unified log viewer
[interface for both API-based and network-based AI security events. The Log Viewer now includes](https://docs.paloaltonetworks.com/ai-runtime-security/administration/detect-and-alert-on-malicious-traffic)
a new log type, **Prisma AIRS AI Runtime Security API**, which displays the scan API logs. This
integration allows Security Operations Center (SOC) teams to be alerted to critical threats.The
integration also enables a powerful query builder to search and analyze scan data and supports
out-of-the-box queries for analyzing threats. Log forwarding is now supported for Prisma AIRS AI
Runtime: API intercept. This ensures comprehensive visibility and streamlines security operations
across multiple supported regions.
#### Enhance AI Security with India Region Support


August 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


You can now deploy API detection services in the India region, ensuring compliance and
improving performance. When creating a deployment profile, you can select India as your
preferred region. This choice determines the underlying region for data processing and storage.

[When you create a deployment profile for the API intercept and associate it with a TSG, you](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/ai-runtime-security-api-intercept-overview/ai-deployment-profile-airs-api-intercept)
can select your preferred region: United States, Europe (Germany), or India. A separate, regionspecific API endpoint is provided for India. This deployment includes all AI Runtime: API intercept
services and routes detection requests to the nearest APAC-based region for each respective
service, reducing latency and data transfer costs.
#### Malicious Code Extraction from Plain Text


July 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


Prisma AIRS AI Runtime Release Notes **18** © 2026 Palo Alto Networks, Inc.


Malicious code embedded directly in plain-text fields of API prompts or responses is detected
across both synchronous and asynchronous scan services. Even if the code isn’t in a traditional file
[format, it is identified and analyzed. For testing purposes, send malicious code in plain text within](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/ai-runtime-security-api-intercept-overview)
the API “prompt” or “response” fields to confirm detection.

As AI applications become more integrated, the risk of malicious code injection through user input
or model responses increases. This feature helps safeguard your AI models and applications by
providing a layer of defense against such threats, even when the code is embedded in formats
other than traditional files.
#### Strengthen Threat Analysis with User IP Data


July 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


You can include the end user's IP address in both synchronous and asynchronous scan requests
[to enhance threat correlation and incident response capabilities. A new `user_ip` field has been](https://pan.dev/prisma-airs/api/airuntimesecurity/prisma-airs-ai-runtime-api-intercept/)
added to the scan request metadata schema, allowing you to incorporate the originating IP
address of the end user in both synchronous and asynchronous scan requests. The `user_ip` field
provides crucial context for security analysis. Understanding the source IP address of an end user
involved in a scan significantly enhances your ability to correlate threats and streamline incident
response.
#### Enhance Python Application Security with Prisma AIRS SDK


May 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[Prisma AIRS API Python SDK, integrates advanced AI security scanning into Python applications.](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/ai-runtime-security-api-intercept-overview/airs-apis-python-sdk)
It supports Python versions 3.9 through 3.13, offering synchronous and asynchronous scanning,
robust error handling, and configurable retry strategies.

This SDK allows developers to "shift left" security, embedding real-time AI-powered threat
detection and prevention directly into their Python applications. By providing a streamlined
interface for scanning prompts and responses for malicious content, data leaks, and other threats,
it helps secure your AI models, data, and applications from the ground up.
#### API Detection Services for the European Region


May 2025

**Supported for:**


Prisma AIRS AI Runtime Release Notes **19** © 2026 Palo Alto Networks, Inc.


   - Prisma AIRS (Managed by Strata Cloud Manager)


You can now use Strata Cloud Manager to manage API detection services hosted in the EU
[(Germany) region. When creating a deployment profile, you select your preferred region, and all](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/activate-your-ai-runtime-security-license/create-an-ai-instance-deployment-profile-in-csp)
subsequent scan requests are routed to the corresponding regional API endpoint. This allows for
localized hosting and processing of your AI security operations.

By enabling regional deployment of AI security services, you can: comply with data residency
requirements, reduce latency by processing security scans closer to your European users and
infrastructure.
#### Automatic Sensitive Data Masking in API Payloads


May 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[Automatic detection and masking of sensitive data patterns are now available in the scan API](https://docs.paloaltonetworks.com/ai-runtime-security/administration/prevent-network-security-threats/api-intercept-create-configure-security-profile)
output, which scans the prompts and responses in Large Language Models (LLM). This feature
replaces sensitive information such as Social Security Numbers and bank account details with "X"
characters while maintaining the original text length. API scan logs indicate sensitive content with
the new "Content Masked" column.

As LLMs become more prevalent, the risk of inadvertently exposing sensitive data increases.
This automatic masking capability enhances data privacy and maintains compliance with data
protection regulations. Proactively obscuring sensitive information reduces the risk of data
leakage, strengthens the security posture of AI applications, and builds greater trust in the use of
AI models by ensuring sensitive details are never fully exposed in logs or intermediary steps.
#### Protect AI Agent Workflows on Low-Code or No-Code Platforms


May 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[You can protect and monitor AI agents against unauthorized actions and system manipulation.](https://docs.paloaltonetworks.com/ai-runtime-security/administration/prevent-network-security-threats/ai-agent-security-low-no-code)
This feature extends security to AI agents developed on low-code/no-code platforms, like
Microsoft Copilot Studio, AWS Bedrock, GCP Vertex AI, and VoiceFlow, as well as custom
workflows.

As AI agents become more prevalent, they introduce new attack surfaces. This protection is
crucial for ensuring the integrity and secure operation of your AI agents, regardless of how the
agents were developed.


Prisma AIRS AI Runtime Release Notes **20** © 2026 Palo Alto Networks, Inc.


#### Prevent Inaccuracies in LLM Outputs with Contextual Grounding

May 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[You can now enable Contextual Grounding detection in your LLM response, which detects](https://docs.paloaltonetworks.com/ai-runtime-security/administration/prevent-network-security-threats/api-intercept-create-configure-security-profile)
responses that contain information not present in or contradicting the provided context. This
feature works by comparing the LLM's generated output against a defined input context. If
the response includes information that wasn't supplied in the context or directly contradicts it,
the detection flags these inconsistencies, helping to identify potential hallucinations or factual
inaccuracies.

Ensuring that LLM responses are grounded in the provided context is critical for applications
where factual accuracy and reliability are paramount.
#### Define AI Content Boundaries with Custom Topic Guardrails


May 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[You can enable the Custom Topic Guardrails detection service to identify a topic violation in the](https://docs.paloaltonetworks.com/ai-runtime-security/administration/prevent-network-security-threats/api-intercept-create-configure-security-profile)
given prompt or response. This feature allows you to define specific topics that must be allowed
or blocked within the prompts and responses processed by your LLM models. The system then
monitors content for violations of these defined boundaries, ensuring that interactions with your
LLMs stay within acceptable or designated subject matter.

Custom Topic Guardrails provide granular control over the content your AI models handle,
offering crucial protection against various risks. For example, you can prevent misuse, maintain
brand integrity, ensure compliance, and enhance the focus of the LLM's outputs.
#### Detect Malicious Code in LLM Outputs


March 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[Code snippets generated by Large Language Models (LLMs) can be protected with Malicious Code](https://docs.paloaltonetworks.com/ai-runtime-security/administration/prevent-network-security-threats/api-intercept-create-configure-security-profile)
[Detection feature for potential security threats. This feature is crucial for preventing supply chain](https://docs.paloaltonetworks.com/ai-runtime-security/administration/prevent-network-security-threats/api-intercept-create-configure-security-profile)
attacks, enhancing application security, maintaining code integrity, and mitigating AI risks.


Prisma AIRS AI Runtime Release Notes **21** © 2026 Palo Alto Networks, Inc.


The system supports scanning for malicious code in multiple languages, including JavaScript,
Python, VBScript, PowerShell, Batch, Shell, and Perl.

To activate this protection, you need to enable it within the API Security Profile. When
configured, this feature can block the execution of potentially malicious code or be set to allow,
depending on your security needs. This capability is vital for organizations that are increasingly
leveraging generative AI for development, as it helps to secure against the risks of LLM poisoning,
where adversaries intentionally introduce malicious data into training datasets to manipulate
model outputs.
#### Detect Toxic Content in LLM Requests and Responses


March 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


To protect AI applications from generating or responding to inappropriate content, a new
[capability adds toxic content detection to LLM requests and responses. This advanced detection](https://docs.paloaltonetworks.com/ai-runtime-security/administration/prevent-network-security-threats/api-intercept-create-configure-security-profile)
is designed to counteract sophisticated prompt injection techniques used by malicious actors to
bypass standard LLM guardrails. The feature identifies and mitigates content that contains hateful,
sexual, violent, or profane themes.

This capability is vital for maintaining the ethical integrity and safety of AI applications. It helps
protect brand reputation, ensures user safety, mitigates misuse, and promotes a responsible AI. By
analyzing both user inputs and model outputs, the system acts as a filter to intercept requests and
responses that violate predefined safety policies.

The system can either block the request entirely or rewrite the output to remove the toxic
language. In addition to detecting toxic content, it also helps prevent bias and misinformation,
which are common risks associated with LLMs. By implementing this security layer, you can
ensure that your AI agents and applications operate securely and responsibly, safeguarding
against both intentional and unintentional generation of harmful content.
#### Centralized Management of AI Firewalls


February 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[You can now manage and monitor your AI firewalls with Panorama. This integration allows you to](https://docs.paloaltonetworks.com/ai-runtime-security/administration/deploy-panorama-managed-airs-firewall)
leverage a central platform for defining and observing AI security policies and logs.

This capability extends to securing VM workloads and Kubernetes clusters, allowing for a unified
approach to security across your diverse environments. Centralized management provides a
number of key benefits, including unified visibility, streamlined operations, consistent policy
enforcement, and accelerated incident response.


Prisma AIRS AI Runtime Release Notes **22** © 2026 Palo Alto Networks, Inc.


#### Customize API Security with Centralized Management

January 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


You can [manage Applications, API Keys, and Security Profiles](https://docs.paloaltonetworks.com/ai-runtime-security/administration/prevent-network-security-threats/airs-apirs-manage-api-keys-profile-apps) from a centralized dashboard
within Strata Cloud Manager. This allows you to create and manage multiple API keys, define
and manage applications, and create and manage AI API security profiles and their revisions. This
centralized approach enables you to tailor security policy rules precisely to the unique needs of
different applications and API integrations.
#### Automate AI Application Security with Programmatic APIs


November 2024

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[Prisma AIRS API intercept is a threat detection service that enables you to discover and secure](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/ai-runtime-security-api-intercept-overview)
applications by programmatically scanning prompts and models for threats. You can implement a
Security-as-Code approach using our REST APIs to protect your AI models, applications, and AI
data.

These REST APIs seamlessly integrate AI security scanning into your application development
and deployment workflows. This methodology enables automated and continuous protection for
your AI models, applications, and the data they process, making security an intrinsic part of your
development lifecycle.
#### Extend Prisma AIRS AI Network Security Across AWS and Azure


October 2024

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[You can now discover your Azure and AWS cloud assets by onboarding your accounts in Strata](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/onboard-and-activate-cloud-account-in-scm)
Cloud Manager for central management. You can deploy and secure these environments with
Prisma AIRS AI Runtime: Network intercept.

This expanded support enables unified multi-cloud protection, enhanced visibility, streamlined
deployment, and reduced risk.


Prisma AIRS AI Runtime Release Notes **23** © 2026 Palo Alto Networks, Inc.


#### Extend AI Network Security to Google Cloud Platform

September 2024

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[You can now discover your GCP cloud assets by onboarding your GCP account in Strata Cloud](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/onboard-and-activate-cloud-account-in-scm)
[Manager. You can deploy and secure your GCP environment with network intercept. This feature](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/onboard-and-activate-cloud-account-in-scm)
enables onboarding your GCP cloud account to a centralized management platform, enabling the
discovery of your cloud assets and providing visibility into your AI workload deployments.

This expanded support for GCP provides dedicated protection, enhanced visibility, streamlined
deployment, and reduced risk.


Prisma AIRS AI Runtime Release Notes **24** © 2026 Palo Alto Networks, Inc.


### AI Model Security

Here are the new Prisma AIRS AI Model Security features.
#### Model Security Adds Support for Two New Model Sources


January 2026

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


AI Model Security now supports **JFrog Artifactory** and **GitLab Model Registry** as sources, adding
to existing support for Local Storage, HuggingFace, S3, GCS, and Azure Blob Storage.

[You can now scan models stored in two new cloud storage types:](https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/scanning-models)

  - **Artifactory** —Models stored in JFrog Artifactory ML Model, Hugging Face, or generic artifact
repositories.

  - **GitLab Model Registry** —Models stored in the GitLab Model Registry.

Organizations can now establish consistent security standards across models regardless of where
development teams store them. Security Groups can enforce the same comprehensive validation
(deserialization threats, neural backdoors, license compliance, insecure formats) for models in
Artifactory and GitLab that you already apply to other Sources.

This expansion reduces operational risk from unvalidated models by eliminating blind spots in
your AI security posture. Teams no longer need to move models between repositories to apply
security rules or generate compliance audit trails.

[Configure Artifactory and GitLab sources through the same Security Group workflows used for](https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/customizing-security-groups)
other model repositories.
#### Custom Labels for AI Model Security Scan


January 2026

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


Custom Labels for AI Model Security Scans enables you to attach custom key-value metadata
to your model scans, providing essential organizational context for enterprise-scale security
operations. When you run security scans on your AI models, the results exist in isolation without
the operational context your security teams need to effectively triage, assign, and remediate
findings. This feature allows you to categorize scan results based on your specific organizational
requirements, whether you need to distinguish between production and development
environments, assign ownership to specific teams, track compliance framework requirements, or
integrate with your existing CI/CD workflows.


Prisma AIRS AI Runtime Release Notes **25** © 2026 Palo Alto Networks, Inc.


**Key Benefits:**

  - **Flexible Labeling Options** [—Attach custom labels to scan results either at scan time through the](https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/viewing-scan-results)
API and SDK or retroactively through the user interface, accommodating both automated and
manual workflows.

  - **Simple Schema-Free Format** —Uses straightforward string key-value pairs that adapt to diverse
organizational structures without enforcing rigid schemas (such as, "environment:production",
"team:ml-platform", "compliance:SOC2").

  - **Rich Contextual Categorization** —Apply multiple custom labels to each scan result, creating
comprehensive categorization that reflects your operational reality.

  - **Powerful Filtering Capabilities** —Quickly isolate scan results by any combination of criteria
rather than manually tracking which scans belong to which systems or teams.

  - **Compliance and Audit Support** —Generate targeted audit reports for specific regulatory
frameworks, enabling compliance teams to focus on relevant security findings.

  - **Team-Specific Focus** —Allow security teams to prioritize production environment issues while
development teams correlate scan results with their deployment pipelines.

  - **Seamless Integration** —Comprehensive API support enables automated custom labelling in CI/
CD systems while providing intuitive user interface controls for manual management.

  - **Enterprise Scalability** —Essential for scaling Model Security across enterprise environments
where hundreds or thousands of scans must be efficiently categorized, filtered, and acted upon
by distributed teams with varying responsibilities and access requirements.
#### Local Scan AI Models Directly from Cloud Storages


January 2026

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


[The AI Model Security client SDK now provides native access to scan machine learning models](https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/scanning-models)
stored across multiple cloud storage platforms without requiring manual downloads. This
enhanced capability allows you to perform security scans directly on models hosted in Amazon
S3, Azure Blob Storage, Google Cloud Storage, JFrog Artifactory repositories, and GitLab Model
Registry using your existing authentication credentials and access controls.

You can leverage this feature when your organization stores trained model repositories that
require authenticated access, eliminating the need to manually download large model files or rely
on external scanning services that may not have access to your secured storage environments.
This approach is particularly valuable when working with proprietary models, models containing
sensitive data, or when operating under strict data governance policies that prohibit transferring
model artifacts outside your controlled infrastructure.

The native storage integration streamlines your security workflow by automatically handling
credential resolution, temporary file management, and cleanup operations while maintaining
the same local scanning capabilities you rely on for file-based model analysis. You benefit from
reduced operational overhead and faster scan execution since the SDK can optimize download
and scanning operations without intermediate storage steps. This capability enables seamless


Prisma AIRS AI Runtime Release Notes **26** © 2026 Palo Alto Networks, Inc.


integration into CI/CD pipelines, automated security workflows, and compliance processes
where model artifacts must remain within your organization's security perimeter throughout the
scanning lifecycle.
#### Customize Security Groups and View Enhanced Scan Results


December 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


The AI Model Security web interface has been enhanced with the following new features that
provide deeper insights into model violations and offer greater flexibility for customizing your
security configuration. Below are the key new capabilities:

  - **Customize Security Groups** —In addition to the set of default groups created for all new users,
[you can now create new custom model security groups directly using Strata Cloud Manager.](https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/customizing-security-groups)
Additionally, edit names and descriptions of existing security groups and delete the unused
security groups (except the default ones).

  - **File Explorer** [—For each scan, you can now view the visualization of every file scanned by](https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/viewing-scan-results#view-scan-results-strata-cloud-manager)
AI Model Security in its original file structure. You can also view detailed, file-level violation
information for every scanned file.

  - **Enhanced JSON View** [—You can now view direct JSON responses from the API for scans,](https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/viewing-scan-results#view-scan-results-strata-cloud-manager)
violations, and rule evaluations. The JSON view also provides detailed instructions on how to
retrieve this data from your local machine.
#### Secure AI Models with AI Model Security


October 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


Models serve as the foundation of AI/ML workloads and power critical systems across
organizations today. Prisma AIRS now features AI Model Security, a comprehensive solution that
ensures only secure, vulnerability-free models are used while maintaining your desired security
posture.

AI/ML models pose significant security risks as they can execute arbitrary code during loading
or inference. This is a critical vulnerability that existing security tools fail to adequately detect.
Compromised models have been exploited in high-impact attacks including cloud infrastructure
takeovers, sensitive data theft, and ransomware deployments. Your valuable training datasets and
inference data processed by these models make them prime targets for cybercriminals seeking to
infiltrate AI-powered systems.

[What you can do with AI Model Security:](https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models)


Prisma AIRS AI Runtime Release Notes **27** © 2026 Palo Alto Networks, Inc.


  - **Model Security Groups** —Create Security Groups that apply different managed rules based
on where your models come from. Set stricter policies for external sources like HuggingFace,
while tailoring controls for internal sources like Local or Object Storage.

  - **Model Scanning** —Scan any model version against your Security Group rules. Get clear pass/
fail results with supporting evidence for every finding, so you can confidently decide whether a
model is safe to deploy.


**Key Benefits:**

   - Prevent Security Risks Before Deployment: Identify vulnerabilities, malicious code, and security
threats in AI models before they reach production environments.

   - Enforce Consistent Security Standards: Apply organization-wide security policies across all
model sources, ensuring every model meets your requirements regardless of origin.

   - Accelerate Secure AI Adoption: Reduce manual security review time with automated scanning,
enabling teams to deploy models faster without compromising security.

   - Maintain Compliance and Governance: Demonstrate security due diligence with detailed scan
evidence and audit trails for regulated industries and internal compliance requirements.


Prisma AIRS AI Runtime Release Notes **28** © 2026 Palo Alto Networks, Inc.



![](images/fetchpdf-1769981278555.pdf-27-0.png)
### AI Red Teaming

Here are the new Prisma AIRS AI Red Teaming features.
#### Secure AI Red Teaming with Network Channels


January 2026

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


Network Channels is a secure connection solution that enables AI Red Teaming to safely access
and analyze your internal endpoints without requiring IP whitelisting or opening inbound ports.
This enterprise-grade solution puts you in complete control of the connection, allowing you to
initiate and terminate access while maintaining your security perimeter.

The **Network Channels** enables you to conduct secure, continuous AI Red Teaming assessments
against user APIs and models hosted within private infrastructure. Network channels eliminates
the need for users to expose inbound ports or modify firewall configurations, adhering strictly to
Zero Trust principles.

A **channel** is a unique communication pathway that clients use to establish connections. Each
channel has a unique connection URL with auth credentials. You will need to create and validate
a channel first, before using it to add a target. Multiple channels can be created for different
environments and each channel can handle multiple targets accessible to it.

The solution utilizes a lightweight **Network Channels** client deployed within the user’s
environment. This client establishes a persistent, secure outbound WebSocket connection to the
Palo Alto Networks environment, facilitating seamless testing of internal systems without the risks
associated with IP whitelisting or inbound access.


Additionally, you will be provided with a docker pull secret from Strata Cloud Manager, which you
can use to pull the docker image and helm chart for the network channels client.

This combined solution is ideal for:


Prisma AIRS AI Runtime Release Notes **29** © 2026 Palo Alto Networks, Inc.



![](images/fetchpdf-1769981278555.pdf-28-0.png)
  - **Restricted Environments** : Conducting assessments for enterprise users with air-gapped
systems or strict compliance requirements.

  - **Continuous Monitoring** : Maintaining reliable, persistent connectivity for real-time AI security
updates.

  - **Automated Workflows** : Deploying network broker clients across distributed infrastructure
using existing container orchestration (Kubernetes/Helm) without manual intervention.

**Key Benefits**

  - **Enhanced Security** : No need to expose internal endpoints or modify firewall rules.

  - **Complete Control** : Initiate and terminate connections on demand.

  - **Easy Setup** : Simple client installation process.

  - **Flexible Management** : Create and manage multiple secure channels for different
environments.

  - **Reusability** : Use the same connection for multiple targets.

  - **Enterprise Ready** : Designed for organizations with strict security requirements.
#### Remediation Recommendations for AI Red Teaming Risk Assessment


January 2026

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


The Recommendations feature enables you to seamlessly transition from identifying AI system
vulnerabilities through Red Teaming assessments to implementing targeted security controls
that address your specific risks. This feature closes the critical gap between AI risk assessment
and mitigation by transforming vulnerability findings into actionable remediation plans. The
[remediation recommendations can be found in all Attack Library and Agent Scan Reports.](https://docs.paloaltonetworks.com/ai-runtime-security/ai-red-teaming/identify-ai-system-risks-with-ai-red-teaming/get-started-with-prisma-airs-ai-red-teaming/reports)

When you conduct AI Red Teaming evaluations on your AI models, applications, or agents, this
integrated solution automatically analyzes the discovered security, safety, brand reputation, and
compliance risks to generate contextual remediation recommendations that directly address your
specific vulnerabilities.

The generated contextual remediation recommendations include two distinct components:

  - **Runtime Security Policy configuration** : Rather than configuring runtime security policies
through trial and error, you receive intelligent guidance that maps each identified risk category
to appropriate guardrail configurations, such as enabling prompt injection protection for
security vulnerabilities or toxic content moderation for safety concerns.

  - **Other recommended measures** : The system identifies successfully compromised
vulnerabilities, and provides the corresponding remediation measures by prioritizing them
based on effectiveness and implementation feasibility, allowing you to eliminate manual
evaluation and focus resources on high-impact fixes.


Prisma AIRS AI Runtime Release Notes **30** © 2026 Palo Alto Networks, Inc.


For organizations deploying AI systems in production environments, this capability ensures
that your runtime security configurations and remediation measures are informed by actual risk
insights rather than generic best practices, resulting in more effective protection against the
specific threats your AI systems face.

The remediation recommendations appear directly in your AI Red Teaming scan reports, providing
actionable guidance. You can then manually create and attach the recommended security profiles
to your desired workloads, transforming AI risk management from a reactive process into a
proactive workflow that connects vulnerability discovery with targeted protection.
#### AI Red Teaming Executive Reports


January 2026

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


When you conduct AI Red Teaming assessments, you often need to share results with executive
stakeholders like CISOs and CIOs who require high-level insights rather than granular technical
[details. The exportable executive PDF report feature addresses this need by transforming your AI](https://docs.paloaltonetworks.com/ai-runtime-security/ai-red-teaming/identify-ai-system-risks-with-ai-red-teaming/get-started-with-prisma-airs-ai-red-teaming/reports)
Red Teaming assessment data into a consumable format. You can now generate comprehensive
PDF reports that consolidate the essential information from the web interface, organized to
highlight critical takeaways and strategic insights in a format that can be shared easily with
executives. While security practitioners can leverage CSV and JSON export formats to access
detailed findings for remediation purposes, this PDF format is highly valuable for CXOs who
intend to understand high level risk assessment of any AI system.

Use this feature to communicate security posture and risk assessments to executive leadership
who may not have the time or technical background to parse through detailed CSV exports or
navigate complex web interfaces. The PDF format ensures you can easily distribute reports
through email or include them in executive briefings and board presentations. The report contains
AI summary, key risk breakdown, high-level overview charts, and metrics that matter most to
decision-makers.

You can use this feature when preparing for executive reviews, board meetings, or any scenario
where you need to demonstrate the effectiveness of your security controls and communicate
risk exposure to non-technical stakeholders. The structured format with AI summary, overview
sections, and detailed attack tables, ensures that both strategic insights and supporting technical
evidence are readily accessible, enabling informed decision-making at the executive level.
#### AI Summary for AI Red Teaming Scans


January 2026

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


Prisma AIRS AI Runtime Release Notes **31** © 2026 Palo Alto Networks, Inc.


When you complete an AI Red Teaming scan, you receive an AI Summary (in the scan report)
that synthesizes key risks and their implications. This executive summary eliminates the need
for manual interpretation of technical data, allowing you to quickly understand which attack
categories or techniques pose the greatest threats to your systems and what the potential
business impact might be.

[The AI Summary contains the scan configuration, key risks, and implications.](https://docs.paloaltonetworks.com/ai-runtime-security/ai-red-teaming/identify-ai-system-risks-with-ai-red-teaming/get-started-with-prisma-airs-ai-red-teaming/reports)

This capability is particularly valuable when you need to communicate AI risk assessment results
across different organizational levels or when preparing briefings for leadership meetings. Rather
than struggling to translate technical vulnerability reports into business language, you can rely
on the AI Red Teaming generated report to articulate security, safety, compliance, brand, and
business risks in terms that resonate with executive audiences. This summary is also valuable in
prioritising remediation measures which teams can adopt for a safer deployment of AI systems in
production.
#### Enhanced AI Red Teaming with Brand Reputation Risk Detection


January 2026

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


You can now assess and protect your AI systems against Brand reputation risks using Prisma
AIRS enhanced AI Red Teaming capabilities. This feature addresses a critical gap in AI security
by identifying vulnerabilities that could damage your organization's reputation when AI systems
interact with users in production environments. Beyond the existing Security, Safety, and
Compliance risk categories, you can now scan for threats including Competitor Endorsements,
Brand Tarnishing Content, Discriminating Claims, and Political Endorsements.

[The enhanced agent assessment capabilities automatically generate goals focused on Brand](https://docs.paloaltonetworks.com/ai-runtime-security/ai-red-teaming/identify-ai-system-risks-with-ai-red-teaming/get-started-with-prisma-airs-ai-red-teaming/scans/start-a-scan?otp=task-dst_zkr_chc#task-dst_zkr_chc)
Reputational risk scenarios that could expose your organization to public relations challenges or
[regulatory scrutiny. You benefit from specialized evaluation methods designed to detect subtle](https://docs.paloaltonetworks.com/ai-runtime-security/ai-red-teaming/identify-ai-system-risks-with-ai-red-teaming/get-started-with-prisma-airs-ai-red-teaming/reports?otp=concept-jk3_hgt_tgc#concept-jk3_hgt_tgc)
forms of reputational risk, including false claims and inappropriate endorsements that traditional
security scanning might miss. This comprehensive approach allows you to proactively identify and
address potential brand vulnerabilities before deploying AI systems to production environments,
protecting both your technical infrastructure and corporate reputation in an increasingly AI-driven
business landscape.
#### Error Logs and Partial Scan Reports


December 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


When you conduct AI Red Teaming scans using Prisma AIRS, you may encounter situations
where scans fail completely or complete only partially due to target system issues or connectivity


Prisma AIRS AI Runtime Release Notes **32** © 2026 Palo Alto Networks, Inc.


[problems. The Error Logs and Partial Scan Reports feature provides you with comprehensive](https://docs.paloaltonetworks.com/ai-runtime-security/ai-red-teaming/identify-ai-system-risks-with-ai-red-teaming/get-started-with-prisma-airs-ai-red-teaming/reports)
visibility into scan failures and enables you to generate actionable reports even when your scans
don't complete successfully. You can access detailed error logs directly within the scan interface,
both during active scans on the progress page and after completion in the scan logs section,
allowing you to quickly identify whether issues stem from your target AI system or the Prisma
AIRS platform itself.

This feature particularly benefits you when conducting Red Teaming assessments against
enterprise AI systems that may have intermittent availability or response issues. When your
scan completes the full simulation but doesn’t receive valid responses for all attacks, AI Red
Teaming marks it as partially complete rather than failed. You can then choose to generate a
comprehensive report based on the available test results, giving you valuable security insights
even from incomplete assessments. AI Red Teaming transparently informs you about credit
consumption before report generation and clearly marks any generated reports as partial scans,
indicating the percentage of attacks that received responses.

By leveraging this capability, you can maximize the value of your Red Teaming efforts,
troubleshoot scanning issues more effectively, and maintain continuous security assessment
workflows even when facing target system limitations or temporary connectivity challenges
during your AI security evaluations.
#### Automated AI Red Teaming


October 2025

**Supported for:**

   - Prisma AIRS (Managed by Strata Cloud Manager)


Palo Alto Networks' **[Prisma AIRS AI Red Teaming](https://docs.paloaltonetworks.com/ai-runtime-security/ai-red-teaming/identify-ai-system-risks-with-ai-red-teaming/get-started-with-prisma-airs-ai-red-teaming)** is an automated solution designed to scan any
**AI system** —including LLMs and LLM-powered applications—for safety and security vulnerabilities.

The tool performs a **Scan** against a specified **Target** (model, application, or agent) by sending
carefully crafted **attack prompts** to simulate real-world threats. The findings are compiled into a
comprehensive **Scan Report** that includes an overall **Risk Score** (ranging from 0 to 100), indicating
the system's susceptibility to attacks.

Prisma AIRS offers three distinct scanning modes for thorough assessment:

**1. Attack Library Scan:** Uses a curated, proprietary library of predefined attack scenarios,
categorized by **Security** (e.g., Prompt Injection, Jailbreak), **Safety** (e.g., Bias, Cybercrime), and
**Compliance** (e.g., OWASP LLM Top 10).

**2. Agent Scan:** Utilizes a dynamic **LLM attacker** to generate and adapt attacks in real-time,
enabling full-spectrum Black-box, Grey-box, and White-box testing.

**3. Custom Attack Scan:** Allows users to upload and execute their own custom prompt sets
alongside the built-in library.

A key feature of the service is its **single-tenant deployment** model, which ensures complete
isolation of compute resources and data for enhanced security and privacy.


Prisma AIRS AI Runtime Release Notes **33** © 2026 Palo Alto Networks, Inc.


### Known Issues

Review the list of known issues as per the latest release for Prisma AIRS:

|Issue ID|Description|
|---|---|
|**SLR-2531**|In deployments where there is no Security Lifecycle Review (SLR) firewall<br>deployed but a regular Prisma AIRS inline firewall exists, the**Overview**<br>section of the SLR report fails to display some information; for example,<br>the_Application Inventory Overview_ in the**Traffic Flow Overview** page.<br>This issue only occurs when the firewall sends logs to the Strata Logging<br>Service (SLS) in large volumes.|
|**AIFW-3035**|During a scale-in event, terminating an instance may take approximately<br>15 minutes to perform the delicensing workflow and effectively release<br>CSP credits.|
|**AIFW-1555**|**Helm Installation Fails Due to Incorrect Endpoints in YAML**<br>When you download a deployment Terraform with traffic steering<br>inspection enabled, the `pan-cni-svc-eps.yaml` file may incorrectly<br>contain multiple endpoints, even if you selected only one zone in the<br>deployment workflow. This can cause the Helm installation to fail.<br>**Workaround:** Manually modify the`pan-cni-svc-eps.yaml` file to<br>remove the extra endpoint information, and ensure it reflects only the<br>zones you selected during configuration.|
|**AIFW-790**|**Pod Traffic Discovery Limitation in AWS Kubernetes Clusters**<br>Prisma AIRS: Network intercept may not fully discover unprotected pod<br>traffic in Kubernetes clusters running on AWS. This impacts the visibility<br>of such traffic in the Strata Cloud Manager discovery command center<br>despite enablingAWS VPC flow logs.<br>**Workaround**: To discover the pod’s traffic, add the<br>**AmazonEKSAdminViewPolicy** to the K8s cluster for the role you created<br>when applying the onboarding Terraform.|
|**AIFW-717**|**Model Traffic Display Delay in AWS Environments**<br>Prisma AIRS: Network intercept may not immediately display unprotected<br>model traffic on theModels page for AWS environments. This occurs<br>because the system cannot properly match instance identifiers between<br>flow logs and model invocation logs, particularly when instance profiles<br>and IAM roles use different naming conventions. As a result, AI traffic<br>from applications to Bedrock models may not appear in the Models page<br>despite being actively used.|



Prisma AIRS AI Runtime Release Notes **34** © 2026 Palo Alto Networks, Inc.


|Issue ID|Description|
|---|---|
|**AIFW-750**|When you destroy the `security_project` Terraform, the Terraform<br>deployment screen (**Insights → AI Runtime Security**) still shows the<br>firewall with a**Deployed** status. You can manually**delete** the Terraform<br>item for the firewall from the deployment screen.|
|**AIFW-720**|Theonboarding workflow in Strata Cloud Manager fails if your Strata<br>Logging Service has expired.<br>Verify your Strata Logging Service license status when creating a<br>deployment profile in the Customer Support Portal. If the Strata Logging<br>Service has expired, renew it before onboarding a cloud account to<br>ensure successful onboarding Terraform generation.|
|**AIFW-506**|The Application breakdown section on the Applications page (**Strata**<br>**Cloud Manager** >** Insights** >** Prisma AIRS** >** Prisma AIRS AI Runtime**<br>**- Network Intercept**) may show a discrepancy in the total number of<br>applications. The breakdown of VM and Pod applications may not sum<br>up to the total number of applications displayed at the top of the page.<br>This is because some applications are categorized as both VM and Pod<br>types, ltheir inclusion in both respective counts within the breakdown.<br>However, the total application count remains accurate, representing the<br>unique number of applications across all types.|
|**PAN-280130**|GKE Autopilot clusters do not supportHelm deployments due to<br>restrictions on modifying the kube-system namespace.|
|**AIFW-690**|GCP account onboarding requires a 10-second wait after a successful<br>Terraform application before clicking "Done" to complete the process.|
|**PAN-256741**|**Traffic Routing Blocked Between `fw-trust-vpc` and `app-vpc`**<br>Traffic routing between fw-trust-vpc and app-vpc via VPC peering is<br>currently blocked because the route export from fw-trust-vpc to app-vpc<br>for 0.0.0.0/0 to ILB is hindered by an existing default gateway route in the<br>app-vpc.<br>**Workaround**: Create a default route in the app-vpc which uses the Prisma<br>AIRS ILB as the next hop. This ensures traffic routes correctly through the<br>Prisma AIRS: Network intercept (AI firewall), enforcing security policies.|


Prisma AIRS AI Runtime Release Notes **35** © 2026 Palo Alto Networks, Inc.



![](images/fetchpdf-1769981278555.pdf-34-0.png)
|Issue ID|Description|
|---|---|
|**PLUG-16395**|IPv6 Tags harvesting is not supported.|
|**AIFW-421**|**Missing CIDR retrieval during AI Runtime Security deployment**<br>While deploying an Prisma AIRS: Network intercept inStrata Cloud<br>Manager, selecting the application namespace does not retrieve the<br>cluster pod and service CIDR.<br>**Workaround**: After generating the Terraform configuration, please<br>whitelist these CIDR values in the Firewall Trust VPC firewall rule.|
|**PAN-266547**|**Tag Collector in TC Mode enters Maintenance Mode after upgrade to**<br>**`v11.2.3`**<br>The issue occurs when you upgrade the AI Runtime Security tag collector<br>from `v11.2.2-h1` to `v11.2.3`, the tag-collector enters a rebooting loop<br>and eventually goes to maintenance mode.<br>**Workaround**: Don’t upgrade to `v11.2.3` as the auto-commit feature is<br>not triggered in `v11.2.3`.|
|**PAN-266547**|Tag Collector running `v11.2.2-h1` enters Maintenance Mode with<br>instance types other than `n2-standard-4` and `Standard_DS3_v2` post<br>bootstrap. This is due to incorrect capacity file computation and excessive<br>memory usage.<br>**Workaround**: Use `n2-standard-4` or `Standard_DS3_v2` instance sizes<br>for running `v11.2.2-h1` to avoid this issue.|


Prisma AIRS AI Runtime Release Notes **36** © 2026 Palo Alto Networks, Inc.


### Addressed Issues

Review the addressed issues in Prisma AIRS.


**ISSUE ID** **DESCRIPTION**


**PAN-265124** **K8s Pod Outbound Traffic Blocked by DNS-Securit**

[When an "allow-all" rule is configured in Strata Clou](http://stratacloudmanager.paloaltonetworks.com/)
with the default "best-practice" **Profile Group**, outb

**Workaround:** To ensure outbound traffic functions


**ADI-34257** Cloning a security policy rule ( **Manage → Configura**
uses an AI profile group does not update the AI prof


**ADI-34273** When moving an AI Security profile ( **Manage → Con**
one device scope to another, deleting the security p



**PAN-264445**
```
Fixed in 11.2.3-h1

```

**PAN-268187**
```
Fixed in 11.2.3-h1

```

**PAN-266218**
```
Fixed in 11.2.3-h1

```

**PAN-266219**
```
Fixed in 11.2.3-h1

```


SSL traffic failed between secure pods with decrypt


Traffic log incorrectly showed non-AI HTTP/2 traffi


Kubernetes cluster ID from the CNI was not detecte


Kubernetes cluster ID was missing in the HTTP/2 tr



Prisma AIRS AI Runtime Release Notes **37** © 2026 Palo Alto Networks, Inc.



