# Project Brief: The "Sugar Trap" Market Gap Analysis

**Client:** Helix CPG Partners (Strategic Food & Beverage Consultancy)  
**Deliverable:** Interactive Dashboard, Code Notebook & Insight Presentation

---

## Executive Summary
The analysis of Open Food Facts snack products cleaned invalid nutrition entries, mapped messy category tags into readable buckets, and identified the under-served quadrant where protein is high and sugar is low. The notebook found a clear gap in the market for high-protein, low-sugar products, specifically products with at least 10g of protein and no more than 2g of sugar per 100g. The strongest business opportunity lies in a healthier snack segment that focuses on dairy and its alternatives.

---

## Project Links
* **Notebook:** [https://colab.research.google.com/drive/1QvpbFkLztWPN3HHDKMJwKhpmj2btu8XD#scrollTo=bZYXB2pxsnJr]
* **Dashboard:** [https://the-market-gap-analysis-ynlkzyuw8wnbbpumownt5s.streamlit.app/]
* **Presentation:** [https://drive.google.com/file/d/1j80-2tP3nWeFmCmHUP1xaVagDQc1WlaG/view?usp=drive_link]

---

## Technical Expertise

**Data Cleaning:** The notebook starts by removing rows with missing or null values in sugars_100g, proteins_100g, and essential metadata such as product_name or category tags. It also filters out invalid nutrition values that are biologically impossible, like negative sugar/protein counts or unrealistically high totals. Outliers are handled by trimming extreme entries so that the analysis reflects a typical snack product distribution instead of data-entry errors. After cleaning, a normalization step standardizes the nutrient columns, making sugar and protein comparable on the same scale for quadrant scoring. This clean, normalized dataset then enables robust category mapping and reliable gap scoring.

**Candidate's Choice Challenge:** The extra feature is a Category Market Gap Explorer that assigns a gap score to each snack category based on its presence in the high protein / low sugar quadrant. It ranks categories by both gap severity and relative under-representation, surfacing under-served segments like dairy alternatives and savory protein snacks. This addition turns the analysis from a generic nutrient chart into a category-level opportunity report. It makes the recommendation more business actionable by highlighting which categories should be prioritized for new product development.

---

