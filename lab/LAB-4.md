# Module 4: AIRS Deep Dive

## Overview

Welcome to Act 2 -- **Understand the Security.**

You have a working ML pipeline. Models train, merge, publish, and deploy. But right now there is nothing stopping a compromised model from flowing straight to production. Before you can secure the pipeline, you need to understand AIRS inside and out -- the way you would need to demo it to a customer.

This module puts you in the seat of someone evaluating AIRS for an enterprise deployment. You will set up least-privilege access, run your first scans, explore the HuggingFace partnership, and build custom security policies in Strata Cloud Manager.

## Objectives

- Create a restricted service account with minimum scanning permissions (RBAC)
- Install the AIRS SDK and run scans from the CLI and Python
- Understand scan responses: eval_outcome, eval_summary, rules_passed, rules_failed
- Explore the PANW-HuggingFace partnership and compare public vs enterprise scanning
- Navigate Strata Cloud Manager (SCM) to find scan reports and manage security groups
- Create custom security groups with different blocking policies

## Prerequisites

- Modules 0-3 completed (working pipeline, deployed model)
- Access to your Prisma AIRS tenant (SCM credentials)
- AIRS SDK credentials: `MODEL_SECURITY_CLIENT_ID`, `MODEL_SECURITY_CLIENT_SECRET`, `TSG_ID`
- GitHub secrets configured from Module 0

## Time Estimate

1 to 1.5 hours

---

## Challenges

### Challenge 4.1: Set Up Least-Privilege Access

> `/lab:explore 01-rbac`

Your security team requires that every automated system follows the principle of least privilege. The scanning pipeline should only be able to submit scans and read results -- it should never be able to create or modify security groups, manage users, or change policies.

Use Claude Code and the SCM API to create a custom role that only allows model scanning operations. Create a service account with that role. You will use this restricted service account for all your scanning work in Modules 4 through 7.

### Challenge 4.2: Your First Scans

> `/lab:explore 02-cli-and-sdk`

A customer asks you to demonstrate AIRS scanning. They want to see what happens with a legitimate model and what happens when something dangerous comes through.

Install the AIRS SDK and run your first scan. Scan a known-safe model from HuggingFace or GCS. Then scan the pickle bomb from `scripts/create_threat_models.py`. Compare the results side by side.

### Challenge 4.3: HuggingFace Integration

> `/lab:explore 03-hf-integration`

A customer tells you, "HuggingFace already scans models. Why do I need AIRS?" You need to understand exactly what the PANW-HuggingFace partnership provides for free, and what AIRS adds on top.

Find Palo Alto Networks' public scan results on HuggingFace. What models have been flagged? What information is freely available vs what AIRS adds for enterprise customers?

### Challenge 4.4: Security Groups Deep Dive

> `/lab:explore 04-security-groups`

An enterprise customer wants different scanning policies for different environments. Development teams should get warnings so they can iterate quickly. Production deployments should be strictly blocked if anything is detected. They also want to understand exactly what each rule does.

Navigate SCM. Find your scan reports from the CLI experiments. Then create two custom security groups: one that blocks on every rule, and one that only warns. Test both against the same model and compare the results.

---

## Customer Talking Points

After completing this module, you should be able to confidently deliver these points:

**On RBAC:** "Here is how to set up least-privilege access for your scanning pipeline. Your CI/CD runner only needs scan permissions, not admin. This follows the same IAM model you use for every other cloud service."

**On HuggingFace:** "When a customer asks about HF scanning vs AIRS, here is the comparison: HF gives you basic checks on public models with default rules. AIRS gives you policy control, private model scanning, pipeline enforcement, and security operations integration. The question is whether you need visibility or control."

**On Security Groups:** "Different environments need different policies. Development gets warnings so teams can iterate. Staging gets mixed policies for testing. Production gets strict blocking. AIRS makes this a configuration decision, not a code change."

## What's Next

You now understand AIRS scanning inside and out. In Module 5, you will integrate this into your pipeline -- adding scanning gates, manifest verification, and evaluation reporting directly into your GitHub Actions workflows. The pipeline currently has no security checks. You are about to change that.
