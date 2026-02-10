# Module 4: AIRS Deep Dive

## Overview

Welcome to Act 2 -- **Understand the Security.**

You have a working ML pipeline. Models train, merge, publish, and deploy. But right now there is nothing stopping a compromised model from flowing straight to production. Before you can secure the pipeline, you need to understand AIRS inside and out -- the way you would need to demo it to a customer.

This module puts you in the seat of someone evaluating AIRS for an enterprise deployment. You will activate AI Model Security on your existing tenant, explore the Strata Cloud Manager console, run your first scans, explore the HuggingFace partnership, and understand how security groups control scanning policy.

## Objectives

- Activate AI Model Security by creating a deployment profile and associating it with your existing AIRS tenant
- Navigate Strata Cloud Manager (SCM) to explore the Model Security UX -- scans, security groups, rules
- Install the AIRS SDK and run scans from the CLI and Python
- Understand scan responses: eval_outcome, eval_summary, rules_passed, rules_failed
- Explore the PANW-HuggingFace partnership and compare public vs enterprise scanning
- Understand security group policy: blocking vs alerting, source type matching, default groups

## Prerequisites

- Modules 0-3 completed (working pipeline, deployed model)
- An existing Prisma AIRS tenant from the AIRS API Lab (with SCM already provisioned)
- AIRS SDK credentials: `MODEL_SECURITY_CLIENT_ID`, `MODEL_SECURITY_CLIENT_SECRET`, `TSG_ID`
- GitHub secrets configured from Module 0
- Access to the Customer Support Portal (CSP) for deployment profile creation

## Time Estimate

1 to 1.5 hours

---

## Challenges

### Challenge 4.1: Activate AI Model Security

> `/lab:explore activation-setup`

You already have a Prisma AIRS tenant from the API Lab. Now you need to enable the Model Security capability on that same tenant. This requires creating a new deployment profile in the Customer Support Portal (CSP) and associating it with your existing tenant.

Once activated, verify that AI Model Security appears in your Strata Cloud Manager console and that your existing AIRS credentials can authenticate scanning requests.

### Challenge 4.2: Explore the SCM Console

> `/lab:explore scm-model-security`

Before you scan anything, understand the tool your customers' security teams will use daily. Navigate the AI Model Security section of SCM. Find your default security groups, understand the rules, and locate the UUIDs you will need for scanning.

This is the management plane. The security admin lives here. The CI/CD pipeline lives in the SDK. Understanding both sides is critical for customer conversations.

### Challenge 4.3: Your First Scans

> `/lab:explore cli-and-sdk`

A customer asks you to demonstrate AIRS scanning. They want to see what happens with a legitimate model and what happens when something dangerous comes through.

Install the AIRS SDK and run your first scan. Scan a known-safe model from HuggingFace or GCS. Then scan the pickle bomb from `scripts/create_threat_models.py`. Compare the results side by side. Then find those scans in SCM and see the per-rule details that the SDK does not expose.

### Challenge 4.4: HuggingFace Integration

> `/lab:explore hf-integration`

A customer tells you, "HuggingFace already scans models. Why do I need AIRS?" You need to understand exactly what the PANW-HuggingFace partnership provides for free, and what AIRS adds on top.

Find Palo Alto Networks' public scan results on HuggingFace. What models have been flagged? What information is freely available vs what AIRS adds for enterprise customers?

### Challenge 4.5: Security Groups & Policy

> `/lab:explore security-groups`

An enterprise customer wants different scanning policies for different environments. Development teams should get warnings so they can iterate quickly. Production deployments should be strictly blocked if anything is detected. They also want to understand exactly what each rule does.

Explore the default security groups in SCM. Toggle rules between "block" and "alert." Test both modes against the same model and observe how the verdict changes while the detection stays the same.

---

## Customer Talking Points

After completing this module, you should be able to confidently deliver these points:

**On Activation:** "AI Model Security is a deployment profile you add to your existing Prisma AIRS tenant. If you already have AIRS for API Runtime, adding Model Security is a CSP deployment profile and a tenant association -- your existing SCM instance, IAM, and service accounts carry over."

**On the SCM Console:** "Security admins manage policy in SCM -- security groups, rules, enforcement modes. The CI/CD pipeline uses the SDK. They are decoupled by design: security teams set policy, engineering teams consume it through the scan API. Neither needs to touch the other's tools."

**On HuggingFace:** "When a customer asks about HF scanning vs AIRS, here is the comparison: HF gives you basic checks on public models with default rules. AIRS gives you policy control, private model scanning, pipeline enforcement, and security operations integration. The question is whether you need visibility or control."

**On Security Groups:** "Different environments need different policies. Development gets warnings so teams can iterate. Staging gets mixed policies for testing. Production gets strict blocking. AIRS makes this a configuration decision, not a code change."

## What's Next

You now understand AIRS scanning inside and out. In Module 5, you will integrate this into your pipeline -- adding scanning gates, manifest verification, and evaluation reporting directly into your GitHub Actions workflows. The pipeline currently has no security checks. You are about to change that.
