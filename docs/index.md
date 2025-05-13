# SmartCRM – Documentation

Welcome to the official documentation for **SmartCRM**, a specialized analytical CRM platform tailored for restaurants and cafes. This documentation covers the system architecture, services, data models, and development workflows used to build the MVP.

---

## ❗ Problem

Small and medium-sized restaurants often lack the tools to:
- Understand customer behavior and loyalty
- Track product performance over time
- Execute data-driven marketing campaigns
- Personalize menu recommendations

Traditional CRMs are too generic and lack the domain-specific insights needed by food and beverage businesses. This gap leads to poor customer retention, ineffective marketing, and underutilized data.

---

## ✅ Solution

**SmartCRM** addresses this gap with a fully integrated, microservice-based CRM that includes:

- A user-friendly Streamlit dashboard
- A FastAPI backend with structured analytics endpoints
- Automated RFM segmentation of customers
- Time-based menu item recommendations
- NFC engagement tracking
- Dockerized ETL pipeline for synthetic data generation

All components are modular and communicate via REST APIs, making the system extendable and cloud-ready.

---

## 🎯 Expected Outcomes

- Restaurant managers gain actionable insights into sales and customer behavior
- Marketing teams can launch targeted campaigns based on customer segments
- Personalized menus improve customer satisfaction and upsell opportunities
- Full-stack data pipeline supports reproducible experiments and data science

---

## 📦 What's Inside

- `api/` – FastAPI backend service
- `frontend/` – Streamlit-based UI
- `etl/` – Data generation and loading scripts
- `notebook/` – Analysis notebook for validation
- `docs/` – This documentation, built with MkDocs

Use the sidebar to explore each component in detail.