# 📊 Motor de Analytics — Dados de Retalho

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📌 Sobre o Projeto

Motor de analytics desenvolvido em Python para análise de eventos em ambientes de varejo, como lojas e shoppings.

O sistema processa eventos de **entrada**, **saída** e **permanência**, permitindo extrair insights sobre comportamento de usuários, fluxo entre zonas e padrões de visita.

Este projeto tem como foco a implementação manual de **estruturas de dados e algoritmos clássicos**, sem o uso de bibliotecas externas de alto nível.

---

## 🎯 Objetivos

- Aplicar conceitos de Estruturas de Dados e Algoritmos na prática  
- Construir um sistema eficiente e modular  
- Comparar desempenho entre algoritmos  
- Simular cenários reais de análise de fluxo  

---

## ⚙️ Funcionalidades

### 📊 Análises Temporais
- Ocupação por zona em intervalos de tempo  
- Média de permanência por hora  
- Identificação de picos de ocupação  
- Comparação entre dias  

### 🏆 Rankings (Top-K)
- Zonas mais visitadas  
- Blocos com maior fluxo  
- Zonas com maior permanência média  

### 🔄 Fluxo e Padrões
- Transição entre zonas  
- Detecção de sequências (KMP)  
- Identificação de anomalias  

### 🔎 Query Composta
- Filtros por:
  - tempo
  - zona
  - gênero
  - faixa etária  

### 🧪 Benchmark
- Comparação entre:
  - Bubble Sort
  - Merge Sort  

---

## 🏗️ Estrutura do Projeto

```bash
motor_analytics/
│
├── main.py
├── menu.py
├── data_loader.py
│
├── models/
├── structures/
├── algorithms/
├── queries/
├── utils/
│
└── data/